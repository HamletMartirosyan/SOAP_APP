from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.exchange_rates_by_date, name='my_soap_app'),
    # re_path(r'^convert/', views.exchange_rates, name='exchange_rates')
]
