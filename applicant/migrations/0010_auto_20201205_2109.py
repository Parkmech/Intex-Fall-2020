# Generated by Django 3.1.2 on 2020-12-05 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0009_auto_20201205_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
