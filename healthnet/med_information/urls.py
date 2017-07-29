from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^admitted/$', views.admitted, name='admitted_patients'),
  url(r'^result/createResult$', views.createTestResult, name='create_test_result'),

]
