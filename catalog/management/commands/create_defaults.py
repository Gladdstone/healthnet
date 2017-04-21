from optparse import make_option
from django.contrib.auth.models import User
from catalog.models import *


from django.core.management.base import  BaseCommand



class Command(BaseCommand):




    def handle(self, **options):
        load_users()

def load_users():
    hospital = Hospital(name='default_hospital')
    hospital.save()
    hospital2 = Hospital(name='default_hospital2')
    hospital2.save()
    admin = User.objects.create_user(username='default_admin', password='default_admin', first_name='admin')
    adminProfile = Admin()
    adminProfile.first_name = 'default'
    adminProfile.last_name = 'admin'
    adminProfile.user = admin
    doctor = User.objects.create_user(username='default_doctor', password='default_doctor', first_name='doctor')
    doctorProfile = Doctor()
    doctorProfile.first_name = 'default'
    doctorProfile.last_name = 'doctor'
    doctorProfile.user = doctor
    nurse = User.objects.create_user(username='default_nurse', password='default_nurse', first_name='nurse')
    nurseProfile = Nurse()
    nurseProfile.first_name = 'default'
    nurseProfile.last_name = 'nurse'
    nurseProfile.user = nurse
    patient = User.objects.create_user(username='default_patient', password='default_patient', first_name='patient')
    patientProfile = Patient()
    patientProfile.first_name = 'default'
    patientProfile.last_name = 'patient'
    patientProfile.user = patient
    medical_info = MedicalInfo()
    medical_info.save()
    patientProfile.medical_info = medical_info
    admin.save()
    doctor.save()
    nurse.save()
    patient.save()
    adminProfile.save()
    doctorProfile.save()
    nurseProfile.save()
    patientProfile.save()
    hospital.people.add(admin, doctor, nurse, patient)
    hospital.save()

    stats = SysStats()
    stats.hospital = hospital
    stats.save()

    stats2 = SysStats()
    stats2.hospital = hospital2
    stats2.save()

def main():
    load_users()

if __name__ == '__main__':
    main()