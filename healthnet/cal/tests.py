from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from users.models.person import Patient, Doctor, Person, Nurse
from .models import Appointment
from . import views

class CalTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create_user(username='Logan', password='alkdfjad;lfkjadfklj', pk='20')
        self.user = User.objects.get(pk='20')
        Person.objects.all().delete()

    def test_can_create_appointment(self):
        p = Patient.objects.create(name='Logan', user=self.user)
        user = User.objects.create_user(username='Something', password='alkdfjad;lfkjadfklj', pk='19')
        Person.objects.all().delete()
        d = Doctor.objects.create(name='Logan', user=user)
        a = Appointment.objects.create(description='Hello', patient=p, doctor=d)
        self.assertEqual(Appointment.objects.get(description='Hello'), a)

    def test_appointment_permissions(self):
        p = Patient.objects.create(name='Logan', user=self.user, is_patient=True)
        self.client.login(username='Roger', password='alkdfjad;lfkjadfklj')
        request = self.factory.get('/cal/create/')
        request.user = self.user
        response = views.create_appointment(request)
        self.assertEqual(response.status_code, 200)
