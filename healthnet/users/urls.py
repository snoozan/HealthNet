from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # index /users
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^update/$', views.update_profile, name='update_patient'),
    url(r'^create_hospital/$', views.create_hospital, name='create_hospital'),
    url(r'^signup/$', views.signup_patient, name='signup'),
    url(r'^update_nurse/$', views.update_nurse, name='update_nurse'),
    url(r'^update_doctor/$', views.update_doctor, name='update_doctor'),
    url(r'^update_admin/$', views.update_admin, name='update_admin'),
    url(r'^admit/$', views.admit_patient, name='admit_patient'),
    url(r'^release/$', views.release_patient, name='release_patient'),
    url(r'^transfer/$', views.transfer_patient, name='transfer_patient'),
]

