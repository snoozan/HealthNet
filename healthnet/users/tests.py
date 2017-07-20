from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from users.models.person import Patient, Doctor, Person, Admin, Nurse
from . import views


class PersonTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        User.objects.create_user(username='Logan', password='alkdfjad;lfkjadfklj', pk='20')
        self.user = User.objects.get(pk='20')
        Person.objects.all().delete()

    def test_create_new_person(self):
        p = Person.objects.create(name='Logan', user=self.user)
        self.assertEqual(Person.objects.get(name='Logan'), p)

    def test_create_new_patient(self):
        Patient.objects.create(name='Logan', user=self.user)
        self.assertEqual(Patient.objects.get(name='Logan').name, 'Logan')

    def test_create_new_doctor(self):
        Doctor.objects.create(name='Logan', user=self.user)
        self.assertEqual(Doctor.objects.get(name='Logan').name, 'Logan')

    def test_create_new_nurse(self):
        Nurse.objects.create(name='Logan', user=self.user)
        self.assertEqual(Nurse.objects.get(name='Logan').name, 'Logan')

    def test_users_can_login(self):
        Patient.objects.create(name='Logan', user=self.user)
        p = Patient.objects.get(name='Logan')
        self.assertTrue(self.user.is_active)

    def test_users_can_signup(self):
        request = self.factory.get('/users/signup/')
        response = views.signup_patient(request)
        self.assertEqual(response.status_code, 200)

    def test_admins_can_admit_patients(self):
        a = Admin(name='Logan', user=self.user)
        request = self.factory.post('/users/admit/')
        request.person = a
        request.user = a.user
        response = views.update(request)
        self.assertEqual(response.status_code, 200)

    def test_admins_can_create_doctor(self):
        a = Admin(name='Logan', user=self.user)
        request = self.factory.post('/users/update_doctor/')
        request.person = a
        request.user = a.user
        response = views.update(request)
        self.assertEqual(response.status_code, 200)

    def test_patient_can_not_create_doctor(self):
        Patient.objects.create(name='Logan', user=self.user)
        p = Patient.objects.get(name='Logan')
        request = self.factory.get('users/update_doctor')
        request.person = p
        request.user = p.user
        response = views.update(request)
        self.assertEqual(response.status_code, 200)






