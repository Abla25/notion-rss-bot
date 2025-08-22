#!/usr/bin/env python3
"""
Sistema di tracking per le chiamate API di Idealista
Tiene traccia del numero di chiamate effettuate e aggiorna un file JSON
"""

import json
import os
from datetime import datetime, date
from typing import Dict, Any

class APITracker:
    def __init__(self, tracker_file: str = "idealista_api_tracker.json"):
        self.tracker_file = tracker_file
        self.data = self._load_tracker()
    
    def _load_tracker(self) -> Dict[str, Any]:
        """Carica i dati del tracker dal file JSON"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"⚠️ Errore nel caricamento del tracker, creo nuovo file")
        
        # Struttura iniziale
        return {
            "total_calls": 0,
            "monthly_calls": {},
            "daily_calls": {},
            "last_call": None,
            "rate_limit": {
                "monthly_limit": 25,
                "daily_limit": 1,
                "remaining_monthly": 25,
                "remaining_daily": 1
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    def _save_tracker(self):
        """Salva i dati del tracker nel file JSON"""
        self.data["updated_at"] = datetime.now().isoformat()
        try:
            with open(self.tracker_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Errore nel salvataggio del tracker: {e}")
    
    def _get_current_month_key(self) -> str:
        """Restituisce la chiave del mese corrente (YYYY-MM)"""
        return datetime.now().strftime("%Y-%m")
    
    def _get_current_day_key(self) -> str:
        """Restituisce la chiave del giorno corrente (YYYY-MM-DD)"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def record_call(self, success: bool = True, error_message: str = None) -> Dict[str, Any]:
        """
        Registra una chiamata API
        
        Args:
            success: Se la chiamata è andata a buon fine
            error_message: Messaggio di errore se la chiamata è fallita
        
        Returns:
            Dict con le informazioni aggiornate
        """
        now = datetime.now()
        current_month = self._get_current_month_key()
        current_day = self._get_current_day_key()
        
        # Aggiorna contatori totali
        self.data["total_calls"] += 1
        
        # Aggiorna contatori mensili
        if current_month not in self.data["monthly_calls"]:
            self.data["monthly_calls"][current_month] = {
                "calls": 0,
                "successful": 0,
                "failed": 0,
                "errors": []
            }
        
        self.data["monthly_calls"][current_month]["calls"] += 1
        if success:
            self.data["monthly_calls"][current_month]["successful"] += 1
        else:
            self.data["monthly_calls"][current_month]["failed"] += 1
            if error_message:
                self.data["monthly_calls"][current_month]["errors"].append({
                    "timestamp": now.isoformat(),
                    "error": error_message
                })
        
        # Aggiorna contatori giornalieri
        if current_day not in self.data["daily_calls"]:
            self.data["daily_calls"][current_day] = {
                "calls": 0,
                "successful": 0,
                "failed": 0
            }
        
        self.data["daily_calls"][current_day]["calls"] += 1
        if success:
            self.data["daily_calls"][current_day]["successful"] += 1
        else:
            self.data["daily_calls"][current_day]["failed"] += 1
        
        # Aggiorna ultima chiamata
        self.data["last_call"] = now.isoformat()
        
        # Calcola rimanenti
        monthly_calls = self.data["monthly_calls"][current_month]["calls"]
        daily_calls = self.data["daily_calls"][current_day]["calls"]
        
        self.data["rate_limit"]["remaining_monthly"] = max(0, 25 - monthly_calls)
        self.data["rate_limit"]["remaining_daily"] = max(0, 1 - daily_calls)
        
        # Salva
        self._save_tracker()
        
        return self.get_status()
    
    def get_status(self) -> Dict[str, Any]:
        """Restituisce lo stato attuale del tracker"""
        current_month = self._get_current_month_key()
        current_day = self._get_current_day_key()
        
        monthly_calls = self.data["monthly_calls"].get(current_month, {}).get("calls", 0)
        daily_calls = self.data["daily_calls"].get(current_day, {}).get("calls", 0)
        
        return {
            "total_calls": self.data["total_calls"],
            "current_month_calls": monthly_calls,
            "current_day_calls": daily_calls,
            "remaining_monthly": self.data["rate_limit"]["remaining_monthly"],
            "remaining_daily": self.data["rate_limit"]["remaining_daily"],
            "last_call": self.data["last_call"],
            "can_make_call": daily_calls < 1 and monthly_calls < 25,
            "rate_limiting": {
                "min_interval": 3.0,
                "description": "1 request every 3 seconds"
            }
        }
    
    def print_status(self):
        """Stampa lo stato del tracker in formato leggibile"""
        status = self.get_status()
        
        print("📊 IDEALISTA API TRACKER STATUS")
        print("=" * 50)
        print(f"📞 Total calls: {status['total_calls']}")
        print(f"📅 This month: {status['current_month_calls']}/25")
        print(f"📆 Today: {status['current_day_calls']}/1")
        print(f"🔄 Remaining monthly: {status['remaining_monthly']}")
        print(f"🔄 Remaining daily: {status['remaining_daily']}")
        print(f"⏱️ Rate limiting: {status['rate_limiting']['description']}")
        print(f"✅ Can make call: {'Yes' if status['can_make_call'] else 'No'}")
        
        if status['last_call']:
            last_call = datetime.fromisoformat(status['last_call'])
            print(f"🕐 Last call: {last_call.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("=" * 50)
    
    def reset_monthly(self):
        """Resetta i contatori mensili (da usare solo per test)"""
        current_month = self._get_current_month_key()
        if current_month in self.data["monthly_calls"]:
            del self.data["monthly_calls"][current_month]
        self._save_tracker()
        print(f"🔄 Reset monthly counters for {current_month}")
    
    def reset_daily(self):
        """Resetta i contatori giornalieri (da usare solo per test)"""
        current_day = self._get_current_day_key()
        if current_day in self.data["daily_calls"]:
            del self.data["daily_calls"][current_day]
        self._save_tracker()
        print(f"🔄 Reset daily counters for {current_day}")

# Funzione di utilità per integrazione con idealista_module.py
def track_api_call(success: bool = True, error_message: str = None) -> Dict[str, Any]:
    """Funzione di utilità per tracciare una chiamata API"""
    tracker = APITracker()
    return tracker.record_call(success, error_message)

if __name__ == "__main__":
    # Test del tracker
    tracker = APITracker()
    tracker.print_status()
    
    # Simula alcune chiamate
    print("\n🧪 Testing API calls...")
    tracker.record_call(success=True)
    tracker.record_call(success=False, error_message="Rate limit exceeded")
    tracker.print_status()
    
    print("\n📊 Note: Rate limits updated to 25 requests/month (1250 rooms total)")
