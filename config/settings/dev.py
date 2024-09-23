import mimetypes

from config.settings.base import *
from config.settings.base import INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = "yux_r7p^axv&6iom1bid+$=mnrlf8)6-%4m^ro!d9^n7w*aoos"

ALLOWED_HOSTS = ["*"]

DEV_ONLY_PACKAGES = ["debug_toolbar"]

INSTALLED_APPS += DEV_ONLY_PACKAGES

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


# Debug Toolbar settings
def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}

INTERNAL_IPS = ["127.0.0.1"]

mimetypes.add_type("application/javascript", ".js", True)

INTERNAL_IPS = ["127.0.0.1"]

ENABLE_DEBUG_TOOLBAR = True
