import os
import urllib
import json


def decode_env(env):
    _env = {}
    for k, v in env.items():
        if type(v) == int:
            _env[k] = v
        elif type(v) == str:
            try:
                _env[k] = json.loads(v)
            except:
                _env[k] = str(v)
    return _env


class Config(object):
    TEMPLATES_AUTO_RELOAD = True
    APP_DIRECTORY = os.getcwd() + "/app"
    TESTING = False


class Production(Config):
    PORT = 8080
    LOCAL_ENV = decode_env(os.environ)
    CLIENT_ID = LOCAL_ENV.get("client_id")
    CLIENT_SECRET = LOCAL_ENV.get("client_secret")
    VCAP_APPLICATION = LOCAL_ENV.get("VCAP_APPLICATION")
    VCAP_SERVICES = LOCAL_ENV.get("VCAP_SERVICES")

    if VCAP_SERVICES:
        DATABASE_HOST = VCAP_SERVICES["aws-rds"][0]["credentials"]["host"]
        DATABASE_USERNAME = VCAP_SERVICES["aws-rds"][0]["credentials"]["username"]
        DATABASE_PASSWORD = VCAP_SERVICES["aws-rds"][0]["credentials"]["password"]
        DATABASE_NAME = VCAP_SERVICES["aws-rds"][0]["credentials"]["db_name"]
        DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}"

    REDIRECT_URI = "https://template-flask-usmc.app.cloud.gov/auth/callback"
    LOGOUT_REDIRECT_URI = "https://template-flask-usmc.app.cloud.gov/"
    UAA_AUTHORIZE_URI = "https://login.fr.cloud.gov/oauth/authorize"
    UAA_LOGOUT_URI = "https://login.fr.cloud.gov/logout"
    UAA_TOKEN_URI = "https://uaa.fr.cloud.gov/oauth/token"


class Testing(Config):
    TEMPLATES_AUTO_RELOAD = True
    TESTING = True
    HOST = "0.0.0.0"
    PORT = 8000
    LOCAL_ENV = decode_env(os.environ)

    CLIENT_ID = "my_client_id"
    CLIENT_SECRET = "my_client_secret"

    DATABASE_HOST = "database"
    DATABASE_USERNAME = "testing"
    DATABASE_PASSWORD = "testing"
    DATABASE_NAME = "testing"
    DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}"

    REDIRECT_URI = f"http://localhost:{PORT}/auth/callback"
    UAA_AUTHORIZE_URI = "http://localhost:8080/oauth/authorize"
    LOGOUT_REDIRECT_URI = f"http://localhost:{PORT}/"
    UAA_LOGOUT_URI = "http://localhost:8080/logout"
    UAA_TOKEN_URI = "http://localhost:8080/oauth/token"
