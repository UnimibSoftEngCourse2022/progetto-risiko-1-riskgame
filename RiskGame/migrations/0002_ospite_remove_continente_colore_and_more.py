# Generated by Django 4.0.1 on 2022-01-31 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RiskGame', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ospite',
            fields=[
                ('Nickname', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Assegnato', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='continente',
            name='Colore',
        ),
        migrations.RemoveField(
            model_name='statistiche',
            name='NicknameGiocatore',
        ),
        migrations.RemoveField(
            model_name='statistiche',
            name='NumeroTruppeGenerate',
        ),
        migrations.RemoveField(
            model_name='statistiche',
            name='NumeroTruppePerse',
        ),
        migrations.RemoveField(
            model_name='statistiche',
            name='TempoDiGioco',
        ),
        migrations.AddField(
            model_name='mappa',
            name='Difficolta',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='statistiche',
            name='IDGiocatore',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='territorio',
            name='Confini',
            field=models.ManyToManyField(blank=True, to='RiskGame.Territorio'),
        ),
        migrations.AddField(
            model_name='territorio',
            name='Mappa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RiskGame.mappa'),
        ),
        migrations.AlterField(
            model_name='mappa',
            name='Autore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='partita',
            name='Giocatori',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='territorio',
            name='NomeTerritorio',
            field=models.CharField(max_length=20),
        ),
        migrations.DeleteModel(
            name='GiocatoreRegistrato',
        ),
        migrations.AddField(
            model_name='partita',
            name='Ospiti',
            field=models.ManyToManyField(to='RiskGame.Ospite'),
        ),
    ]
