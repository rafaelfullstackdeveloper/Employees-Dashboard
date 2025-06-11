#-------------------------------------------------------------------------------
# Name:        settings.py
# Purpose:     Main configuration for the Django project for the job tracking app.
#
# Author:      rafaelfullstackdeveloper
#
# Created:     31/05/2025
# Copyright:   (c) rafaelfullstackdeveloper 2025
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------

import os
from decouple import config
from pathlib import Path

# Defines the base directory of the project, pointing to the parent directory of the settings.py file.
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key used for cryptographic security in Django. Loaded from environment variable for increased security.
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')

# Habilita ou desabilita o modo de depuração. Deve ser False em produção para evitar exposição de informações sensíveis.
DEBUG = config('DEBUG', default=True, cast=bool)

# List of allowed hosts to run the application. Includes localhost for development.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# List of installed apps in the project, including Django default apps, REST Framework, CORS, and the custom 'job_tracker' app.
INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin interface.
    'django.contrib.auth',           # User authentication system.
    'django.contrib.contenttypes',   # Framework for generic content types.
    'django.contrib.sessions',       # Session management support.
    'django.contrib.messages',       # Notification messaging framework.
    'django.contrib.staticfiles',    # Static files management.
    'rest_framework',                # Django REST Framework for building APIs.
    'corsheaders',                   # Support for CORS (Cross-Origin Resource Sharing).
    'job_tracker',                   # Custom app for job tracking.
]

# List of middleware that process requests and responses. Each middleware adds specific functionality.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',                 # Allows requests from different origins (CORS).
    'django.middleware.security.SecurityMiddleware',         # Adds security headers (e.g., HTTPS).
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages user sessions.
    'django.middleware.common.CommonMiddleware',             # Common functionalities like URL attack prevention.
    'django.middleware.csrf.CsrfViewMiddleware',             # Protection against CSRF attacks.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Binds authenticated users to requests.
    'django.contrib.messages.middleware.MessageMiddleware',     # Manages notification messages.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Protects against clickjacking attacks.
]

# Defines the project's root URL module, which maps the application's routes.
ROOT_URLCONF = 'myproject.urls'

# List of allowed origins for CORS requests, used to allow communication with local frontends.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # Frontend running locally on port 3000.
    "http://127.0.0.1:3000",    # Alternative address for localhost.
]

# Django REST Framework settings for API permissions and pagination.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allows unrestricted access to APIs by default (should be adjusted in production).
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Enables pagination in API responses.
    'PAGE_SIZE': 20  # Sets the number of items per page in paginated responses.
}

# Database configuration. Uses SQLite by default for simplicity in development.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite database engine.
        'NAME': BASE_DIR / 'db.sqlite3',         # Path to the database file.
    }
}

# Default language code for the application, set to Brazilian Portuguese.
LANGUAGE_CODE = 'pt-br'

# Application time zone, set to São Paulo, Brazil.
TIME_ZONE = 'America/Sao_Paulo'

# Enables internationalization (translations) support.
USE_I18N = True

# Enables time zone support for dates and times in the project.
USE_TZ = True
