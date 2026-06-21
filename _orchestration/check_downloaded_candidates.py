import json

with open("/Users/mac/korea-trails/_orchestration/photo-candidates-B5.json", "r") as f:
    candidates = json.load(f)

print(f"Total candidates: {len(candidates)}")

m_counts = {}
for c in candidates:
    m_id = c["mountain_id"]
    m_counts[m_id] = m_counts.get(m_id, 0) + 1

print("\nCounts per mountain:")
for m_id, count in m_counts.items():
    print(f"  - {m_id}: {count}")

print("\nDetail of first 3 candidates for each mountain:")
by_m = {}
for c in candidates:
    by_m.setdefault(c["mountain_id"], []).append(c)

for m_id, list_c in by_m.items():
    print(f"\n--- {m_id} ---")
    for c in list_c[:5]:
        print(f"  Source: {c['source']}, ID: {c['photo_id']}, Author: {c['author']}, Query: {c['query_used']}")
        print(f"  Geo Hint: {c['geo_hint']}")
