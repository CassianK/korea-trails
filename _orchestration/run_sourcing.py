import urllib.request
import urllib.parse
import json
import time
import ssl
import sys

# Load API keys
try:
    with open("/Users/mac/korea-trails/_orchestration/config.json", "r") as f:
        config = json.load(f)
        UNSPLASH_ACCESS_KEY = config.get("UNSPLASH_ACCESS_KEY")
        PEXELS_API_KEY = config.get("PEXELS_API_KEY")
except Exception as e:
    print(f"Error loading config.json: {e}")
    sys.exit(1)

# Target mountains
TARGET_MOUNTAIN_IDS = ["myeongseongsan", "taebaeksan", "yushan", "xueshan", "yangmingshan"]

# Load inventory to get metadata
try:
    with open("/Users/mac/korea-trails/_orchestration/inventory.json", "r") as f:
        inventory = json.load(f)
except Exception as e:
    print(f"Error loading inventory.json: {e}")
    sys.exit(1)

mountains_dict = {m["id"]: m for m in inventory if m["id"] in TARGET_MOUNTAIN_IDS}

# Helper to verify if description points to natural landscape
def is_natural_landscape(desc, alt):
    desc = (desc or "").lower()
    alt = (alt or "").lower()
    
    exclude_terms = [
        "illustration", "vector", "drawing", "painting", "sketch", "clipart", "render", "3d", "mockup",
        "interior", "indoor", "room", "kitchen", "office", "bedroom", "bathroom", "living room", "furniture",
        "food", "dish", "plate", "cooking", "restaurant", "meal", "coffee", "cup",
        "portrait", "selfie", "close up of a face", "face of a", "studio portrait",
        "text", "poster", "banner", "flyer", "logo", "infographic"
    ]
    
    for term in exclude_terms:
        if term in desc or term in alt:
            return False
    return True

# Helper to build geo hint
def get_geo_hint(photo, source, query_used):
    hints = []
    if source == "Unsplash":
        user_loc = photo.get("user", {}).get("location")
        if user_loc:
            hints.append(f"User location: {user_loc}")
        desc = photo.get("description")
        if desc:
            hints.append(desc)
        alt = photo.get("alt_description")
        if alt:
            hints.append(alt)
    elif source == "Pexels":
        alt = photo.get("alt")
        if alt:
            hints.append(alt)
    hints.append(f"Query: {query_used}")
    return " | ".join(hints)

