DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'codeinthehole_prod',                      # Or path to database file if using sqlite3.
        'USER': 'codeinthehole',                      # Not used with sqlite3.
        'PASSWORD': 'asdfjk433sdfoi123sdfnkl123i',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
DEBUG = False

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader',
        (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
    ),
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
