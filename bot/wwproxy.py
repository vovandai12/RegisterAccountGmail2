import requests
import json
from models.model import Wwproxy


def get_proxy(key):
    wwproxy = None
    try:
        url = f"https://wwproxy.com/api/client/proxy/available?key={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        if result:
            if result["status"] == "OK":
                if result["data"]:
                    wwproxy = Wwproxy(result["data"])
                    return wwproxy
        return wwproxy
    except Exception as e:
        return None
