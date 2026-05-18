# own_openclaw - Technical Architecture & Implementation Guide

## 1. Projektbeschreibung & Zielsetzung
Dieses Projekt dient als interaktive Lern- und Experimentierumgebung zur Erforschung, Entwicklung und Orchestrierung autonomer KI-Agenten (Agentic Systems). Der Fokus liegt auf dem tiefgreifenden Verständnis der zugrundeliegenden Prozesse, API-Kommunikation, Tool-Use (Function Calling) und der sicheren Ausführung isolierter KI-Workloads.

## 2. Technologie-Stack & Versionierung
* **Backend API:** Python 3.12+, FastAPI, Uvicorn
* **Package Management:** uv
* **Infrastruktur & Orchestrierung:** Docker, Docker Compose, Docker SDK for Python (`docker` pip package)
* **Datenbank:** PostgreSQL 16+ (inkl. `pgvector` Plugin), pgAdmin 4
* **KI-Backend:** Ollama (lokal) mit Function-Calling-kompatiblen Modellen (z.B. Llama 3 oder Mistral)
* **Frontend:** HTML/CSS/Vanilla JS (serviert über FastAPI als statische Dateien)

---

## 3. Architektur & Phasen-Implementierung

### Phase 1: Infrastruktur & Sandboxing

**3.1. Verzeichnisstruktur & Docker-Setup:**
* `docker-compose.yml`: Definiert drei Services: `gateway` (FastAPI), `postgres` (mit pgvector) und `pgadmin`. Der Agent-Container wird *nicht* hierüber permanent gestartet, sondern dynamisch vom Gateway gespawnt.
* `Dockerfile.gateway`: Basiert auf `python:3.12-slim`, installiert `uv`, kopiert die `requirements.txt`/`pyproject.toml` und startet FastAPI.
* `Dockerfile.agent`: Basiert auf `ubuntu:24.04`. 
  * **Security Profile:** Der Container läuft im `--network none` (falls keine externe API gefordert ist) oder in einem isolierten Bridge-Network. Drop aller unnötigen Linux-Capabilities (`--cap-drop=ALL`). Run als Non-Root User.
  * **Tooling:** Installation der erlaubten CLI-Tools: `cat`, `vim`, `curl`, `ping`, `ssh`, `ls`, `pwd`, `cd`, `touch`, `mkdir`, `cp`, `mv`, `rm`, `grep`, `find`, `chmod`, `chown`, `ip`, `ss`, `rsync`, `tar`, `ps`, `kill`, `htop`, `df`, `du`, `git`, `apt`.

**3.2. Netzwerk & Volumes:**
* `own_openclaw_net`: Dediziertes Docker-Netzwerk für die interne Kommunikation (Gateway <-> Postgres <-> pgAdmin).
* `pg_data`: Persistentes Docker-Volume für PostgreSQL.

### Phase 2: API-Gateway & Lifecycle-Management

**2.1. FastAPI Struktur (`/app`):**
* `main.py`: Entrypoint, FastAPI App-Instanz.
* `routes/chat.py`: Endpunkte für die Frontend-Kommunikation.
* `services/docker_manager.py`: Nutzt das `docker` Python-Package zur Steuerung des Agent-Containers.
* `services/ollama_client.py`: Handhabt HTTP-Requests an die Ollama API (`http://localhost:11434/api/chat`).

**2.2. Lifecycle Management (Docker Manager):**
* **Start:** Prüft via Docker API, ob der Container `agent_sandbox` läuft. Wenn nicht, wird er gestartet (`client.containers.run(..., detach=True)`).
* **Execution:** Befehle werden über `container.exec_run("befehl")` ausgeführt. stdout/stderr und Exit-Codes werden zurückgegeben.
* **Idle-Timeout:** Ein asynchroner Background-Task prüft den letzten Timestamp einer Befehlsausführung. Ist `datetime.now() - last_exec > 4 Minuten`, wird `container.stop()` getriggert.

**2.3. Befehls-Registry:**
* Eine `tools.json` oder Python-Dict, welches die verfügbaren Befehle (z. B. `run_bash_command`) als JSON-Schema definiert. Dieses Schema wird im Ollama-Request als `tools`-Parameter mitgegeben.

### Phase 3: Frontend & Message Routing

**3.1. UI Design (Minimalist):**
* Zwei-Spalten-Layout (HTML/CSS/Vanilla JS).
* Links: Einstellungs-Panel (Provider URL, Model-Auswahl, System-Prompt).
* Rechts: Chat-Interface (Scrollable Message-History, Input-Feld).

**3.2. Routing & Function Calling Logik (Backend):**
1. User sendet Text an `POST /api/chat`.
2. Gateway ruft Ollama API auf, injiziert Chat-Historie und `tools`.
3. Ollama antwortet:
   * **Szenario A (Text-Antwort):** Gateway speichert in DB und leitet den Text ans Frontend.
   * **Szenario B (Tool Call):** Ollama gibt JSON mit Tool-Name und Parametern zurück (z.B. `{"name": "run_bash", "arguments": {"cmd": "ls -la"}}`).
4. Gateway fängt Tool Call ab, ruft `docker_manager.py` auf, führt den Befehl in der Sandbox aus.
5. Gateway sendet das Resultat (stdout) sofort als neue "Tool"-Nachricht an Ollama zurück.
6. Ollama generiert finale Antwort -> Weiterleitung an Frontend.

### Phase 4: Langzeitgedächtnis & Personalisierung (RAG)

**4.1. Datenbank-Schema (PostgreSQL):**
* Tabelle `sessions`: `id` (UUID), `created_at`.
* Tabelle `messages`: `id` (UUID), `session_id` (FK), `role` (user/assistant/tool), `content` (Text), `embedding` (vector(768) oder entsprechendes Modellmaß), `timestamp`.

**4.2. Embedding & Suche:**
* Vor dem Speichern generiert das Gateway via Ollama (`/api/embeddings`) einen Vektor der Nachricht.
* **Vector Search:** SQL-Query mit Cosine Similarity (`ORDER BY embedding <=> query_embedding LIMIT 5`).
* **Full Text Search:** PostgreSQL `tsvector` und `tsquery` auf der `content`-Spalte.

**4.3. Agent-Autonomie (Self-RAG):**
* Die Tools `search_memory_semantic(query)` und `search_memory_exact(keyword)` werden den Agent-Tools hinzugefügt, sodass er selbstständig in seiner Historie suchen kann.
