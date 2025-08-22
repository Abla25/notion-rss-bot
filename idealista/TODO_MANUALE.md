# 📋 TODO MANUALE - Integrazione Idealista V2

## 🚨 ATTENZIONE: Tutte queste cose devi farle TU manualmente!

### **1. 🏗️ Setup Branch V2**
```bash
# Assicurati di essere sul branch V2 (con la maiuscola)
git checkout V2

# Verifica che sei sul branch giusto
git branch
# Dovrebbe mostrare: * V2
```

### **2. 🗄️ Database Notion Idealista**
**Crea un nuovo database in Notion con nome "Idealista Listings Barcelona"**

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

**⚠️ IMPORTANTE**: Copia l'ID del database (dalla URL di Notion)

### **3. 🔑 GitHub Secrets**
**Vai su GitHub → Settings → Secrets and variables → Actions**

Aggiungi questi 3 secrets **NUOVI**:

```
IDEALISTA_API_KEY=your_api_key_here
IDEALISTA_API_SECRET=your_api_secret_here  
IDEALISTA_NOTION_DATABASE_ID=your_database_id_here
```

**⚠️ IMPORTANTE**: 
- Sostituisci `your_api_key_here` con la tua API key di Idealista
- Sostituisci `your_api_secret_here` con il tuo API secret di Idealista
- Sostituisci `your_database_id_here` con l'ID del database Notion
- **NOTION_API_KEY**: Già presente, non serve aggiungerla di nuovo!

### **4. 📁 Spostare Workflow**
```bash
# Dalla root del progetto
cp idealista/.github/workflows/* .github/workflows/

# Verifica che siano stati copiati
ls -la .github/workflows/idealista-*.yml
```

### **5. 🧪 Test Locale**
```bash
# Test API Tracker
cd idealista
python3 api_tracker.py

# Test Modulo Idealista (solo se hai configurato i secrets)
python3 populate_idealista.py

# Test Esportazione (solo se hai configurato i secrets)
node fetch_idealista.js
```

### **6. 🌐 Test Frontend**
```bash
# Dalla root del progetto
open index.html
```

**Verifica che funzioni:**
- [ ] Mix Control Panel visibile
- [ ] Filtri condizionali funzionanti
- [ ] Caricamento dati Facebook + Idealista
- [ ] Statistiche corrette

### **7. 🔄 Attivare Workflow**
**Vai su GitHub → Actions**

Verifica che i workflow siano attivi:
- `idealista-populate.yml` (popolamento giornaliero)
- `idealista-export.yml` (esportazione ogni 6 ore)

### **8. 📊 Verificare API Tracker**
Il sistema di tracking creerà automaticamente:
- `idealista/idealista_api_tracker.json` - File con contatori
- Controllo rate limit: 2 chiamate/giorno, 50/mese
- Status visibile quando esegui `python3 api_tracker.py`

## 🎯 Funzionalità Implementate

### **✅ Mix Control Panel**
- **Balanced Mix**: 70% Facebook, 30% Idealista
- **Facebook Only**: Solo annunci Facebook
- **Idealista Only**: Solo annunci Idealista
- **Custom Mix**: Slider 0-100% personalizzabile

### **✅ Filtri Condizionali**
- **Filtri Facebook**: Zone, Prezzo, Data, Affidabilità
- **Filtri Idealista**: + Stanze, Bagni, Metratura
- **Mostra/Nascondi**: Filtri Idealista solo quando rilevanti

### **✅ API Tracker**
- **Contatore chiamate**: Aggiornamento automatico
- **Rate limit**: Controllo 1/giorno, 25/mese
- **Rate limiting**: 1 richiesta ogni 3 secondi
- **File JSON**: `idealista_api_tracker.json`
- **Status**: Visualizzazione chiara

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
- Controlla `idealista/idealista_api_tracker.json`
- Verifica rate limit (1/giorno, 25/mese)
- Aspetta 24h se necessario

#### **"Database not found"**
- Verifica ID database Notion
- Controlla permessi API Notion
- Verifica integrazione database

## ✅ Checklist Completamento

- [ ] Branch V2 attivo
- [ ] Database Notion creato e configurato
- [ ] GitHub Secrets aggiunti
- [ ] Workflow spostati
- [ ] Test locale eseguiti
- [ ] Frontend testato
- [ ] Workflow attivati
- [ ] API Tracker funzionante

## 🎉 Quando tutto funziona:

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

## 📞 Supporto

Se qualcosa non funziona:
1. Controlla la checklist sopra
2. Verifica i log di errore
3. Controlla `idealista/VERIFICATION_CHECKLIST.md`
4. Testa ogni componente separatamente

**Buona fortuna! 🚀**
