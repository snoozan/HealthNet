from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from users.models.person import Patient, Doctor, Person, Admin, Nurse
from .models.prescription import Prescription
from . import views

class MedicalTestCases(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create_user(username='Logan', password='alkdfjad;lfkjadfklj', pk='20')
        self.user = User.objects.get(pk='20')
        Person.objects.all().delete()

    def test_can_create_prescription(self):
        p = Patient.objects.create(name="Logan", user=self.user)
        request = self.factory.get('/med/prescription/create/')
        request.user = self.user
        response = views.createPrescription(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.post('/med/prescription/create/')
        request.user = self.user
        request.person = p
        response = views.createPrescription(request, p.id)
        self.assertEqual(response.status_code, 302)

    def test_can_create_test_result(self):
        request = self.factory.get('/med/result/create/')
        request.user = self.user
        response = views.createTestResult(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.post('/med/result/create/')
        request.user = self.user
        response = views.createTestResult(request)
        self.assertEqual(response.status_code, 302)

    def test_can_create_record(self):
        request = self.factory.get('/med/record/create/')
        request.user = self.user
        response = views.createRecord(request)
        self.assertEqual(response.status_code, 302)
        request = self.factory.post('/med/record/create/')
        request.user = self.user
        response = views.createRecord(request)
        self.assertEqual(response.status_code, 302)

    def test_view_prescription(self):
        Patient.objects.create(name='Logan', user=self.user)
        request = self.factory.get('/med/prescription/view/')
        request.user = self.user
        response = views.viewPrescription(request)
        self.assertEqual(response.status_code, 302)
