import urllib.request
import urllib.parse
import json
import ssl

def search_unsplash(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.unsplash.com/search/photos?query={encoded_query}&orientation=landscape&per_page=10"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Client-ID MrzCYdY-9WA151pj1UHYURT8RLjDCcD8uqji_3Y7Eco")
    req.add_header("Accept-Version", "v1")
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Unsplash error for {query}: {e}")
        return None

def search_pexels(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.pexels.com/v1/search?query={encoded_query}&orientation=landscape&per_page=10"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "KWYEYD54GanmYAye7HULjec3KpkxV8EFMvfbiXOD1FHf1yT22Zrm2dxy")
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Pexels error for {query}: {e}")
        return None

def analyze(mountain_id, name_en, queries):
    print(f"\n==================== {name_en} ({mountain_id}) ====================")
    for q in queries:
        print(f"\n--- Query: {q} ---")
        # Unsplash
        u_data = search_unsplash(q)
        if u_data and u_data.get("results"):
            print("  Unsplash results:")
            for photo in u_data["results"][:5]:
                print(f"    - ID: {photo['id']}, Desc: {photo.get('description')}, Alt: {photo.get('alt_description')}, UserLoc: {photo.get('user', {}).get('location')}")
        else:
            print("  Unsplash: No results")
            
        # Pexels
        p_data = search_pexels(q)
        if p_data and p_data.get("photos"):
            print("  Pexels results:")
            for photo in p_data["photos"][:5]:
                print(f"    - ID: {photo['id']}, Alt: {photo.get('alt')}, Photographer: {photo.get('photographer')}")
        else:
            print("  Pexels: No results")

analyze("myeongseongsan", "Myeongseongsan", ["Myeongseongsan", "명성산", "Sanjeong Lake"])
analyze("taebaeksan", "Taebaeksan", ["Taebaeksan", "태백산", "Taebaeksan National Park"])
analyze("yushan", "Yushan", ["Yushan", "玉山", "Yushan National Park", "Jade Mountain Taiwan"])
analyze("xueshan", "Xueshan", ["Xueshan", "雪山", "Xueshan Taiwan", "Snow Mountain Taiwan"])
analyze("yangmingshan", "Yangmingshan", ["Yangmingshan", "陽明山", "Yangmingshan National Park", "Qixingshan"])
