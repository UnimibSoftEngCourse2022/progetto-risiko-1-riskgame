# Generated by Django 4.0.1 on 2022-01-11 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Continente',
            fields=[
                ('IDContinente', models.IntegerField(primary_key=True, serialize=False)),
                ('NomeContinente', models.CharField(max_length=45)),
                ('Colore', models.CharField(max_length=45)),
                ('NumeroTruppe', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GiocatoreRegistrato',
            fields=[
                ('NickName', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Nome', models.CharField(max_length=45)),
                ('Cognome', models.CharField(max_length=45)),
                ('Email', models.CharField(max_length=45)),
                ('Password', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Mappa',
            fields=[
                ('IDMappa', models.IntegerField(primary_key=True, serialize=False)),
                ('NomeMappa', models.CharField(max_length=45)),
                ('PercorsoMappa', models.CharField(max_length=100)),
                ('Autore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RiskGame.giocatoreregistrato')),
            ],
        ),
        migrations.CreateModel(
            name='Statistiche',
            fields=[
                ('NicknameGiocatore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='RiskGame.giocatoreregistrato')),
                ('NumeroPartiteVinte', models.IntegerField()),
                ('NumeroPartitePerse', models.IntegerField()),
                ('PercentualeVinte', models.FloatField()),
                ('NumeroScontriVinti', models.IntegerField()),
                ('NumeroScontriPersi', models.IntegerField()),
                ('NumeroScontriVintiATK', models.IntegerField()),
                ('NumeroScontriPersiATK', models.IntegerField()),
                ('NumeroScontriVintiDEF', models.IntegerField()),
                ('NumeroScontriPersiDEF', models.IntegerField()),
                ('PercentualeScontriVintiATK', models.FloatField()),
                ('TempoDiGioco', models.TimeField()),
                ('NumeroTruppeGenerate', models.IntegerField()),
                ('NumeroTruppePerse', models.IntegerField()),
                ('NumeroPartiteGiocate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Territorio',
            fields=[
                ('IDTerritorio', models.IntegerField(primary_key=True, serialize=False)),
                ('NomeTerritorio', models.CharField(max_length=45)),
                ('Continente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RiskGame.continente')),
            ],
        ),
        migrations.CreateModel(
            name='Partita',
            fields=[
                ('IDPartita', models.IntegerField(primary_key=True, serialize=False)),
                ('NumeroGiocatori', models.IntegerField()),
                ('Difficolta', models.IntegerField()),
                ('Giocatori', models.ManyToManyField(to='RiskGame.GiocatoreRegistrato')),
                ('Mappa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RiskGame.mappa')),
            ],
        ),
        migrations.AddField(
            model_name='continente',
            name='Mappa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RiskGame.mappa'),
        ),
        migrations.CreateModel(
            name='Carta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Simbolo', models.CharField(max_length=45)),
                ('Jolly', models.IntegerField()),
                ('Territorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RiskGame.territorio')),
            ],
        ),
    ]
