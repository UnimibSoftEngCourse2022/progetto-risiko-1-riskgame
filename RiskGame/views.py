from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegistrazioneView(TemplateView):
    template_name = "registrazione.html"


class MenuView(TemplateView):
    template_name = "menu.html"
