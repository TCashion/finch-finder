# Generated by Django 3.0.5 on 2020-06-17 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='date',
        ),
    ]
