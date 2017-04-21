# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 04:07
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date(2000, 1, 1))),
                ('time', models.TimeField(default=datetime.time)),
                ('year', models.IntegerField()),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('doctor', models.CharField(max_length=200)),
                ('patient', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('associated_doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointment', to=settings.AUTH_USER_MODEL)),
                ('associated_patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_appointment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
