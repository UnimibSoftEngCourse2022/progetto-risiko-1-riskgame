from dataclasses import dataclass
import dataclasses
import json
import math
import random
from xmlrpc.client import boolean
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Partita, Territorio, Continente, Statistiche
from typing import List
from pathlib import Path


@dataclass
class ClasseTerritorio:
    numTruppe: int = 0
    giocatore: str = ""
    nome: str = ""
    continente: str = ""


@dataclass
class ClasseContinente:
    IDContinente: int = 0
    NomeContinente: str = ""
    NumeroTruppe: int = 0


@dataclass
class ClasseGiocatore:
    nickname: str = ""
    numTruppe: int = 0
    numeroTruppeTurno: int = 0
    carte: List[int] = None
    ingioco: boolean = True
    vittoriaPartita: boolean = False


@dataclass
class ClasseStatistiche:
    IDGiocatore: str = "",
    NumeroPartiteVinte: int = 0,
    NumeroPartitePerse: int = 0,
    PercentualeVinte: float = 0.0,
    NumeroScontriVinti: int = 0,
    NumeroScontriPersi: int = 0,
    NumeroScontriVintiATK: int = 0,
    NumeroScontriPersiATK: int = 0,
    NumeroScontriVintiDEF: int = 0,
    NumeroScontriPersiDEF: int = 0,
    PercentualeScontriVintiATK: float = 0.0,
    NumeroPartiteGiocate: int = 0


