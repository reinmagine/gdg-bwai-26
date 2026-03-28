document.addEventListener("DOMContentLoaded", () => {
    const searchTitle = document.getElementById("search-title");
    const searchSpeaker = document.getElementById("search-speaker");
    const searchCategory = document.getElementById("search-category");
    const eventCards = document.querySelectorAll(".event-card");
    const noResults = document.getElementById("no-results");

    function filterEvents() {
        const titleQuery = searchTitle.value.toLowerCase().trim();
        const speakerQuery = searchSpeaker.value.toLowerCase().trim();
        const categoryQuery = searchCategory.value.trim().toLowerCase();

        let visibleCount = 0;

        eventCards.forEach(card => {
            const title = card.getAttribute("data-title") || "";
            const speakers = card.getAttribute("data-speakers") || "";
            const categories = card.getAttribute("data-category") || "";
            
            // Should we hide break cards if they don't match the search?
            // Actually yes, it makes sense to hide breaks if you are searching for a specific speaker.
            // But if all fields are empty, shows breaks.
            const isBreak = card.classList.contains("break-card");

            const matchesTitle = title.includes(titleQuery);
            const matchesSpeaker = speakers.includes(speakerQuery);
            const matchesCategory = categoryQuery === "" || categories.split(',').includes(categoryQuery);

            if (matchesTitle && matchesSpeaker && matchesCategory) {
                card.style.display = "flex";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });

        if (visibleCount === 0) {
            noResults.style.display = "block";
        } else {
            noResults.style.display = "none";
        }
    }

    searchTitle.addEventListener("input", filterEvents);
    searchSpeaker.addEventListener("input", filterEvents);
    searchCategory.addEventListener("change", filterEvents);
});
