# Generated by Django 4.2.1 on 2023-07-05 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0007_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]