class PartitaConsumer(WebsocketConsumer):

    http_user = True
    listaGiocatori = []
    listaTerritori = []
    listaContinenti = []
    listaStatistiche = []
    giocatoreAttivo = ""
    indexGiocatoreAttivo = -1
    numeroTurno = 0
    operazione: boolean = False

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['PartitaID']
        self.room_group_name = 'partita_%s' % self.room_name

        global idPartita, nomeMappa, jsonMappa
        idPartita = self.room_name
        nomeMappa = Partita.getMappa(idPartita)

        with open(str(Path(__file__).absolute().parent) + '/static/Mappe/' + nomeMappa + '.map.json') as json_file:
            jsonMappa = json.load(json_file)
        json_file.close()

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
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
            Partita.disconnettiOspite(
                text_data_json['idPartita'], text_data_json['sender'])
        elif (tipo == 'iniziaPartita'):
            self.assegnazioneTerritoriTruppeIniziali()
            self.giocatoreAttivo = self.listaGiocatori[0].nickname
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': 'iniziaTurno',
                    'sender': mittente
                }
            )
        elif (tipo == 'iniziaTurno'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )
        elif (tipo == 'truppeAssegnate'):
            self.ricezioneAssegnazioneTruppeTerritorio(
                text_data_json['listaTerritoriSocket'])
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )
            if (self.numeroTurno > 0):
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'evento_gioco',
                        'tipo': 'scegliOpzione',
                        'sender': mittente
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'evento_gioco',
                        'tipo': 'iniziaTurno',
                        'sender': mittente
                    }
                )
        elif(tipo == 'chiamataAttacco'):
            territorioAtt = None
            territorioDef = None
            for territorio in self.listaTerritori:
                if territorio.nome == text_data_json['territorioAtt']:
                    territorioAtt = territorio
                elif territorio.nome == text_data_json['territorioDef']:
                    territorioDef = territorio
            self.chiamataAttacco(territorioAtt, int(text_data_json['truppeAttaccante']),
                                 territorioDef, int(text_data_json['truppeDifensore']))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'evento_gioco',
                    'tipo': tipo,
                    'sender': mittente
                }
            )
        elif(tipo == 'chiamataSpostamento'):
            self.chiamataSpostamento(mittente, text_data_json['mittenteSocket'],
                                     text_data_json['riceventeSocket'], text_data_json['numeroTruppeSocket'])
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

        if (tipo == 'iniziaPartita'):  # Dice agli utenti di togliere la chat e disegnare il gioco
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'mappa': jsonMappa,
                'nomeMappa': nomeMappa
            }))
        elif (tipo == 'iniziaTurno'):
            self.indexGiocatoreAttivo += 1
            if (self.indexGiocatoreAttivo >= len(self.listaGiocatori)):
                self.indexGiocatoreAttivo = 0
                self.numeroTurno += 1
            self.giocatoreAttivo = self.listaGiocatori[self.indexGiocatoreAttivo].nickname
            if (self.numeroTurno > 0):
                self.chiamataAssegnazioneTruppeTerritorio(self.giocatoreAttivo)
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'numeroTurno': self.numeroTurno
            }))
        elif (tipo == 'truppeAssegnate'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'numeroTurno': self.numeroTurno
            }))
        elif (tipo == 'scegliOpzione'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'numeroTurno': self.numeroTurno
            }))
        elif (tipo == 'chiamataAttacco'):
            self.send(text_data=json.dumps({
                'tipo': 'esitoAttacco',
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'numeroTurno': self.numeroTurno,
            }))
        elif (tipo == 'chiamataSpostamento'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': mittente,
                'giocatoreAttivo': self.giocatoreAttivo,
                'listaGiocatori': self.serializzaLista(self.listaGiocatori),
                'listaTerritori': self.serializzaLista(self.listaTerritori),
                'esitoOperazione': self.operazione,
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
        xlistaGiocatori = Partita.getListaGiocatori(idPartita)
        xlistaContinenti = Continente.getListaContinentiMappa(nomeMappa)
        #xlistaStatistiche = ClasseStatistiche
        for territorio in xlistaTerritori:
            self.listaTerritori.append(ClasseTerritorio(numTruppe=0, giocatore="",
                                                        nome=territorio.NomeTerritorio, continente=territorio.Continente.NomeContinente))
        h = math.floor(len(xlistaTerritori)/len(xlistaGiocatori))
        k = 0

        for i in xlistaGiocatori:
            self.listaGiocatori.append(ClasseGiocatore(nickname=i, numTruppe=35, numeroTruppeTurno=0,
                                                       carte=[], ingioco=True, vittoriaPartita=False))
            # if not (i.find("Ospite")):
            if not (i[0:6] == 'Ospite'):
                # self.listaStatistiche.append(Statistiche.getListaStatistiche(i))
                oggStat = Statistiche.getListaStatistiche(i)
                self.listaStatistiche.append(ClasseStatistiche(i, oggStat.NumeroPartiteVinte,
                    oggStat.NumeroPartitePerse, oggStat.PercentualeVinte, oggStat.NumeroScontriVinti,
                    oggStat.NumeroScontriPersi, oggStat.NumeroScontriVintiATK, oggStat.NumeroScontriPersiATK,
                    oggStat.NumeroScontriVintiDEF, oggStat.NumeroScontriPersiDEF, oggStat.PercentualeScontriVintiATK,
                    oggStat.NumeroPartiteGiocate))
            for j in range(k , h):
                if (h > len(self.listaTerritori)):
                    break
                self.listaTerritori[j].giocatore = i
            k = h
            h = h + h

        for continente in xlistaContinenti:
            self.listaContinenti.append(ClasseContinente(continente.IDContinente,
                                                         continente.NomeContinente, continente.NumeroTruppe))

        # for statistiche in xlistaStatistiche:
            #self.listaStatistiche.append(ClasseStatistiche(statistiche.IDGiocatore, statistiche.NumeroPartiteVinte, statistiche.NumeroPartitePerse, statistiche.PercentualeVinte, statistiche.NumeroScontriVinti, statistiche.NumeroScontriPersi, statistiche.NumeroScontriPersiATK, statistiche.NumeroScontriVintiDEF, statistiche.NumeroScontriPersiDEF, statistiche.PercentualeScontriVintiATK, statistiche.NumeroPartiteGiocate))

    def chiamataAssegnazioneTruppeTerritorio(self, classeGiocatore):
        
        k = 0
        cont = 0
        xgiocatore: ClasseGiocatore
        for giocatore in self.listaGiocatori:
            if giocatore.nickname == classeGiocatore:
                xgiocatore = giocatore
        if giocatore.carte.count(1) > 1 and giocatore.carte.count(4) > 0:
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(2) > 1 and giocatore.carte.count(4) > 0:
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(3) > 1 and giocatore.carte.count(4) > 0:
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            giocatore.carte.remove(4)
            k = 12
        elif giocatore.carte.count(3) > 0 and giocatore.carte.count(2) > 0 and giocatore.carte.count(1) > 0:
            giocatore.carte.remove(3)
            giocatore.carte.remove(2)
            giocatore.carte.remove(1)
            k = 10
        elif giocatore.carte.count(3) > 2:
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            giocatore.carte.remove(3)
            k = 8
        elif giocatore.carte.count(2) > 2:
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            giocatore.carte.remove(2)
            k = 6
        elif giocatore.carte.count(1) > 2:
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            giocatore.carte.remove(1)
            k = 4

# calcolo truppe continente
        for i in self.listaContinenti:
            territoriContinente = 0
            territoriPosseduti = 0
            for j in self.listaTerritori:
                if i.NomeContinente == j.continente:
                    territoriContinente = territoriContinente + 1
                    if j.giocatore == xgiocatore.nickname:
                        territoriPosseduti = territoriPosseduti + 1
            if territoriContinente == territoriPosseduti:
                k = k + i.NumeroTruppe

        for i in self.listaTerritori:
            if xgiocatore.nickname == i.giocatore:
                cont = cont + 1
        xgiocatore.numeroTruppeTurno = math.floor(cont/3)
        if xgiocatore.numeroTruppeTurno == 0:
            xgiocatore.numeroTruppeTurno = 1
        xgiocatore.numeroTruppeTurno = xgiocatore.numeroTruppeTurno + k
        print(xgiocatore.numeroTruppeTurno)
        xgiocatore.numTruppe = xgiocatore.numTruppe + xgiocatore.numeroTruppeTurno
        print(xgiocatore.numTruppe)
        for i in self.listaGiocatori:
            if xgiocatore.nickname == i.nickname:
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
                if j.nome == i['nome']:
                    j.numTruppe = int(i['numTruppe'])
                    break

    def chiamataAttacco(self, territorioATK, truppeATK, territorioDEF, truppeDEF):
        valATK = []
        valDEF = []
        statisticheATK: ClasseStatistiche
        statisticheDEF: ClasseStatistiche
        giocatoreATK: ClasseGiocatore
        giocatoreDEF: ClasseGiocatore
        vittoria: boolean = False
        totTerritori: int = 0

        for giocatore in self.listaGiocatori:
            if giocatore.nickname == territorioATK.giocatore:
                giocatoreATK = giocatore
            elif giocatore.nickname == territorioDEF.giocatore:
                giocatoreDEF = giocatore

        for statistiche in self.listaStatistiche:
            if statistiche.IDGiocatore == giocatoreATK.nickname:
                statisticheATK = statistiche
            elif statistiche.IDGiocatore == giocatoreDEF.nickname:
                statisticheDEF = statistiche

        for i in range(0, truppeATK):
            valATK.append(random.randint(0, 5))

        for i in range(0, truppeDEF):
            valDEF.append(random.randint(0, 5))

        valATK.reverse()
        valDEF.reverse()

        if len(valDEF) > len(valATK):
            for i in range(0, len(valATK)):
                if valATK[i] > valDEF[i]:
                    territorioDEF.numTruppe = territorioDEF.numTruppe - 1
                    giocatoreDEF.numTruppe = giocatoreDEF.numTruppe - 1
                    statisticheATK.NumeroScontriVinti = statisticheATK.NumeroScontriVinti + 1
                    statisticheATK.NumeroScontriVintiATK = statisticheATK.NumeroScontriVintiATK + 1
                    statisticheDEF.NumeroScontriPersi = statisticheDEF.NumeroScontriPersi + 1
                    statisticheDEF.NumeroScontriPersiDEF = statisticheDEF.NumeroScontriPersiDEF + 1
                else:
                    territorioATK.numTruppe = territorioATK.numTruppe - 1
                    giocatoreATK.numTruppe = giocatoreATK.numTruppe - 1
                    statisticheATK.NumeroScontriPersi = statisticheATK.NumeroScontriPersi + 1
                    statisticheATK.NumeroScontriPersiATK = statisticheATK.NumeroScontriPersiATK + 1
                    statisticheDEF.NumeroScontriVinti = statisticheDEF.NumeroScontriVinti + 1
                    statisticheDEF.NumeroScontriVintiDEF = statisticheDEF.NumeroScontriVintiDEF + 1

        else:
            for i in range(0, len(valDEF)):
                if valATK[i] > valDEF[i]:
                    territorioDEF.numTruppe = territorioDEF.numTruppe - 1
                    giocatoreDEF.numTruppe = giocatoreDEF.numTruppe - 1
                    statisticheATK.NumeroScontriVinti = statisticheATK.NumeroScontriVinti + 1
                    statisticheATK.NumeroScontriVintiATK = statisticheATK.NumeroScontriVintiATK + 1
                    statisticheDEF.NumeroScontriPersi = statisticheDEF.NumeroScontriPersi + 1
                    statisticheDEF.NumeroScontriPersiDEF = statisticheDEF.NumeroScontriPersiDEF + 1
                else:
                    territorioATK.numTruppe = territorioATK.numTruppe - 1
                    giocatoreATK.numTruppe = giocatoreATK.numTruppe - 1
                    statisticheATK.NumeroScontriPersi = statisticheATK.NumeroScontriPersi + 1
                    statisticheATK.NumeroScontriPersiATK = statisticheATK.NumeroScontriPersiATK + 1
                    statisticheDEF.NumeroScontriVinti = statisticheDEF.NumeroScontriVinti + 1
                    statisticheDEF.NumeroScontriVintiDEF = statisticheDEF.NumeroScontriVintiDEF + 1

        statisticheATK.PercentualeScontriVintiATK = statisticheATK.NumeroScontriVintiATK / \
            (statisticheATK.NumeroScontriVintiATK +
             statisticheATK.NumeroScontriPersiATK) * 100

        if territorioDEF.numTruppe == 0:
            territorioDEF.giocatore = territorioATK.giocatore
            vittoria = True
        if giocatoreDEF.numTruppe == 0:
            giocatoreDEF.ingioco = False

        if vittoria:
            giocatoreATK.carte.append(random.randint(1, 4))

        for i in self.listaTerritori:
            for j in self.listaTerritori:
                if j.nome == territorioATK.nome:
                    j = territorioATK
                if j.nome == territorioDEF.nome:
                    j = territorioDEF

        # controllo vittoriaPartita

        for i in self.listaTerritori:
            if i.giocatore == giocatoreATK.nickname:
                totTerritori = totTerritori + 1

        if totTerritori >= len(self.listaTerritori):
            giocatoreATK.vittoriaPartita = True
            self.aggiornaStatisticheVittoria(giocatoreATK)

        for giocatore in self.listaGiocatori:
            if giocatore.nickname == territorioATK.giocatore:
                giocatore = giocatoreATK
            if giocatore.nickname == territorioDEF.giocatore:
                giocatore = giocatoreDEF

    def chiamataSpostamento(self, postinoSocket, mittenteSocket, riceventeSocket, numeroTruppeSocket):
        postino : ClasseGiocatore = ClasseGiocatore()
        mittente : ClasseTerritorio = ClasseTerritorio()
        ricevente : ClasseTerritorio = ClasseTerritorio()   

        for giocatore in self.listaGiocatori:
            if giocatore.nickname == postinoSocket:
                postino = giocatore

        for territorio in self.listaTerritori:
            if territorio.nome == mittenteSocket:
                mittente = territorio
            if territorio.nome == riceventeSocket:
                ricevente = territorio

        if mittente.giocatore == postino.nickname:
            if (mittente.numTruppe - 1) >= int(numeroTruppeSocket):
                mittente.numTruppe = mittente.numTruppe - \
                    int(numeroTruppeSocket)
                ricevente.numTruppe = ricevente.numTruppe + \
                    int(numeroTruppeSocket)
                self.operazione = True

        for territorio in self.listaTerritori:
            if territorio.nome == mittenteSocket:
                territorio = mittente
            if territorio.nome == riceventeSocket:
                territorio = ricevente

    def aggiornaStatisticheVittoria(self, vincitore):
        statistiche: ClasseStatistiche
        for i in self.listaGiocatori:
            if (i.nickname == vincitore.nickname):
                i.NumeroPartiteVinte = i.NumeroPartiteVinte + 1
                i.PercentualeVinte = i.NumeroPartiteVinte / \
                    (i.NumeroPartiteVinte + i.NumeroPartitePerse) * 100
            else:
                i.NumeroPartitePerse = i.NumeroPartitePerse + 1
            i.NumeroPartiteGiocate = i.NumeroPartiteGiocate + 1


"""assegna truppe, sposta truppe, attacca, termina turno"""
