from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view_calendar, name='calendar'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.view_calendar, name='view_calendar'),
    url(r'^create/$', views.create_appointment, name='create'),
    url(r'^delete/([0-9]+)$', views.delete_appointment, name='delete'),
    url(r'^edit/$', views.edit_appointment, name='edit'),
    url(r'^update/([0-9]+)$', views.edit_appointment, name='update')
]
