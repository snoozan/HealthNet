from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admitted$', views.admitted, name='admitted'),
    #url(r'^create/(?P<pid>[0-9]+)/$', views.create_appointment, name='createwithpatient'),

]
