__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'

import dj_database_url

DEBUG = False

DATABASES = {
    "default": dj_database_url.config()
}
