from django.urls import path
from .views import HomePageView, LoginView

urlpatterns = [
    path("", HomePageView.as_view(), name = "home"),
    path("login", LoginView.as_view(), name = "login"),
]