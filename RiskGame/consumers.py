from dataclasses import dataclass
import dataclasses, json, math
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Partita, Territorio
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
    numeroTruppeTurno: int = 0

# per far si che questi sopra siano serializzabili 
# fare listaGiocatori.append(dataclasses.asdict(ClasseGiocatore('prova', 14, [])))

class PartitaConsumer(WebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    listaGiocatori = []
    listaTerritori = []
    giocatoreAttivo = ""
    indexGiocatoreAttivo = 0
    numeroTurno = 0

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
            # Partita.disconnettiGiocatore(text_data_json['idPartita'], self.scope['user'].username)
            Partita.disconnettiGiocatore(text_data_json['idPartita'], mittente)
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
            self.giocatoreAttivo = self.listaGiocatori[0].nickname
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': 'iniziaTurno',
                    'sender': mittente
                }
            )
            self.indexGiocatoreAttivo += 1
            if (self.indexGiocatoreAttivo >= len(self.listaGiocatori)):
                self.indexGiocatoreAttivo = 0
                self.numeroTurno += 1
        elif (tipo == 'iniziaTurno'):
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
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'mappa': jsonMappa,
                'nomeMappa': nomeMappa
            }))
        elif (tipo == 'iniziaTurno'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'numeroTurno': self.numeroTurno
            }))


    # Eventi di gioco

    def serializzaLista(self, lista):
        nuovaLista = []
        for elemento in lista:
            nuovaLista.append(dataclasses.asdict(elemento))
        return nuovaLista


    def assegnazioneTerritoriTruppeIniziali(self):
        xlistaTerritori = Territorio.getListaTerritoriMappa(nomeMappa)

        for territorio in xlistaTerritori:
            self.listaTerritori.append(ClasseTerritorio(numTruppe=0, giocatore="",
                nome=territorio.NomeTerritorio, continente=territorio.Continente.NomeContinente))

        xlistaGiocatori = Partita.getListaGiocatori(idPartita)

        h = math.floor(len(xlistaTerritori)/len(xlistaGiocatori))
        k = 0
        for i in xlistaGiocatori:
            self.listaGiocatori.append(ClasseGiocatore(nickname=i,
                numTruppe=14, numeroTruppeTurno=0))
            for j in range(k , h):
                self.listaTerritori[j].giocatore = i
            k = h
            h = h + h
            

    def chiamataMetodoAssegnazioneTruppeTerritorio(self, classeGiocatore):
        xlistaTerritori = []
        for giocatore in self.listaGiocatori:
            if giocatore.nickname == classeGiocatore.nickname:
                giocatore.numeroTruppeTurno = len(giocatore.territori)/3
            break
        for i in self.listaTerritori:
            if i.giocatore == classeGiocatore.nickname:
                xlistaTerritori.append(ClasseTerritorio(i.numTruppe, i.giocatore, i.nome, i.continente))
        return xlistaTerritori


    def metodoAssegnazioneTruppeTerritorio(self, listaTerritoriSocket):
        for i in listaTerritoriSocket:
            for j in self.listaTerritori:
                if self.listaTerritori.nome == listaTerritoriSocket.nome:
                    j = i
