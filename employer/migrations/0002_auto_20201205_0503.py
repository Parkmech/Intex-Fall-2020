# Generated by Django 3.1.2 on 2020-12-05 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]
