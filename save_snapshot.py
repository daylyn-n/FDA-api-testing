import requests
import json
import os

response = requests.get("https://api.fda.gov/drug/event.json?limit=5")

# open and save the snap shot in our json file
with open("data/sample_responses.json", "w") as f:
    json.dump(response.json(), f, indent=2)

print("sample saved")

