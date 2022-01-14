from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS GiocatoreRegistrato"
                   "(Nickname TEXT NOT NULL PRIMARY KEY,"
                   "Nome TEXT NOT NULL,"
                   "Cognome NOT NULL,"
                   "Email TEXT NOT NULL UNIQUE,"
                   "Password TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Mappa"
                   "(IDMappa INTEGER NOT NULL PRIMARY KEY,"
                   "NomeMappa TEXT NOT NULL,"
                   "Autore TEXT NOT NULL,"
                   "PercorsoMappa TEXT NOT NULL,"
                   "FOREIGN KEY (Autore) REFERENCES GiocatoreRegistrato(Nickname))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Partita"
                   "(IDPartita INTEGER NOT NULL PRIMARY KEY,"
                   "NumeroGiocatori INTEGER NOT NULL,"
                   "Difficolta INTEGER NOT NULL,"
                   "Mappa INTEGER NOT NULL,"
                   "FOREIGN KEY (Mappa) REFERENCES Mappa(IDMappa))")
    cursor.execute("CREATE TABLE IF NOT EXISTS GiocatoreRegistrato_Partita"
                   "(NicknameGiocatore TEXT NOT NULL,"
                   "IdPartita INTEGER NOT NULL,"
                   "PRIMARY KEY (NicknameGiocatore, IdPartita),"
                   "FOREIGN KEY (NicknameGiocatore) REFERENCES GiocatoreRegistrato(Nickname),"
                   "FOREIGN KEY (IdPartita) REFERENCES Partita(IDPartita))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Statistiche"
                   "(NicknameGiocatore TEXT NOT NULL PRIMARY KEY,"
                   "NumeroPartiteVinte INTEGER NOT NULL,"
                   "NumeroPartitePerse INTEGER NOT NULL,"
                   "PercentualeVinte FLOAT NOT NULL,"
                   "NumeroScontriVinti INTEGER NOT NULL,"
                   "NumeroScontriPersi INTEGER NOT NULL,"
                   "NumeroScontriVintiATK INTEGER NOT NULL,"
                   "NumeroScontriPersiATK INTEGER NOT NULL,"
                   "PercentualeScontriVintiATK REAL NOT NULL,"
                   "TempoDiGioco INTEGER NOT NULL,"
                   "NumeroTruppeGenerate INTEGER NOT NULL,"
                   "NumeroTruppePerse INTEGER NOT NULL,"
                   "NumeroPartiteGiocate INTEGER NOT NULL,"
                   "FOREIGN KEY (NicknameGiocatore) REFERENCES GiocatoreRegistrato(Nickname))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Continente"
                   "(IDContinente INTEGER NOT NULL PRIMARY KEY,"
                   "NomeContinente TEXT NOT NULL,"
                   "Colore TEXT NOT NULL,"
                   "NumeroTruppe INTEGER NOT NULL,"
                   "Mappa INTEGER NOT NULL,"
                   "FOREIGN KEY (Mappa) REFERENCES Mappa(IDMappa))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Territorio"
                   "(IDTerritorio INTEGER NOT NULL PRIMARY KEY,"
                   "NomeTerritorio TEXT NOT NULL,"
                   "Continente INTEGER NOT NULL,"
                   "FOREIGN KEY (Continente) REFERENCES Continente(IDContinente))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Carta"
                   "(Territorio INTEGER NOT NULL PRIMARY KEY,"
                   "Simbolo TEXT NOT NULL,"
                   "Jolly INT NOT NULL,"
                   "FOREIGN KEY (Territorio) REFERENCES Territorio(IDTerritorio))")