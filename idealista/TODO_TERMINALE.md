# 📋 TODO COMPLETO - Terminale (Da Zero)

## 🚨 ATTENZIONE: Tutte queste cose devi farle TU manualmente!

### **1. 🏗️ Setup Iniziale (Terminale)**

```bash
# Vai nella directory del progetto
cd /Users/andrea/Documents/GitHub/notion-rss-bot

# Verifica che sei nella directory giusta
pwd
# Dovrebbe mostrare: /Users/andrea/Documents/GitHub/notion-rss-bot

# Verifica lo stato del repository
git status
```

### **2. 🏗️ Branch V2 (Terminale)**

```bash
# Crea e passa al branch V2
git checkout -b V2

# Verifica che sei sul branch giusto
git branch
# Dovrebbe mostrare: * V2

# Push del branch su GitHub
git push -u origin V2
```

### **3. 🗄️ Database Notion Idealista**

**Fai questo manualmente su Notion:**

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

### **4. 🔑 GitHub Secrets (Terminale)**

**Fai questo manualmente su GitHub:**

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

### **5. 📁 Spostare Workflow (Terminale)**

```bash
# Assicurati di essere sul branch V2
git checkout V2

# Crea la directory workflows se non esiste
mkdir -p .github/workflows

# Copia i workflow dalla cartella idealista
cp idealista/.github/workflows/* .github/workflows/

# Verifica che siano stati copiati
ls -la .github/workflows/idealista-*.yml
# Dovrebbe mostrare:
# idealista-export.yml
# idealista-populate.yml
```

### **6. 🧪 Test Locale (Terminale)**

```bash
# Vai nella cartella idealista
cd idealista

# Test API Tracker
python3 api_tracker.py

# Test Modulo Idealista (solo se hai configurato i secrets)
python3 populate_idealista.py

# Test Esportazione (solo se hai configurato i secrets)
node fetch_idealista.js

# Torna alla root
cd ..
```

### **7. 🌐 Test Frontend (Terminale)**

```bash
# Apri il frontend nel browser
open index.html

# Oppure se hai un server locale
python3 -m http.server 8000
# Poi vai su http://localhost:8000
```

### **8. 🔄 Commit e Push (Terminale)**

```bash
# Aggiungi tutti i file
git add .

# Commit delle modifiche
git commit -m "feat: Integrazione Idealista V2 completa"

# Push su GitHub
git push origin V2
```

### **9. 🧪 Test Workflow (Terminale)**

```bash
# Verifica che i workflow siano attivi
# Vai su GitHub → Actions e controlla che appaiano:
# - idealista-populate.yml
# - idealista-export.yml

# Oppure usa GitHub CLI se lo hai installato
gh workflow list
```

### **10. 📊 Verificare API Tracker (Terminale)**

```bash
# Vai nella cartella idealista
cd idealista

# Verifica che il file tracker esista
ls -la idealista_api_tracker.json

# Mostra il contenuto
cat idealista_api_tracker.json

# Mostra lo status
python3 api_tracker.py
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

### **Se non funziona:**

#### **"Missing environment variables"**
```bash
# Verifica che i secrets siano configurati
echo $IDEALISTA_API_KEY
echo $IDEALISTA_API_SECRET
echo $IDEALISTA_NOTION_DATABASE_ID
echo $NOTION_API_KEY  # Già presente nel sistema esistente
```

#### **"Cannot make API call"**
```bash
# Controlla il tracker
cd idealista
cat idealista_api_tracker.json
python3 api_tracker.py
```

#### **"Database not found"**
- Verifica ID database Notion
- Controlla permessi API Notion
- Verifica integrazione database

#### **"Workflow not found"**
```bash
# Verifica che i workflow siano nella posizione giusta
ls -la .github/workflows/idealista-*.yml
```

## ✅ Checklist Completamento

- [ ] Branch V2 creato e attivo
- [ ] Database Notion creato e configurato
- [ ] GitHub Secrets aggiunti (3 nuovi)
- [ ] Workflow spostati
- [ ] Test locale eseguiti
- [ ] Frontend testato
- [ ] Commit e push completati
- [ ] Workflow attivati
- [ ] API Tracker funzionante

## 🎉 Quando tutto funziona:

```bash
# Crea Pull Request
gh pr create --title "feat: Integrazione Idealista V2" --body "Integrazione completa Idealista con Mix Control Panel e filtri condizionali"

# Oppure vai su GitHub e crea manualmente la PR
# GitHub → Pull requests → New pull request
# Base: main ← Compare: V2
```

## 📞 Supporto

Se hai problemi:
1. Controlla la checklist sopra
2. Verifica i log di errore
3. Controlla `idealista/VERIFICATION_CHECKLIST.md`
4. Testa ogni componente separatamente

**Buona fortuna! 🚀**
