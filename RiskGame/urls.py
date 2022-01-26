from django.urls import path, re_path
from .views import *
from . import views

app_name = "RiskGame"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    # path("login", LoginView.as_view(template_name='login.html'), name="login"),
    path('registrazione', views.register, name='register'),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("menu", MenuView.as_view(), name="menu"),
    path("crea-partita", views.CreazioneView.draw, name="creazione"),
    path("settings", ImpostazioniView.as_view(), name="impostazione"),
    path("match-list", views.PartecipaView.loadPartite, name="partecipa"),
    path('partita<PartitaID>', PartitaView.as_view(), name="partita"),
    # path("registrazione-salvataggio", views.RegistrazioneView.saveUserData, name="saveUserData"),
    path("login-control", views.controlUserData, name="controlUserData"),
    path("statistiche", views.StatisticheView.draw, name="statistiche"),
    path("credenziali", views.CredenzialiView.draw, name="credenziali"),
    path("credenziali-aggiornamento",
         views.CredenzialiView.updateData, name="updateData"),
    path("editor-mappa", MappaView.as_view(), name="editor"),
    path("save-mappa", views.MappaView.saveMappa, name="saveMappa"),
    #path("load-mappa", views.MappaView.loadMappaDifficile, name="loadMappa"),
]
