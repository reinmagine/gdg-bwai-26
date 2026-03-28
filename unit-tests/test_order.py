import pytest
from unittest.mock import Mock
from order import (
    Order, 
    InventoryShortageError, 
    PaymentFailedError, 
    InvalidOrderError,
    InventoryService,
    PaymentGateway
)

@pytest.fixture
def mock_inventory():
    return Mock(spec=InventoryService)

@pytest.fixture
def mock_payment():
    return Mock(spec=PaymentGateway)

@pytest.fixture
def order(mock_inventory, mock_payment):
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="test@example.com",
        is_vip=False
    )

@pytest.fixture
def vip_order(mock_inventory, mock_payment):
    return Order(
        inventory_service=mock_inventory,
        payment_gateway=mock_payment,
        customer_email="vip@example.com",
        is_vip=True
    )

class TestOrderInitialization:
    def test_initial_state(self, order):
        assert order.customer_email == "test@example.com"
        assert not order.is_vip
        assert order.items == {}
        assert not order.is_paid
        assert order.status == "DRAFT"

class TestAddItem:
    def test_add_new_item(self, order):
        order.add_item("item1", 10.0, 2)
        assert "item1" in order.items
        assert order.items["item1"] == {"price": 10.0, "qty": 2}

    def test_add_existing_item(self, order):
        order.add_item("item1", 10.0, 2)
        order.add_item("item1", 10.0, 3)
        assert order.items["item1"]["qty"] == 5
        assert order.items["item1"]["price"] == 10.0

    def test_add_item_invalid_price(self, order):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            order.add_item("item1", -5.0, 1)

    def test_add_item_invalid_quantity(self, order):
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            order.add_item("item1", 10.0, 0)
        
        with pytest.raises(ValueError, match="Quantity must be greater than zero"):
            order.add_item("item1", 10.0, -2)

class TestRemoveItem:
    def test_remove_existing_item(self, order):
        order.add_item("item1", 10.0, 2)
        order.remove_item("item1")
        assert "item1" not in order.items

    def test_remove_nonexistent_item(self, order):
        order.add_item("item1", 10.0, 2)
        order.remove_item("item2") # Should not raise error
        assert "item1" in order.items

class TestPricingAndDiscounts:
    def test_total_price_empty(self, order):
        assert order.total_price == 0.0

    def test_total_price_calculation(self, order):
        order.add_item("item1", 10.0, 2) # 20.0
        order.add_item("item2", 15.0, 3) # 45.0
        assert order.total_price == 65.0

    def test_apply_discount_regular_under_100(self, order):
        order.add_item("item1", 50.0, 1)
        assert order.apply_discount() == 50.0

    def test_apply_discount_regular_over_100(self, order):
        order.add_item("item1", 60.0, 2) # Total 120.0
        assert order.apply_discount() == 108.0 # 10% off

    def test_apply_discount_vip_under_100(self, vip_order):
        vip_order.add_item("item1", 50.0, 1)
        assert vip_order.apply_discount() == 40.0 # 20% off

    def test_apply_discount_vip_over_100(self, vip_order):
        vip_order.add_item("item1", 60.0, 2) # Total 120.0
        assert vip_order.apply_discount() == 96.0 # 20% off

class TestCheckout:
    def test_checkout_empty_cart(self, order):
        with pytest.raises(InvalidOrderError, match="Cannot checkout an empty cart"):
            order.checkout()

    def test_checkout_inventory_shortage(self, order, mock_inventory):
        order.add_item("item1", 10.0, 5)
        mock_inventory.get_stock.return_value = 3 # Only 3 in stock
        
        with pytest.raises(InventoryShortageError, match="Not enough stock for item1"):
            order.checkout()
        
        mock_inventory.get_stock.assert_called_once_with("item1")

    def test_checkout_payment_declined(self, order, mock_inventory, mock_payment):
        order.add_item("item1", 10.0, 5)
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.return_value = False # Gateway declined
        
        with pytest.raises(PaymentFailedError, match="Transaction declined by gateway"):
            order.checkout()

        mock_payment.charge.assert_called_once()
        # Ensure inventory wasn't decremented
        mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_exception(self, order, mock_inventory, mock_payment):
        order.add_item("item1", 10.0, 5)
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.side_effect = Exception("Network timeout")
        
        with pytest.raises(PaymentFailedError, match="Payment gateway error: Network timeout"):
            order.checkout()
            
        # Ensure inventory wasn't decremented
        mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_success(self, order, mock_inventory, mock_payment):
        order.add_item("item1", 10.0, 5)
        mock_inventory.get_stock.return_value = 10
        mock_payment.charge.return_value = True
        
        result = order.checkout()
        
        assert result == {"status": "success", "charged_amount": 50.0}
        assert order.is_paid
        assert order.status == "COMPLETED"
        
        mock_inventory.get_stock.assert_called_once_with("item1")
        mock_payment.charge.assert_called_once_with(50.0, "USD")
        mock_inventory.decrement_stock.assert_called_once_with("item1", 5)

    def test_checkout_success_vip(self, vip_order, mock_inventory, mock_payment):
        vip_order.add_item("item1", 100.0, 2) # 200 total, 160 with VIP
        mock_inventory.get_stock.return_value = 5
        mock_payment.charge.return_value = True
        
        result = vip_order.checkout()
        
        assert result == {"status": "success", "charged_amount": 160.0}
        mock_payment.charge.assert_called_once_with(160.0, "USD")
