# Generated by Django 4.0.1 on 2022-01-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiskGame', '0002_ospite_remove_continente_colore_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappa',
            name='PercorsoMappa',
            field=models.CharField(default='', max_length=100),
        ),
    ]