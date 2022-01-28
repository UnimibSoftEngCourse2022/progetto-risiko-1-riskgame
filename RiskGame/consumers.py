from dataclasses import dataclass
import dataclasses, json, math, random
from xmlrpc.client import boolean
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
    numeroTruppeTurno: int = 0
    carte : list = []
    ingioco : boolean = True

# per far si che questi sopra siano serializzabili 
# fare listaGiocatori.append(dataclasses.asdict(ClasseGiocatore('prova', 14, [])))

class PartitaConsumer(WebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    listaGiocatori = []
    listaTerritori = []
    giocatoreAttivo = ""
    indexGiocatoreAttivo = 0;

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
                'listaTerritori': self.serializzaLista(self.listaTerritori)
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
            

    def chiamataAssegnazioneTruppeTerritorio(self, classeGiocatore):
        k = 0
        cont = 0
        xgiocatore : ClasseGiocatore
        for giocatore in self.listaGiocatori:
            if giocatore.nickname == classeGiocatore.nickname:
                xgiocatore = classeGiocatore
        if giocatore.carte.count(1)>1 and giocatore.carte.count(4)>0:
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(2)>1 and giocatore.carte.count(4)>0:
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(3)>1 and giocatore.carte.count(4)>0:
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(3)>0 and giocatore.carte.count(2)>0 and giocatore.carte.count(1)>0:
            giocatore.carte.remove(3)
            giocatore.carte.remove(2)
            giocatore.carte.remove(1)
            k = 10
        elif giocatore.carte.count(3)>2:
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            k=8
        elif giocatore.carte.count(2)>2:
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            k=6
        elif giocatore.carte.count(1)>2:
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            k=4
        for i in self.listaTerritori:
            if xgiocatore.nickname == i.giocatore:
                cont = cont + 1
        xgiocatore.numeroTruppeTurno = math.floor(cont/3)
        if xgiocatore.numeroTruppeTurno == 0:
            xgiocatore.numeroTruppeTurno = 1
        xgiocatore.numeroTruppeTurno = xgiocatore.numeroTruppeTurno + k
        xgiocatore.numTruppe = xgiocatore.numTruppe + xgiocatore.numeroTruppeTurno
        for i in self.listaGiocatori:
            if xgiocatore.nickname == i.nickname :
                i = xgiocatore

        
        """ LEGENDA : 1 Cannoni, 2 Fanti, 3 Cavalieri, 4 Jolly:
            4 armate con tre cannoni;
            6 armate con tre fanti;
            8 armate con tre cavalieri;
            10 armate con tre simboli diversi;
            12 armate con un simbolo jolly e altri due simboli uguali."""


    def ricezioneAssegnazioneTruppeTerritorio(self, listaTerritoriSocket):
        for i in listaTerritoriSocket:
            for j in self.listaTerritori:
                if self.listaTerritori.nome == listaTerritoriSocket.nome:
                    j = i
                    break
    

    def chiamataAttacco(self, attacante, truppeATK, difensore, truppeDEF):
        valATK = []
        valDEF = []
        giocatoreATK : ClasseGiocatore
        giocatoreDEF : ClasseGiocatore
        territorioATK : ClasseTerritorio
        territorioDEF : ClasseTerritorio
        vittoria : boolean = False

        for giocatore in self.listaGiocatori:
            if giocatore.nickname == attacante.giocatore:
                giocatoreATK = giocatore
            if giocatore.nickname == difensore.giocatore:
                giocatoreDEF = giocatore

        for territorio in self.listaTerritori:
            if territorio.nome == difensore.nome:
                territorioDEF = territorio
            if territorio.nome == attacante.nome:
                territorioATK = territorio
        
        for i in truppeATK:
            valATK[i] = random.randint(0,5)
        
        for i in truppeATK:
            valDEF[i] = random.randint(0,5)

        valATK.reverse()
        valDEF.reverse()

        if len(valDEF) > len(valATK):
            for i in valATK:
                if valATK[i] > valDEF[i]:
                    territorioDEF.numTruppe = territorioDEF.numTruppe - 1
                    giocatoreDEF.numTruppe = giocatoreDEF.numTruppe -1
                    vittoria = True
                else:
                    territorioATK.numTruppe = territorioATK.numTruppe - 1
                    giocatoreATK.numTruppe = giocatoreATK.numTruppe -1
        
        else :
             for i in valDEF:
                if valATK[i] > valDEF[i]:
                    territorioDEF.numTruppe = territorioDEF.numTruppe - 1
                    giocatoreDEF.numTruppe = giocatoreDEF.numTruppe -1
                    vittoria = True
                else:
                    territorioATK.numTruppe = territorioATK.numTruppe - 1
                    giocatoreATK.numTruppe = giocatoreATK.numTruppe -1

        if territorioDEF.numTruppe == 0:
            territorioDEF.giocatore = territorioATK.giocatore
        if giocatoreDEF.numTruppe == 0:
            giocatoreDEF.ingioco = False

        if vittoria :
            giocatoreATK.carte.append(random.randint(0,3) + 1)

        

        for i in self.listaTerritori:
            for j in self.listaTerritori:
                if self.listaTerritori.nome == territorioATK.nome:
                    j = territorioATK
                if self.listaTerritori.nome == territorioDEF.nome:
                    j = territorioDEF


"""assegna truppe, sposta truppe, attacca, termina turno"""
                    
                