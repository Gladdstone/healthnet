# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-04-18 12:27
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('hospital', models.CharField(default='', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='AdmissionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('discharge_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admission_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('hospital', models.CharField(default='', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, unique=True)),
                ('people', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_entry', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['time'],
            },
        ),
        migrations.CreateModel(
            name='MedicalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.CharField(help_text='inches', max_length=200)),
                ('weight', models.CharField(help_text='lbs', max_length=200)),
                ('eye_color', models.CharField(max_length=200)),
                ('birthday', models.DateField(default=datetime.date(2000, 1, 1))),
                ('race', models.CharField(max_length=200)),
                ('sex', models.CharField(max_length=200)),
                ('diastolic_blood_pressure', models.IntegerField(blank=True, help_text='mmHg', null=True)),
                ('systolic_blood_pressure', models.IntegerField(blank=True, help_text='mmHg', null=True)),
                ('heart_rate', models.IntegerField(blank=True, help_text='BPM', null=True)),
            ],
            options={
                'ordering': ['birthday'],
            },
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('hospital', models.CharField(default='', max_length=200)),
                ('current_doctor', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_doctor', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nurse_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('insurance', models.CharField(default='', max_length=200)),
                ('pref_hospital', models.CharField(default='', max_length=200)),
                ('emergency_contact_first_name', models.CharField(default='', max_length=200)),
                ('emergency_contact_last_name', models.CharField(default='', max_length=200)),
                ('emergency_contact_email', models.CharField(default='', max_length=200, validators=[django.core.validators.RegexValidator(message="Email must be entered in the format: 'xxxx@yyyy.zzz'.", regex='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)')])),
                ('admission_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Hospital')),
                ('emergency_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('medical_info', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.MedicalInfo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Prescriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('notes', models.CharField(blank=True, max_length=500)),
                ('patient', models.CharField(default='', max_length=200)),
                ('associated_doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_prescription', to=settings.AUTH_USER_MODEL)),
                ('associated_hospital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hospital_prescriptions', to=settings.AUTH_USER_MODEL)),
                ('associated_patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_prescription', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_field', models.CharField(max_length=200)),
                ('sender_field', models.CharField(max_length=200)),
                ('message_content', models.CharField(max_length=200)),
                ('created_at', models.TimeField(default=datetime.time)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SysStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_count', models.IntegerField(default=0)),
                ('doctor_count', models.IntegerField(default=0)),
                ('nurse_count', models.IntegerField(default=0)),
                ('admin_count', models.IntegerField(default=0)),
                ('timestamp', models.DateField(default=django.utils.timezone.now)),
                ('hospital', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='catalog.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('results', models.CharField(max_length=500)),
                ('comments', models.CharField(max_length=200)),
                ('released', models.BooleanField()),
                ('doctor', models.CharField(max_length=50)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['type', 'doctor'],
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=200)),
                ('password', models.CharField(default='', max_length=200)),
                ('re_enter_password', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200, validators=[django.core.validators.RegexValidator(message="Email must be entered in the format: 'xxxx@yyyy.zzz'.", regex='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)')])),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.AddField(
            model_name='admissioninfo',
            name='statistics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admissions', to='catalog.SysStats'),
        ),
    ]