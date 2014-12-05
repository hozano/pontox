# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiaTrabalho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField()),
            ],
            options={
                'ordering': ['-data'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registro', models.DateTimeField(verbose_name=b'%m/%d/%Y %H:%M')),
                ('dia_trabalho', models.ForeignKey(to='core.DiaTrabalho')),
            ],
            options={
                'ordering': ['-registro'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Regra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('horario_entrada', models.TimeField()),
                ('horario_saida', models.TimeField()),
                ('departamento', models.ForeignKey(to='core.Departamento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=120)),
                ('arquivo', models.FileField(upload_to=b'media/%Y%m%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=120)),
                ('carga_horaria_semanal', models.IntegerField(default=20, blank=True)),
                ('departamento', models.ForeignKey(to='core.Departamento')),
            ],
            options={
                'ordering': ['nome'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='diatrabalho',
            name='usuario',
            field=models.ForeignKey(to='core.Usuario'),
            preserve_default=True,
        ),
    ]
