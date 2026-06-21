import json

with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "r") as f:
    results = json.load(f)

print("=== Taebaek Pexels Results ===")
taebaek_photos = results.get("taebaeksan", {}).get("Taebaek", [])
for p in taebaek_photos[:10]:
    print(f"  ID: {p['id']}, Alt: {p['alt']}, URL: {p['url']}")

print("\n=== Taebaeksan Pexels Results ===")
taebaeksan_photos = results.get("taebaeksan", {}).get("Taebaeksan", [])
for p in taebaeksan_photos[:10]:
    print(f"  ID: {p['id']}, Alt: {p['alt']}, URL: {p['url']}")
