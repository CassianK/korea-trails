import urllib.request
import json
import ssl

def test_unsplash():
    url = "https://api.unsplash.com/search/photos?query=Yangmingshan&orientation=landscape&per_page=1"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Client-ID MrzCYdY-9WA151pj1UHYURT8RLjDCcD8uqji_3Y7Eco")
    req.add_header("Accept-Version", "v1")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            print("=== UNSPLASH SAMPLE RESULT ===")
            if data['results']:
                photo = data['results'][0]
                print(json.dumps(photo, indent=2))
            else:
                print("No results found on Unsplash")
    except Exception as e:
        print("Unsplash error:", e)

def test_pexels():
    url = "https://api.pexels.com/v1/search?query=Yangmingshan&orientation=landscape&per_page=1"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "KWYEYD54GanmYAye7HULjec3KpkxV8EFMvfbiXOD1FHf1yT22Zrm2dxy")
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            print("=== PEXELS SAMPLE RESULT ===")
            if data['photos']:
                photo = data['photos'][0]
                print(json.dumps(photo, indent=2))
            else:
                print("No results found on Pexels")
    except Exception as e:
        print("Pexels error:", e)

if __name__ == "__main__":
    test_unsplash()
    print("\n" + "="*40 + "\n")
    test_pexels()
