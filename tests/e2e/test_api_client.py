import requests
from sandwichchampion import config


def test_api_is_running():
    url = config.get_api_url()
    r = requests.get(f"{url}/api/is_alive")

    assert r.status_code == 200
    assert r.json()["message"] == "It's alive!"
