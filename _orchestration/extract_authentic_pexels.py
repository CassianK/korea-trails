import json

with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "r") as f:
    results = json.load(f)

keywords = {
    "myeongseongsan": ["pocheon", "sanjeong", "myeongseong", "명성", "포천", "산정"],
    "taebaeksan": ["taebaek", "cheonjedan", "태백", "천제단"],
    "yushan": ["yushan", "jade mountain", "mt. jade", "玉山"],
    "xueshan": ["xueshan", "snow mountain taiwan", "shei-pa", "syue", "雪山"],
    "yangmingshan": ["yangmingshan", "qixingshan", "qingtiangang", "陽明山", "칠성산", "칭티엔강"]
}

for m_id, kws in keywords.items():
    print(f"\n==================== {m_id} ====================")
    matched = []
    # Collect all photos for this mountain across all queries
    all_photos = []
    seen = set()
    for q, photos in results.get(m_id, {}).items():
        for p in photos:
            if p["id"] not in seen:
                seen.add(p["id"])
                all_photos.append(p)
                
    for p in all_photos:
        text = f"{p.get('alt', '')} {p.get('url', '')}".lower()
        found = [kw for kw in kws if kw in text]
        if found:
            matched.append((p, found))
            
    print(f"Matched {len(matched)} / {len(all_photos)} unique Pexels photos")
    for p, found in matched[:10]:
        print(f"  - ID: {p['id']} | KWs: {found}")
        print(f"    Alt: {p['alt']}")
