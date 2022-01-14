from django.shortcuts import render
from django.views.generic import TemplateView
from . import models


# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegistrazioneView(TemplateView):
    template_name = "registrazione.html"




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


def saveUserData(request):
        if request.method == "POST":
            NickName = request.POST['nickname']
            Nome = request.POST['nome']
            Cognome = request.POST['cognome']
            Email = request.POST['email']
            Password = request.POST['password']
            GiocatoreRegistrato.objects.create(Nome=Nome, Cognome=Cognome, NickName=NickName, Email=Email,
                                               Password=Password)
            messages.success(request, 'I dati sono stati salvati')
        return render(request, 'registrazione.html')