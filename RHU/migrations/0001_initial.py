# Generated by Django 3.2 on 2022-03-21 01:32

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(0, 'Unknown'), (10, 'Patient'), (20, 'Doctor'), (30, 'Admin')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MorbidityReport',
            fields=[
                ('report_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('barangay', models.CharField(blank=True, choices=[('Aripdip', 'Aripdip'), ('Ilongbukid', 'Ilongbukid'), ('Poscolon', 'Poscolon'), ('San Florentino', 'San Florentino'), ('Calaigang', 'Calaigang')], max_length=50)),
                ('disease', models.CharField(blank=True, max_length=100)),
                ('classification', models.CharField(blank=True, choices=[('C', 'Communicable Disease'), ('NC', 'Non-communicable Disease')], max_length=10)),
                ('cases', models.IntegerField(blank=True, null=True)),
                ('totalcases', models.IntegerField(blank=True, null=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Morbidity Report',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=50)),
                ('lastname', models.CharField(blank=True, max_length=50)),
                ('sex', models.CharField(blank=True, choices=[('', '-----'), ('M', 'Male'), ('F', 'Female')], default=0, max_length=1)),
                ('birthday', models.DateField(default=datetime.date(1000, 1, 1))),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('stats_id', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('stats', models.CharField(max_length=100)),
                ('freq', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('timeslot_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('prescription_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField()),
                ('medication', models.CharField(max_length=100)),
                ('strength', models.CharField(max_length=30)),
                ('instruction', models.CharField(max_length=200)),
                ('refill', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('header', models.CharField(max_length=300)),
                ('body', models.CharField(max_length=1000)),
                ('read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='RHU.account')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to='RHU.account')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalTest',
            fields=[
                ('medtest_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=200)),
                ('private', models.BooleanField(default=True)),
                ('completed', models.BooleanField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docs', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Medical Tests',
            },
        ),
        migrations.CreateModel(
            name='MedicalInfo',
            fields=[
                ('date', models.DateField(null=True)),
                ('caseNumber', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('age', models.CharField(max_length=3, null=True)),
                ('sex', models.CharField(blank=True, choices=[('', '-----'), ('M', 'Male'), ('F', 'Female')], default=0, max_length=1)),
                ('civilStatus', models.CharField(blank=True, choices=[('', '-----'), ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Separated', 'Separated'), ('Widowed', 'Widowed')], default=0, max_length=20)),
                ('barangay', models.CharField(blank=True, choices=[('', '------'), ('Aripdip', 'Aripdip'), ('Ilongbukid', 'Ilongbukid'), ('Poscolon', 'Poscolon'), ('San Florentino', 'San Florentino'), ('Calaigang', 'Calaigang'), ('San Dionisio', 'San Dionisio')], default=0, max_length=50)),
                ('temperature', models.CharField(max_length=5, null=True)),
                ('pulse', models.CharField(max_length=5, null=True)),
                ('respiration', models.CharField(max_length=5, null=True)),
                ('bloodPressure', models.CharField(max_length=10, null=True)),
                ('height', models.CharField(max_length=5, null=True)),
                ('weight', models.CharField(max_length=5, null=True)),
                ('bloodType', models.CharField(choices=[('', '-----'), ('A+', 'A+ TYPE'), ('B+', 'B+ TYPE'), ('AB+', 'AB+ TYPE'), ('O+', 'O+ TYPE'), ('A-', 'A- TYPE'), ('B-', 'B- TYPE'), ('AB-', 'AB- TYPE'), ('O-', 'O- TYPE')], default=0, max_length=10)),
                ('comments', models.CharField(max_length=700)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Medical Info',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL)),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RHU.timeslot')),
            ],
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'None'), (1, 'Account'), (2, 'Patient'), (3, 'Admin'), (4, 'Appointment'), (5, 'Medical Test'), (6, 'Prescription'), (7, 'Admission'), (8, 'Medical Info'), (9, 'Message'), (10, 'Morbidity Report')], default=0)),
                ('timePerformed', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RHU.profile'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
