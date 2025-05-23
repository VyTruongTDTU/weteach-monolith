"""
URL configuration for configuration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Dynamically include all app URLs
apps_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apps')
app_names = [name for name in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, name))]

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Include each app's urls.py
for app_name in app_names:
    try:
        urlpatterns.append(path(f'{app_name}/', include(f'apps.{app_name}.urls')))
    except ModuleNotFoundError:
        pass  # Skip apps without a urls.py file
    # try:
    #     urlpatterns.append(path(f'api/{app_name}/', include(f'apps.{app_name}.api_urls')))
    # except ModuleNotFoundError:
    #     pass  # Skip apps without a urls.py file

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    