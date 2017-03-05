# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 23:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_auto_20170304_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientProfileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('phone_number', models.CharField(default='', max_length=200)),
                ('insurance', models.CharField(default='', max_length=200)),
                ('pref_hospital', models.CharField(default='', max_length=200)),
                ('emergency_contact', models.CharField(default='', max_length=200)),
                ('medical_info', models.CharField(default='', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='PatientRegisterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=200)),
                ('password', models.CharField(default='', max_length=200)),
                ('email', models.CharField(default='', max_length=200)),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]