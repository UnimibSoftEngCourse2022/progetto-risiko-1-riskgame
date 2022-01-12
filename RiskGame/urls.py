from django.urls import path
from .views import HomePageView, LoginView, RegistrazioneView, MenuView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("registrazione", RegistrazioneView.as_view(), name="registrazione"),
    path("menu", MenuView.as_view(), name="menu"),
]