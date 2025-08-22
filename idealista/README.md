# 🏠 Integrazione Idealista

Questa cartella contiene tutti i file relativi all'integrazione con l'API di Idealista per RoomRadar.

## 📁 Struttura

```
idealista/
├── README.md                    # Questo file
├── idealista_module.py          # Modulo Python per l'API Idealista
├── populate_idealista.py        # Script per popolare il database
├── fetch_idealista.js           # Script Node.js per esportare i dati
└── .github/workflows/           # Workflow GitHub Actions
    ├── idealista-populate.yml   # Popolamento giornaliero
    └── idealista-export.yml     # Esportazione ogni 6 ore
```

## 🔧 Configurazione

### Variabili d'Ambiente Richieste

```bash
# Nuove variabili per Idealista
IDEALISTA_API_KEY=your_api_key_here
IDEALISTA_API_SECRET=your_api_secret_here
IDEALISTA_NOTION_DATABASE_ID=your_database_id_here

# Variabile esistente (già presente nel sistema)
NOTION_API_KEY=your_notion_api_key_here
```

### Database Notion Schema

```
Database: "Idealista Listings Barcelona"
Properties:
- property_code (Text, unique)
- title (Title)
- description (Rich text)
- price (Number)
- rooms (Number)
- bathrooms (Number)
- size (Number)
- address (Rich text)
- district (Select)
- neighborhood (Rich text)
- municipality (Rich text)
- province (Rich text)
- latitude (Number)
- longitude (Number)
- url (URL)
- thumbnail (URL)
- status (Select: active/expired)
- new_development (Checkbox)
- publication_date (Date)
- last_seen (Date)
- source (Select: "Idealista")
```

## 🚀 Utilizzo

### Popolamento Database
```bash
cd idealista
python populate_idealista.py
```

### Esportazione Dati
```bash
cd idealista
node fetch_idealista.js
```

## 📊 Rate Limits

- **25 richieste API al mese** (1250 camere totali)
- **Popolamento**: 1 richiesta/giorno
- **Esportazione**: ogni 6 ore

## 🔄 Workflow

1. **Popolamento**: Ogni giorno alle 8:00 UTC
2. **Esportazione**: Ogni 6 ore + dopo popolamento
3. **Deploy**: Automatico su GitHub Pages

## 📈 Statistiche

- Fonte complementare a Facebook
- Dati strutturati e completi
- Prezzi di mercato affidabili
- Informazioni dettagliate (stanze, bagni, metratura)
