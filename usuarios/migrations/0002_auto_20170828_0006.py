# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivacionUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('key1', models.CharField(max_length=100)),
                ('key2', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.IntegerField(choices=[(1, 'Medico'), (2, 'Paciente')])),
            ],
        ),
        migrations.AddField(
            model_name='medico',
            name='activado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paciente',
            name='activado',
            field=models.BooleanField(default=False),
        ),
    ]
