from django.urls import path
from .views import HomePageView, RegistrazioneView, MenuView, CreazioneView, ImpostazioniView
from . import views
app_name = "RiskGame"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    #path("login", LoginView.as_view(template_name='login.html'), name="login"),
    path('registrazione', views.register, name='register'),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("menu", MenuView.as_view(), name="menu"),
    path("crea-partita", CreazioneView.as_view(), name="creazione"),
    path("settings", ImpostazioniView.as_view(), name="impostazione"),
    # path("registrazione-salvataggio", views.saveUserData, name="saveUserData"),

]
