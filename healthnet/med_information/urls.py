from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admitted/$', views.admitted, name='admitted_patients'),
]
