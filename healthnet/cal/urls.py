from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_appointment, name='create_appointment')
]
