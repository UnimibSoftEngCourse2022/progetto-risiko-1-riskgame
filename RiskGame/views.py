from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import UserRegisterForm
from RiskGame.models import *
import os
import random
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registrazione.html', {'form': form})


class HomePageView(TemplateView):
    template_name = "home.html"

    # class LoginView(TemplateView):
    #   template_name = "login.html"

    def controlUserData(request):
        if request.method == "POST":
            NickName = request.POST['nickname']
            Password = request.POST['password']
            if GiocatoreRegistrato.objects.filter(NickName=NickName, Password=Password).exists():
                return render(request, 'menu.html')
            else:
                messages.warning(request, 'i dati sono errati')
                return render(request, 'login.html')


class RegistrazioneView(TemplateView):
    template_name = "registrazione.html"

    def saveUserData(request):
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
            return redirect(reverse('RiskGame:home'))


class MenuView(TemplateView):
    template_name = "menu.html"


class ImpostazioniView(TemplateView):
    template_name = "impostazione.html"


class CreazioneView(TemplateView):
    def draw(request):
        username = User.objects.get(username = request.user.username)
        template_name = "creazione.html"
        mappe = Mappa.objects.filter(Autore = username)
        maps = {
            "mappe": mappe
        }
        return render(request, template_name, maps)


class PartecipaView(TemplateView):
    template_name = "partecipa.html"

    def loadPartite(request):
        temp_data = Partita.objects.all()
        return render(request, "partecipa.html", {"partita_package": temp_data})


class PartitaView(TemplateView):
    template_name = "partita.html"


class StatisticheView(TemplateView):
    def draw(request):
        username = request.user.username
        template_name = "statistiche.html"
        statistica = Statistiche.objects.all()
        stats = {
            "statistiche": statistica
        }
        return render(request, template_name, stats)


class CredenzialiView(TemplateView):
    def draw(request):
        template_name = "credenziali.html"
        credenziali = GiocatoreRegistrato.objects.all()
        cred = {
            "credenziali": credenziali
        }
        return render(request, template_name, cred)

    def updateData(request):
        if request.method == "POST":
            NickName = request.POST['nickname']
            Nome = request.POST['nome']
            Cognome = request.POST['cognome']
            Email = request.POST['email']
            Password = request.POST['password']
            g = GiocatoreRegistrato.objects.get(NickName=NickName)
            g.Nome = Nome
            g.Cognome = Cognome
            g.NickName = NickName
            g.Email = Email
            g.Password = Password
            g.save()
            return render(request, 'menu.html')


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


def controlUserData(request):
    if request.method == "POST":
        NickName = request.POST['nickname']
        Password = request.POST['password']
        if GiocatoreRegistrato.objects.filter(NickName=NickName, Password=Password).exists():
            return render(request, 'menu.html')
        else:
            messages.warning(request, 'i dati sono errati')
            return render(request, 'login.html')


class MappaView(TemplateView):
    template_name = "editor.html"
    def saveMappa(request):
        template_name = "editor.html"
        if request.method == "POST":
            n_random = random.randint(0,1000)
            nome_mappa = request.POST['nome-mappa']
            username = User.objects.get(username = request.user.username)
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'static\Mappe')
            while Mappa.objects.filter(IDMappa = n_random).exists():
                n_random = random.randint(0, 1000)
            Mappa.objects.create(IDMappa = n_random, NomeMappa = nome_mappa, Autore = username, PercorsoMappa = filename)
            return render(request, 'menu.html')
