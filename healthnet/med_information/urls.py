from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^result/create/(?P<patientid>[0-9]+)$', views.createTestResult, name='create_result'),
    url(r'^result/update/(?P<resultid>[0-9]+)/$', views.updateTestResult, name='update_result'),
    url(r'^result/view/(?P<patientid>[0-9]+)/$', views.viewTestResult, name='view_result'),
    url(r'^result/view/$', views.viewTestResult, name='view_result'),
    url(r'^prescription/create/(?P<patientid>[0-9]+)$', views.createPrescription, name='create_prescription'),
    url(r'^prescription/update/(?P<prescriptionid>[0-9]+)/$', views.updatePrescription, name='update_prescription'),
    url(r'^prescription/view/(?P<patientid>[0-9]+)/$', views.viewPrescription, name='view_prescription'),
    url(r'^prescription/view/$', views.viewPrescription, name='view_prescription'),
    url(r'^record/create/(?P<patientid>[0-9]+)$', views.createRecord, name='create_record'),
    url(r'^record/update/(?P<recordid>[0-9]+)/$', views.updateRecord, name='update_record'),
    url(r'^record/view/(?P<patientid>[0-9]+)/$', views.viewRecord, name='view_record'),
    url(r'^record/view/$', views.viewRecord, name='view_record')
]
