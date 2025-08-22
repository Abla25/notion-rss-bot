# 📋 TODO COMPLETO - GitHub Web (Senza Terminale)

## 🚨 ATTENZIONE: Tutte queste cose devi farle TU manualmente!

### **1. 🏗️ Branch V2 (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Clicca su "main"** (dropdown in alto a sinistra)
3. **Clicca "View all branches"**
4. **Clicca "New branch"**
5. **Nome branch**: `V2` (con la maiuscola)
6. **Clicca "Create branch"**

### **2. 🗄️ Database Notion Idealista**

1. **Vai su Notion** → Crea nuovo database
2. **Nome**: "Idealista Listings Barcelona"
3. **Aggiungi queste 21 proprietà**:

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| property_code | Text | Unique identifier | ✅ |
| title | Title | Property title | ✅ |
| description | Rich text | Full description | ✅ |
| price | Number | Monthly rent in € | ✅ |
| rooms | Number | Number of rooms | ✅ |
| bathrooms | Number | Number of bathrooms | ✅ |
| size | Number | Size in m² | ✅ |
| address | Rich text | Full address | ✅ |
| district | Select | Barcelona district | ✅ |
| neighborhood | Rich text | Specific neighborhood | ✅ |
| municipality | Rich text | Municipality | ✅ |
| province | Rich text | Province | ✅ |
| latitude | Number | GPS coordinates | ✅ |
| longitude | Number | GPS coordinates | ✅ |
| url | URL | Idealista listing URL | ✅ |
| thumbnail | URL | Main image URL | ✅ |
| status | Select | Values: "active", "expired" | ✅ |
| new_development | Checkbox | Is it new development | ✅ |
| publication_date | Date | When published on Idealista | ✅ |
| last_seen | Date | Last time we saw this listing | ✅ |
| source | Select | Value: "Idealista" | ✅ |

4. **Copia l'ID del database** dalla URL di Notion

### **3. 🔑 GitHub Secrets (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Clicca "Settings"** (tab in alto)
3. **Clicca "Secrets and variables"** → **"Actions"**
4. **Clicca "New repository secret"**
5. **Aggiungi questi 3 secrets NUOVI**:

```
Name: IDEALISTA_API_KEY
Value: your_api_key_here

Name: IDEALISTA_API_SECRET  
Value: your_api_secret_here

Name: IDEALISTA_NOTION_DATABASE_ID
Value: your_database_id_here
```

**⚠️ IMPORTANTE**: 
- Sostituisci i valori con quelli reali
- **NOTION_API_KEY**: Già presente, non serve aggiungerla!

### **4. 📁 Spostare Workflow (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Vai su branch V2** (dropdown in alto)
3. **Clicca su cartella `.github/workflows/`**
4. **Clicca "Add file"** → **"Upload files"**
5. **Carica questi 2 file** dalla cartella `idealista/.github/workflows/`:
   - `idealista-populate.yml`
   - `idealista-export.yml`

### **5. 🧪 Test Locale (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Vai su branch V2**
3. **Clicca "Actions"** (tab in alto)
4. **Clicca su workflow "Populate Idealista Database"**
5. **Clicca "Run workflow"** → **"Run workflow"**
6. **Ripeti per "Export Idealista Data"**

### **6. 🌐 Test Frontend (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Vai su branch V2**
3. **Clicca su file `index.html`**
4. **Clicca "Raw"** (pulsante in alto a destra)
5. **Copia l'URL** e aprilo nel browser
6. **Verifica che funzioni**:
   - [ ] Mix Control Panel visibile
   - [ ] Filtri condizionali funzionanti
   - [ ] Caricamento dati Facebook + Idealista
   - [ ] Statistiche corrette

### **7. 🔄 Attivare Workflow (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Clicca "Actions"** (tab in alto)
3. **Verifica che i workflow siano attivi**:
   - `idealista-populate.yml` (popolamento giornaliero)
   - `idealista-export.yml` (esportazione ogni 6 ore)

### **8. 📊 Verificare API Tracker (GitHub Web)**

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Vai su branch V2**
3. **Clicca su cartella `idealista/`**
4. **Verifica che esista** `idealista_api_tracker.json`
5. **Clicca sul file** per vedere i contatori

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

### **Se non funziona:**

#### **"Missing environment variables"**
- Verifica che i 3 secrets siano configurati correttamente
- Controlla che i nomi siano esatti (maiuscole/minuscole)

#### **"Cannot make API call"**
- Controlla `idealista/idealista_api_tracker.json`
- Verifica rate limit (1/giorno, 25/mese)
- Aspetta 24h se necessario

#### **"Database not found"**
- Verifica ID database Notion
- Controlla permessi API Notion
- Verifica integrazione database

#### **"Workflow not found"**
- Verifica che i file siano nella cartella `.github/workflows/`
- Controlla che siano sul branch V2
- Verifica sintassi YAML

## ✅ Checklist Completamento

- [ ] Branch V2 creato su GitHub
- [ ] Database Notion creato e configurato
- [ ] GitHub Secrets aggiunti (3 nuovi)
- [ ] Workflow spostati su GitHub
- [ ] Test workflow eseguiti
- [ ] Frontend testato
- [ ] Workflow attivati
- [ ] API Tracker funzionante

## 🎉 Quando tutto funziona:

1. **Vai su GitHub** → Il tuo repository `notion-rss-bot`
2. **Vai su branch V2**
3. **Clicca "Pull requests"**
4. **Clicca "New pull request"**
5. **Base: main** ← **Compare: V2**
6. **Clicca "Create pull request"**
7. **Clicca "Merge pull request"**

## 📞 Supporto

Se hai problemi:
1. Controlla la checklist sopra
2. Verifica i log di errore in Actions
3. Controlla `idealista/VERIFICATION_CHECKLIST.md`
4. Testa ogni componente separatamente

**Buona fortuna! 🚀**
