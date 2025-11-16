# SAP Build Quiz - Web App

App web interattiva per memorizzare le 60 domande del quiz SAP Build C_LCNC_2406.

## 🚀 Installazione

1. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## 📱 Esecuzione

Per avviare l'app web:

```bash
streamlit run sap_quiz_web.py
```

L'app si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

## 📲 Accesso da iPhone

### Opzione 1: Rete Locale
1. Assicurati che iPhone e computer siano sulla stessa rete WiFi
2. Avvia l'app con:
```bash
streamlit run sap_quiz_web.py --server.address 0.0.0.0
```
3. Trova l'indirizzo IP del tuo computer:
   - Mac: `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - Windows: `ipconfig`
4. Sul tuo iPhone, apri Safari e vai a: `http://TUO_IP:8501`

### Opzione 2: Deploy Online (Consigliato)
Per rendere l'app accessibile da qualsiasi dispositivo:

1. **Streamlit Cloud** (Gratuito):
   - Vai su https://streamlit.io/cloud
   - Connetti il tuo repository GitHub
   - Deploy automatico!

2. **Heroku**:
   - Crea un account su Heroku
   - Installa Heroku CLI
   - Deploy con: `heroku create` e `git push heroku main`

3. **Render**:
   - Vai su https://render.com
   - Crea un nuovo Web Service
   - Connetti il repository e deploy

## ✨ Funzionalità

- ✅ Tema scuro moderno
- ✅ Design responsive (ottimizzato per mobile)
- ✅ Quiz in ordine normale o casuale
- ✅ Tecniche di memoria per ogni domanda
- ✅ Tracking dello score intelligente
- ✅ Navigazione avanti/indietro tra le domande
- ✅ Salvataggio automatico delle risposte

## 📝 Note

- L'app funziona completamente nel browser
- Non richiede installazione su iPhone
- I dati vengono salvati nella sessione del browser
- Funziona offline dopo il primo caricamento (se configurato come PWA)

