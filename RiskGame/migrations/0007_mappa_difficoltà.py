# Generated by Django 4.0.1 on 2022-01-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiskGame', '0006_remove_mappa_difficoltà'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappa',
            name='Difficoltà',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
