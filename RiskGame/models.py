from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class GiocatoreRegistrato(models.Model):
    # campi del modello
    NickName = models.CharField(max_length=16, primary_key=True)
    Nome = models.CharField(max_length=45)
    Cognome = models.CharField(max_length=45)
    Email = models.CharField(max_length=45)
    Password = models.CharField(max_length=16)


class Mappa(models.Model):
    IDMappa = models.IntegerField(primary_key=True)
    NomeMappa = models.CharField(max_length=45)
    # Autore = models.ForeignKey(GiocatoreRegistrato, on_delete=models.CASCADE)
    Autore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    PercorsoMappa = models.CharField(max_length=100)


class Partita(models.Model):
    IDPartita = models.IntegerField(primary_key=True)
    NumeroGiocatori = models.IntegerField()
    Difficolta = models.IntegerField()
    Mappa = models.ForeignKey(Mappa, on_delete=models.CASCADE)
    # Giocatori = models.ManyToManyField(GiocatoreRegistrato)
    Giocatori = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def getNuovoID():
        if (Partita.objects.count() == 0):
            return 1
        else: 
            maxID = Partita.objects.latest('IDPartita').IDPartita
            return maxID + 1

    def disconnettiGiocatore(idPartita, username):
        giocatore = User.objects.get(username=username)
        partita = Partita.objects.get(IDPartita=idPartita)
        partita.Giocatori.remove(giocatore)
        if (partita.Giocatori.count() == 0):
            Partita.objects.get(IDPartita=idPartita).delete()


class Statistiche(models.Model):
    # NicknameGiocatore = models.OneToOneField(GiocatoreRegistrato, primary_key=True, on_delete=models.CASCADE)
    IDGiocatore = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True,
                                       on_delete=models.CASCADE)
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


class Continente(models.Model):
    IDContinente = models.IntegerField(primary_key=True)
    NomeContinente = models.CharField(max_length=45)
    Colore = models.CharField(max_length=45)
    NumeroTruppe = models.IntegerField()
    Mappa = models.ForeignKey(Mappa, on_delete=models.CASCADE)


class Territorio(models.Model):
    IDTerritorio = models.IntegerField(primary_key=True)
    NomeTerritorio = models.CharField(max_length=20)
    Continente = models.ForeignKey(Continente, on_delete=models.CASCADE)
    Confini = models.ManyToManyField('self', blank=True)
    # La riga sopra aggiunge anche il territorio come confine a se stesso,
    # andranno fatti dei controlli dopo


class Carta(models.Model):
    Territorio = models.ForeignKey(Territorio, on_delete=models.CASCADE)
    Simbolo = models.CharField(max_length=45)
    Jolly = models.IntegerField()

#class GiocatoreRegistrato_Partita(models.Model): incluso in Partita
