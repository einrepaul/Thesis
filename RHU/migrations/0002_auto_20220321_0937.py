# Generated by Django 3.2 on 2022-03-21 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RHU', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'verbose_name_plural': 'Appointments'},
        ),
        migrations.AlterModelOptions(
            name='timeslot',
            options={'verbose_name_plural': 'Time Slots'},
        ),
    ]