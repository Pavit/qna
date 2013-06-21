# Django settings for qna project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os
import dj_database_url
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

if not os.environ.get("HEROKU_DEV", False):  ### LOCAL DATABASE SETTINGS / FACEBOOK INFO
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'django_db',                      # Or path to database file if using sqlite3.
            'USER': 'django_login',                      # Not used with sqlite3.
            'PASSWORD': 'samir342',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
    FACEBOOK_APP_ID = '343120432448964'
    FACEBOOK_API_SECRET  = 'f43073165e02ef728f31a315cd9fa6de'
else:
    # HEROKU DATABASE SETTINGS / FACEBOOK INFO
    DATABASES = {'default': dj_database_url.config()}
    FACEBOOK_API_SECRET  = "924a5a01f43de7d991cd1c17edf4469b"
    FACEBOOK_APP_ID = "406831919365032"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fy-vjj@x#h+qdo)8hf_!tlarj&amp;kv_iz@b-f-juu#h6ts1pxa3u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'qna.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'qna.wsgi.application'

ROOT_PATH = os.path.dirname(__file__)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH,"templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # 'south',
    'core',
    'questions',
    # 'social_auth',
    'facepy',
    'wadofstuff.django.serializers',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # 'social_auth.context_processors.social_auth_login_redirect',
    # 'social_auth.context_processors.social_auth_backends',

)

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PROFILE_MODULE= 'core.UserProfile'
#---------social_auth settings--------------------
# SOCIAL_AUTH_USER_MODEL = 'core.UserProfile'
LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/questions/'
LOGIN_ERROR_URL    = '/login-error/'

FACEBOOK_EXTENDED_PERMISSIONS = [
    'email','friends_likes','user_about_me',
    'user_birthday', 'friends_birthday', 'friends_about_me',
    'user_location', 'friends_location','user_relationships','friends_relationships',
    'friends_education_history','user_education_history','user_interests',
    'friends_interests','user_relationship_details','friends_relationship_details','user_religion_politics',
    'friends_religion_politics',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
