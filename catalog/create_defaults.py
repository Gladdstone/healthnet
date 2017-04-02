from optparse import make_option

from django.conf import settings

settings.configure()
from django.contrib.auth.models import User
from .models import Hospital


from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        load_users()

def load_users(self):
    hospital = Hospital(name='default_hospital')
    hospital.save()
    hospital2 = Hospital(name='default_hospital2')
    hospital2.save()
    admin = User.objects.create_user(username='default_admin', password='default_admin', first_name='admin')
    doctor = User.objects.create_user(username='default_doctor', password='default_doctor', first_name='doctor')
    nurse = User.objects.create_user(username='default_nurse', password='default_nurse', first_name='nurse')
    patient = User.objects.create_user(username='default_patient', password='default_patient', first_name='patient')
    admin.save()
    doctor.save()
    nurse.save()
    patient.save()


def main():
    load_users()

if __name__ == '__main__':
    main()