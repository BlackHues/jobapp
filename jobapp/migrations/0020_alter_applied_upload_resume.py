# Generated by Django 4.2.1 on 2023-07-11 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0019_rename_companyname_applied_company_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applied',
            name='upload_resume',
            field=models.FileField(upload_to='jobapp/static'),
        ),
    ]