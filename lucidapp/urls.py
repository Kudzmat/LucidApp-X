from django.urls import path
from . import views

app_name = 'lucidapp'
# The URL patterns for the lucidapp application
urlpatterns = [
    path("", views.home, name='home'),
]