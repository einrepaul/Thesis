# Generated by Django 3.2.1 on 2022-03-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RHU', '0008_auto_20220328_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_id',
        ),
        migrations.AddField(
            model_name='appointment',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
