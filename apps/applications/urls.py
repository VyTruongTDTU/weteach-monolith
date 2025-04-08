from django.urls import path
from . import views

app_name = 'apps.applications'

urlpatterns = [
    # Example URL patterns
    path('', views.index, name='index'),
]