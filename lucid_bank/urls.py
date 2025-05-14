from django.urls import path
from . import views

app_name = 'lucid_bank'
urlpatterns = [
    path("bank-withdrawal/", views.withdrawal, name='bank_withdrawal'),
]