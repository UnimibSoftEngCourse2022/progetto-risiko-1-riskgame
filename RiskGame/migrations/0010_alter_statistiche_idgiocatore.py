# Generated by Django 4.0.1 on 2022-01-30 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RiskGame', '0009_remove_statistiche_numerotruppegenerate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistiche',
            name='IDGiocatore',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]