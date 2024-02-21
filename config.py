import json
from file_paths import FilePaths

RUN = "run"
SUCCESS = "success"
ERROR = "error"
NONE = "none"

TMPROXY = "https://tmproxy.com"
PROXYSHOPLIKE = "https://proxy.shoplike.vn"
PROXYFB = "https://proxyfb.com"

BOSSOTP = "https://bossotp.com"
IRONSIM = "https://ironsim.com"
VIOTP = "https://viotp.com"
SIMOTP = "https://simotp.net"
HCOTP = "https://hcotp.com"


def LoadConfig():
    config = None
    try:
        with open(FilePaths.CONFIG_JSON.value, encoding="utf-8") as f:
            config_json = json.load(f)
            config = Config(config_json)
    except Exception as e:
        config = Config({})
        WriteConfig(config)
    return config


def WriteConfig(config):
    config_json = json.dumps(config.__dict__)
    with open(FilePaths.CONFIG_JSON.value, "w", encoding="utf-8") as f:
        f.write(config_json)


class Config:
    def __init__(self, config={}):
        self.methodProxy = config.get("methodProxy", NONE)
        self.keyProxy = config.get("keyProxy", [])
        self.numberAccount = config.get("numberAccount", 1000)
        self.numberThread = config.get("numberThread", 5)
        self.methodOtp = config.get("methodOtp", NONE)
        self.keyOtp = config.get("keyOtp", NONE)
        self.defaultPassword = config.get("defaultPassword", NONE)
        self.randomPassword = config.get("randomPassword", NONE)
        self.fullName = config.get("fullName", NONE)
        self.gender = config.get("gender", NONE)
        self.token = config.get("token", NONE)
        self.numberCol = config.get("numberCol", 10)
        self.serialKey = config.get("serialKey", NONE)
        self.fileRecovery = config.get("fileRecovery", NONE)


global_config = Config()
