# 📚 SAP Build Quiz - C_LCNC_2406

App interattiva web per memorizzare le 60 domande del quiz SAP Build C_LCNC_2406.

## 🚀 Demo Online

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## ✨ Funzionalità

- ✅ **Tema scuro moderno** - Interfaccia elegante e confortevole per gli occhi
- ✅ **Design responsive** - Ottimizzato per mobile, tablet e desktop
- ✅ **Due modalità di studio**:
  - 📋 Ordine normale (sequenziale)
  - 🎲 Ordine casuale (per una sfida maggiore)
- ✅ **Tecniche di memoria** - Aiuto per memorizzare ogni risposta
- ✅ **Score tracking intelligente** - Non conta doppio se rispondi correttamente più volte
- ✅ **Navigazione completa** - Vai avanti e indietro tra le domande
- ✅ **Salvataggio automatico** - Le tue risposte vengono salvate durante la sessione

## 📱 Come Usare

### Versione Web (Consigliata)
1. Apri il link dell'app online nel browser
2. Funziona su iPhone, Android, tablet e desktop
3. Non richiede installazione

### Versione Desktop (macOS)
1. Fai doppio clic su `Avvia Quiz.command`
2. Oppure esegui: `python3.11 sap_quiz_app.py`

## 🛠️ Installazione Locale

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'app web
streamlit run sap_quiz_web.py

# Oppure avvia l'app desktop
python3.11 sap_quiz_app.py
```

## 📂 Struttura File

- `sap_quiz_web.py` - App web Streamlit (per deploy online)
- `sap_quiz_app.py` - App desktop Tkinter (per macOS/Windows/Linux)
- `sap_quiz_data.json` - Database delle 60 domande
- `requirements.txt` - Dipendenze Python

## 🌐 Deploy Online

Vedi `DEPLOY_GUIDE.md` per istruzioni dettagliate su come pubblicare l'app online.

**Opzioni consigliate:**
- [Streamlit Cloud](https://streamlit.io/cloud) - Gratuito, più semplice
- [Render](https://render.com) - Gratuito, supporta repo privati
- [Heroku](https://heroku.com) - Alternativa popolare

## 📝 Note

- L'app web funziona completamente nel browser
- I dati vengono salvati nella sessione del browser
- Compatibile con tutti i dispositivi moderni

## 📄 Licenza

Uso personale per preparazione esame SAP Build C_LCNC_2406.

