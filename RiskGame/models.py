from django.db import models

# Create your models here.


class GiocatoreRegistrato(models.Model):
    # campi del modello
    NickName = models.CharField(max_length=16, primary_key=true)
    Nome = models.CharField(max_length=45)
    Cognome = models.CharField(max_length=45)
    Email = models.CharField(max_length=45)
    Password = models.CharField(max_length=16)
    pass


class Mappa(models.Model):
    IDMappa = models.IntegerField(primary_key=true)
    NomeMappa = models.CharField(max_length=45)
    Autore = models.ForeignKey(GiocatoreRegistrato)
    PercorsoMappa = models.CharField(max_length=100)
    pass


class Partita(models.Model):
    IDPartita = models.IntegerField(primary_key=true)
    NumeroGiocatori = models.IntegerField
    Difficolta = models.IntegerChoices('1', '2', '3')
    Mappa = models.ForeignKey(Mappa)
    Giocatori = models.ManyToManyField(GiocatoreRegistrato)
    pass


class Statistiche(models.Model):
    NicknameGiocatore = models.ForeignKey(GiocatoreRegistrato, primary_key=true)
    NumeroPartiteVinte = models.IntegerField()
    NumeroPartitePerse = models.IntegerField()
    PercentualeVinte = models.FloatField()
    NumeroScontriVinti = models.IntegerField()
    NumeroScontriPersi = models.IntegerField()
    NumeroScontriVintiATK = models.IntegerField()
    NumeroScontriPersiATK = models.IntegerField()
    NumeroScontriVintiDEF = models.IntegerField()
    NumeroScontriPersiDEF = models.IntegerField()
    PercentualeScontriVintiATK = models.FloatField()
    TempoDiGioco = models.TimeField()
    NumeroTruppeGenerate = models.IntegerField()
    NumeroTruppePerse = models.IntegerField()
    NumeroPartiteGiocate = models.IntegerField()
    pass


class Continente(models.Model):
    IDContinente = models.IntegerField(primary_key=true)
    NomeContinente = models.CharField(max_length=45)
    Colore = models.CharField(max_length=45)
    NumeroTruppe = models.IntegerField()
    Mappa = models.ForeignKey(Mappa)
    pass


class Territorio(models.Model):
    IDTerritorio = models.IntegerField(primary_key=true)
    NomeTerritorio = models.CharField(max_length=45)
    Continente = models.ForeignKey(Continente)
    pass


class Carta(models.Model):
    Territorio = models.ForeignKey(Territorio)
    Simbolo = models.CharField(max_length=45)
    Jolly = models.IntegerField()
    pass

#class GiocatoreRegistrato_Partita(models.Model): incluso in Partita
