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

# Regional and mountain keywords to ensure authenticity
def check_regional_authenticity(m_id, text):
    text = text.lower()
    
    # Exclude known false positives
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

final_candidates = []
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
            final_candidates.append(c)

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
                    # Construct Pexels image URL using Pexels photo pattern
                    # Pexels pattern is usually: https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg
                    url_full = f"https://images.pexels.com/photos/{p['id']}/pexels-photo-{p['id']}.jpeg"
                    final_candidates.append({
                        "mountain_id": m_id,
                        "source": "Pexels",
                        "photo_id": str(p["id"]),
                        "url_full": url_full,
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

# Filter out candidates if we exceed 15 candidates per mountain, keeping the most relevant ones.
# We will sort to put ones with the exact mountain name or landmark in their alt/description first.
def score_relevance(c):
    m_id = c["mountain_id"]
    text = c["geo_hint"].lower()
    
    score = 0
    if m_id == "myeongseongsan":
        if "myeongseong" in text or "명성" in text: score += 10
        if "sanjeong" in text or "산정" in text: score += 8
        if "pocheon" in text or "포천" in text: score += 5
    elif m_id == "taebaeksan":
        if "taebaek" in text or "태백" in text: score += 10
        if "cheonjedan" in text or "천제단" in text: score += 8
        if "pyeongchang" in text or "평창" in text: score += 5
    elif m_id == "yushan":
        if "yushan" in text or "玉山" in text: score += 10
        if "jade mountain" in text or "mt. jade" in text: score += 8
    elif m_id == "xueshan":
        if "xueshan" in text or "雪山" in text: score += 10
        if "snow mountain" in text: score += 8
        if "shei-pa" in text or "369" in text: score += 5
    elif m_id == "yangmingshan":
        if "yangmingshan" in text or "陽明山" in text: score += 10
        if "qixingshan" in text or "칠성산" in text: score += 8
        if "qingtiangang" in text or "칭티엔강" in text: score += 8
        
    # Unsplash generally has higher verification or meta-data. Pexels is also good.
    # We prefer photos with higher score.
    return score

# Filter list per mountain to keep at least 8 (up to 12 if available)
filtered_final = []
for m_id in ["myeongseongsan", "taebaeksan", "yushan", "xueshan", "yangmingshan"]:
    m_list = [c for c in final_candidates if c["mountain_id"] == m_id]
    # Sort by relevance score descending
    m_list.sort(key=score_relevance, reverse=True)
    # Keep up to 12 candidates
    filtered_final.extend(m_list[:12])

# Verify count per mountain
final_counts = {}
for c in filtered_final:
    final_counts[c["mountain_id"]] = final_counts.get(c["mountain_id"], 0) + 1

print("\n--- Final Candidates Counts ---")
for m_id, count in final_counts.items():
    print(f"  - {m_id}: {count}")

# Save to target files
output_b5 = "/Users/mac/korea-trails/_orchestration/photo-candidates-B5.json"
output_global = "/Users/mac/korea-trails/_orchestration/photo-candidates.json"

try:
    with open(output_b5, "w", encoding="utf-8") as f:
        json.dump(filtered_final, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(filtered_final)} candidates to {output_b5}")
except Exception as e:
    print(f"Error saving to {output_b5}: {e}")

try:
    # Try to load existing global candidates if any
    try:
        with open(output_global, "r", encoding="utf-8") as f:
            global_candidates = json.load(f)
            if not isinstance(global_candidates, list):
                global_candidates = []
    except FileNotFoundError:
        global_candidates = []
        
    # Merge, replacing any matching photo_id + source
    global_seen = {(c["photo_id"], c["source"]): c for c in global_candidates}
    for c in filtered_final:
        global_seen[(c["photo_id"], c["source"])] = c
        
    merged_list = list(global_seen.values())
    
    with open(output_global, "w", encoding="utf-8") as f:
        json.dump(merged_list, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated global file {output_global} (now has {len(merged_list)} candidates)")
except Exception as e:
    print(f"Error updating {output_global}: {e}")
