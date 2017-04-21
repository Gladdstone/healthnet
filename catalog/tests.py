from django.test import TestCase
from django.contrib.auth.models import User

from .models import *
import os



"""def main():

    HospitalTests.test_hospital()"""
class CatalogTests(TestCase):
    def setUp(self):
        admin = User.objects.create_user(username = 'test_admin', password= 'test_admin', first_name='admin')
        admin.save()
        patient = User.objects.create_user(username='test_patient', password='test_patient', first_name='patient')
        patient.save()
        doctor = User.objects.create_user(username='test_doctor', password='test_doctor', first_name='doctor')
        doctor.save()
        nurse = User.objects.create_user(username='test_nurse', password='test_nurse', first_name='nurse')
        nurse.save()
    def test_hospital(self):
        hospital = Hospital(name='test')

        admin = User.objects.get(username='test_admin')
        patient = User.objects.get(username='test_patient')
        doctor = User.objects.get(username='test_doctor')
        nurse = User.objects.get(username='test_nurse')

        hospital.save()
        hospital.people.add(admin)
        hospital.people.add(patient)
        hospital.people.add(doctor)
        hospital.people.add(nurse)

        self.assertEqual(hospital.people.all().count(), 4)
        self.assertEqual(admin.hospital_set.get(name='test'), hospital)
        hospital.people.remove(admin)
        self.assertEqual(hospital.people.all().count(), 3)
        hospital.people.add(admin)
        self.assertEqual(hospital.people.all().count(), 4)
        self.assertEqual(hospital.people.filter(first_name='admin').count(), 1)
        admin2 = User.objects.create_user(username='test_admin2', password='test_admin2', first_name='admin')
        admin2.save()
        hospital.people.add(admin2)
        self.assertEqual(Hospital.objects.all()[0], hospital)



"""if __name__ == '__main__':
    main()"""