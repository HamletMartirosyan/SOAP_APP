from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^by_date/$', views.exchange_rates_by_date),
    re_path(r'^by_date_by_iso/$', views.exchange_rates_by_date_by_iso),
    re_path(r'^/latest/', views.exchange_rates_latest),
    re_path(r'^/latest_by_iso/', views.exchange_rates_latest_by_iso),
    re_path(r'^/iso_odes/', views.exchange_rates_iso_codes),
]
