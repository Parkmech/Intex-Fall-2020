# Generated by Django 3.1.2 on 2020-12-05 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0005_auto_20201205_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=3000),
        ),
    ]