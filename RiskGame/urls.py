from django.urls import path, re_path
from .views import *
from . import views

app_name = "RiskGame"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('registrazione', views.RegistrazioneView.register, name='register'),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("crea-partita", views.CreazioneView.draw, name="creazione"),
    path("menu", views.MenuView.drawMenu, name="menu"),
    path("menuospite", views.MenuView.drawOspite, name="menuospite"),
    path("settings", ImpostazioniView.as_view(), name="impostazione"),
    path("match-list", views.PartecipaView.loadPartite, name="partecipa"),
    #path("login-control", views.controlUserData, name="controlUserData"),
    path("statistiche", views.StatisticheView.draw, name="statistiche"),
    path("credenziali", views.CredenzialiView.draw, name="credenziali"),
    #path("credenziali-aggiornamento",
         #views.CredenzialiView.updateData, name="updateData"),
    path("editor-mappa", views.MappaView.draw, name="editor"),
    path("save-mappa", views.MappaView.checkButton, name="checkButton"),
    #path("load-mappa", views.MappaView.loadMappaDifficile, name="loadMappa"),
    #path("logout", views.userLogout, name="logout"),
    path('creaPartita', views.PartitaView.creaPartita, name="creaPartita"),
    path('partecipaPartita<PartitaID>', views.PartitaView.partecipaPartita, name="partecipaPartita"),
    #path('menu-mappa', MenuMappaView.as_view(), name="menumappa"),
    #path('cerca-eliminazione', views.EliminazioneMappaView.draw, name="eliminazione"),
    #path('eliminazione-mappa', views.EliminazioneMappaView.eliminazioneMappa, name="eliminazioneMappa"),

]
