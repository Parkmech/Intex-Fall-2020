# Generated by Django 3.1.2 on 2020-12-09 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='files'),
        ),
    ]
