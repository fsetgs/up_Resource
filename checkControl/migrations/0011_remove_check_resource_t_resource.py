# Generated by Django 3.2 on 2023-01-04 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkControl', '0010_check_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='check_resource',
            name='t_resource',
        ),
    ]
