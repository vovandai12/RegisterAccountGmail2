import requests
import json
from models.model import Tmproxy


def get_proxy(key):
    tmproxy = None
    try:
        url = "https://tmproxy.com/api/proxy/get-new-proxy"
        payload = json.dumps({"api_key": key})
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        if result["code"] == 0:
            if result["data"]:
                tmproxy = Tmproxy(result["data"])
                return tmproxy
        return tmproxy
    except Exception as e:
        return None
