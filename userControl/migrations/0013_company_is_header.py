# Generated by Django 3.2 on 2023-01-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userControl', '0012_auto_20221229_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_header',
            field=models.CharField(default='0', max_length=5, verbose_name='是否为总部'),
        ),
    ]
