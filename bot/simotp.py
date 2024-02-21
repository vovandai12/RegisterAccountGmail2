import requests
import json
from models.model import Simotp


def buy_phone_number(key, service):
    simotp = None
    try:
        if key is None:
            return None
        url = "https://simotp.net/api/v1/order"
        payload = json.dumps({"service": service})
        headers = {
            "Authorization": f"OTP {key}",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        if result:
            if "data" in result:
                simotp = Simotp(result["data"])
        return simotp
    except Exception as e:
        return None


def get_otp(key, id_phone):
    simotp = None
    try:
        url = "https://simotp.net/api/v1/order/{}".format(id_phone)
        headers = {
            "Authorization": f"OTP {key}",
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers)
        result = json.loads(response.text)
        print(result)
        if result:
            if "data" in result:
                simotp = Simotp(result["data"])
        return simotp
    except Exception as e:
        return None
