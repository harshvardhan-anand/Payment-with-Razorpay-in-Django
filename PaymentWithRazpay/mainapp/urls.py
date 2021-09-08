from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('simplepay', views.simple_payment, name='simplepay'),
    path('store_verify', views.store_and_verify_payment, name='store_verify'),
]