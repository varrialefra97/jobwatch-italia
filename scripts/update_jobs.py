import json
from datetime import datetime

jobs = [
    {
        "title": "Junior Marketing Specialist",
        "company": "Enel",
        "location": "Roma",
        "degree": "Laurea Triennale",
        "url": "https://www.enel.com",
        "category": "marketing"
    },
    {
        "title": "Communication Assistant",
        "company": "Ferrovie dello Stato",
        "location": "Milano",
        "degree": "Laurea Triennale",
        "url": "https://fscareers.gruppofs.it",
        "category": "comunicazione"
    }
]

output = {
    "updated_at": datetime.utcnow().isoformat(),
    "jobs": jobs
}

with open("data/jobs.json", "w") as f:
    json.dump(output, f, indent=2)
