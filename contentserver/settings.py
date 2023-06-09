"""
Django settings for contentserver project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


import os


import django
from django.utils.translation import gettext
django.utils.translation.ugettext = gettext
gettext = lambda s: s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's80n+h2p)j$4yv08ny^&pvohmc@fl1+8h3ghxn=_tiz7%q&099'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [

    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_countries',
    'phonenumber_field',
    'users',
    #'PhoneNumber',
    'products',
    'orders',
    'payment',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.yahoo',
    'allauth.socialaccount.providers.amazon',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'cms',
    'menus',
    'api',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'aldryn_apphooks_config',
    'parler',
    'taggit',
    'taggit_autosuggest',
    'meta',
    'sortedm2m',
    'djangocms_blog',
    'django_extensions',
    'djangocms_bootstrap5',
    'djangocms_file',
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_googlemap',
    'djangocms_video',
    'contentserver',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
]


ROOT_URLCONF = 'contentserver.urls'

WSGI_APPLICATION = 'contentserver.wsgi.application'


DATABASES = {
    'default': {
        'CONN_HEALTH_CHECKS': 'False',
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST': 'jodybeggs.mysql.pythonanywhere-services.com',
        # 'NAME': 'jodybeggs$content_server',
        'HOST': '127.0.0.1',
        'NAME': 'plantsanctuary$content_server',
        'PASSWORD': 'dfasdfsdaf424ffdsdad!@',
        'PORT': '',
        'USER': 'jodybeggs'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_ROOT = '/home/jodybeggs/contentserver/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/jodybeggs/contentserver/static'
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'contentserver', 'static'),
)

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'server', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]


MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]



LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'en',
            'name': gettext('en'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('ps_home.html', 'Home'),
    ('ps_about.html', 'About'),
    ('ps_shop.html', 'Shop'),
    ('ps_shop_details.html', 'Shop Details'),
    ('ps_portfolio.html', 'Portfolio'),
    ('ps_single_portfolio.html', 'Single Portfolio'),
    ('ps_contact.html', 'Contact'),
    ('ps_checkout.html', 'Checkout'),
    ('ps_blog.html', 'Blog'),
    ('ps_single_post.html', 'Blog - Single Post'),
    ('services.html', 'Services'),
    ('products.html', 'Products'),
)

X_FRAME_OPTIONS = 'SAMEORIGIN'

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#LOGIN AND
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v13.0',
    },
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url',
        ]
    }
}
TOKEN_LENGTH = 100

STRIPE_SECRET_KEY = 'Fsdfasfdafsd4f3@R231R'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
META_SITE_PROTOCOL = 'https'  # set 'http' for non ssl enabled websites
META_USE_SITES = True

# META_USE_OG_PROPERTIES=True
# META_USE_TWITTER_PROPERTIES=True
# META_USE_GOOGLEPLUS_PROPERTIES=True # django-meta 1.x+
# META_USE_SCHEMAORG_PROPERTIES=True  # django-meta 2.x+

PARLER_LANGUAGES = {
    1: (
        {'code': 'en',},
        # {'code': 'it',},
        # {'code': 'fr',},
    ),
    'default': {
        'fallbacks': [
            'en',
            #'it',
            #'fr'
        ],
    }
}

BLOG_AVAILABLE_PERMALINK_STYLES = (
    ('full_date', 'Full date'),
    ('short_date', 'Year /  Month'),
    ('category', 'Category'),
)

BLOG_PERMALINK_URLS = {
    "full_date": "<int:year>/<int:month>/<int:day>/<str:slug>/",
    "short_date": "<int:year>/<int:month>/<str:slug>/",
    "category": "<str:category>/<str:slug>/",
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'
