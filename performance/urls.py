from django.urls import path
from . import views

app_name = 'performance'
urlpatterns = [
    path("view-orders/", views.view_orders, name='view_orders'),
    path("monthly-performance/", views.view_monthly_performance, name='monthly_performance'),
    path("yearly-performance/", views.view_yearly_performance, name='yearly_performance'),
]