# Generated by Django 3.1.1 on 2020-09-01 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clearedlogs',
            name='clearance_time',
        ),
    ]
