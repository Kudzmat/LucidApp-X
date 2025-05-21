from django.urls import path
from . import views

app_name = 'performance'
urlpatterns = [
    path("view-orders/", views.view_orders, name='view_orders'),
]