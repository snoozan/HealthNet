# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 03:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170721_0219'),
        ('cal', '0002_appointment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='hospital',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Hospital'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time_hour',
            field=models.CharField(choices=[('8', '8 a.m.'), ('9', '9 a.m.'), ('10', '10 a.m.'), ('11', '11 a.m.'), ('12', '12 p.m.'), ('1', '1 p.m.'), ('2', '2 p.m.'), ('3', '3 p.m.'), ('4', '4 p.m.'), ('5', '5 p.m.')], default='12', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='time_min',
            field=models.CharField(choices=[('00', '00'), ('30', '30')], default='00', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Doctor'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Patient'),
        ),
    ]