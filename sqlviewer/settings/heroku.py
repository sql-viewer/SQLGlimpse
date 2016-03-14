from sqlviewer.settings.common import *

__author__ = 'Stefan Martinov <stefan.martinov@gmail.com>'

import dj_database_url

DEBUG = False

DATABASES = {
    "default": dj_database_url.config(default=os.environ['DATABASE_URL'])
}
