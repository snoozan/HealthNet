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
        response = views.createPrescription(request)
        self.assertEqual(response.status_code, 200)
        request = self.factory.post('/med/prescription/create/')
        request.user = self.user
        request.person = p
        response = views.createPrescription(request, p.id)
        self.assertEqual(response.status_code, 302)

    def test_can_update_prescription(self):
        Prescription.objects.create(title="Hi", duration=10, startDate='2017-04-20', instructions='up it')
        request = self.factory.get('/med/prescription/update/')
        response = views.updatePrescription(request, 1)
        self.assertEqual(response.status_code, 200)


