# Generated by Django 5.1.1 on 2024-09-03 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_parser', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='uri',
            new_name='url',
        ),
    ]
