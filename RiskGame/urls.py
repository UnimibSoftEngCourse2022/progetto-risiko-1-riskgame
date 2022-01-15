from django.urls import path
from .views import HomePageView, LoginView, RegistrazioneView, MenuView, CreazioneView, ImpostazioniView
from . import views
app_name = "RiskGame"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("menu", MenuView.as_view(), name="menu"),
    path("crea-partita", CreazioneView.as_view(), name="creazione"),
    path("settings", ImpostazioniView.as_view(), name="impostazione"),
    path("registrazione-salvataggio", views.RegistrazioneView.saveUserData, name="saveUserData"),
    path("login-control", views.controlUserData, name="controlUserData"),
]