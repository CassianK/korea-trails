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

# Target mountains for Batch 3
TARGET_MOUNTAIN_IDS = ["wolchulsan", "mudeungsan", "baekhaksan", "duryunsan", "minjusan"]

# Load inventory to get metadata
try:
    with open("/Users/mac/korea-trails/_orchestration/inventory.json", "r") as f:
        inventory = json.load(f)
except Exception as e:
    print(f"Error loading inventory.json: {e}")
    sys.exit(1)

mountains_dict = {m["id"]: m for m in inventory if m["id"] in TARGET_MOUNTAIN_IDS}

# Global flag to track Unsplash rate limit status
unsplash_blocked = False

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
    if source == "unsplash":
        user_loc = photo.get("user", {}).get("location")
        if user_loc:
            hints.append(f"User location: {user_loc}")
        desc = photo.get("description")
        if desc:
            hints.append(desc)
        alt = photo.get("alt_description")
        if alt:
            hints.append(alt)
    elif source == "pexels":
        alt = photo.get("alt")
        if alt:
            hints.append(alt)
    hints.append(f"Query: {query_used}")
    return " | ".join(hints)

# API caller
def call_api(url, headers):
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, context=ctx) as response:
        return json.loads(response.read().decode('utf-8'))

def search_unsplash(query, mountain_id):
    global unsplash_blocked
    if unsplash_blocked:
        return []
        
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.unsplash.com/search/photos?query={encoded_query}&orientation=landscape&per_page=30"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
        "Accept-Version": "v1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
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
                    "source": "unsplash",
                    "photo_id": photo.get("id"),
                    "url_full": photo.get("urls", {}).get("full"),
                    "url_download_trigger": photo.get("links", {}).get("download_location"),
                    "author": photo.get("user", {}).get("name"),
                    "author_url": photo.get("user", {}).get("links", {}).get("html"),
                    "license": "Unsplash License",
                    "width": width,
                    "height": height,
                    "query_used": query,
                    "geo_hint": get_geo_hint(photo, "unsplash", query),
                    "authenticity_confidence": 0.0
                })
            return candidates
    except urllib.error.HTTPError as e:
        print(f"  Unsplash HTTP Error {e.code} for query '{query}': {e.reason}")
        if e.code in [403, 429]:
            print("  Unsplash is rate limited or blocked. Disabling Unsplash calls.")
            unsplash_blocked = True
        return []
    except Exception as e:
        print(f"  Unsplash error: {e}")
        return []

def search_pexels(query, mountain_id):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.pexels.com/v1/search?query={encoded_query}&orientation=landscape&per_page=30"
    headers = {
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
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
                    "source": "pexels",
                    "photo_id": str(photo.get("id")),
                    "url_full": photo.get("src", {}).get("original"),
                    "url_download_trigger": None,
                    "author": photo.get("photographer"),
                    "author_url": photo.get("photographer_url"),
                    "license": "Pexels License",
                    "width": width,
                    "height": height,
                    "query_used": query,
                    "geo_hint": get_geo_hint(photo, "pexels", query),
                    "authenticity_confidence": 0.0
                })
            return candidates
    except urllib.error.HTTPError as e:
        print(f"  Pexels HTTP Error {e.code} for query '{query}': {e.reason}")
        return []
    except Exception as e:
        print(f"  Pexels error: {e}")
        return []

all_candidates = []

for mountain_id in TARGET_MOUNTAIN_IDS:
    m = mountains_dict.get(mountain_id)
    if not m:
        print(f"Warning: mountain {mountain_id} not found in inventory.json")
        continue
        
    print(f"\n--- Sourcing photos for {m['name_en']} ({m['name_ko']}) ---")
    
    # Prioritized search query matrix
    queries = []
    
    # Capitalize target name as standard English name
    name_en = m["name_en"]
    if any(ord(c) > 127 for c in name_en):
        name_en = m["id"].capitalize()
        
    if name_en not in queries:
        queries.append(name_en)
        
    # Add search terms from inventory
    for term in m.get("search_terms", []):
        if term not in queries:
            queries.append(term)
            
    # Add National Park version
    np_term = f"{name_en} National Park"
    if np_term not in queries:
        queries.append(np_term)
        
    # Add Mountain version
    mt_term = f"{name_en} Mountain"
    if mt_term not in queries:
        queries.append(mt_term)
        
    # Add landmarks
    for lm in m.get("landmarks", []):
        if lm not in queries:
            queries.append(lm)
            
    # Add Korean Name
    if m.get("name_ko") and m["name_ko"] not in queries:
        queries.append(m["name_ko"])
        
    print(f"Generated query matrix: {queries}")
    
    mountain_candidates = []
    seen_ids = set()
    
    # Search loop
    for query in queries:
        if len(mountain_candidates) >= 15: # Gather a good pool of candidates (target 15-20, min 8)
            print(f"Reached target number of candidates (>=15) for {m['name_en']}")
            break
            
        print(f"Searching Unsplash for: '{query}'")
        u_results = search_unsplash(query, mountain_id)
        for item in u_results:
            key = (item["photo_id"], item["source"])
            if key not in seen_ids:
                seen_ids.add(key)
                mountain_candidates.append(item)
                
        time.sleep(2.0) # Respect rate limits (2s delay)
        
        if len(mountain_candidates) >= 15:
            print(f"Reached target number of candidates (>=15) for {m['name_en']}")
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

# Save result to _orchestration/photo-candidates-B3.json
output_file = "/Users/mac/korea-trails/_orchestration/photo-candidates-B3.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_candidates, f, ensure_ascii=False, indent=2)
    print(f"\nSuccessfully wrote {len(all_candidates)} candidates to {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")
