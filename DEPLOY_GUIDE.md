# 🚀 Guida al Deploy Online - Streamlit Cloud

## Metodo 1: Streamlit Cloud (Consigliato - Gratuito)

### Passo 1: Crea un account GitHub
1. Vai su https://github.com e crea un account (se non ce l'hai)
2. È completamente gratuito

### Passo 2: Crea un nuovo repository
1. Clicca su "New repository" (o vai su https://github.com/new)
2. Nome repository: `sap-quiz-app` (o qualsiasi nome tu preferisca)
3. Seleziona **Public** (Streamlit Cloud richiede repository pubblici per il piano gratuito)
4. **NON** inizializzare con README, .gitignore o licenza
5. Clicca "Create repository"

### Passo 3: Carica i file su GitHub

**Opzione A - Usando GitHub Desktop (Più facile):**
1. Scarica GitHub Desktop: https://desktop.github.com
2. Installa e accedi con il tuo account
3. File → Add Local Repository
4. Scegli la cartella "SAP NCLC"
5. Inserisci un messaggio di commit (es: "Initial commit")
6. Clicca "Commit to main"
7. Clicca "Publish repository"

**Opzione B - Usando Git da terminale:**
```bash
cd "/Users/Massimiliano/Desktop/SAP NCLC"

# Inizializza git (se non già fatto)
git init

# Aggiungi tutti i file
git add .

# Crea il primo commit
git commit -m "Initial commit - SAP Quiz Web App"

# Aggiungi il repository remoto (sostituisci USERNAME con il tuo username GitHub)
git remote add origin https://github.com/USERNAME/sap-quiz-app.git

# Carica i file
git branch -M main
git push -u origin main
```

### Passo 4: Deploy su Streamlit Cloud
1. Vai su https://streamlit.io/cloud
2. Clicca "Sign up" e accedi con il tuo account GitHub
3. Clicca "New app"
4. Seleziona il repository `sap-quiz-app`
5. Seleziona il branch `main`
6. Main file path: `sap_quiz_web.py`
7. Clicca "Deploy!"

### Passo 5: La tua app è online! 🎉
Streamlit Cloud ti darà un URL tipo: `https://sap-quiz-app.streamlit.app`

**Condividi questo link con chiunque - funziona su iPhone, Android, desktop!**

---

## Metodo 2: Render (Alternativa Gratuita)

### Passo 1: Crea account su Render
1. Vai su https://render.com
2. Clicca "Get Started for Free"
3. Accedi con GitHub

### Passo 2: Crea un Web Service
1. Clicca "New +" → "Web Service"
2. Connetti il repository GitHub
3. Configurazione:
   - **Name**: `sap-quiz-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run sap_quiz_web.py --server.port $PORT --server.address 0.0.0.0`
4. Clicca "Create Web Service"

### Passo 3: Attendi il deploy
Render impiegherà qualche minuto per buildare e deployare l'app.

---

## Metodo 3: Heroku (Alternativa)

### Passo 1: Installa Heroku CLI
```bash
# Mac
brew tap heroku/brew && brew install heroku

# Oppure scarica da: https://devcenter.heroku.com/articles/heroku-cli
```

### Passo 2: Crea Procfile
Crea un file chiamato `Procfile` (senza estensione) nella cartella:
```
web: streamlit run sap_quiz_web.py --server.port=$PORT --server.address=0.0.0.0
```

### Passo 3: Setup Heroku
```bash
cd "/Users/Massimiliano/Desktop/SAP NCLC"

# Login
heroku login

# Crea app
heroku create sap-quiz-app

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

---

## 📝 File necessari per il deploy

Assicurati di avere questi file nel repository:
- ✅ `sap_quiz_web.py` (app principale)
- ✅ `sap_quiz_data.json` (dati del quiz)
- ✅ `requirements.txt` (dipendenze)
- ✅ `README.md` (opzionale ma consigliato)

---

## 🔒 Privacy e Sicurezza

- **Streamlit Cloud (piano gratuito)**: Richiede repository pubblici
- **Render**: Supporta repository privati anche nel piano gratuito
- **Heroku**: Supporta repository privati

Se hai dati sensibili, usa Render o Heroku con repository privato.

---

## 🆘 Problemi Comuni

### L'app non trova `sap_quiz_data.json`
Assicurati che il file sia nel repository e nella stessa directory di `sap_quiz_web.py`

### Errore "Module not found"
Verifica che `requirements.txt` contenga tutte le dipendenze necessarie

### L'app si carica ma è vuota
Controlla i log su Streamlit Cloud per vedere eventuali errori

---

## 💡 Suggerimenti

1. **Streamlit Cloud** è la scelta più semplice per iniziare
2. Il deploy è automatico: ogni push su GitHub aggiorna l'app
3. L'app è accessibile 24/7 da qualsiasi dispositivo
4. Puoi condividere il link con chiunque

