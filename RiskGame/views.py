import secrets

from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import *
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import logout

import views
from .forms import UserRegisterForm
from RiskGame.models import *
from django.db.models import Count
import os
import random
from django.contrib.auth.models import User
import json
import math
from django.http import HttpResponse
import pytest
from urllib import request


# Create your views here.
@require_http_methods(["POST", "GET"])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            user = User.objects.filter(username=username).first()
            Statistiche.objects.create(
                IDGiocatore=user,
                NumeroPartiteVinte=0,
                NumeroPartitePerse=0,
                PercentualeVinte=0.0,
                NumeroScontriVinti=0,
                NumeroScontriPersi=0,
                NumeroScontriVintiATK=0,
                NumeroScontriPersiATK=0,
                NumeroScontriVintiDEF=0,
                NumeroScontriPersiDEF=0,
                PercentualeScontriVintiATK=0.0,
                NumeroPartiteGiocate=0
            )
            return redirect('home')
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
            return redirect(reverse('home'))"""


class MenuView(TemplateView):
    template_name = "menu.html"

    @require_http_methods(["POST", "GET"])
    def drawMenu(request):
        request.session['ospite'] = 'null'
        return render(request, MenuView.template_name)

    @require_http_methods(["POST", "GET"])
    def drawOspite(request):
        request.session['ospite'] = Ospite.assegnaOspite()
        return render(request, MenuView.template_name)


class ImpostazioniView(TemplateView):
    template_name = "impostazione.html"


class CreazioneView(TemplateView):
    @require_http_methods(["POST", "GET"])
    def draw(request):
        list_mappe = ["MappaDefault"]
        template_name = "creazione.html"
        if request.user.is_authenticated:
            username = User.objects.get(username=request.user.username)
            mappe = Mappa.objects.filter(Autore=username)
            for i in mappe:
                nome = i.NomeMappa
                if not nome in list_mappe:
                    list_mappe.append(nome)
        maps = {
            "nomi": list_mappe
        }
        return render(request, template_name, maps)


class PartecipaView(TemplateView):
    template_name = "partecipa.html"

    @require_http_methods(["POST", "GET"])
    def loadPartite(request):
        temp_data = Partita.objects.all()
        return render(request, "partecipa.html", {"partita_package": temp_data})


class PartitaView(TemplateView):
    template_name = "partita.html"

    @require_http_methods(["POST", "GET"])
    def creaPartita(request):
        # Crea la partita nel DB, aggiunge il nuovo giocatore e lo reindirizza alla partita
        nome = request.POST['nome-mappa']
        difficolta = request.POST['difficolta']
        # nome_mappa = nome + "-" + "Difficile"
        nuovoID = Partita.getNuovoID()
        numGiocatori = request.POST['giocatori']
        mappa = None
        percorso = None
        intDiff = 0
        if request.user.is_authenticated:
            if nome == "MappaDefault":
                mappa = Mappa.objects.filter(
                    NomeMappa=nome, Difficolta="Difficile").first()
            else:
                username = User.objects.get(username=request.user.username)
                mappa = Mappa.objects.filter(
                    NomeMappa=nome, Autore=username, Difficolta="Difficile").first()
        else:
            mappa = Mappa.objects.filter(
                NomeMappa=nome, Difficolta="Difficile").first()
        if difficolta == "Difficile":
            intDiff = 3
            #percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
        elif difficolta == 'Semplice':
            intDiff = 1
            percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
            file = open(percorso)
            data = json.load(file)
            MappaView.collassaConfiniDifficolta(request, data)
            percorso = mappa.PercorsoMappa
            MappaView.saveJson(nome, difficolta, percorso, data)
            file.close()
            MappaView.saveMappaEditor(request)
        elif difficolta == 'Media':
            intDiff = 2
            percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
            file = open(percorso)
            data = json.load(file)
            MappaView.collassaConfiniDifficolta(request, data)
            percorso = mappa.PercorsoMappa
            MappaView.saveJson(nome, difficolta, percorso, data)
            file.close()
            MappaView.saveMappaEditor(request)

        """if difficolta == "Difficile" and nome != "MappaDefault":
            username = User.objects.get(username=request.user.username)
            mappa = Mappa.objects.filter(NomeMappa=nome, Difficolta=difficolta, Autore=username).first()
            #percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
            intDiff = 3
        else:
            if request.user.is_authenticated:
                username = User.objects.get(username=request.user.username)
                if nome != "MappaDefault":
                    mappa = Mappa.objects.filter(NomeMappa=nome, Autore=username, Difficolta="Difficile").first()
                    percorso = mappa.PercorsoMappa + "\\" + nome + "-" + difficolta + ".map.json"
            else:
                mappa = Mappa.objects.filter(NomeMappa=nome, Difficolta="Difficile").first()
                percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"""
        n_continenti = Continente.objects.filter(Mappa=mappa).count()
        if "collassaGiocatori" in request.POST:
            if n_continenti != int(numGiocatori):
                if request.user.is_authenticated:
                    if nome == "MappaDefault":
                        mappa = Mappa.objects.filter(
                            NomeMappa=nome, Difficolta=difficolta).first()
                    else:
                        username = User.objects.get(
                            username=request.user.username)
                        mappa = Mappa.objects.filter(
                            NomeMappa=nome, Autore=username, Difficolta=difficolta).first()
                else:
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Difficolta=difficolta).first()
                if difficolta == "Difficile":
                    percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
                else:
                    percorso = mappa.PercorsoMappa + "\\" + nome + "-" + difficolta + ".map.json"
                print(percorso)
                file = open(percorso)
                data = json.load(file)
                MappaView.collassaConfiniGiocatori(
                    request, data, mappa, numGiocatori)
                percorso = mappa.PercorsoMappa
                MappaView.saveJson(nome, difficolta, percorso, data)
                file.close()
            else:
                messages.error(request,
                               "La mappa contiene già un numero di continenti pari al numero di giocatori inserito")
                return render(request, 'creazione.html')
        # mappa = Mappa.objects.filter(NomeMappa=nome, Autore=username, Difficolta= difficolta).first()
        if int(numGiocatori) <= n_continenti:
            Partita.objects.create(IDPartita=nuovoID, NumeroGiocatori=numGiocatori,
                                   Difficolta=intDiff, Mappa=mappa)
            if (request.user.is_authenticated):
                Partita.objects.get(
                    IDPartita=nuovoID).Giocatori.add(request.user)
            else:
                print(request.session['ospite'])
                ospite = Ospite.objects.get(Nickname=request.session['ospite'])
                Partita.objects.get(IDPartita=nuovoID).Ospiti.add(ospite)

            return redirect(reverse('RiskGame:partecipaPartita', kwargs={'PartitaID': nuovoID}))
        else:
            messages.error(
                request, "Il numero di giocatori inserito non è compatibile con la mappa")
            return render(request, 'creazione.html')

    @require_http_methods(["POST", "GET"])
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
    @require_http_methods(["POST", "GET"])
    def draw(request):
        username = User.objects.get(username=request.user.username)
        template_name = "statistiche.html"
        statistica = Statistiche.objects.filter(IDGiocatore=username)
        stats = {
            "statistiche": statistica
        }
        return render(request, template_name, stats)


class CredenzialiView(TemplateView):
    @require_http_methods(["POST", "GET"])
    def draw(request):
        userprofile_form = UserRegisterForm(request.POST if request.POST else None,
                                            instance=User.objects.get(username=request.user))
        if request.method == 'POST':
            if userprofile_form.is_valid():
                userprofile_form.save()
                return redirect('login')

        return render(request, 'credenziali.html', context={'userprofile_form': userprofile_form})


class MappaView(TemplateView):
    template_name = "editor.html"

    @require_http_methods(["POST", "GET"])
    def checkButton(request):
        if request.method == "POST":
            nome_mappa = request.POST['nome-mappa']
            username = User.objects.get(username=request.user.username)
            if "conferma" in request.POST:
                if nome_mappa == "MappaDefault":
                    messages.error(
                        request, "Il nome della mappa inserito non può essere scelto")
                    return render(request, 'editor.html')
                if Mappa.objects.filter(NomeMappa=nome_mappa, Autore=username).exists():
                    messages.error(
                        request, "Il nome della mappa inserito esiste già")
                    return render(request, 'editor.html')
                MappaView.saveMappaEditor(request)
            if "elimina" in request.POST:
                EliminazioneMappaView.eliminazioneMappa(request)
        return render(request, "editor.html")

    def saveMappaEditor(request):
        if request.method == "POST":
            n_random = secrets.randbelow(1000)
            nome_mappa = request.POST['nome-mappa']
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'static\Mappe')
            while Mappa.objects.filter(IDMappa=n_random).exists():
                n_random = secrets.randbelow(0, 1000)
            if request.user.is_authenticated:
                username = User.objects.get(username=request.user.username)
                if not "difficolta" in request.POST:
                    if nome_mappa == "MappaDefault":
                        username = None
                    Mappa.objects.create(IDMappa=n_random, NomeMappa=nome_mappa, Autore=username,
                                         PercorsoMappa=filename,
                                         Difficolta="Difficile")
                    MappaView.saveConfigurazione(request)
                    return render(request, 'menu.html')
                else:
                    difficolta = request.POST['difficolta']
                    if nome_mappa == "MappaDefault":
                        username = None
                    if not Mappa.objects.filter(NomeMappa=nome_mappa, Autore=username, PercorsoMappa=filename,
                                                Difficolta=difficolta).exists():
                        Mappa.objects.create(IDMappa=n_random, NomeMappa=nome_mappa, Autore=username,
                                             PercorsoMappa=filename,
                                             Difficolta=difficolta)
                        MappaView.saveConfigurazione(request)
                        return render(request, 'menu.html')
            else:
                if not Mappa.objects.filter(NomeMappa="MappaDefault", PercorsoMappa=filename, Autore=None,
                                            Difficolta="Difficile").exists():
                    Mappa.objects.create(NomeMappa="MappaDefault", PercorsoMappa=filename, Autore=None,
                                         Difficolta="Difficile")
                    MappaView.saveConfigurazione(request)
                    return render(request, 'menu.html')

    def saveJson(nome, difficolta, percorso, data):
        if not os.path.exists(percorso):
            os.makedirs(percorso)
        filename = nome + "-" + difficolta + ".map.json"
        with open(os.path.join(percorso, filename), "w") as jsonFile:
            json.dump(data, jsonFile)

    def saveConfigurazione(request):
        template_name = "editor.html"
        mappa = None
        data = None
        if request.method == "POST":
            nome = request.POST['nome-mappa']
            if not "difficolta" in request.POST:
                difficolta = "Difficile"
            else:
                difficolta = request.POST['difficolta']
            if request.user.is_authenticated:
                username = User.objects.get(username=request.user.username)
                if nome == "MappaDefault":
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Difficolta=difficolta).first()
                else:
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Autore=username, Difficolta=difficolta).first()
            else:
                mappa = Mappa.objects.filter(
                    NomeMappa="MappaDefault", Difficolta=difficolta).first()
            if difficolta == "Difficile":
                percorso = mappa.PercorsoMappa + "\\" + nome + ".map.json"
            else:
                percorso = mappa.PercorsoMappa + "\\" + nome + "-" + difficolta + ".map.json"
            file = open(percorso)
            data = json.load(file)
            if (Continente.objects.count() == 0) and (Territorio.objects.count() == 0):
                n_continente = 0
                n_territorio = 0
            else:
                n_continente = Continente.objects.latest(
                    'IDContinente').IDContinente + 1
                n_territorio = Territorio.objects.latest(
                    'IDTerritorio').IDTerritorio + 1
            for i in data['map']['areas']:
                if not Continente.objects.filter(NomeContinente=i['group'], Mappa=mappa).exists():
                    Continente.objects.create(IDContinente=n_continente, NomeContinente=i['group'], NumeroTruppe=0,
                                              Mappa=mappa)
                    n_continente = n_continente + 1
                continente = Continente.objects.filter(
                    NomeContinente=i['group'], Mappa=mappa).first()
                if not Territorio.objects.filter(NomeTerritorio=i['title'], Continente=continente).exists():
                    Territorio.objects.create(IDTerritorio=n_territorio, NomeTerritorio=i['title'],
                                              Continente=continente, Mappa=mappa)
                    n_territorio = n_territorio + 1
            result = Continente.objects.filter(Mappa=mappa).order_by('IDContinente').annotate(
                count=Count('territorio'))
            for x in result:
                numero_truppe = int(math.floor(x.count / 3))
                if numero_truppe == 0:
                    numero_truppe = 1
                Continente.objects.filter(NomeContinente=x.NomeContinente).update(
                    NumeroTruppe=numero_truppe)
            MappaView.generaConfini(data, mappa)
            file.close()

    def generaConfini(data, mappa):
        for i in data['map']['areas']:
            territorio1 = Territorio.objects.filter(
                NomeTerritorio=i['title'], Mappa=mappa).first()
            for j in data['map']['areas']:
                stop = False
                for h in i['coords']:
                    for k in j['coords']:
                        if h['x'] == k['x'] and h['y'] == k['y']:
                            territorio2 = Territorio.objects.filter(
                                NomeTerritorio=j['title'], Mappa=mappa).first()
                            territorio1.Confini.add(territorio2)
                            stop = True
                            break
                    if stop:
                        break

    def findContinenteJson(data, name):
        for i in data['map']['areas']:
            if i['title'] == name:
                return i['group']

    def collassaConfiniDifficolta(request, data):
        selected = []
        difficolta = request.POST['difficolta']
        for i in range(0, len(data['map']['areas'])):
            if data['map']['areas'][i]['coords'] is not None and not data['map']['areas'][i]['title'] in selected:
                temp_i = data['map']['areas'][i]['coords'].copy()
                temp_i.append(data['map']['areas'][i]['coords'][0])
                for j in range(0, len(data['map']['areas']) - 1):
                    coordinate = []
                    if data['map']['areas'][i]['title'] != data['map']['areas'][j]['title'] and data['map']['areas'][j][
                            'group'] == data['map']['areas'][i]['group'] and data['map']['areas'][j][
                            'coords'] is not None and not data['map']['areas'][j]['title'] in selected:
                        adiacenza = MappaView.controlloAdiacenzaTerritori(
                            data, i, j)
                        if adiacenza:
                            temp_j = data['map']['areas'][j]['coords'].copy()
                            temp_j.insert(0, temp_i[0])
                            temp_j.append(data['map']['areas'][j]['coords'][0])
                            for h in temp_i:
                                coordinate.append(h)
                            for k in temp_j:
                                coordinate.append(k)
                            data['map']['areas'][i]['coords'] = data['map']['areas'][i]['coords'] + coordinate
                            data['map']['areas'][j]['coords'] = None
                        if difficolta == "Media":
                            selected.append(data['map']['areas'][i]['title'])
                            break
        temp = data['map']['areas'].copy()
        for i in range(0, len(data['map']['areas']) - 1):
            if data['map']['areas'][i]['coords'] is None:
                temp.remove(data['map']['areas'][i])
        data['map']['areas'] = temp

    def collassaConfiniGiocatori(request, data, mappa, numGiocatori):
        length = Continente.objects.filter(
            Mappa=mappa).count() - int(numGiocatori)
        n_continenti_visitati = 0
        while n_continenti_visitati < length:
            selected = []
            for i in range(0, len(data['map']['areas'])):
                if not data['map']['areas'][i]['group'] in selected:
                    continente_nuovo = Continente.objects.filter(NomeContinente=data['map']['areas'][i]['group'],
                                                                 Mappa=mappa).first()
                    for j in range(0, len(data['map']['areas']) - 1):
                        adiacenza = MappaView.controlloAdiacenzaTerritori(
                            data, i, j)
                        if data['map']['areas'][i]['title'] != data['map']['areas'][j]['title'] and \
                                data['map']['areas'][j]['group'] != data['map']['areas'][i][
                            'group'] and adiacenza \
                                and not data['map']['areas'][j]['group'] in selected:
                            for h in range(0, len(data['map']['areas']) - 1):
                                if data['map']['areas'][h]['group'] == data['map']['areas'][j]['group']:
                                    continente_vecchio = Continente.objects.filter(
                                        NomeContinente=data['map']['areas'][h]['group'], Mappa=mappa).first()
                                    Territorio.objects.filter(NomeTerritorio=data['map']['areas'][h]['title'],
                                                              Continente=continente_vecchio, Mappa=mappa).update(
                                        Continente=continente_nuovo)
                                    data['map']['areas'][h]['group'] = data['map']['areas'][i]['group']
                            n_continenti_visitati = n_continenti_visitati + 1
                            break

    def controlloAdiacenzaTerritori(data, territorio1, territorio2):
        for elem1 in data['map']['areas'][territorio1]['coords']:
            for elem2 in data['map']['areas'][territorio2]['coords']:
                if elem1 == elem2:
                    for elem3 in data['map']['areas'][territorio1]['coords']:
                        for elem4 in data['map']['areas'][territorio2]['coords']:
                            if elem3 == elem4 and elem1 != elem3 and elem2 != elem4:
                                return True
        return False


class MenuMappaView(TemplateView):
    template_name = "menumappa.html"


class EliminazioneMappaView(TemplateView):
    """def draw(request):
        username = User.objects.get(username=request.user.username)
        template_name = "eliminazioneMappa.html"
        mappe = Mappa.objects.filter(Autore=username)
        list_mappe = []
        for i in mappe:
            nome = i.NomeMappa
            if not nome in list_mappe and nome != "MappaDefault":
                list_mappe.append(nome)
        maps = {
            "nomi": list_mappe
        }
        return render(request, template_name, maps)"""

    def eliminazioneMappa(request):
        if request.method == "POST":
            nome = request.POST['nome-mappa']
            username = User.objects.get(username=request.user.username)
            if not Mappa.objects.filter(NomeMappa=nome, Autore=username).exists():
                messages.error(
                    request, "Il nome della mappa inserito non esiste")
                return render(request, 'editor.html')
            if nome == "MappaDefault":
                messages.error(
                    request, "La mappa selezionata non può essere eliminata")
                return render(request, 'editor.html')
            else:
                if Mappa.objects.filter(NomeMappa=nome, Autore=username, Difficolta="Difficile").exists():
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Autore=username, Difficolta="Difficile").first()
                    percorso = mappa.PercorsoMappa + "\\" + \
                        mappa.NomeMappa + "-" + mappa.Difficolta + ".map.json"
                    if os.path.exists(percorso):
                        os.remove(percorso)
                    mappa.delete()
                    percorso = mappa.PercorsoMappa + "\\" + mappa.NomeMappa + ".map.json"
                    if os.path.exists(percorso):
                        os.remove(percorso)
                    mappa.delete()
                if Mappa.objects.filter(NomeMappa=nome, Autore=username, Difficolta="Media").exists():
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Autore=username, Difficolta="Media").first()
                    percorso = mappa.PercorsoMappa + "\\" + \
                        mappa.NomeMappa + "-" + mappa.Difficolta + ".map.json"
                    if os.path.exists(percorso):
                        os.remove(percorso)
                    mappa.delete()
                if Mappa.objects.filter(NomeMappa=nome, Autore=username, Difficolta="Semplice").exists():
                    mappa = Mappa.objects.filter(
                        NomeMappa=nome, Autore=username, Difficolta="Semplice").first()
                    percorso = mappa.PercorsoMappa + "\\" + \
                        mappa.NomeMappa + "-" + mappa.Difficolta + ".map.json"
                    if os.path.exists(percorso):
                        os.remove(percorso)
                    mappa.delete()
