import requests
from models.model import Profile, ProfileRun
from fake_useragent import UserAgent
import traceback


class GPMLoginAPI(object):
    API_START_PATH = "/api/v3/profiles/start"
    API_STOP_PATH = "/api/v3/profiles/close"
    API_CREATE_PATH = "/api/v3/profiles/create"
    API_PROFILE_LIST_PATH = "/api/v3/profiles"
    API_PROFILE_PATH = "/api/v3/profile"
    API_DELETE_PATH = "/api/v3/profiles/delete"

    _apiUrl = ""

    def __init__(self, apiUrl: str):
        self._apiUrl = apiUrl

    # Lấy danh sách profiles
    def GetProfiles(self):
        try:
            data = []
            url = f"{self._apiUrl}{self.API_PROFILE_LIST_PATH}"
            print(url)
            resp = requests.get(url)
            result = resp.json()
            if isinstance(result["data"], list):
                for item in result["data"]:
                    data.append(Profile(data=item))
            elif isinstance(result["data"], dict):
                data = Profile(data=result["data"])
            else:
                data = None
            return data
        except Exception as e:
            print(f"error GetProfiles() {type(e)} {str(e)}")
            return None

    # Lấy thông tin 1 profile
    def GetProfile(self, id=""):
        try:
            data = None
            url = f"{self._apiUrl}{self.API_PROFILE_PATH}/{id}"
            print(url)
            resp = requests.get(url)
            result = resp.json()
            data = Profile(data=result["data"])
            return data
        except Exception as e:
            print(f"error GetProfile() id={id} {type(e)} {str(e)}")
            return None

    # Tạo mới 1 profile
    # raw_proxy
    # HTTP proxy| IP:Port:User:Pass
    # Socks5| socks5://IP:Port:User:Pass
    # TMProxy| tm://API_KEY|True,False
    # TinProxy| tin://API_KEY|True,False
    # TinsoftProxy| tinsoft://API_KEY|True,False
    def CreateProfile(
        self,
        profile_name: str,
        group: str = "All",
        raw_proxy: str = "",
        startup_urls: str = "",
    ):
        try:
            user_agent = UserAgent(browsers=["edge", "chrome"]).random
            url = f"{self._apiUrl}{self.API_CREATE_PATH}"
            print(url)
            data = {
                "profile_name": f"{profile_name}",
                "group_name": f"{group}",
                "browser_core": "chromium",
                "browser_name": "Chrome",
                "browser_version": "127.0.6533.73",
                "is_random_browser_version": False,
                "raw_proxy": f"{raw_proxy}",
                "startup_urls": f"{startup_urls}",
                "user_agent": f"{user_agent}",
            }
            resp = requests.post(url, json=data)
            result = resp.json()
            return Profile(data=result["data"])
        except Exception as e:
            print(f"error CreateProfile() {type(e)} {str(e)}")
            return None

    # Mở profile
    def Start(
        self,
        profileId: str,
        win_scale: int = 0.8,
        win_pos: str = "0,0",
        win_size: str = "800,600",
    ):
        try:
            data = None
            url = f"{self._apiUrl}{self.API_START_PATH}/{profileId}"
            if win_scale > 0:
                url += f"?win_scale={win_scale}"
            if win_pos != "":
                url += f"&win_pos={win_pos}"
            if win_size != "":
                url += f"&win_size={win_size}"
            print(url)
            resp = requests.get(url)
            result = resp.json()
            data = ProfileRun(data=result["data"])
            return data
        except Exception as e:
            print(f"error Start() {type(e)} {str(e)}")
            return None

    # Đóng profile
    def Stop(self, profileId: str):
        try:
            url = f"{self._apiUrl}{self.API_STOP_PATH}/{profileId}"
            requests.get(url)
        except Exception as e:
            print(f"error Stop() {type(e)} {str(e)}")

    # Xoá profile
    def Delete(self, profileId: str):
        try:
            url = f"{self._apiUrl}{self.API_DELETE_PATH}/{profileId}"
            requests.get(url)
        except Exception as e:
            print(f"error Delete() {type(e)} {str(e)}")
