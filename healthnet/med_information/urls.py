from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^admitted/$', views.admitted, name='admitted_patients'),
  url(r'^result/create/$', views.createTestResult, name='create_test_result'),
  url(r'^prescription/create/$', views.createPrescription, name='create_prescription'),
  url(r'^record/create/$', views.createRecord, name='create_record')
]
