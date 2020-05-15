"""
Django settings for project project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z5^%hz=%(5p-+=w1l=^^yo6$ybhh49du2&_on%0c=ip8_wzw0+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DB_ALIAS_MASTER = 'default'
DATABASES = {
    DB_ALIAS_MASTER: {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PGDATABASE') or 'drr',
        'USER': os.environ.get('PGUSER') or 'drr_user',
        'PASSWORD': os.environ.get('PGPASSWORD') or 'pass',
        'HOST': os.environ.get('PGHOST') or 'localhost',
        'PORT': int(os.environ.get('PGPORT') or 5432),
    },

}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

# Specifics to Django Read Replicas (DRR)

DB_ALIAS_REPLICA_1 = 'replica1'
# Need autocommit so mirror can see actions of master.
# Otherwise, master actions are inside a transaction.
DATABASES[DB_ALIAS_MASTER]['AUTOCOMMIT'] = True

# Replica definition
DATABASES[DB_ALIAS_REPLICA_1] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ.get('PGDATABASE') or 'drr',
    'USER': os.environ.get('PGUSER') or 'drr_user',
    'PASSWORD': os.environ.get('PGPASSWORD') or 'pass',
    'HOST': os.environ.get('PGHOST_REPLICA_1') or 'localhost',
    'PORT': int(os.environ.get('PGPORT_REPLICA_1') or 5433),
    'TEST': {
        # Non-standard Django DATABASES > TEST key for use in DRR
        'REPLICA': True,
    }
}

DATABASE_ROUTERS = ['replicas.db.MasterReplicaRouter']

TEST_RUNNER = 'replicas.test.DiscoverRunnerWithReadReplicas'

print('Printing DATABASES for debugging purposes')
print(DATABASES)
