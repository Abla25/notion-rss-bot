#!/usr/bin/env python3
"""
Script per popolare gradualmente il database Idealista
Rispetta i limiti: 25 richieste/mese = ~1 richiesta/giorno
"""

import os
import time
from datetime import datetime, timedelta
from idealista_module import IdealistaAPI

def main():
    print("🏠 Starting Idealista database population...")
    
    # TESTING MODE: Skip API calls
    print("🧪 TESTING MODE: Skipping API calls to avoid rate limits")
    print("📊 Using existing database data only")
    return
    
    try:
        api = IdealistaAPI()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Mostra stato del tracker
    print("\n📊 API Tracker Status:")
    api.api_tracker.print_status()
    print()
    
    # Controlla se è il momento di aggiornare (1 volta al giorno)
    today = datetime.now().date()
    print(f"📅 Starting Idealista update for {today}")
    
    # Controllo giornaliero esplicito
    last_update_file = "last_idealista_update.txt"
    if os.path.exists(last_update_file):
        with open(last_update_file, 'r') as f:
            last_update_str = f.read().strip()
            try:
                last_update = datetime.fromisoformat(last_update_str).date()
                if today == last_update:
                    print("✅ Already updated today, skipping...")
                    return
            except ValueError:
                print("⚠️ Invalid last update timestamp, proceeding...")
    
    print("🔄 Proceeding with daily update...")
    
    # Ottimizzazione: controlla prima quali annunci esistono già
    print("🔍 Checking existing listings to avoid duplicates...")
    existing_codes = api.get_existing_property_codes()
    print(f"📊 Found {len(existing_codes)} existing listings in database")
    
    # Fetch con esclusione di annunci esistenti
    print("📡 Fetching new listings (excluding existing ones)...")
    all_listings = []
    page = 1
    max_pages = 1  # Solo 1 pagina per rispettare limiti API (50 annunci)
    
    while page <= max_pages:
        listings = api.fetch_listings(page=page, max_items=50, exclude_codes=existing_codes)
        if not listings:
            break
            
        # Filtra i risultati per escludere annunci esistenti
        new_listings = []
        for listing in listings:
            property_code = listing.get("propertyCode", "")
            if property_code and property_code not in existing_codes:
                new_listings.append(listing)
        
        all_listings.extend(new_listings)
        print(f"📄 Page {page}: {len(listings)} fetched, {len(new_listings)} new")
        
        # Se non ci sono nuovi annunci in questa pagina, possiamo fermarci
        if len(new_listings) == 0:
            print("🛑 No new listings in this page, stopping pagination")
            break
        
        # Se riceviamo meno di 50 risultati, abbiamo finito
        if len(listings) < 50:
            break
            
        page += 1
        
        # Piccola pausa tra le pagine per rispettare rate limits
        if page <= max_pages:
            time.sleep(3)
    
    print(f"📊 Total new listings found: {len(all_listings)}")
    
    if not all_listings:
        print("✅ No new listings found")
        # Salva comunque il timestamp per evitare riprove
        with open(last_update_file, 'w') as f:
            f.write(datetime.now().isoformat())
        return
    
    # Processa e salva solo i nuovi
    created_count = 0
    
    for i, listing in enumerate(all_listings, 1):
        property_code = listing.get("propertyCode", "")
        title = listing.get("title", "")[:50]
        
        print(f"📝 Processing {i}/{len(all_listings)}: {title}...")
        
        if property_code:
            # Salva in Notion (dovrebbe essere sempre nuovo)
            page_id = api.save_to_notion(listing)
            
            if page_id:
                created_count += 1
            else:
                print(f"⚠️ Failed to save listing: {title}")
        
        # Piccola pausa tra le operazioni per non sovraccaricare Notion
        time.sleep(0.5)
    
    # Nota: Logica expired/active rimossa temporaneamente
    # Verrà reimplementata in seguito
    
    # Nota: Non salviamo più il timestamp in un file per evitare problemi di permessi
    # Il timestamp viene gestito internamente dal modulo API
    
    # Salva timestamp aggiornamento
    with open(last_update_file, 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"\n🎉 Idealista update completed!")
    print(f"   📊 New listings found: {len(all_listings)}")
    print(f"   ➕ Successfully created: {created_count}")
    print(f"   📅 Next update: {today + timedelta(days=1)}")

if __name__ == "__main__":
    main()
