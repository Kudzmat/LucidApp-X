from django.urls import path
from . import views

app_name = 'local_orders'
urlpatterns = [
    path("new-local-order/", views.new_local_order, name='new_local_order'),
]