# Generated by Django 4.2.1 on 2023-07-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0020_alter_applied_upload_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applied',
            name='upload_resume',
            field=models.ImageField(upload_to='jobapp/static'),
        ),
    ]
