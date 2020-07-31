# Projekt im Umfang des Moduls Netzwerkprogrammierung


## Aufgabenstellung:
1) Verhindert werden soll unter anderen ein Split-Brain Szenario, d.h. eine Mehrheit aller Server
muss zu dem gleichen Ergebnis kommen wer von ihnen der Master ist (Quorum).
2) Die Bedingung unter denen ein Master ermittelt wird muss eindeutig sein.
3) Aktionen die auf dem Master bzw. Nicht-Master ausgeführt werden, sollen frei konfigurierbar sein
(z.B. durch Ausführen eines Python/Shell Skripts).


## Lösungsansatz
Für diese Aufgabe müssen wir zuerst eine Kommunikation zwischen den Serven aufbauen. 
Das habe mit Flask realisiert, da hier einfach über aufrufen eines URL Information
ausgetauscht werden kann.
Desweiteren kennt jeder Controller zu Beginn alle anderen Controller um die Aufgabenstellung zu 
vereinfachen. <br/>
Das wird gerade dann wichtig wenn ein Quorum gebraucht wird um den Master zu bestimmen.
Es müssen also mehr als die Hälfte der Controller laufen damit die Routine des abstimmens gestartet wird. <br/>
Alle aktiven Controller kommunizieren in regelmäßigen Abständen mit allen anderen Controllern und
speichern deren Zustand(aktiv oder inaktiv) und welchen Master diese haben.
Durch diese Information kann ein neuer Master jederzeit bestimmt werden bzw. festgestellt werden ob es 
bereits einen aktiven Master gibt. 
Der Master, sofern ein neuer Master benötigt wird, wird eindeutig durch die niedrigste IP und zusätzlich
den niedrigsten Port bestimmt. <br/>
Wenn sich der Status eines Controllers von Worker zu Master, Master zu Worker oder initial der Worker Status 
zugewiesen wird kann ein Python Skript ausgeführt werden.


## Installation
Für das Projekt habe ich Python 3.8 benutzt. <br/>
Da die app einen Flask Server benutzt muss das Modul installiert werden. Zudem benutze ich für die requests
eine Funktion aus der 
````
pip install Flask
pip install requests

Note: Für gewöhnlich möchte man sogenannte Virtual Environments nutzen. In dem Fall benutze:
pipenv install Flask
pipenv install requests
````

## Anwendungsfall
Eine Applikation kann wie folgt gestartet werde: <br/>
Zunächst navigiere mit einer Kommandozeile zum Ordner in dem app.py liegt. 
Dann kann das Programm wie folgt gestartet werden:
````
python app.py <ip> <port> <master_script> <worker_script>
````
Damit die Funktion wirklich überprüft werden kann solten mehrere Terminals gestartet werden mit den IP's 
und Ports in der app.py Datei. Diese können bei Bedarf auch im Code geändert werden. Hier die Liste der verfügbaren Adressen und Ports:
````
http://127.0.0.1:5000 mit IP=127.0.0.1 und Port=5000
http://127.0.0.1:5001 mit IP=127.0.0.1 und Port=5001
http://127.0.0.1:5002 mit IP=127.0.0.1 und Port=5002
http://127.0.0.1:5003 mit IP=127.0.0.1 und Port=5003
http://127.0.0.1:5004 mit IP=127.0.0.1 und Port=5004
````
Also könnte man die Server wie folgt starten:
````
python app.py 127.0.0.1 5000
````
Den Wissensstand jedes Controller kann man angenehm in dessen Adresse überprüfen unter:
````
http://127.0.0.1:5000/
````


## PyDoc
Die PyDocs können jederzeit mit: 
````
pydoc -b app.py
oder
python -m pydoc -b app.py
````




### Lizenz
[MIT](https://choosealicense.com/licenses/mit/)
