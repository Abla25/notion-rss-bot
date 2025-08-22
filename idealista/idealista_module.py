import os
import requests
import json
import time
import base64
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from api_tracker import APITracker

class IdealistaAPI:
    def __init__(self):
        self.api_key = os.environ.get("IDEALISTA_API_KEY")
        self.api_secret = os.environ.get("IDEALISTA_API_SECRET")
        self.notion_db_id = os.environ.get("IDEALISTA_NOTION_DATABASE_ID")
        self.access_token = None
        self.token_expires = None
        
        if not all([self.api_key, self.api_secret, self.notion_db_id]):
            raise ValueError("Missing required environment variables for Idealista API")
        
        # Notion headers
        self.notion_headers = {
            "Authorization": f"Bearer {os.environ.get('NOTION_API_KEY')}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # Inizializza il tracker API
        self.api_tracker = APITracker()
        
        # Rate limiting: 1 richiesta ogni 3 secondi
        self.last_request_time = None
        self.min_request_interval = 3.0  # secondi
        
    def authenticate(self) -> bool:
        """OAuth2 client_credentials flow"""
        if self.access_token and self.token_expires and datetime.now() < self.token_expires:
            return True
        
        # Controlla rate limiting per autenticazione
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.min_request_interval:
                wait_time = self.min_request_interval - time_since_last
                print(f"⏳ Rate limiting: waiting {wait_time:.1f} seconds before authentication...")
                time.sleep(wait_time)
            
        print("🔐 Authenticating with Idealista API...")
        
        # Aggiorna timestamp ultima richiesta
        self.last_request_time = time.time()
        
        auth_string = f"{self.api_key}:{self.api_secret}"
        auth_b64 = base64.b64encode(auth_string.encode()).decode()
        
        response = requests.post(
            "https://api.idealista.com/oauth/token",
            headers={
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            },
            data={
                "grant_type": "client_credentials",
                "scope": "read"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            self.token_expires = datetime.now() + timedelta(seconds=data["expires_in"])
            print(f"✅ Authentication successful, token expires at {self.token_expires}")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code} - {response.text}")
            return False
    
    def fetch_listings(self, page: int = 1, max_items: int = 50, exclude_codes: Set[str] = None) -> List[Dict]:
        """Fetch listings from Idealista API, excluding existing property codes"""
        if not self.authenticate():
            return []
        
        # Controlla se possiamo fare la chiamata
        status = self.api_tracker.get_status()
        if not status["can_make_call"]:
            print(f"❌ Cannot make API call: {status['current_day_calls']}/1 daily, {status['current_month_calls']}/25 monthly")
            print(f"⏰ Next available: {status.get('next_available', 'unknown')}")
            return []
        
        # Controlla rate limiting (1 richiesta ogni 3 secondi)
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.min_request_interval:
                wait_time = self.min_request_interval - time_since_last
                print(f"⏳ Rate limiting: waiting {wait_time:.1f} seconds before next request...")
                time.sleep(wait_time)
        
        print(f"📡 Fetching Idealista listings (page {page}, max {max_items})...")
        
        params = {
            "country": "es",
            "operation": "rent",
            "propertyType": "bedrooms",
            "center": "41.3851,2.1734",  # Coordinate centro Barcellona
            "distance": 8000,             # 8km dal centro
            "maxItems": max_items,
            "numPage": page,
            "sinceDate": "W",  # Last week
            "order": "publicationDate",
            "sort": "desc",
            "locale": "es",
            # Room-specific filters
            "housemates": "2,3,4"  # 2,3,4 coinquilini
        }
        
        # Nota: Idealista API non supporta esclusione diretta via parametri
        # Il filtro viene applicato dopo la risposta
        if exclude_codes:
            print(f"🚫 Will filter out {len(exclude_codes)} existing listings from response")
        
        # Debug: stampa i parametri
        print(f"🔍 API Parameters: {params}")
        
        try:
            # Aggiorna timestamp ultima richiesta
            self.last_request_time = time.time()
            
            # Richiesta con parametri corretti secondo documentazione
            response = requests.post(
                "https://api.idealista.com/3.5/es/search",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
                },
                data=params
            )
            
            if response.status_code == 200:
                data = response.json()
                listings = data.get("elementList", [])
                print(f"✅ Fetched {len(listings)} listings from Idealista")
                print(f"🎯 Parametri inviati: {response.request.body}")
                
                # Traccia chiamata di successo
                self.api_tracker.record_call(success=True)
                
                return listings
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ Failed to fetch listings: {error_msg}")
                print(f"🔍 Response headers: {dict(response.headers)}")
                
                # Traccia chiamata fallita
                self.api_tracker.record_call(success=False, error_message=error_msg)
                
                return []
                
        except Exception as e:
            error_msg = f"Request error: {str(e)}"
            print(f"❌ Request failed: {error_msg}")
            
            # Traccia chiamata fallita
            self.api_tracker.record_call(success=False, error_message=error_msg)
            
            return []
    
    def save_to_notion(self, listing: Dict) -> Optional[str]:
        """Save listing to Notion database"""
        try:
            # Create new listing (we already filtered out existing ones)
            return self.create_new_listing(listing)
                
        except Exception as e:
            print(f"❌ Error saving listing to Notion: {e}")
            return None
    
    def get_existing_property_codes(self) -> Set[str]:
        """Get all existing property codes from database"""
        existing_codes = set()
        page = 0
        
        while True:
            query_payload = {
                "page_size": 100,
                "start_cursor": page
            }
            
            try:
                response = requests.post(
                    f"https://api.notion.com/v1/databases/{self.notion_db_id}/query",
                    headers=self.notion_headers,
                    json=query_payload
                )
                
                if response.status_code != 200:
                    print(f"❌ Error querying database: {response.text}")
                    break
                    
                data = response.json()
                listings = data.get("results", [])
                
                if not listings:
                    break
                
                # Extract property codes
                for listing in listings:
                    props = listing.get("properties", {})
                    property_code_prop = props.get("property_code", {})
                    property_code = property_code_prop.get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    if property_code:
                        existing_codes.add(property_code)
                
                # Check if there are more pages
                if not data.get("has_more"):
                    break
                    
                page = data.get("next_cursor")
                
            except Exception as e:
                print(f"❌ Error getting existing codes: {e}")
                break
        
        return existing_codes
    
    def find_existing_listing(self, property_code: str) -> Optional[str]:
        """Find existing listing by property_code"""
        if not property_code:
            return None
            
        query_payload = {
            "filter": {
                "property": "property_code",
                "rich_text": {
                    "equals": property_code
                }
            },
            "page_size": 1
        }
        
        try:
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.notion_db_id}/query",
                headers=self.notion_headers,
                json=query_payload
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    return results[0]["id"]
            
        except Exception as e:
            print(f"❌ Error finding existing listing: {e}")
        
        return None
    
    def create_new_listing(self, listing: Dict) -> Optional[str]:
        """Create new listing in Notion"""
        try:
            payload = {
                "parent": {"database_id": self.notion_db_id},
                "properties": self._build_notion_properties(listing)
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.notion_headers,
                json=payload
            )
            
            if response.status_code == 200:
                page_id = response.json()["id"]
                print(f"✅ Created new listing: {listing.get('title', '')[:50]}...")
                return page_id
            else:
                print(f"❌ Failed to create listing: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating listing: {e}")
            return None
    
    def update_existing_listing(self, page_id: str, listing: Dict) -> Optional[str]:
        """Update existing listing in Notion"""
        try:
            payload = {
                "properties": self._build_notion_properties(listing)
            }
            
            response = requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=self.notion_headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"✅ Updated existing listing: {listing.get('title', '')[:50]}...")
                return page_id
            else:
                print(f"❌ Failed to update listing: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error updating listing: {e}")
            return None
    
    def _build_notion_properties(self, listing: Dict) -> Dict:
        """Build Notion properties from Idealista listing"""
        property_code = listing.get("propertyCode", "")
        title = listing.get("title", "")
        description = listing.get("description", "")
        price = listing.get("price", 0)
        rooms = listing.get("rooms", 0)
        bathrooms = listing.get("bathrooms", 0)
        size = listing.get("size", 0)
        address = listing.get("address", "")
        district = listing.get("district", "")
        neighborhood = listing.get("neighborhood", "")
        municipality = listing.get("municipality", "")
        province = listing.get("province", "")
        latitude = listing.get("latitude", 0)
        longitude = listing.get("longitude", 0)
        url = listing.get("url", "")
        thumbnail = listing.get("thumbnail", "")
        new_development = listing.get("newDevelopment", False)
        publication_date = listing.get("publicationDate", "")
        
        # Room-specific filters
        new_gender = listing.get("newGender", "")
        housemates = listing.get("housemates", "")
        
        properties = {
            "property_code": {
                "rich_text": [{"text": {"content": property_code}}]
            },
            "title": {
                "title": [{"text": {"content": title}}]
            },
            "description": {
                "rich_text": [{"text": {"content": description}}]
            },
            "price": {
                "number": price
            },
            "rooms": {
                "number": rooms
            },
            "bathrooms": {
                "number": bathrooms
            },
            "size": {
                "number": size
            },
            "address": {
                "rich_text": [{"text": {"content": address}}]
            },
            "neighborhood": {
                "rich_text": [{"text": {"content": neighborhood}}]
            },
            "municipality": {
                "rich_text": [{"text": {"content": municipality}}]
            },
            "province": {
                "rich_text": [{"text": {"content": province}}]
            },
            "latitude": {
                "number": latitude
            },
            "longitude": {
                "number": longitude
            },
            "url": {
                "url": url
            },
            "thumbnail": {
                "url": thumbnail
            },
            "status": {
                "select": {"name": "active"}
            },
            "new_development": {
                "checkbox": new_development
            },
            "source": {
                "select": {"name": "Idealista"}
            },
            "last_seen": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
        
        # Aggiungi proprietà condizionali solo se hanno valori validi
        if district:
            properties["district"] = {"select": {"name": district}}
            
        if new_gender in ["male", "female"]:
            properties["new_gender"] = {"select": {"name": new_gender}}
            
        if housemates:
            properties["housemates"] = {"rich_text": [{"text": {"content": housemates}}]}
        
        # Add publication_date if available
        if publication_date:
            properties["publication_date"] = {
                "date": {"start": publication_date}
            }
        
        return properties
    
    def mark_expired_listings(self, active_property_codes: List[str]):
        """Mark listings as expired if not in active list - OPTIMIZED"""
        print(f"🗑️ Checking for expired listings...")
        
        # Convert active_codes to set for O(1) lookup
        active_codes_set = set(active_property_codes)
        expired_count = 0
        page = 0
        
        while True:
            # Get active listings with pagination
            query_payload = {
                "filter": {
                    "property": "status",
                    "select": {"equals": "active"}
                },
                "page_size": 100,
                "start_cursor": page
            }
            
            try:
                response = requests.post(
                    f"https://api.notion.com/v1/databases/{self.notion_db_id}/query",
                    headers=self.notion_headers,
                    json=query_payload
                )
                
                if response.status_code != 200:
                    print(f"❌ Error querying database: {response.text}")
                    break
                    
                data = response.json()
                active_listings = data.get("results", [])
                
                if not active_listings:
                    break
                
                # Process listings in batch
                expired_page_ids = []
                for listing in active_listings:
                    props = listing.get("properties", {})
                    property_code_prop = props.get("property_code", {})
                    property_code = property_code_prop.get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    
                    if property_code and property_code not in active_codes_set:
                        expired_page_ids.append(listing["id"])
                
                # Batch update expired listings
                if expired_page_ids:
                    self._batch_mark_expired(expired_page_ids)
                    expired_count += len(expired_page_ids)
                
                # Check if there are more pages
                if not data.get("has_more"):
                    break
                    
                page = data.get("next_cursor")
                
            except Exception as e:
                print(f"❌ Error checking expired listings: {e}")
                break
        
        print(f"✅ Marked {expired_count} listings as expired")
    
    def _batch_mark_expired(self, page_ids: List[str]):
        """Mark multiple listings as expired in batch"""
        if not page_ids:
            return
            
        print(f"🔄 Marking {len(page_ids)} listings as expired...")
        
        # Process in smaller batches to avoid rate limits
        batch_size = 10
        for i in range(0, len(page_ids), batch_size):
            batch = page_ids[i:i + batch_size]
            
            # Update each listing in the batch
            for page_id in batch:
                try:
                    payload = {
                        "properties": {
                            "status": {"select": {"name": "expired"}}
                        }
                    }
                    
                    response = requests.patch(
                        f"https://api.notion.com/v1/pages/{page_id}",
                        headers=self.notion_headers,
                        json=payload
                    )
                    
                    if response.status_code != 200:
                        print(f"❌ Failed to mark listing {page_id} as expired: {response.text}")
                        
                except Exception as e:
                    print(f"❌ Error marking listing {page_id} as expired: {e}")
            
            # Small delay between batches
            if i + batch_size < len(page_ids):
                time.sleep(1)
    
    def _mark_listing_expired(self, page_id: str):
        """Mark a single listing as expired (legacy method)"""
        self._batch_mark_expired([page_id])
