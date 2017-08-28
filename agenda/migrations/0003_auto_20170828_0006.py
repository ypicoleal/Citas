# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 00:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_auto_20170823_0512'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionCita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cancelado', models.BooleanField()),
                ('calendario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.CalendarioCita')),
            ],
        ),
        migrations.RemoveField(
            model_name='citamedica',
            name='fin',
        ),
        migrations.RemoveField(
            model_name='citamedica',
            name='inicio',
        ),
        migrations.AlterField(
            model_name='citacancelada',
            name='cita',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.AsignacionCita'),
        ),
        migrations.AlterField(
            model_name='citareprogramada',
            name='cita',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.AsignacionCita'),
        ),
        migrations.AddField(
            model_name='asignacioncita',
            name='cita',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.CitaMedica'),
        ),
    ]
