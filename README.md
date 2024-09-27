# Rasberry Pi Oppsett
## Laste ned Rasberry Pi og Ubuntu som Operativsystem
### Teksten under er oppsettet for Rasberry Pi i rekkefølge.
1. Begynn med å ha en sd-kort som er satt inn i pc-en, dette sd-kortet skal settes inn i Rasberry Pi enheten din senere.
2. Last ned Rasberry Imager fra https://www.raspberrypi.com/software/
3. Åpne imager.exe filen som du nettopp lastet ned, og klikk ```Install```
4. Deretter klikker du ```Finish```
5. Når Rasberry Pi Imager er installert og åpnet, skal du velge enheten, operativsystemet og lagring.
    * Har du en Rasberry Pi 4 enhet, velger du det.
    * For operativsystemet (OS) skal vi velge nyeste versjonen av Ubuntu. For å gjøre dette, klikk ```CHOOSE OS``` > ```Other General-Purpose OS``` > ```Ubuntu```, også nyeste versjonen av ubuntu, som vanligvis ligger øverst på listen.
    * For lagrningsplass, velger du sd-kortet som du skal bruke for Rasberry Pi-en din.
6. Deretter Klikker du ```Next```, også ```YES``` når den spør deg om å slette alt som ligger i sd-kortet.
7. Etter at det nødvenige innholdet er lastet ned i sd-kortet, klikker du ```CONTINUE```
8. Nå kan du lukke Rasberry Pi Imager, og ta ut sd-kortet. Sett den inn i Rasberry Pi enheten din.

## MariaDB Installasjon og setup
Åpne terminalen ved å trykke tastene ```CTRL + Alt + T``` samtidig.

Vi begynner med å oppdatere og opgradere systemet i tilfelle det er noen filer datamaskinen mangler. Skriv in følgene kommandoer:
```system
sudo apt update
```
```system
sudo apt upgrade
```

Last ned mariadb serveren:
```system
sudo apt install mariadb-server
```
Denne kommandoen vil sikre MariaDB:
```system
sudo mysql_secure_installation
```
```Enter current password for root (enter for none):```
Skriv in ```Y```

```Switch to unix_socket authentication [Y/N]```
Skrv in ```Y```

```Change the root password? [Y/N]```
skriv in ```N```

```Remove anonymous users? [Y/N]```
skriv in ```Y```

```Disallow root login remotely? [Y/N]```
Skrv in ```Y```

```Remove test database and access to it? [Y/N]```
Skriv in ```Y```

```Reload priviliege tables now? [Y/N]```
Skriv in ```Y```



Deretter kjører vi MariaDB med følgende kommando:
```system
sudo mariadb -u server
```
Videre så lager vi en bruker til MariaDB. Brukernavnet og passordet er valgfritt:
```system
CREATE USER 'brukernavn'@'localhost' IDENTIFIED BY 'passord';
```
Deretter gir vi denne brukeren full makt:
```system
GRANT ALL PRIVILEGES ON *.* TO 'brukernavn'@'localhost';
```
Etter at du har tildelt privilegier til bruken, kjører du denne kommandoen for å sikre at MariaDB oppdaterer rettighetene umiddelbart:
```system
FLUSH PRIVILEGES;
```
Deretter kjører vi denne kommandoen for å avslutte MariaDB-sesjonen og tar deg tilbake til terminalen:
```system
EXIT;
```
## Python, MariaDB og SSH

### 1. Åpne terminalen med CTRL + ALT + T
Her skriver du kommandoene under.

### 2. Se etter og installer oppdateringer til all programvare som er installert
a. `sudo apt update` (finner oppdateringer)  
b. `sudo apt upgrade` (installerer oppdateringer)

### 3. Sett opp brannmur med UFW (uncomplicated firewall)
a. `sudo apt install ufw` (installerer UFW)  
b. `sudo ufw enable` (aktiverer brannmuren ved oppstart)  
c. `sudo ufw allow ssh` (tillater SSH-tilkoblinger gjennom brannmuren)  
d. Senere kan du sjekke statusen på brannmuren ved å skrive `sudo ufw status`

### 4. Skru på ssh
a. `sudo apt install openssh-server` (installerer SSH-serveren)  
b. `sudo systemctl enable ssh` (gjør sånn at SSH skrur seg på ved oppstart)  
c. `sudo systemctl start ssh` (starter SSH her og nå)

### 5. Finn IPen din – den trenger du når du skal bruke SSH
a. `ip a`  
b. Hvis du har kablet nettverk, vil IP vises ved eth0: linje. Hvis du kun har trådløst, vil IP vises ved wlan0: linje. IP-adresse er vanligvis 10.2.3.x eller noe lignende (hvor x er et nummer mellom 2 og 254).

