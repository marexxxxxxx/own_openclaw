# own_openclaw

## Projektbeschreibung
Dieses Projekt dient als interaktive Lern- und Experimentierumgebung zur Erforschung, Entwicklung und Orchestrierung autonomer KI-Agenten (Agentic Systems). Der Fokus liegt auf dem tiefgreifenden Verständnis der zugrundeliegenden Prozesse, der API-Kommunikation und der sicheren Ausführung isolierter KI-Workloads.

## Technologie-Stack
* **Backend & API:** Python, FastAPI, uv (Package Manager)
* **Infrastruktur:** Ubuntu Server, Docker, Docker Compose
* **Datenbank:** PostgreSQL (inkl. pgvector Plugin), pgAdmin
* **KI-Backend:** Ollama

---

### Phase 1: Infrastruktur & Sandboxing
Aufbau der isolierten Basisumgebung mittels Docker:
* **Base-Image:** Ein Dockerfile, das grundlegende Build-Tools, Python und `uv` bereitstellt.
* **Agent-Sandbox:** Ein dediziertes Dockerfile (basierend auf Ubuntu Server) für den KI-Agenten. Im Fokus steht ein striktes Security-Konzept zur Verhinderung von Container-Breakouts. Der Container erhält Zugriff auf essenzielle CLI-Tools (`cat`, `vim`, `curl`, `ping`, `ssh`).
* **Orchestrierung:** Eine `docker-compose.yml`, die das Zusammenspiel der Container steuert und die PostgreSQL-Datenbank (inkl. Vektor-Plugin) sowie pgAdmin hochfährt.

### Phase 2: API-Gateway & Lifecycle-Management
Entwicklung des zentralen FastAPI-Gateways mit folgenden Kernfunktionen:
* **Schnittstellen:** Verbindungsaufbau zum lokalen Ollama-Service und zur PostgreSQL-Datenbank.
* **Command-Management:** Verwaltung einer Basis-Datei mit den zulässigen Befehlen für den Agent-Container.
* **Lifecycle-Management:** Dynamisches Starten des Agent-Containers durch das Gateway und Implementierung eines automatischen Shutdowns nach 4 Minuten Inaktivität (Idle-Timeout).
* **Ausführung:** Aufbau der Verbindung zum Agent-Container zur Befehlsausführung.
* **Testing-Fokus:** * Erfolgreicher Container-Start via Gateway.
  * Zuverlässiges Herunterfahren beim Idle-Timeout.
  * Korrekte Weiterleitung, Ausführung und Rückmeldung von Befehlen aus dem Container (inkl. Timeout-Timer für die Antworten).

### Phase 3: Frontend & Message Routing
Entwicklung eines minimalistischen Web-Interfaces zur Interaktion:
* **UI-Aufbau:** Ein geteiltes Interface zur Spezifikation des Providers und ein separates Chat-Fenster für die Kommunikation mit dem Agenten.
* **Routing-Logik:** Der User sendet Nachrichten an das Gateway, welches diese an Ollama weiterleitet. 
* **Function Calling:** Das Gateway verarbeitet die Ollama-Response. Handelt es sich um einen Function Call, führt das Gateway den entsprechenden Befehl im Agent-Container aus, sendet das Resultat zurück an Ollama und leitet die finale Antwort an die Web-UI. Ist kein Function Call nötig, wird die Antwort direkt an die UI durchgereicht.

### Phase 4: Langzeitgedächtnis & Personalisierung (RAG)
Erweiterung des Agenten um die Fähigkeit zur Individualisierung durch Zugriff auf vergangene Konversationen:
* **Persistenz:** Anlage einer Datenbanktabelle zur dauerhaften Speicherung aller Chatnachrichten.
* **Suchfunktionen:** Implementierung von Vektorsuche (Vector Search) und Volltextsuche (Full Text Search) auf dem Chatverlauf.
* **Autonomie:** Erweiterung der Standard-Befehlsdatei des Agenten um spezifische Suchbefehle, sodass der Agent selbstständig in seiner eigenen Historie nach Kontext suchen kann.
