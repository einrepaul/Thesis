# Generated by Django 3.2 on 2021-07-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RHU', '0018_alter_morbidityreport_cases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='morbidityreport',
            name='cases',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
