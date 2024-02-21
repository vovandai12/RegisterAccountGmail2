import requests
import json
from models.model import ProxyShopLike


def get_proxy(key):
    proxyShopLike = None
    try:
        url = f"http://proxy.shoplike.vn/Api/getNewProxy?access_token={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        if result["status"] == "success":
            if result["data"]:
                proxyShopLike = ProxyShopLike(result["data"])
                return proxyShopLike
        return proxyShopLike
    except Exception as e:
        return None
