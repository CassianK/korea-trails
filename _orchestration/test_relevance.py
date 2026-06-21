import urllib.request
import urllib.parse
import json
import ssl
import time

UNSPLASH_ACCESS_KEY = "MrzCYdY-9WA151pj1UHYURT8RLjDCcD8uqji_3Y7Eco"
PEXELS_API_KEY = "KWYEYD54GanmYAye7HULjec3KpkxV8EFMvfbiXOD1FHf1yT22Zrm2dxy"

def search_unsplash(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.unsplash.com/search/photos?query={encoded_query}&orientation=landscape&per_page=30"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Client-ID {UNSPLASH_ACCESS_KEY}")
    req.add_header("Accept-Version", "v1")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Unsplash error: {e}")
        return None

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
        print(f"Pexels error: {e}")
        return None

def test_mountain(mountain_id, queries, keywords):
    print(f"\n==================== {mountain_id} ====================")
    for q in queries:
        print(f"--- Query: {q} ---")
        u_data = search_unsplash(q)
        time.sleep(1.0)
        p_data = search_pexels(q)
        time.sleep(1.0)
        
        # Check Unsplash
        if u_data and "results" in u_data:
            print("  Unsplash Matches:")
            count = 0
            for photo in u_data["results"]:
                desc = (photo.get("description") or "").lower()
                alt = (photo.get("alt_description") or "").lower()
                user_loc = (photo.get("user", {}).get("location") or "").lower()
                
                # Check if any keyword matches
                matched = [kw for kw in keywords if kw.lower() in desc or kw.lower() in alt or kw.lower() in user_loc]
                if matched:
                    print(f"    - ID: {photo['id']}, Matched KWs: {matched}, Alt: {alt[:60]}, Desc: {desc[:60]}")
                    count += 1
            if count == 0:
                print("    No keyword-matched photos")
                
        # Check Pexels
        if p_data and "photos" in p_data:
            print("  Pexels Matches:")
            count = 0
            for photo in p_data["photos"]:
                alt = (photo.get("alt") or "").lower()
                url = (photo.get("url") or "").lower()
                
                # Check if any keyword matches
                matched = [kw for kw in keywords if kw.lower() in alt or kw.lower() in url]
                if matched:
                    print(f"    - ID: {photo['id']}, Matched KWs: {matched}, Alt: {alt[:60]}")
                    count += 1
            if count == 0:
                print("    No keyword-matched photos")

test_mountain("myeongseongsan", ["Myeongseongsan", "Sanjeong Lake", "명성산"], ["Myeongseongsan", "Myeongseong", "Pocheon", "Sanjeong", "명성산", "산정호수"])
test_mountain("taebaeksan", ["Taebaeksan", "Cheonjedan", "태백산"], ["Taebaeksan", "Taebaek", "Cheonjedan", "태백산", "천제단"])
test_mountain("yushan", ["Yushan", "Jade Mountain Taiwan", "玉山"], ["Yushan", "Jade Mountain", "Paiyun", "Tataka", "玉山"])
test_mountain("xueshan", ["Xueshan", "Snow Mountain Taiwan", "雪山"], ["Xueshan", "Snow Mountain", "Shei-Pa", "369 Cabin", "雪山"])
test_mountain("yangmingshan", ["Yangmingshan", "Qixingshan", "陽明山"], ["Yangmingshan", "Qixingshan", "Qingtiangang", "陽明山"])
