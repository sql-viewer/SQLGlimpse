import dj_database_url
from sqlviewer.settings.common import *

DEBUG = True
db_from_env = dj_database_url.config(conn_max_age=500)
# we only need the engine name, as heroku takes care of the rest
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

DATABASES['default'].update(db_from_env)
