# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0009_consultorio_hora_maxima'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultorio',
            name='hora_maxima',
            field=models.TimeField(verbose_name='Hora m\xe1xima de reserva'),
        ),
    ]
