# Hydro settings

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
APPLICATION_NAME = 'HYDRO'

SECRET_KEY = '8lu*6g0lg)9w!ba+a$edk)xx)x%rxgb$i1&amp;022shmi1jcgihb*'

# SESSION_TIMEOUT is used in validate_session_active decorator to see if the
# session is active.
SECOND = 1
MINUTE = SECOND * 60
SECONDS_IN_DAY = SECOND*86400

MYSQL_CACHE_DB = 'cache'
MYSQL_STATS_DB = 'stats'
MYSQL_CACHE_TABLE = 'hydro_cache_table'

CACHE_IN_MEMORY_KEY_EXPIRE = 600
CACHE_DB_KEY_EXPIRE = 86400
USE_STATS_DB = False

DATABASES = {
    'stats': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_STATS_DB,
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;",
            "compress": True
        },
    },

    'cache': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_CACHE_DB,
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;",
            "compress": True
        },
    },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cache',
        'USER': 'root',
        'PASSWORD': 'xxxx',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            "init_command": "SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;",
            "compress": True
        }
    },
}
