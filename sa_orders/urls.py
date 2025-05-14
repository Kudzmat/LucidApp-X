from django.urls import path
from . import views

app_name = 'sa_orders'
urlpatterns = [
    path("new-sa-order/", views.new_sa_order, name='new_sa'),
]