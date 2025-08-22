# 🚀 Setup Branch V2 - Integrazione Idealista

## 📋 Checklist Manuale

### **1. Creare Branch V2**
```bash
git checkout -b V2
```

### **2. Database Notion Idealista**
Crea un nuovo database in Notion con nome **"Idealista Listings Barcelona"** e queste proprietà:

| Property | Type | Description |
|----------|------|-------------|
| property_code | Text | Unique identifier (Idealista propertyCode) |
| title | Title | Property title |
| description | Rich text | Full description |
| price | Number | Monthly rent in € |
| rooms | Number | Number of rooms |
| bathrooms | Number | Number of bathrooms |
| size | Number | Size in m² |
| address | Rich text | Full address |
| district | Select | Barcelona district |
| neighborhood | Rich text | Specific neighborhood |
| municipality | Rich text | Municipality |
| province | Rich text | Province |
| latitude | Number | GPS coordinates |
| longitude | Number | GPS coordinates |
| url | URL | Idealista listing URL |
| thumbnail | URL | Main image URL |
| status | Select | Values: "active", "expired" |
| new_development | Checkbox | Is it new development |
| publication_date | Date | When published on Idealista |
| last_seen | Date | Last time we saw this listing |
| source | Select | Value: "Idealista" |

### **3. GitHub Secrets**
Vai su GitHub → Settings → Secrets and variables → Actions e aggiungi:

```
IDEALISTA_API_KEY=your_api_key_here
IDEALISTA_API_SECRET=your_api_secret_here
IDEALISTA_NOTION_DATABASE_ID=your_new_database_id_here
```

### **4. Spostare Workflow**
```bash
cp idealista/.github/workflows/* .github/workflows/
```

### **5. Test Locale**
```bash
# Test popolamento
cd idealista
python populate_idealista.py

# Test esportazione
node fetch_idealista.js
```

## 🎯 Funzionalità V2

### **Mix Control Panel**
- **Balanced Mix**: 70% Facebook, 30% Idealista
- **Facebook Only**: Solo annunci Facebook
- **Idealista Only**: Solo annunci Idealista  
- **Custom Mix**: Slider personalizzabile 0-100%

### **Filtri Avanzati**
- **Filtri Facebook**: Zone, Prezzo, Data, Affidabilità
- **Filtri Idealista**: + Stanze, Bagni, Metratura
- **Filtri Condizionali**: Si mostrano solo quando rilevanti

### **UI/UX Migliorata**
- Badge sorgente (📌 Facebook, 🏠 Idealista)
- Statistiche in tempo reale
- Mix control intuitivo
- Filtri dinamici

## 🔄 Workflow

### **Popolamento**
- **Frequenza**: Ogni giorno alle 8:00 UTC
- **Limite**: 1-2 richieste/giorno (50/mese)
- **Dati**: 50 annunci più recenti

### **Esportazione**
- **Frequenza**: Ogni 6 ore + dopo popolamento
- **Output**: `public/data-idealista.json`
- **Deploy**: Automatico su GitHub Pages

## 📊 Rate Limits

- **25 richieste API al mese** (1250 camere totali)
- **Popolamento controllato**: 1/giorno
- **Esportazione frequente**: ogni 6 ore

## 🧪 Testing

### **Test Frontend**
1. Apri `index.html` nel browser
2. Verifica il Mix Control Panel
3. Testa i filtri condizionali
4. Controlla le statistiche

### **Test Backend**
1. Verifica autenticazione OAuth2
2. Testa fetch listings
3. Controlla salvataggio Notion
4. Verifica esportazione JSON

## 🚨 Troubleshooting

### **Errori Comuni**
- **Missing secrets**: Verifica GitHub Secrets
- **Database ID errato**: Controlla ID database Notion
- **Rate limit**: Aspetta 24h tra le esecuzioni
- **CORS errors**: Verifica path file JSON

### **Debug**
```bash
# Log dettagliati
python populate_idealista.py --debug

# Verifica workflow
gh run list --workflow=idealista-populate.yml
```

## ✅ Checklist Completamento

- [ ] Branch v2 creato
- [ ] Database Notion configurato
- [ ] GitHub Secrets aggiunti
- [ ] Workflow spostati
- [ ] Test locale eseguiti
- [ ] Frontend testato
- [ ] Workflow attivati
- [ ] Deploy verificato
