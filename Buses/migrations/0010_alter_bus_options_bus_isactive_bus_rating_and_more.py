# Generated by Django 4.0.10 on 2024-02-14 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buses', '0009_alter_orderingmodel_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bus',
            options={'ordering': ['-rating']},
        ),
        migrations.AddField(
            model_name='bus',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='rating',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AddField(
            model_name='bus',
            name='service',
            field=models.CharField(default='Semi-Sitting', max_length=100),
        ),
    ]