# API caller with retry-after and exponential backoff
def call_api(url, headers):
    ctx = ssl._create_unverified_context()
    retries = 3
    delay = 2.0
    for attempt in range(retries):
        req = urllib.request.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                wait_time = int(retry_after) if retry_after and retry_after.isdigit() else delay
                print(f"Rate limited (429). Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                delay *= 2
            else:
                print(f"HTTP Error {e.code} for URL {url}: {e.reason}")
                break
        except Exception as e:
            print(f"Network error: {e}")
            time.sleep(delay)
            delay *= 2
    return None

def search_unsplash(query, mountain_id):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.unsplash.com/search/photos?query={encoded_query}&orientation=landscape&per_page=30"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = call_api(url, headers)
    candidates = []
    if data and "results" in data:
        for photo in data["results"]:
            width = photo.get("width", 0)
            height = photo.get("height", 0)
            
            # Filters: orientation and width
            if width < 1600 or width <= height:
                continue
                
            desc = photo.get("description")
            alt = photo.get("alt_description")
            if not is_natural_landscape(desc, alt):
                continue
                
            candidates.append({
                "mountain_id": mountain_id,
                "source": "Unsplash",
                "photo_id": photo.get("id"),
                "url_full": photo.get("urls", {}).get("full"),
                "url_download_trigger": photo.get("links", {}).get("download_location"),
                "author": photo.get("user", {}).get("name"),
                "author_url": photo.get("user", {}).get("links", {}).get("html"),
                "license": "Unsplash License",
                "width": width,
                "height": height,
                "query_used": query,
                "geo_hint": get_geo_hint(photo, "Unsplash", query),
                "authenticity_confidence": 0.0
            })
    return candidates

def search_pexels(query, mountain_id):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.pexels.com/v1/search?query={encoded_query}&orientation=landscape&per_page=30"
    headers = {
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = call_api(url, headers)
    candidates = []
    if data and "photos" in data:
        for photo in data["photos"]:
            width = photo.get("width", 0)
            height = photo.get("height", 0)
            
            # Filters: orientation and width
            if width < 1600 or width <= height:
                continue
                
            alt = photo.get("alt")
            if not is_natural_landscape(None, alt):
                continue
                
            candidates.append({
                "mountain_id": mountain_id,
                "source": "Pexels",
                "photo_id": str(photo.get("id")),
                "url_full": photo.get("src", {}).get("original"),
                "url_download_trigger": "",
                "author": photo.get("photographer"),
                "author_url": photo.get("photographer_url"),
                "license": "Pexels License",
                "width": width,
                "height": height,
                "query_used": query,
                "geo_hint": get_geo_hint(photo, "Pexels", query),
                "authenticity_confidence": 0.0
            })
    return candidates

all_candidates = []

for mountain_id in TARGET_MOUNTAIN_IDS:
    m = mountains_dict.get(mountain_id)
    if not m:
        print(f"Warning: mountain {mountain_id} not found in inventory.json")
        continue
        
    print(f"\n--- Sourcing photos for {m['name_en']} ({m['name_ko']}) ---")
    
    # Prioritized search query matrix
    queries = []
    # 1. English Official Name
    queries.append(m["name_en"])
    
    # 2. National Park / Modifier (e.g. Taebaeksan National Park)
    # Check if there is an explicit search term like "Taebaeksan National Park" or "Yangmingshan National Park"
    for term in m.get("search_terms", []):
        if term not in queries:
            queries.append(term)
            
    # Add National Park version if not already in search terms
    # Let's see: if region is 대만 (Taiwan) or country is TW, add "National Park" version
    is_taiwan = m.get("country") == "TW" or m.get("region") == "대만"
    
    np_term = f"{m['name_en']} National Park"
    if np_term not in queries:
        queries.append(np_term)
        
    # 3. Landmarks
    for lm in m.get("landmarks", []):
        # Translate or keep as is? Let's check search terms in inventory, it has landmarks like Sanjeong lake in English.
        # If it's a landmark, we'll try to find it in English search terms or add landmark directly if it's alphanumeric.
        if lm not in queries:
            queries.append(lm)
            
    # 4. Korean Name
    if m.get("name_ko") and m["name_ko"] not in queries:
        queries.append(m["name_ko"])
        
    # 5. Hanja/Chinese Name for Taiwan mountains
    if is_taiwan and m.get("name_hanja") and m["name_hanja"] not in queries:
        queries.append(m["name_hanja"])
        
    print(f"Generated query matrix: {queries}")
    
    mountain_candidates = []
    seen_ids = set()
    
    # Search loop
    for query in queries:
        if len(mountain_candidates) >= 12:
            print(f"Reached target number of candidates (>=12) for {m['name_en']}")
            break
            
        print(f"Searching Unsplash for: '{query}'")
        u_results = search_unsplash(query, mountain_id)
        for item in u_results:
            key = (item["photo_id"], item["source"])
            if key not in seen_ids:
                seen_ids.add(key)
                mountain_candidates.append(item)
                
        time.sleep(2.0) # Respect rate limits (2s delay)
        
        if len(mountain_candidates) >= 12:
            print(f"Reached target number of candidates (>=12) for {m['name_en']}")
            break
            
        print(f"Searching Pexels for: '{query}'")
        p_results = search_pexels(query, mountain_id)
        for item in p_results:
            key = (item["photo_id"], item["source"])
            if key not in seen_ids:
                seen_ids.add(key)
                mountain_candidates.append(item)
                
        time.sleep(2.0) # Respect rate limits (2s delay)
        
    # Log summary for this mountain
    print(f"Found {len(mountain_candidates)} candidates for {m['name_en']}")
    if len(mountain_candidates) < 8:
        print(f"Warning: Only found {len(mountain_candidates)} candidates (less than 8!) for {m['name_en']}")
    all_candidates.extend(mountain_candidates)

# Save result
output_file = "/Users/mac/korea-trails/_orchestration/photo-candidates-B5.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, ensure_ascii=False, indent=2)
    print(f"\nSuccessfully wrote {len(all_candidates)} candidates to {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")
