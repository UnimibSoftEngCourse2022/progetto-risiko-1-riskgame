from django.test import TestCase, Client
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import UserRegisterForm
from django.urls import reverse
from django.contrib.auth.models import User

class registerTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",password="userTestPass",email="userTestEmail",pk="00000",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/registrazione')
        self.assertEqual(response.status_code, 200)

class statsTest (TestCase):
    def setUp(self):
        self.client=Client()
        #self.user = User.objects.create_user(username="userTestName",password="userTestPass",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/statistiche')
        self.assertEqual(response.status_code, 200)

class matchListTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/match-list')
        self.assertEqual(response.status_code, 200)

class menuTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/menu')
        self.assertEqual(response.status_code, 200)

class logOutTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

class logInTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName", password="userTestPass",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

class impostazioniTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)

class homeTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName", password="userTestPass",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
# editor ancora da implementare
"""    class editorTest (TestCase):
        def setUp(self):
            self.client=Client()
            self.user = User.objects.create_user(username="userTestName",)

        def test_view_url_exists_at_desired_location(self):
            response = self.client.get('/editor-mappa')
            self.assertEqual(response.status_code, 200) 
"""
class credenzialiTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName", password="userTestPass",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/credenziali')
        self.assertEqual(response.status_code, 200)

class creazioneTest (TestCase):
    def setUp(self):
        self.client=Client()
        self.user = User.objects.create_user(username="userTestName",)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/crea-partita')
        self.assertEqual(response.status_code, 200)