import json

with open("/Users/mac/korea-trails/_orchestration/photo-candidates-B5.json", "r") as f:
    candidates = json.load(f)

keywords = {
    "myeongseongsan": ["myeongseongsan", "myeongseong", "pocheon", "sanjeong", "명성산", "산정호수"],
    "taebaeksan": ["taebaeksan", "taebaek", "cheonjedan", "장군봉", "천제단", "문수봉", "주목", "태백산"],
    "yushan": ["yushan", "jade mountain", "paiyun", "tataka", "위산", "玉山"],
    "xueshan": ["xueshan", "snow mountain", "shei-pa", "369 cabin", "369 camp", "설산", "雪山"],
    "yangmingshan": ["yangmingshan", "qixingshan", "qingtiangang", "xiaoyoufeng", "양명산", "陽明山", "칭티엔강"]
}

for m_id, kws in keywords.items():
    print(f"\n==================== {m_id} ====================")
    matched = []
    for c in candidates:
        if c["mountain_id"] == m_id:
            text = f"{c.get('geo_hint', '')} {c.get('query_used', '')} {c.get('url_full', '')}".lower()
            found = [kw for kw in kws if kw in text]
            if found:
                matched.append((c, found))
    print(f"Matched {len(matched)} / {len([c for c in candidates if c['mountain_id'] == m_id])}")
    for c, found in matched[:10]:
        print(f"  - ID: {c['photo_id']} ({c['source']}) | KWs: {found}")
        print(f"    Alt/Geo: {c['geo_hint'][:120]}")
