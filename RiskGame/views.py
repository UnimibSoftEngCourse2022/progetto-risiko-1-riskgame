from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm
from RiskGame.models import *
from django.db.models import Count
import os
import random
from django.contrib.auth.models import User
import json
import math
from django.http import HttpResponse


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            user=User.objects.filter(username = username).first()
            Statistiche.objects.create(
                IDGiocatore = user, 
                NumeroPartiteVinte = 0, 
                NumeroPartitePerse = 0, 
                PercentualeVinte = 0.0, 
                NumeroScontriVinti = 0,
                NumeroScontriPersi = 0,
                NumeroScontriVintiATK = 0,
                NumeroScontriPersiATK = 0,
                NumeroScontriVintiDEF = 0,
                NumeroScontriPersiDEF = 0,
                PercentualeScontriVintiATK = 0.0,
                TempoDiGioco = None,
                NumeroTruppeGenerate = 0,
                NumeroTruppePerse = 0,
                NumeroPartiteGiocate = 0
            )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registrazione.html', {'form': form})


class HomePageView(TemplateView):
    template_name = "home.html"

    # class LoginView(TemplateView):
    #   template_name = "login.html"

    """def controlUserData(request):
        if request.method == "POST":
            NickName = request.POST['nickname']
            Password = request.POST['password']
            if GiocatoreRegistrato.objects.filter(NickName=NickName, Password=Password).exists():
                return render(request, 'menu.html')
            else:
                messages.warning(request, 'i dati sono errati')
                return render(request, 'login.html')"""


class RegistrazioneView(TemplateView):
    template_name = "registrazione.html"

    """def saveUserData(request):
        if request.method == "POST":
            NickName = request.POST['nickname']
            Nome = request.POST['nome']
            Cognome = request.POST['cognome']
            Email = request.POST['email']
            Password = request.POST['password']

            GiocatoreRegistrato.objects.create(Nome=Nome, Cognome=Cognome, NickName=NickName,
                                               Email=Email,
                                               Password=Password)
            messages.success(request, 'I dati sono stati salvati')
            return redirect(reverse('RiskGame:home'))"""


class MenuView(TemplateView):
    template_name = "menu.html"

    def drawMenu(request):
        request.session['ospite'] = 'null'
        return render(request, "menu.html")
    
    def drawOspite(request):
        request.session['ospite'] = Ospite.assegnaOspite()
        return render(request, "menu.html")


class ImpostazioniView(TemplateView):
    template_name = "impostazione.html"


class CreazioneView(TemplateView):
    def draw(request):
        username = User.objects.get(username=request.user.username)
        template_name = "creazione.html"
        mappe = Mappa.objects.filter(Autore=username)
        list_mappe = []
        for i in mappe:
            div = i.NomeMappa.split("-")
            nome = div[0]
            if not nome in list_mappe:
                list_mappe.append(nome)
        maps = {
            "nomi": list_mappe
        }
        return render(request, template_name, maps)



class PartecipaView(TemplateView):
    template_name = "partecipa.html"

    def loadPartite(request):
        temp_data = Partita.objects.all()
        return render(request, "partecipa.html", {"partita_package": temp_data})


class PartitaView(TemplateView):
    template_name = "partita.html"

    def creaPartita(request):
        # Crea la partita nel DB, aggiunge il nuovo giocatore e lo reindirizza alla partita
        nuovoID = Partita.getNuovoID()
        numGiocatori = request.GET['giocatori']
        difficolta = request.GET['difficolta']
        mappa = Mappa.objects.filter(NomeMappa=request.GET['mappa']+'-'+difficolta).first()

        if (difficolta=='Semplice'):
            intDiff = 1
        elif (difficolta=='Media'):
            intDiff = 2
        elif (difficolta=='Difficile'):
            intDiff = 3

        Partita.objects.create(IDPartita=nuovoID, NumeroGiocatori=numGiocatori,
            Difficolta=intDiff, Mappa=mappa)
        if (request.user.is_authenticated):
            Partita.objects.get(IDPartita=nuovoID).Giocatori.add(request.user)
        else:
            ospite = Ospite.objects.get(Nickname=request.session['ospite'])
            Partita.objects.get(IDPartita=nuovoID).Ospiti.add(ospite)

        return redirect(reverse('RiskGame:partecipaPartita', kwargs={'PartitaID': nuovoID}))

    def partecipaPartita(request, PartitaID):
        # Aggiunge il giocatore alla lista giocatori e lo reindirizza alla partita
        partita = Partita.objects.get(IDPartita=PartitaID)
        if request.user.is_authenticated:
            partita.Giocatori.add(request.user)
        else:
            ospite = Ospite.objects.get(Nickname=request.session['ospite'])
            partita.Ospiti.add(ospite)
        return render(request, "partita.html", {"Partita": partita, "PartitaID": PartitaID,
            "Ospite": request.session['ospite']})
        


