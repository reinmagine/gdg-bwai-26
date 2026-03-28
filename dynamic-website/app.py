from flask import Flask, render_template

app = Flask(__name__)

# Dummy Data for Google Cloud Technologies Conference
events = [
    {
        "id": 1,
        "title": "Keynote: The Future of Google Cloud",
        "category": ["Keynote", "Strategy"],
        "description": "An overview of upcoming features and the strategic vision for Google Cloud.",
        "time": "09:00 - 10:00",
        "speakers": [
            {"first_name": "Sundar", "last_name": "Pichai", "linkedin": "https://linkedin.com/in/sundarpichai"}
        ],
        "is_break": False
    },
    {
        "id": 2,
        "title": "Scaling Applications with Kubernetes",
        "category": ["Infrastructure", "Containers"],
        "description": "Deep dive into GKE and best practices for scaling microservices.",
        "time": "10:00 - 11:00",
        "speakers": [
            {"first_name": "Kelsey", "last_name": "Hightower", "linkedin": "https://linkedin.com/in/kelseyhightower"}
        ],
        "is_break": False
    },
    {
        "id": 3,
        "title": "Data Engineering with BigQuery and Dataflow",
        "category": ["Data", "Analytics"],
        "description": "Learn how to build scalable data pipelines using BigQuery and Dataflow.",
        "time": "11:00 - 12:00",
        "speakers": [
            {"first_name": "Felipe", "last_name": "Hoffa", "linkedin": "https://linkedin.com/in/felipehoffa"}
        ],
        "is_break": False
    },
    {
        "id": "lunch",
        "title": "Lunch Break",
        "category": ["Break"],
        "description": "Networking lunch in the main hall. Enjoy complimentary food and drinks.",
        "time": "12:00 - 13:00",
        "speakers": [],
        "is_break": True
    },
    {
        "id": 4,
        "title": "Generative AI with Vertex AI",
        "category": ["AI", "Machine Learning"],
        "description": "A practical guide to implementing LLMs in production using Vertex AI.",
        "time": "13:00 - 14:00",
        "speakers": [
            {"first_name": "Jeff", "last_name": "Dean", "linkedin": "https://linkedin.com/in/jeffdean"},
            {"first_name": "Demis", "last_name": "Hassabis", "linkedin": "https://linkedin.com/in/demishassabis"}
        ],
        "is_break": False
    },
    {
        "id": 5,
        "title": "Serverless at Scale: Cloud Run",
        "category": ["Infrastructure", "Serverless"],
        "description": "Design patterns for event-driven serverless architectures on Google Cloud.",
        "time": "14:00 - 15:00",
        "speakers": [
            {"first_name": "Steren", "last_name": "Giannini", "linkedin": "https://linkedin.com/in/steren"}
        ],
        "is_break": False
    },
    {
        "id": 6,
        "title": "Securing Your Cloud Environment with IAM",
        "category": ["Security"],
        "description": "Essential security practices and zero-trust architecture in Google Cloud.",
        "time": "15:00 - 16:00",
        "speakers": [
            {"first_name": "Sunil", "last_name": "Potti", "linkedin": "https://linkedin.com/in/sunilpotti"}
        ],
        "is_break": False
    },
    {
        "id": 7,
        "title": "Modernizing Apps with Anthos",
        "category": ["Hybrid Cloud", "Infrastructure"],
        "description": "Managing hybrid and multi-cloud environments effectively.",
        "time": "16:00 - 17:00",
        "speakers": [
            {"first_name": "Eyal", "last_name": "Manor", "linkedin": "https://linkedin.com/in/eyalmanor"}
        ],
        "is_break": False
    },
    {
        "id": 8,
        "title": "Closing Panel: What's Next for GCP?",
        "category": ["Keynote", "Networking"],
        "description": "Panel discussion with all speakers, followed by a networking mixer.",
        "time": "17:00 - 18:00",
        "speakers": [
            {"first_name": "Thomas", "last_name": "Kurian", "linkedin": "https://linkedin.com/in/thomaskurian"}
        ],
        "is_break": False
    },
    {
        "id": 9,
        "title": "Mastering Cloud Spanner",
        "category": ["Database", "Scalability"],
        "description": "An in-depth look at Google Cloud Spanner's capabilities and global scale use cases.",
        "time": "18:00 - 19:00",
        "speakers": [
            {"first_name": "Eric", "last_name": "Brewer", "linkedin": "https://www.linkedin.com/in/eric-brewer-319b26/"}
        ],
        "is_break": False
    },
    {
        "id": 10,
        "title": "Cloud Operations and Monitoring",
        "category": ["Operations", "SRE"],
        "description": "Best practices for Site Reliability Engineering using Google Cloud Operations Suite.",
        "time": "19:00 - 20:00",
        "speakers": [
            {"first_name": "Niall", "last_name": "Murphy", "linkedin": "https://linkedin.com/in/niallmurphy"}
        ],
        "is_break": False
    }
]

@app.route("/")
def index():
    return render_template(
        "index.html",
        events=events,
        date="October 25, 2026",
        location="Moscone Center, San Francisco"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
