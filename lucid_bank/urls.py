from django.urls import path
from . import views

app_name = 'lucid_bank'
urlpatterns = [
    path("bank-withdrawal/", views.withdrawal, name='bank_withdrawal'),
    path("make-payment/", views.make_payment, name='make_payment'),
    path("make-transfer/", views.make_transfer, name='make_transfer'),
    path("view-statement/", views.view_statement, name='view_statement'),
]