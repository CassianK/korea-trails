import json

with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "r") as f:
    results = json.load(f)

for m_id, q_dict in results.items():
    print(f"\n==================== Mountain: {m_id} ====================")
    for q, photos in q_dict.items():
        print(f"  Query '{q}': {len(photos)} photos")
        if photos:
            print("    Samples:")
            for p in photos[:5]:
                print(f"      - ID: {p['id']}, Alt: {p['alt']}")
