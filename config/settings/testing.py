from config.settings.base import *

DEBUG = False

SECRET_KEY = "test_secret_key"

ALLOWED_HOSTS = ["*"]

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

LOGGING_CONFIG = None
