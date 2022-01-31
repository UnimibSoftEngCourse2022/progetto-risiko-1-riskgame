from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


"""class GiocatoreRegistrato(models.Model):
    # campi del modello
    NickName = models.CharField(max_length=16, primary_key=True)
    Nome = models.CharField(max_length=45)
    Cognome = models.CharField(max_length=45)
    Email = models.CharField(max_length=45)
    Password = models.CharFielTerritorio.objects.count()d(max_length=16)"""


class Ospite(models.Model):
    Nickname = models.CharField(max_length=16, primary_key=True)
    Assegnato = models.IntegerField()

    @staticmethod
    def assegnaOspite():
        try:
            ospite = Ospite.objects.get(Assegnato=0)
            ospite.Assegnato = 1
            ospite.save()
        except ObjectDoesNotExist:
            ospite = Ospite(Nickname='Ospite' + str(Ospite.objects.count() + 1), Assegnato=1)
            ospite.save()
        return ospite.Nickname

    @staticmethod
    def rilasciaOspite(username):
        ospite = Ospite.objects.get(Nickname=username)
        ospite.Assegnato = 0
        ospite.save()


class Mappa(models.Model):
    IDMappa = models.IntegerField(primary_key=True)
    NomeMappa = models.CharField(max_length=45)
    # Autore = models.ForeignKey(GiocatoreRegistrato, on_delete=models.CASCADE)
    Autore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    PercorsoMappa = models.CharField(max_length=100, default="")
    Difficolta = models.CharField(max_length=20, default="")


class Partita(models.Model):
    IDPartita = models.IntegerField(primary_key=True)
    NumeroGiocatori = models.IntegerField()
    Difficolta = models.IntegerField()
    Mappa = models.ForeignKey(Mappa, on_delete=models.CASCADE)
    # Giocatori = models.ManyToManyField(GiocatoreRegistrato)
    Giocatori = models.ManyToManyField(settings.AUTH_USER_MODEL)
    Ospiti = models.ManyToManyField(Ospite)

    @staticmethod
    def getNuovoID():
        if (Partita.objects.count() == 0):
            return 1
        else:
            maxID = Partita.objects.latest('IDPartita').IDPartita
            return maxID + 1

    @staticmethod
    def getGiocatoriConnessi(idPartita):
        partita = Partita.objects.get(IDPartita=idPartita)
        return partita.Giocatori.count() + partita.Ospiti.count()

    @staticmethod
    def disconnettiGiocatore(idPartita, username):
        giocatore = User.objects.get(username=username)
        partita = Partita.objects.get(IDPartita=idPartita)
        partita.Giocatori.remove(giocatore)
        if (partita.Giocatori.count() + partita.Ospiti.count() == 0):
            Partita.objects.get(IDPartita=idPartita).delete()

    @staticmethod
    def connettiOspite(idPartita, username):
        ospite = Ospite.objects.get(Nickname=username)
        partita = Partita.objects.get(IDPartita=idPartita)
        partita.Giocatori.add(ospite)

    @staticmethod
    def disconnettiOspite(idPartita, username):
        ospite = Ospite.objects.get(Nickname=username)
        partita = Partita.objects.get(IDPartita=idPartita)
        partita.Ospiti.remove(ospite)
        if (partita.Giocatori.count() + partita.Ospiti.count() == 0):
            Partita.objects.get(IDPartita=idPartita).delete()

    @staticmethod
    def getMappa(idPartita):
        return Partita.objects.get(IDPartita=idPartita).Mappa.NomeMappa

    @staticmethod
    def getListaGiocatori(idPartita):
        partita = Partita.objects.get(IDPartita=idPartita)
        listRegistrati = partita.Giocatori.all()
        listOspiti = partita.Ospiti.all()
        listaGiocatori = []
        for giocatore in listRegistrati:
            listaGiocatori.append(giocatore.username)
        for ospite in listOspiti:
            listaGiocatori.append(ospite.Nickname)
        return listaGiocatori


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
    NumeroPartiteGiocate = models.IntegerField()

    @staticmethod
    def getListaStatistiche(usernamePl):
        idGiocatore = User.objects.filter(username=usernamePl).first().pk
        return Statistiche.objects.get(IDGiocatore=idGiocatore)


class Continente(models.Model):
    IDContinente = models.IntegerField(primary_key=True)
    NomeContinente = models.CharField(max_length=45)
    NumeroTruppe = models.IntegerField()
    Mappa = models.ForeignKey(Mappa, on_delete=models.CASCADE)

    @staticmethod
    def getListaContinentiMappa(mappa):
        objMappa = Mappa.objects.filter(NomeMappa=mappa).first()
        return Continente.objects.filter(Mappa=objMappa.IDMappa)


class Territorio(models.Model):
    IDTerritorio = models.IntegerField(primary_key=True)
    NomeTerritorio = models.CharField(max_length=20)
    Continente = models.ForeignKey(Continente, on_delete=models.CASCADE)
    Confini = models.ManyToManyField('self', blank=True)
    Mappa = models.ForeignKey(Mappa, on_delete=models.CASCADE, null=True)

    @staticmethod
    def getListaTerritoriMappa(mappa):
        listaTerritori = []
        listaContinenti = Continente.getListaContinentiMappa(mappa)
        for continente in listaContinenti:
            territoriContinente = Territorio.objects.filter(Continente=continente.IDContinente)
            for territorio in territoriContinente:
                listaTerritori.append(territorio)
        return listaTerritori


class Carta(models.Model):
    Territorio = models.ForeignKey(Territorio, on_delete=models.CASCADE)
    Simbolo = models.CharField(max_length=45)
    Jolly = models.IntegerField()

# class GiocatoreRegistrato_Partita(models.Model): incluso in Partita
