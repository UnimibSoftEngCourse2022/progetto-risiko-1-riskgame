from asyncio.windows_events import NULL
from dataclasses import dataclass
import dataclasses, json, math
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from typing import List
from pathlib import Path

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

        global idPartita, nomeMappa, jsonMappa
        idPartita = self.room_name
        nomeMappa = Partita.getMappa(idPartita)

        with open(str(Path(__file__).absolute().parent) +'/static/Mappe/' + nomeMappa + '.map.json') as json_file:
            jsonMappa = json.load(json_file)

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
            self.assegnazioneTerritoriTruppeIniziali()
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

        if (tipo == 'iniziaPartita'): # Dice agli utenti di togliere la chat e disegnare il gioco
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'listaGiocatori': self.serializzaLista(listaGiocatori),
                'mappa': jsonMappa,
                'nomeMappa': nomeMappa
            }))

    # Eventi di gioco

    def serializzaLista(self, lista):
        nuovaLista = []
        for elemento in lista:
            nuovaLista.append(dataclasses.asdict(elemento))
        return nuovaLista


    def assegnazioneTerritoriTruppeIniziali(self):
        xlistaTerritori = Territorio.getListaTerritoriMappa(nomeMappa)
        xlistaGiocatori = Partita.getListaGiocatori(idPartita)
        h = math.floor(len(listaTerritori)/len(xlistaGiocatori))
        print(h)
        print('stop')
        k = 0
        for i in xlistaGiocatori:
            listaGiocatori.append(ClasseGiocatore(nickname=i,
                numTruppe=14, territori=[], numeroTruppeTurno=0))
            for j in range(k , h):
                print(j)
                listaTerritori.append(ClasseTerritorio(numTruppe=0, giocatore=i,
                    nome=xlistaTerritori[j].NomeTerritorio,
                    continente=xlistaTerritori[j].Continente))
                i.territori.append(xlistaTerritori[j].NomeTerritorio)
                k = k + 1
            h = h + h
            

    def chiamataMetodoAssegnazioneTruppeTerritorio(self, classeGiocatore):
        xlistaTerritori = []
        for giocatore in listaGiocatori:
            if giocatore.nickname == classeGiocatore.nickname:
                giocatore.numeroTruppeTurno = len(giocatore.territori)/3
            break
        for i in listaTerritori:
            if i.giocatore == classeGiocatore.nickname:
                xlistaTerritori.append(ClasseTerritorio(i.numTruppe, i.giocatore, i.nome, i.continente))
        return xlistaTerritori


    def metodoAssegnazioneTruppeTerritorio(self, listaTerritoriSocket):
        for i in listaTerritoriSocket:
            for j in listaTerritori:
                if listaTerritori.nome == listaTerritoriSocket.nome:
                    j = i
