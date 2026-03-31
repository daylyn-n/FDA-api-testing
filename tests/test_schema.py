import requests

def test_get_post():
    response = requests.get("https://api.fda.gov/drug/event.json?limit=5")
    assert response.status_code == 200