## Python med MariaDB

1. Opprett databasen og tabellen: Kjør følgende SQL-kommandoer i MariaDB-konsollen:
```
CREATE DATABASE telefonkatalog;
USE telefonkatalog;

CREATE TABLE person (
    id int NOT NULL AUTO_INCREMENT,
    fornavn VARCHAR(255) NOT NULL,
    etternavn VARCHAR(255) NOT NULL,
    telefonnummer CHAR(8),
    PRIMARY KEY (id)
);
```
2. Avslutt MariaDB:
```
EXIT;
```

## Python Filen
1. Opprett en ny Python-fil, f.eks. telefonkatalog.py:
```
nano telefonkatalog.py
```

2. Lim inn følgende kode i filen (Husk å erstatte ip_adressen_til_PI, username og password med dine faktiske MariaDB-tilkoblingsdetaljer.):
```
import mysql.connector  # pip install mysql-connector-python

mydb = mysql.connector.connect(
    host="ip_adressen_til_PI",
    user="username",
    password="password",
    database="telefonkatalog"
)

cursor = mydb.cursor()
cursor.execute("SELECT * FROM person")
resultater = cursor.fetchall()

for dings in resultater:
    print(dings)

def printMeny():
    print("------------------- Telefonkatalog -------------------")
    print("| 1. Legg til ny person                              |")
    print("| 2. Søk opp person eller telefonnummer              |")
    print("| 3. Vis alle personer                               |")
    print("| 4. Avslutt                                         |")
    print("------------------------------------------------------")
    menyvalg = input("Skriv inn tall for å velge fra menyen:")
    utfoerMenyvalg(menyvalg)

def utfoerMenyvalg(valgtTall):
    if(valgtTall == "1"):
        registrerPerson()
    elif(valgtTall == "2"):
        sokPerson()
        printMeny()
    elif(valgtTall == "3"):
        visAllePersoner()
    elif(valgtTall == "4"):
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N")
        if(bekreftelse == "J" or bekreftelse == "j"):
            exit()
        else:
            printMeny()             
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-4.")
        utfoerMenyvalg(nyttForsoek)

def registrerPerson():
    fornavn = input("Skriv inn fornavn:")
    etternavn = input("Skriv inn etternavn:")
    telefonnummer = input("Skriv inn telefonnummer:")

    lagreIDatabase(fornavn, etternavn, telefonnummer)

    input("Trykk en tast for å gå tilbake til menyen")
    printMeny()

def visAllePersoner():
    mydb = mysql.connector.connect(
        host="ip_adressen_til_PI",
        user="username",
        password="password",
        database="telefonkatalog"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM person")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    mydb.close()
    printMeny()

def sokPerson():
    print("1. Søk på fornavn")
    print("2. Søk på etternavn")
    print("3. Søk på telefonnummer")
    print("4. Tilbake til hovedmeny")
    sokefelt = input("Skriv inn ønsket søk 1-3, eller 4 for å gå tilbake:")
    if(sokefelt == "1"):
        navn = input("Fornavn:")
        finnPerson("fornavn", navn)
    elif(sokefelt == "2"):
        navn = input("Etternavn:")
        finnPerson("etternavn", navn)
    elif(sokefelt == "3"):
        tlfnummer = input("Telefonnummer:")
        finnPerson("telefonnummer", tlfnummer)
    elif(sokefelt == "4"):
        printMeny()
    else:
        print("Ugyldig valg. Velg et tall mellom 1-4.")
        sokPerson()

def finnPerson(typeSok, sokeTekst):
    mydb = mysql.connector.connect(
        host="ip_adressen_til_PI",
        user="username",
        password="password",
        database="telefonkatalog"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM person where " + typeSok + " ='" + sokeTekst + "'")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

def lagreIDatabase(fornavn, etternavn, telefonnummer):
    mydb = mysql.connector.connect(
        host="ip_adressen_til_PI",
        user="username",
        password="password",
        database="telefonkatalog"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO person (fornavn, etternavn, telefonnummer) VALUES (%s, %s, %s)"
    val = (fornavn, etternavn, telefonnummer)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

printMeny()  # Starter programmet ved å skrive menyen første gang
```
3. Lagre og lukk filen. Hvis du bruker nano, trykk ```CTRL + X```, så ```Y``` for å lagre, og ENTER for å bekrefte.
## Kjør Python skriptet
* For å kjøre skriptet, bruk følgende kommando i terminalen:
```
python3 telefonkatalog.py
``` 
* Husk å erstatte ip_adressen_til_PI, username og password med dine faktiske MariaDB-tilkoblingsdetaljer.
