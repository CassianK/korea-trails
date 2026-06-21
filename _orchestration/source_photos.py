import json
import urllib.request
import urllib.parse
import time
import ssl
import sys
from urllib.error import HTTPError, URLError

CONFIG_PATH = '/Users/mac/korea-trails/_orchestration/config.json'
INVENTORY_PATH = '/Users/mac/korea-trails/_orchestration/inventory.json'
OUTPUT_PATH = '/Users/mac/korea-trails/_orchestration/photo-candidates-B1.json'

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

UNSPLASH_KEY = config.get("UNSPLASH_ACCESS_KEY")
PEXELS_KEY = config.get("PEXELS_API_KEY")

if not UNSPLASH_KEY or not PEXELS_KEY:
    print("Error: API keys are missing in config.json")
    sys.exit(1)

TARGET_MOUNTAINS = ["seoraksan", "hallasan", "jirisan", "bukhansan", "sobaeksan", "gayasan"]

with open(INVENTORY_PATH, 'r') as f:
    inventory = json.load(f)

mountain_records = [m for m in inventory if m['id'] in TARGET_MOUNTAINS]
print(f"Loaded {len(mountain_records)} mountain records for Batch 1: {TARGET_MOUNTAINS}\n")

def make_request(url, headers, max_retries=3):
    ctx = ssl._create_unverified_context()
    delay = 2.0
    for attempt in range(max_retries):
        req = urllib.request.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            print(f"  HTTPError: {e.code} for URL: {url}")
            if e.code == 429:
                retry_after = e.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = float(retry_after)
                        print(f"  Rate limited (429). Retry-after header found: sleeping for {wait_time} seconds.")
                        time.sleep(wait_time)
                        continue
                    except ValueError:
                        pass
            print(f"  Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries})...")
            time.sleep(delay)
            delay *= 2
        except URLError as e:
            print(f"  URLError: {e.reason} for URL: {url}")
            print(f"  Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries})...")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            print(f"  Unexpected error: {e}")
            break
    return None

def search_unsplash(query):
    url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(query)}&orientation=landscape&per_page=25"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_KEY}",
        "Accept-Version": "v1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = make_request(url, headers)
    if data:
        return data.get("results", [])
    return []

