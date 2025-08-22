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
    last_update_file = "last_idealista_update.txt"
    today = datetime.now().date()
    
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
    
    print(f"📅 Starting Idealista update for {today}")
    
    # Fetch solo la prima pagina (50 risultati)
    listings = api.fetch_listings(page=1, max_items=50)
    
    if not listings:
        print("❌ No listings fetched")
        return
    
    print(f"📊 Processing {len(listings)} listings...")
    
    # Processa e salva
    active_codes = []
    created_count = 0
    updated_count = 0
    
    for i, listing in enumerate(listings, 1):
        property_code = listing.get("propertyCode", "")
        title = listing.get("title", "")[:50]
        
        print(f"📝 Processing {i}/{len(listings)}: {title}...")
        
        if property_code:
            active_codes.append(property_code)
            
            # Salva o aggiorna in Notion
            page_id = api.save_to_notion(listing)
            
            if page_id:
                # Determina se è stato creato o aggiornato
                existing_page_id = api.find_existing_listing(property_code)
                if existing_page_id and existing_page_id != page_id:
                    updated_count += 1
                else:
                    created_count += 1
            else:
                print(f"⚠️ Failed to save listing: {title}")
        
        # Piccola pausa tra le operazioni per non sovraccaricare Notion
        time.sleep(0.5)
    
    # Marca come expired quelli non più attivi
    api.mark_expired_listings(active_codes)
    
    # Salva timestamp aggiornamento
    with open(last_update_file, 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"\n🎉 Idealista update completed!")
    print(f"   📊 Total processed: {len(listings)}")
    print(f"   ➕ New listings: {created_count}")
    print(f"   🔄 Updated listings: {updated_count}")
    print(f"   ✅ Active property codes: {len(active_codes)}")
    print(f"   📅 Next update: {today + timedelta(days=1)}")

if __name__ == "__main__":
    main()
