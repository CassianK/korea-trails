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

def check_regional_authenticity(m_id, text):
    text = text.lower()
    if "yulong" in text or "lijiang" in text or "yunnan" in text or "china" in text:
        if not ("taiwan" in text and m_id == "xueshan" and "yulong" not in text):
            return False

    if m_id == "myeongseongsan":
        if any(x in text for x in ["pocheon", "sanjeong", "myeongseong", "포천", "산정", "명성"]):
            return True
        if ("korea" in text or "seoul" in text) and any(x in text for x in ["lake", "mountain", "hills", "valley", "autumn", "foliage", "forest", "scenery", "landscape", "pond"]):
            return True
    elif m_id == "taebaeksan":
        if any(x in text for x in ["taebaek", "pyeongchang", "gangwon", "cheonjedan", "태백", "천제단", "평창", "강원"]):
            return True
        if ("korea" in text or "south korea" in text) and any(x in text for x in ["mountain", "hills", "valley", "snow", "winter", "forest", "scenery", "landscape", "summit", "peak"]):
            return True
    elif m_id == "yushan":
        if any(x in text for x in ["yushan", "jade mountain", "mt. jade", "paiyun", "tataka", "玉山"]):
            return True
        if "taiwan" in text and any(x in text for x in ["mountain", "peak", "hills", "valley", "clouds", "scenery", "landscape", "national park", "hiking", "trail", "campsite", "highland"]):
            return True
    elif m_id == "xueshan":
        if any(x in text for x in ["xueshan", "snow mountain taiwan", "shei-pa", "369 cabin", "syue", "雪山"]):
            return True
        if "taiwan" in text and any(x in text for x in ["mountain", "peak", "hills", "valley", "clouds", "scenery", "landscape", "national park", "hiking", "trail", "hehuanshan", "hehuan"]):
            return True
    elif m_id == "yangmingshan":
        if any(x in text for x in ["yangmingshan", "qixingshan", "qingtiangang", "陽明山", "칭티엔강", "칠성산"]):
            return True
        if "taiwan" in text and any(x in text for x in ["yangmingshan", "taipei", "volcanic", "hot spring", "sulfur", "steaming", "grassy hill"]):
            return True
    return False

clean_candidates = []
seen = set()

# Process Unsplash candidates
for c in unsplash_candidates:
    w, h = c["width"], c["height"]
    if w < 1600 or w <= h:
        continue
    geo_text = c.get('geo_hint', '').lower()
    if "query:" in geo_text:
        geo_text = geo_text.split("query:")[0].strip()
    if not is_valid_landscape(geo_text):
        continue
    m_id = c["mountain_id"]
    if check_regional_authenticity(m_id, geo_text):
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
            if check_regional_authenticity(m_id, alt_text):
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

for m_id in ["myeongseongsan", "taebaeksan", "yushan", "xueshan", "yangmingshan"]:
    print(f"\n==================== {m_id} ====================")
    matched = [c for c in clean_candidates if c["mountain_id"] == m_id]
    print(f"Matched {len(matched)} photos")
    for c in matched[:5]:
        print(f"  - Source: {c['source']} | ID: {c['photo_id']} | Author: {c['author']}")
        print(f"    Alt: {c['geo_hint'][:150]}")
