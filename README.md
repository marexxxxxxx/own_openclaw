# own_openclaw

##Projektbeschreibung

Dieses Projekt soll veranschaulichen und als eigenes Lernprojekt dazu verwnedet werden um die tieferen abläufe von agentic systems zu verstehen und selbst auszuführen und zu entiwckeln.

###Phase 1

Initialisierung von:
- Dockerfile für einen Container welcher Grundlegende Build tools, Python, uv beherbergt.
- Dockerfile für den Ai Agent. Also mit grundlegenden befehlen, aber mit einem security konzept, sodass der Agent nciht aus dem Docker container ausbrechen kann. Das image sollte ein Linux Ubuntu Server Image sein. Gebe dem Container auch grundlegende befehle wie cat vim curl ping ssh etc...
- Dockercompose für die Dockerfile und eine POSTGRES Datenbank mit hinzufügen von einem vektor plugin und Pgadmin
### Phase 2
Erstellung des Gateways. Mit Grundlegenden Funktionen wie:
- Verbindungsaufbau zu Ollama Service
- Verbindung zu Datenbank
- Grundlegende File mit Commands für den Dockercontainer für den Ai Agent
- Starten von dem Dockercontainer für den Agenten und bei inaktivätet bei mehr als 4 min automaitsches herrunterfahren
- Verbindung zu dem Dockercontainer für den Ai Agent
Teste folgende Funktionalitäten und überprüfe ob das klappt:
- Teste ob das Gateway den Docker Container hochfahren kann.
- Teste ob der Container bei inaktivtät sich wieder herrunterfährt.
- Teste ob befehle über das Gateway an den Container gesendet werden, und was das Ergebnis ist. Prüfe das bei allen Befehlen, und ob es einen Timer gibt der nach einer Gewissen zeit automatisch etwas zurück meldet.
### Phase 3
Ich will das der Agent die Möglichkeit bekommt sich zu individualsieren. ich will das du eine Tabelle hinzufügst worin alle Chatnachrichten gespeichert werden. es soll die Möglichkeit geben das er da drinne suchen kann, via vector search aber auch mit full text searchh. schreibe ihm dafür die benötigten befehle sowie hinterlege sie in der Datei mit den standard befehlen die er benutzten kann. 
