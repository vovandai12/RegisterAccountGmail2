import requests
import json
from models.model import Proxyfb


def get_proxy(key):
    proxyfb = None
    try:
        url = f"http://api.proxyfb.com/api/changeProxy.php?key={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        if "success" in result:
            if result["success"]:
                proxyfb = Proxyfb(result)
                return proxyfb
        return proxyfb
    except Exception as e:
        return None
