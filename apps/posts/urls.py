from django.urls import path
from .views import HomePageView

app_name = 'apps.posts'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]