from sqlviewer.settings.common import *

DEBUG = True
# we only need the engine name, as heroku takes care of the rest
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

