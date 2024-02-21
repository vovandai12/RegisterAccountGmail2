import requests
import json
from models.model import Viotp, ViotpSMS


def buy_phone_number(key):
    viotp = None
    try:
        url = f"https://api.viotp.com/request/getv2?token={key}&serviceId=3"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if result["status_code"] == 200:
            if result["data"]:
                viotp = Viotp(result["data"])
                return viotp
        return viotp
    except Exception as e:
        return None


def get_otp(key, id_phone):
    viotpsms = None
    try:
        url = f"https://api.viotp.com/session/getv2?requestId={id_phone}&token={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        if result["status_code"] == 200:
            if result["data"]:
                viotpsms = ViotpSMS(result["data"])
                return viotpsms
        return viotpsms
    except Exception as e:
        return viotpsms