class StatisticheView(TemplateView):
    def draw(request):
        username = User.objects.get(username=request.user.username)
        template_name = "statistiche.html"
        statistica = Statistiche.objects.filter(IDGiocatore=username)
        stats = {
            "statistiche": statistica
        }
        return render(request, template_name, stats)


class CredenzialiView(TemplateView):
    def draw(request):
        userprofile_form = UserRegisterForm(request.POST if request.POST else None,
                                           instance=User.objects.get(username=request.user))
        if request.method == 'POST':
            if userprofile_form.is_valid():
                userprofile_form.save()
                return redirect('login')

        return render(request, 'credenziali.html', context={'userprofile_form': userprofile_form})


"""def saveUserData(request):
    if request.method == "POST":
        NickName = request.POST['nickname']
        Nome = request.POST['nome']
        Cognome = request.POST['cognome']
        Email = request.POST['email']
        Password = request.POST['password']
        GiocatoreRegistrato.objects.create(Nome=Nome, Cognome=Cognome, NickName=NickName, Email=Email,
                                           Password=Password)
        messages.success(request, 'I dati sono stati salvati')
    return render(request, 'registrazione.html')"""


"""def controlUserData(request):
    if request.method == "POST":
        NickName = request.POST['nickname']
        Password = request.POST['password']
        if GiocatoreRegistrato.objects.filter(NickName=NickName, Password=Password).exists():
            return render(request, 'menu.html')
        else:
            messages.warning(request, 'i dati sono errati')

            return render(request, 'login.html')"""


class MappaView(TemplateView):
    template_name = "editor.html"

    def saveMappa(request):
        if request.method == "POST":
            n_random = random.randint(0, 1000)
            nome_mappa = request.POST['nome-mappa']
            username = User.objects.get(username=request.user.username)
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'static\Mappe')
            while Mappa.objects.filter(IDMappa=n_random).exists():
                n_random = random.randint(0, 1000)
            div = nome_mappa.split("-")
            difficolta = div[1]
            Mappa.objects.create(IDMappa=n_random, NomeMappa=nome_mappa, Autore=username, PercorsoMappa=filename, Difficolta = difficolta)
            if difficolta == "Difficile":
                MappaView.loadMappaDifficile(request)
            if difficolta == "Media":
                MappaView.loadMappaDifficile(request)
            if difficolta == "Semplice":
                MappaView.loadMappaDifficile(request)
            return render(request, 'menu.html')

    def loadMappaDifficile(request):
        template_name = "editor.html"
        mappa = None
        data = None
        if request.method == "POST":
            nome_mappa = request.POST['nome-mappa']
            username = User.objects.get(username=request.user.username)
            mappa = Mappa.objects.filter(NomeMappa=nome_mappa, Autore=username).first()
            percorso = mappa.PercorsoMappa + "\\" + nome_mappa + ".map.json"
            file = open(percorso)
            data = json.load(file)
            if (Continente.objects.count() == 0) and (Territorio.objects.count() == 0):
                n_continente = 0
                n_territorio = 0
            else:
                n_continente = Continente.objects.latest('IDContinente').IDContinente + 1
                n_territorio = Territorio.objects.latest('IDTerritorio').IDTerritorio + 1
            for i in data['map']['areas']:
                if not Continente.objects.filter(NomeContinente=i['group'], Mappa = mappa).exists():
                    Continente.objects.create(IDContinente=n_continente, NomeContinente=i['group'], NumeroTruppe=0, Mappa=mappa)
                    n_continente = n_continente + 1
                continente = Continente.objects.filter(NomeContinente=i['group'], Mappa=mappa).first()
                if not Territorio.objects.filter(NomeTerritorio=i['title'], Continente = continente).exists():
                     Territorio.objects.create(IDTerritorio=n_territorio, NomeTerritorio=i['title'], Continente=continente, Mappa = mappa)
                     n_territorio = n_territorio + 1
            result = Continente.objects.filter(Mappa=mappa).order_by('IDContinente').annotate(
                count=Count('territorio'))
            for x in result:
                numero_truppe = int(math.floor(x.count / 3))
                if numero_truppe == 0:
                    numero_truppe = 1
                Continente.objects.filter(NomeContinente=x.NomeContinente).update(NumeroTruppe=numero_truppe)
            MappaView.generaConfini(data, mappa)
            file.close()
            return render(request, 'menu.html')


    def generaConfini(data, mappa):
        for i in data['map']['areas']:
            territorio1 = Territorio.objects.filter(NomeTerritorio=i['title'], Mappa = mappa).first()
            for j in data['map']['areas']:
                stop = False
                for h in i['coords']:
                    for k in j['coords']:
                        if h['x'] == k['x'] and h['y'] == k['y']:
                            territorio2 = Territorio.objects.filter(NomeTerritorio=j['title'], Mappa = mappa).first()
                            territorio1.Confini.add(territorio2)
                            stop = True
                            break
                    if stop:
                        break

    def findContinenteJson(data, name):
        for i in data['map']['areas']:
            if i['title'] == name:
                return i['group']

