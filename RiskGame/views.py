from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from RiskGame.models import *
from django.contrib import messages

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(TemplateView):
    template_name = "login.html"

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
            try:
                GiocatoreRegistrato.objects.create(Nome=Nome, Cognome=Cognome, NickName=NickName,
                                                                      Email=Email,
                                                                      Password=Password)
            except:
                print("Dati già esistenti")
                return render(request, 'registrazione.html')
            print("Altrimenti")
            return render(request, 'menu.html')


class MenuView(TemplateView):
    template_name = "menu.html"


class ImpostazioniView(TemplateView):
    template_name = "impostazione.html"


class CreazioneView(TemplateView):
    template_name = "creazione.html"

    def loadMappe(self, request):
        if request.user.is_authenticated():
            nickname = request.user.username
            mappe = Mappa.objects.filter(Autore=nickname)
            return render(request, self.template_name, {'mappe': mappe})


class PartecipaView(TemplateView):
    template_name = "partecipa.html"

    def loadPartite(request):
        temp_data = Partita.objects.all()
        return render(request, "partecipa.html", {"partita_package": temp_data})


class PartitaView(TemplateView):
    template_name = "partita.html"
