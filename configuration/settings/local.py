from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS += ["debug_toolbar"]  # Add dev-only packages

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
