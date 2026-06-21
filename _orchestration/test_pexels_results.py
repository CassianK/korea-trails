import urllib.request
import urllib.parse
import json
import ssl

PEXELS_API_KEY = "KWYEYD54GanmYAye7HULjec3KpkxV8EFMvfbiXOD1FHf1yT22Zrm2dxy"

def search_pexels(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.pexels.com/v1/search?query={encoded_query}&orientation=landscape&per_page=30"
    req = urllib.request.Request(url)
    req.add_header("Authorization", PEXELS_API_KEY)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return None

queries_to_test = {
    "myeongseongsan": ["Myeongseongsan", "Sanjeong Lake", "Pocheon", "명성산"],
    "taebaeksan": ["Taebaeksan", "Taebaek", "태백산", "Taebaeksan National Park"],
    "yushan": ["Yushan", "Jade Mountain Taiwan", "Yushan National Park", "玉山"],
    "xueshan": ["Xueshan", "Snow Mountain Taiwan", "Shei-Pa", "雪山"],
    "yangmingshan": ["Yangmingshan", "Qixingshan", "Yangmingshan National Park", "陽明山"]
}

results = {}
for m_id, q_list in queries_to_test.items():
    results[m_id] = {}
    for q in q_list:
        data = search_pexels(q)
        if data and "photos" in data:
            results[m_id][q] = [
                {
                    "id": p["id"],
                    "alt": p.get("alt"),
                    "url": p["url"],
                    "width": p["width"],
                    "height": p["height"],
                    "photographer": p["photographer"]
                }
                for p in data["photos"]
            ]
        else:
            results[m_id][q] = []

with open("/Users/mac/korea-trails/_orchestration/pexels_results_all.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done! Results written to pexels_results_all.json")
