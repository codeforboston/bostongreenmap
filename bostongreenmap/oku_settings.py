# Parse database configuration from $DATABASE_URL
from os import environ

GEOS_LIBRARY_PATH = environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = environ.get('GDAL_LIBRARY_PATH')

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'dev.files.bostongreenmap.org'

import dj_database_url
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['OPTIONS'] = {
      'options': '-c search_path=bostongreenmap,public'
    }


AWS_QUERYSTRING_AUTH = False
MEDIA_URL = '/media/'
MEDIA_ROOT = '//dev.files.bostongreenmap.org/'

AWS_S3_SECURE_URLS = False

AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'dev.files.bostongreenmap.org'
AWS_PRELOAD_METADATA = True

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '/'


STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# MEDIA_ROOT = '/'
# MEDIA_URL = 'http://dev.files.bostongreenmap.org/'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
POSTGIS_VERSION = (2,1,2)
# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))