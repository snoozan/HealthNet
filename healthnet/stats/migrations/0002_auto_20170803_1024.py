# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 14:24
from __future__ import unicode_literals

from django.db import migrations

def create_stats(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Stats = apps.get_model('stats', 'Statistics')
    Hospital = apps.get_model('users', 'Hospital')

    uor = Hospital.objects.using(db_alias).get(name="UoR Hospital")
    strong = Hospital.objects.using(db_alias).get(name="Strong Memorial Hospital")

    Stats.objects.using(db_alias).create(hospital=uor)
    Stats.objects.using(db_alias).create(hospital=strong)


def delete_stats(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Stats = apps.get_model('stats', 'Statistics')

    Stats.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_stats,  delete_stats),
    ]
