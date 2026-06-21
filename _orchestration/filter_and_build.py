import json

# Load Unsplash candidates from the first run
try:
    with open("/Users/mac/korea-trails/_orchestration/photo-candidates-B5.json", "r") as f:
        unsplash_candidates = json.load(f)
except Exception as e:
    unsplash_candidates = []

# Load Pexels search results
try:
    with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "r") as f:
        pexels_results = json.load(f)
except Exception as e:
    pexels_results = {}

# Exclude terms for non-landscape
def is_valid_landscape(text):
    exclude_terms = [
        "illustration", "vector", "drawing", "painting", "sketch", "clipart", "render", "3d", "mockup",
        "interior", "indoor", "room", "kitchen", "office", "bedroom", "bathroom", "living room", "furniture",
        "food", "dish", "plate", "cooking", "restaurant", "meal", "coffee", "cup", "spoon", "knife", "fabric",
        "portrait", "selfie", "close up of a face", "face of a", "studio portrait",
        "text", "poster", "banner", "flyer", "logo", "infographic", "nft", "tezos", "crypto", "jacket",
        "man smiling", "woman smiling", "person smiling", "smiling man", "smiling woman", "man with a beard",
        "man wearing", "woman wearing", "person wearing", "close-up of a young man", "boy with a yellow jacket",
        "holding two fingers up", "photoshoot", "model", "monk reading", "monks reading", "table setup",
        "seed pod", "braided bun", "hairpin", "hanbok", "woman in traditional", "man and woman sitting on a beach",
        "couple of men standing", "people taking a selfie", "group enjoying lakeside selfie"
    ]
    for term in exclude_terms:
        if term in text:
            return False
    return True

# Mountain keyword checkers to ensure authenticity
def check_relevance(m_id, text):
    # This checks actual photo metadata text (no query_used!)
    text = text.lower()
    if m_id == "myeongseongsan":
        return any(x in text for x in ["pocheon", "sanjeong", "myeongseong", "명성", "포천", "산정"])
    elif m_id == "taebaeksan":
        return any(x in text for x in ["taebaek", "pyeongchang", "cheonjedan", "태백", "천제단", "평창"])
    elif m_id == "yushan":
        return any(x in text for x in ["yushan", "jade mountain", "mt. jade", "paiyun", "tataka", "玉山"])
    elif m_id == "xueshan":
        if "yulong" in text or "lijiang" in text:
            return False
        return any(x in text for x in ["xueshan", "snow mountain taiwan", "shei-pa", "369 cabin", "syue", "雪山", "hehuanshan", "hehuan"])
    elif m_id == "yangmingshan":
        return any(x in text for x in ["yangmingshan", "qixingshan", "qingtiangang", "陽明山", "칭티엔강", "칠성산"])
    return False

clean_candidates = []
seen = set()

# Process Unsplash candidates
for c in unsplash_candidates:
    w, h = c["width"], c["height"]
    if w < 1600 or w <= h:
        continue
        
    # Check relevance ONLY on the geo_hint (which has description, alt_description, and user location)
    # NOT query_used!
    geo_text = c.get('geo_hint', '').lower()
    # Remove 'query: myeongseongsan' part from geo_hint if it's there
    if "query:" in geo_text:
        geo_text = geo_text.split("query:")[0].strip()
        
    if not is_valid_landscape(geo_text):
        continue
        
    m_id = c["mountain_id"]
    if check_relevance(m_id, geo_text):
        key = (c["photo_id"], c["source"])
        if key not in seen:
            seen.add(key)
            clean_candidates.append(c)

# Process Pexels candidates
for m_id, q_dict in pexels_results.items():
    for q, photos in q_dict.items():
        for p in photos:
            w, h = p["width"], p["height"]
            if w < 1600 or w <= h:
                continue
                
            alt_text = p.get('alt', '').lower()
            if not is_valid_landscape(alt_text):
                continue
                
            if check_relevance(m_id, alt_text):
                key = (str(p["id"]), "Pexels")
                if key not in seen:
                    seen.add(key)
                    clean_candidates.append({
                        "mountain_id": m_id,
                        "source": "Pexels",
                        "photo_id": str(p["id"]),
                        "url_full": p["url"].replace("https://www.pexels.com/photo/", "https://images.pexels.com/photos/") + "pexels-photo-" + str(p["id"]) + ".jpeg",
                        "url_download_trigger": "",
                        "author": p["photographer"],
                        "author_url": p["url"],
                        "license": "Pexels License",
                        "width": w,
                        "height": h,
                        "query_used": q,
                        "geo_hint": f"{p.get('alt')} | Query: {q}",
                        "authenticity_confidence": 0.0
                    })

counts = {}
for c in clean_candidates:
    m_id = c["mountain_id"]
    counts[m_id] = counts.get(m_id, 0) + 1

print("\n--- Strict Candidates Found ---")
for m_id in ["myeongseongsan", "taebaeksan", "yushan", "xueshan", "yangmingshan"]:
    print(f"  - {m_id}: {counts.get(m_id, 0)}")

print("\nDetail of all STRICT candidates:")
for c in clean_candidates:
    print(f"[{c['mountain_id']}] Source: {c['source']}, ID: {c['photo_id']}, Author: {c['author']}, Query: {c['query_used']}")
    print(f"  Alt/Geo: {c['geo_hint']}")
