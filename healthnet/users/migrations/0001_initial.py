# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 19:34
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.models import User, Permission

from users.models import Person, Hospital, Admin

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('is_patient', models.BooleanField(default=False)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_nurse', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('signup', 'Signup as a user'),),
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Person')),
            ],
            options={
                'permissions': (('transfer', 'Transfer patient'), ('update_patient', 'Signup as a user'), ('update', 'Signup as a user'), ('logs', 'Look at activity logs')),
            },
            bases=('users.person',),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Person')),
                ('specialty_field', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'permissions': (('admit', 'Admit patient'), ('release', 'Release patient')),
            },
            bases=('users.person',),
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Person')),
                ('title', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'permissions': (('admit', 'Admit patient'), ('release', 'Release patient')),
            },
            bases=('users.person',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.Person')),
                ('admitted', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('update_patient', 'Signup as a user'), ('update', 'Signup as a user')),
            },
            bases=('users.person',),
        ),
        migrations.AddField(
            model_name='person',
            name='hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Hospital'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': (('admit', 'Admit patient'), ('release', 'Release patient'), ('view_cal', 'View patient calendar'))},
        ),
        migrations.AlterModelOptions(
            name='nurse',
            options={'permissions': (('admit', 'Admit patient'),)},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': (('admit', 'Admit patient'), ('release', 'Release patient'), ('view_cal', 'View patient calendar'), ('create_med_info', 'create med info'), ('update_med_info', 'update med info'), ('view_med_info', 'view med info'))},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'permissions': (('update_patient', 'Signup as a user'), ('update', 'Signup as a user'), ('view_med_info', 'view med info'))},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': (('admit', 'Admit patient'), ('release', 'Release patient'), ('view_cal', 'View patient calendar'), ('create_med_info', 'create med info'), ('update_med_info', 'update med info'), ('view_med_info', 'view med info'), ('transfer', 'transfer patient'))},
        ),
    ]
