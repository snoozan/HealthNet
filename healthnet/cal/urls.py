from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_calendar, name='calendar'),
    url(r'^create/$', views.create_appointment, name='create'),
    url(r'^delete/$', views.delete_appointment, name='delete'),
    url(r'^edit/$', views.edit_appointment, name='edit')
]
