import json

with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "r") as f:
    results = json.load(f)

print("=== Pocheon Pexels Results ===")
pocheon_photos = results.get("myeongseongsan", {}).get("Pocheon", [])
for p in pocheon_photos:
    print(f"  ID: {p['id']}, Alt: {p['alt']}, URL: {p['url']}")

print("\n=== Sanjeong Lake Pexels Results ===")
sanjeong_photos = results.get("myeongseongsan", {}).get("Sanjeong Lake", [])
for p in sanjeong_photos:
    print(f"  ID: {p['id']}, Alt: {p['alt']}, URL: {p['url']}")
