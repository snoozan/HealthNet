# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_auto_20170721_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time_hour',
            field=models.CharField(choices=[('8', '8 a.m.'), ('9', '9 a.m.'), ('10', '10 a.m.'), ('11', '11 a.m.'), ('12', '12 p.m.'), ('1', '1 p.m.'), ('2', '2 p.m.'), ('3', '3 p.m.'), ('4', '4 p.m.')], default='12', max_length=2, null=True),
        ),
    ]
