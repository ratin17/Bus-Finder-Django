# Generated by Django 4.0.10 on 2024-01-25 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buses', '0007_alter_bus_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bus',
            options={'ordering': ['b_name']},
        ),
    ]
