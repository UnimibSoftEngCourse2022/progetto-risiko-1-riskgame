from django.urls import path, re_path
from .views import *
from . import views

app_name = "RiskGame"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('registrazione', views.register, name='register'),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("menu", views.MenuView.drawMenu, name="menu"),
    path("menuospite", views.MenuView.drawOspite, name="menuospite"),
    path("crea-partita", CreazioneView.as_view(), name="creazione"),
    path("settings", ImpostazioniView.as_view(), name="impostazione"),
    path("match-list", views.PartecipaView.loadPartite, name="partecipa"),
    path("login-control", views.controlUserData, name="controlUserData"),
    path("statistiche", views.StatisticheView.draw, name="statistiche"),
    path("credenziali", views.CredenzialiView.draw, name="credenziali"),
    path("credenziali-aggiornamento",
         views.CredenzialiView.updateData, name="updateData"),
    path("logout", views.userLogout, name="logout"),
    path('creaPartita', views.PartitaView.creaPartita, name="creaPartita"),
    path('partecipaPartita<PartitaID>', views.PartitaView.partecipaPartita, name="partecipaPartita")
]
