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
    url(r'^signup/$', views.signup_patient, name='signup'),
    url(r'^update_nurse/(?P<pk>[0-9]+)/$', views.update_nurse, name='update_nurse'),
    url(r'^update_doctor/(?P<pk>[0-9]+)/$', views.update_doctor, name='update_doctor'),
    url(r'^update_admin/(?P<pk>[0-9]+)/$', views.update_admin, name='update_admin'),
    url(r'^create_nurse/$', views.create_nurse, name='create_nurse'),
    url(r'^create_doctor/$', views.create_doctor, name='create_doctor'),
    url(r'^create_admin/$', views.create_admin, name='create_admin'),
    url(r'^update_employees/$', views.update, name='update'),
    url(r'^admit/$', views.admit_patient, name='admit_patient'),
    url(r'^release/$', views.release_patient, name='release_patient'),
    url(r'^transfer/$', views.transfer_view, name='transfer_patients'),
    url(r'^transfer/(?P<pk>[0-9]+)/$', views.transfer_patient, name='transfer'),
]

