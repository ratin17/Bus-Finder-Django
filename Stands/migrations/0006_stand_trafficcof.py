# Generated by Django 4.0.10 on 2024-07-21 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stands', '0005_area_a_no_stand_s_no_alter_stand_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='stand',
            name='trafficCof',
            field=models.PositiveIntegerField(default=50),
        ),
    ]
