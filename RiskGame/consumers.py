from asyncio.windows_events import NULL
from dataclasses import dataclass
import dataclasses
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from typing import List

@dataclass
class ClasseTerritorio:
    numTruppe: int = 0
    giocatore: str = ""
    nome: str = ""
    continente: str = ""

@dataclass
class ClasseGiocatore:
    nickname: str = ""
    numTruppe: int = 0
    territori: List[str] = None
    numeroTruppeTurno: int = 0

# per far si che questi sopra siano serializzabili 
# fare listaGiocatori.append(dataclasses.asdict(ClasseGiocatore('prova', 14, [])))

class PartitaConsumer(WebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    global listaGiocatori, listaTerritori
    listaGiocatori = []
    listaTerritori = []

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['PartitaID']
        self.room_group_name = 'partita_%s' % self.room_name

        global idPartita
        idPartita = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

 
    def receive(self, text_data):
        # Chiamato alla ricezione di un messaggio (testo o bytes)
        text_data_json = json.loads(text_data)
        tipo = text_data_json['tipo']

        mittente = text_data_json['sender']

        # Metti messaggio in room group (locale) per gestire la richiesta
        if (tipo == 'messaggio'):
            messaggio = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'messaggio',
                    'message': messaggio,
                    'sender': mittente
                }
            )
        elif (tipo == 'nuovoGiocatore'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'nuovoGiocatore',
                    'sender': mittente
                }
            )
        elif (tipo == 'abbandonaUtente'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'abbandona',
                    'sender': mittente
                }
            )
            Partita.disconnettiGiocatore(text_data_json['idPartita'], self.scope['user'].username)
        elif (tipo == 'abbandonaOspite'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'abbandona',
                    'sender': mittente
                }
            )
            Partita.disconnettiOspite(text_data_json['idPartita'], text_data_json['sender'])
        elif (tipo == 'iniziaPartita'):
            self.inizializzaPartita()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': 'rappresentazionePartita',
                    'sender': mittente
                }
            )
        elif(tipo == 'assegnazioneTruppe'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )
        elif (tipo == 'assegnaTruppe'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )


    # Riceve il messaggio dalla room group (locale)
    def chat_message(self, event):
        tipo = event['tipo']

        # Invia esternamente alla WebSocket
        if (tipo == 'messaggio'):
            messaggio = event['message']
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'message': messaggio,
                'sender': event['sender']
            }))
        elif (tipo == 'nuovoGiocatore'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': event['sender']
            }))
        elif (tipo == 'abbandona'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': event['sender']
            }))

    def evento_gioco(self, event):
        tipo = event['tipo']
        mittente = event['sender']

        if (tipo == 'rappresentazionePartita'): # Dice agli utenti di togliere la chat e disegnare il gioco
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'listaGiocatori': json.dumps(listaGiocatori)
            }))

    # Eventi di gioco

    def assegnazioneTerritoriTruppeIniziali():
        mappa = Partita.getMappa(idPartita)
        xlistaTerritori = Territorio.getListaTerritoriMappa(mappa)
        xlistaGiocatori = Partita.getListaGiocatori(idPartita)
        h = len(listaTerritori)/len(xlistaGiocatori)
        k = 0
        for i  in xlistaGiocatori:
            listaGiocatori.append(ClasseGiocatore(14, [], i))
            for j in range(k , h):
                listaTerritori.append(ClasseTerritorio(0, i, j.NomeTerritorio,j.Continente))
                i.territori.append(j.NomeTerritorio)
                k = k + 1
            h = h + h
            

    def chiamataMetodoAssegnazioneTruppeTerritorio(classeGiocatore):
        xlistaTerritori = []
        listaGiocatori.numeroTruppeTurno = len(listaGiocatori.territori)/3
        for i in listaTerritori:
            if listaTerritori.giocatore == classeGiocatore.nickname:
                xlistaTerritori.append(ClasseTerritorio(listaTerritori.numTruppe,listaTerritori.giocatore, listaTerritori.nome, listaTerritori.continente))
        
        return xlistaTerritori


    def metodoAssegnazioneTruppeTerritorio(listaTerritoriSocket):
        for i in listaTerritoriSocket:
            for j in listaTerritori:
                if listaTerritori.nome == listaTerritoriSocket.nome:
                    j = i


    def inizializzaPartita():
        listaTemp = Partita.getListaGiocatori(idPartita)
        for giocatore in listaTemp:
            listaGiocatori.append(dataclasses.asdict(ClasseGiocatore(giocatore, 0, [])))