def search_pexels(query):
    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&orientation=landscape&per_page=25"
    headers = {
        "Authorization": PEXELS_KEY,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = make_request(url, headers)
    if data:
        return data.get("photos", [])
    return []

def is_natural_landscape(photo, source):
    text_content = ""
    if source == 'unsplash':
        desc = photo.get('description') or ""
        alt_desc = photo.get('alt_description') or ""
        text_content = f"{desc} {alt_desc}".lower()
    elif source == 'pexels':
        alt = photo.get('alt') or ""
        text_content = alt.lower()

    exclusions = [
        "indoor", "room", "illustration", "vector", "drawing", "painting", 
        "map", "portrait", "close-up", "closeup", "food", "face", "selfie", 
        "text", "overlay", "logo", "graphic", "cartoon", "art", "sign", 
        "hotel", "restaurant", "cafe", "interior", "house", "building", 
        "cityscape", "architecture", "night-view", "street", "car", "vehicle", 
        "kitchen", "living room", "bedroom", "bathroom", "furniture", "table", 
        "chair", "sofa", "bed", "desk", "computer", "phone", "clothing", 
        "apparel", "model", "man", "woman", "person close-up"
    ]

    for word in exclusions:
        if word in text_content:
            return False

    if photo.get('width', 0) < 1600:
        return False

    if photo.get('width', 0) <= photo.get('height', 0):
        return False

    return True

all_candidates = []

for rec in mountain_records:
    m_id = rec['id']
    name_ko = rec['name_ko']
    name_en = rec['name_en']
    landmarks = rec.get('landmarks', [])
    search_terms = rec.get('search_terms', [])
    
    print(f"==================================================")
    print(f"Processing Mountain: {m_id} ({name_ko} / {name_en})")
    print(f"==================================================")
    
    # Priority query generation
    queries = []
    
    # 1. <EnglishName> National Park
    queries.append(f"{name_en} National Park")
    
    # 2. <EnglishName> mountain Korea
    queries.append(f"{name_en} mountain Korea")
    
    # 3. Landmarks
    for term in search_terms:
        if term not in queries and term != name_en:
            queries.append(term)
    for lmark in landmarks:
        if lmark not in queries:
            queries.append(lmark)
            
    # 4. Korean name
    if name_ko not in queries:
        queries.append(name_ko)
        
    # De-duplicate queries list
    unique_queries = []
    for q in queries:
        if q not in unique_queries:
            unique_queries.append(q)
            
    print(f"Generated queries queue: {unique_queries}")
    
    collected_for_mountain = []
    seen_ids = set()
    
    for query in unique_queries:
        if len(collected_for_mountain) >= 12:
            print(f"Sufficient candidates ({len(collected_for_mountain)}) gathered for {m_id}. Skipping remaining queries.")
            break
            
        print(f"Querying Unsplash for '{query}'...")
        u_results = search_unsplash(query)
        time.sleep(2.0)  # Rate limiting delay
        
        for p in u_results:
            pid = p.get('id')
            key = f"unsplash_{pid}"
            if key in seen_ids:
                continue
            if is_natural_landscape(p, 'unsplash'):
                geo_parts = []
                if p.get('description'):
                    geo_parts.append(p['description'])
                if p.get('alt_description'):
                    geo_parts.append(p['alt_description'])
                user_loc = p.get('user', {}).get('location')
                if user_loc:
                    geo_parts.append(f"User location: {user_loc}")
                geo_hint = " | ".join(geo_parts)
                
                candidate = {
                    "mountain_id": m_id,
                    "source": "unsplash",
                    "photo_id": pid,
                    "url_full": p.get('urls', {}).get('full') or p.get('urls', {}).get('raw'),
                    "url_download_trigger": p.get('links', {}).get('download_location'),
                    "author": p.get('user', {}).get('name'),
                    "author_url": p.get('user', {}).get('links', {}).get('html'),
                    "license": "Unsplash License",
                    "width": p.get('width'),
                    "height": p.get('height'),
                    "query_used": query,
                    "geo_hint": geo_hint,
                    "authenticity_confidence": 0.0
                }
                collected_for_mountain.append(candidate)
                seen_ids.add(key)
                
        if len(collected_for_mountain) >= 12:
            print(f"Sufficient candidates ({len(collected_for_mountain)}) gathered for {m_id}. Skipping Pexels for this query.")
            break
            
        print(f"Querying Pexels for '{query}'...")
        p_results = search_pexels(query)
        time.sleep(2.0)  # Rate limiting delay
        
        for p in p_results:
            pid = str(p.get('id'))
            key = f"pexels_{pid}"
            if key in seen_ids:
                continue
            if is_natural_landscape(p, 'pexels'):
                candidate = {
                    "mountain_id": m_id,
                    "source": "pexels",
                    "photo_id": pid,
                    "url_full": p.get('src', {}).get('original'),
                    "url_download_trigger": None,
                    "author": p.get('photographer'),
                    "author_url": p.get('photographer_url'),
                    "license": "Pexels License",
                    "width": p.get('width'),
                    "height": p.get('height'),
                    "query_used": query,
                    "geo_hint": p.get('alt') or "",
                    "authenticity_confidence": 0.0
                }
                collected_for_mountain.append(candidate)
                seen_ids.add(key)
                
    print(f"Finished sourcing for {m_id}. Gathered {len(collected_for_mountain)} candidates.")
    if len(collected_for_mountain) < 8:
        print(f"WARNING: Only gathered {len(collected_for_mountain)} candidates for {m_id} (minimum is 8).")
        
    all_candidates.extend(collected_for_mountain)

# Output candidates to B1 JSON file
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(all_candidates, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully wrote {len(all_candidates)} candidates to {OUTPUT_PATH}")
