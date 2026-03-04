# Nutze ein leichtgewichtiges Python-Image (Stand 2025)
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# System-Abhängigkeiten für Audio-Support (optional für Web)
RUN apt-get update && apt-get install -y mpv libnotify-bin && rm -rf /var/lib/apt/lists/*

# Kopiere die Anforderungen und installiere sie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Codes
COPY . .

# Flask-Port freigeben
EXPOSE 5000

# Starte die Web-App (bindet an 0.0.0.0 für externen Zugriff)
CMD ["python", "web_app.py"]
