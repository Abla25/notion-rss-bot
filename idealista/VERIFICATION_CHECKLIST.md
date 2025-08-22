# ✅ VERIFICATION CHECKLIST - Integrazione Idealista V2

## 🔍 Verifica Struttura File

### **File Creati**
- [ ] `idealista/idealista_module.py` - Modulo principale API
- [ ] `idealista/populate_idealista.py` - Script popolamento
- [ ] `idealista/fetch_idealista.js` - Script esportazione
- [ ] `idealista/api_tracker.py` - Sistema tracking chiamate
- [ ] `idealista/.github/workflows/idealista-populate.yml` - Workflow popolamento
- [ ] `idealista/.github/workflows/idealista-export.yml` - Workflow esportazione
- [ ] `idealista/README.md` - Documentazione
- [ ] `idealista/V2_SETUP.md` - Setup branch V2
- [ ] `idealista/VERIFICATION_CHECKLIST.md` - Questo file

### **File Modificati**
- [ ] `index.html` - Frontend con Mix Control Panel e filtri condizionali

## 🧪 Test Locale

### **1. Test API Tracker**
```bash
cd idealista
python api_tracker.py
```
**Risultato atteso**: Status del tracker e test chiamate

### **2. Test Modulo Idealista**
```bash
cd idealista
python populate_idealista.py
```
**Risultato atteso**: 
- Status tracker
- Controllo rate limit
- Fetch listings (se possibile)
- Salvataggio Notion

### **3. Test Esportazione**
```bash
cd idealista
node fetch_idealista.js
```
**Risultato atteso**: 
- Lettura database Notion
- Creazione `public/data-idealista.json`

### **4. Test Frontend**
```bash
# Apri index.html nel browser
open index.html
```
**Risultato atteso**:
- Mix Control Panel visibile
- Filtri condizionali funzionanti
- Caricamento dati Facebook + Idealista
- Statistiche corrette

## 🔧 Configurazione Manuale

### **1. Branch V2**
```bash
git checkout V2
```

### **2. Database Notion**
- [ ] Database "Idealista Listings Barcelona" creato
- [ ] Tutte le proprietà configurate correttamente
- [ ] ID database copiato

### **3. GitHub Secrets**
- [ ] `IDEALISTA_API_KEY` aggiunto (NUOVO)
- [ ] `IDEALISTA_API_SECRET` aggiunto (NUOVO)
- [ ] `IDEALISTA_NOTION_DATABASE_ID` aggiunto (NUOVO)
- [ ] `NOTION_API_KEY` già presente (NON serve aggiungere)

### **4. Workflow**
```bash
cp idealista/.github/workflows/* .github/workflows/
```

## 🎯 Funzionalità da Verificare

### **Mix Control Panel**
- [ ] **Balanced Mix**: 70% Facebook, 30% Idealista
- [ ] **Facebook Only**: Solo annunci Facebook
- [ ] **Idealista Only**: Solo annunci Idealista
- [ ] **Custom Mix**: Slider 0-100% funzionante
- [ ] **Statistiche**: Conteggi aggiornati in tempo reale

### **Filtri Condizionali**
- [ ] **Filtri Facebook**: Zone, Prezzo, Data, Affidabilità
- [ ] **Filtri Idealista**: Stanze, Bagni, Metratura
- [ ] **Mostra/Nascondi**: Filtri Idealista solo quando rilevanti
- [ ] **Gestione**: Include, rimuovi, cancella tutti

### **API Tracker**
- [ ] **Contatore chiamate**: Aggiornamento automatico
- [ ] **Rate limit**: Controllo 1/giorno, 25/mese
- [ ] **Rate limiting**: 1 richiesta ogni 3 secondi
- [ ] **File JSON**: `idealista_api_tracker.json` creato
- [ ] **Status**: Visualizzazione chiara

## 🚨 Troubleshooting

### **Errori Comuni**

#### **"Missing environment variables"**
```bash
# Verifica variabili
echo $IDEALISTA_API_KEY
echo $IDEALISTA_API_SECRET
echo $IDEALISTA_NOTION_DATABASE_ID
```

#### **"Cannot make API call"**
- Controlla `idealista_api_tracker.json`
- Verifica rate limit (2/giorno, 50/mese)
- Aspetta 24h se necessario

#### **"Database not found"**
- Verifica ID database Notion
- Controlla permessi API Notion
- Verifica integrazione database

#### **"CORS errors"**
- Verifica path `public/data-idealista.json`
- Controlla server locale
- Verifica struttura JSON

### **Debug Commands**
```bash
# Status tracker
cd idealista && python -c "from api_tracker import APITracker; APITracker().print_status()"

# Test modulo
cd idealista && python -c "from idealista_module import IdealistaAPI; api = IdealistaAPI(); print('✅ Module loaded')"

# Verifica workflow
ls -la .github/workflows/idealista-*.yml
```

## 📊 Metriche di Successo

### **Backend**
- [ ] API tracker funzionante
- [ ] Rate limit rispettato
- [ ] Database popolato
- [ ] JSON esportato

### **Frontend**
- [ ] Mix control responsive
- [ ] Filtri condizionali
- [ ] Statistiche accurate
- [ ] UX fluida

### **Workflow**
- [ ] Popolamento giornaliero
- [ ] Esportazione ogni 6h
- [ ] Deploy automatico
- [ ] Log completi

## ✅ Checklist Finale

- [ ] Tutti i test passano
- [ ] Configurazione completa
- [ ] Frontend funzionante
- [ ] Backend operativo
- [ ] Workflow attivi
- [ ] Documentazione aggiornata
- [ ] Branch V2 pronto per merge

## 🎉 Deployment

```bash
# Commit e push
git add .
git commit -m "feat: Integrazione Idealista V2 completa"
git push origin V2

# Merge in main (quando pronto)
git checkout main
git merge V2
git push origin main
```
