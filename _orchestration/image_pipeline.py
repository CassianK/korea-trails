import os
import json
import urllib.request
import urllib.parse
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import pillow_avif

# Disable decompression bomb limit in PIL
Image.MAX_IMAGE_PIXELS = None

# Config files
CONFIG_PATH = "_orchestration/config.json"
INVENTORY_PATH = "_orchestration/inventory.json"
SELECTED_PATH = "_orchestration/photo-selected.json"
MANIFEST_PATH = "_orchestration/image-manifest.json"
CREDITS_PATH = "CREDITS.md"

# Load config
try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        UNSPLASH_ACCESS_KEY = config.get("UNSPLASH_ACCESS_KEY")
except Exception as e:
    print(f"Error loading config.json: {e}")
    UNSPLASH_ACCESS_KEY = None

# Load inventory and selected photos
with open(INVENTORY_PATH, "r") as f:
    inventory = json.load(f)
mountains_map = {m["id"]: m for m in inventory}

with open(SELECTED_PATH, "r") as f:
    selected_photos = json.load(f)

# Load existing manifest if present
existing_manifest = {}
if os.path.exists(MANIFEST_PATH):
    try:
        with open(MANIFEST_PATH, "r") as f:
            manifest_list = json.load(f)
            for entry in manifest_list:
                key = (entry["mountain_id"], entry["role"])
                existing_manifest[key] = entry
    except Exception as e:
        print(f"Warning loading existing manifest: {e}")

# Create assets directory if not exists
os.makedirs("assets/img", exist_ok=True)

# SSL context
ssl_context = ssl._create_unverified_context()

def trigger_unsplash_download(url_trigger):
    if not UNSPLASH_ACCESS_KEY or not url_trigger:
        return
    try:
        req = urllib.request.Request(url_trigger)
        req.add_header("Authorization", f"Client-ID {UNSPLASH_ACCESS_KEY}")
        req.add_header("Accept-Version", "v1")
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            response.read() # Read and discard
    except Exception as e:
        print(f"Unsplash download trigger warning: {e}")

def download_image(url, photo_id, source):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            return response.read()
    except Exception as e:
        raise Exception(f"Download failed for {source} ID {photo_id} from {url}: {e}")

def generate_alt_texts(m, role, geo_hint):
    name_ko = m["name_ko"]
    name_en = m["name_en"]
    geo_lower = (geo_hint or "").lower()
    
    # Landmark match within geo_hint
    matched_lm_ko = None
    matched_lm_en = None
    
    # Hardcoded/mapped common landmarks translation for cleaner output
    landmark_translation = {
        "ulsanbawi": ("울산바위", "Ulsanbawi"),
        "daecheongbong": ("대청봉", "Daecheongbong"),
        "공룡능선": ("공룡능선", "Dinosaur Ridge"),
        "dinosaur ridge": ("공룡능선", "Dinosaur Ridge"),
        "baengnokdam": ("백록담", "Baengnokdam"),
        "백록담": ("백록담", "Baengnokdam"),
        "cheonwangbong": ("천왕봉", "Cheonwangbong"),
        "천왕봉": ("천왕봉", "Cheonwangbong"),
        "baegundae": ("백운대", "Baegundae"),
        "백운대": ("백운대", "Baegundae"),
        "insubong": ("인수봉", "Insubong"),
        "인수봉": ("인수봉", "Insubong"),
        "birobong": ("비로봉", "Birobong"),
        "비로봉": ("비로봉", "Birobong"),
        "sanjeong": ("산정호수", "Sanjeong Lake"),
        "yushan": ("위산 주봉", "Yushan Main Peak"),
        "jade mountain": ("위산 주봉", "Yushan Main Peak"),
        "xueshan": ("설산 주봉", "Xueshan Main Peak"),
        "snow mountain": ("설산 주봉", "Xueshan Main Peak"),
        "yangmingshan": ("양명산", "Yangmingshan"),
        "qingtiangang": ("칭티엔강 초원", "Qingtiangang Grassland")
    }
    
    for key, (ko, en) in landmark_translation.items():
        if key in geo_lower:
            matched_lm_ko = ko
            matched_lm_en = en
            break

    if role == "hero":
        if matched_lm_ko:
            alt_ko = f"{name_ko} 국립공원의 대표 명소인 {matched_lm_ko}와 아름다운 산세 풍경"
            alt_en = f"Beautiful landscape of {matched_lm_en} and majestic mountain ridges in {name_en} National Park"
        else:
            alt_ko = f"{name_ko} 정상과 웅장한 산세가 어우러진 대자연 풍경"
            alt_en = f"Majestic natural landscape of {name_en} mountain peaks and ridges"
    elif role == "gallery_1":
        alt_ko = f"{name_ko} 등산로를 따라 펼쳐진 수려한 주변 경관"
        alt_en = f"Scenic hiking trail and beautiful surroundings of {name_en}"
    elif role == "gallery_2":
        if matched_lm_ko:
            alt_ko = f"{name_ko} 산행 중 마주하는 {matched_lm_ko}의 수려한 모습"
            alt_en = f"Scenic view of {matched_lm_en} encountered during the {name_en} climb"
        else:
            alt_ko = f"{name_ko} 국립공원의 사계절 자연미가 느껴지는 풍경"
            alt_en = f"Beautiful landscape showcasing the natural beauty of {name_en} National Park"
    elif role == "gallery_3":
        alt_ko = f"{name_ko} 산등성이와 푸른 하늘이 조화를 이루는 자연 경관"
        alt_en = f"Harmonious view of {name_en} mountain ridges under a clear sky"
    elif role == "gallery_4":
        alt_ko = f"{name_ko} 숲길과 기암괴석이 어우러진 아름다운 비경"
        alt_en = f"Beautiful scenery of lush forests and rugged rocks in {name_en}"
    else:
        alt_ko = f"{name_ko}의 아름다운 자연 풍경"
        alt_en = f"Beautiful nature scenery of {name_en}"
        
    return alt_ko, alt_en

def save_image_with_budget(img, output_path, format_name, base_quality=80, max_size_kb=400):
    quality = base_quality
    # PIL expects 'jpeg' for JPG, 'webp' for WebP, 'avif' for AVIF
    ext_format = format_name.lower()
    if ext_format == "jpg":
        ext_format = "jpeg"
        
    while quality > 30:
        # Save to file
        img.save(output_path, format=ext_format, quality=quality, keep_rgb=True if ext_format == "avif" else None)
        sz_kb = os.path.getsize(output_path) / 1024.0
        if sz_kb <= max_size_kb:
            return sz_kb
        quality -= 5
        
    return os.path.getsize(output_path) / 1024.0

def check_files_exist(m_id, role):
    role_map = {
        "hero": "hero",
        "gallery_1": "g1",
        "gallery_2": "g2",
        "gallery_3": "g3",
        "gallery_4": "g4"
    }
    prefix = role_map[role]
    m_dir = f"assets/img/{m_id}"
    
    if role == "hero":
        widths = [640, 1024, 1600, 2400]
        for w in widths:
            for fmt in ["avif", "webp", "jpg"]:
                if not os.path.exists(f"{m_dir}/{prefix}-{w}.{fmt}"):
                    return False
        return True
    else:
        for fmt in ["avif", "webp", "jpg"]:
            if not os.path.exists(f"{m_dir}/{prefix}.{fmt}"):
                return False
        if prefix == "g1":
            if not os.path.exists(f"{m_dir}/g1-640.webp") or not os.path.exists(f"{m_dir}/g1-640.jpg"):
                return False
        return True

def process_single_photo(photo_data):
    m_id = photo_data["mountain_id"]
    photo_id = photo_data["photo_id"]
    source = photo_data["source"]
    role = photo_data["role"]
    url_full = photo_data["url_full"]
    url_trigger = photo_data["url_download_trigger"]
    geo_hint = photo_data["geo_hint"]
    
    m = mountains_map[m_id]
    m_dir = f"assets/img/{m_id}"
    
    # Check if files already exist and we have manifest entry
    key = (m_id, role)
    if check_files_exist(m_id, role) and key in existing_manifest:
        print(f"[{m_id}] Skipping {role} (files already exist)")
        return existing_manifest[key]
        
    print(f"[{m_id}] Starting processing for {role} (ID: {photo_id} from {source})")
    
    # 1. Trigger Unsplash download endpoint if Unsplash
    if source.lower() == "unsplash" and url_trigger:
        trigger_unsplash_download(url_trigger)
        
    # 2. Download original image
    try:
        img_bytes = download_image(url_full, photo_id, source)
    except Exception as e:
        print(f"Error downloading photo {photo_id}: {e}")
        return None
        
    # Save raw bytes to a temp file
    temp_raw_path = f"{m_dir}/temp_raw_{role}.jpg"
    with open(temp_raw_path, "wb") as f:
        f.write(img_bytes)
        
    # 3. Process and resize
    manifest_entry = None
    
    try:
        with Image.open(temp_raw_path) as img:
            # Ensure RGB mode
            if img.mode != "RGB":
                img = img.convert("RGB")
                
            orig_w, orig_h = img.size
            
            # Map role to filename prefix
            role_map = {
                "hero": "hero",
                "gallery_1": "g1",
                "gallery_2": "g2",
                "gallery_3": "g3",
                "gallery_4": "g4"
            }
            prefix = role_map[role]
            
            alt_ko, alt_en = generate_alt_texts(m, role, geo_hint)
            
            if role == "hero":
                # Generate 4 widths: [640, 1024, 1600, 2400]
                widths = [640, 1024, 1600, 2400]
                for w in widths:
                    # Calculate height preserving aspect ratio
                    h = int(orig_h * (w / orig_w))
                    img_resized = img.resize((w, h), Image.Resampling.LANCZOS)
                    
                    # Target filenames
                    for fmt in ["avif", "webp", "jpg"]:
                        out_path = f"{m_dir}/{prefix}-{w}.{fmt}"
                        # Enforce budget of 400KB for hero images
                        save_image_with_budget(img_resized, out_path, fmt, base_quality=80, max_size_kb=400)
                        
                manifest_entry = {
                    "mountain_id": m_id,
                    "role": role,
                    "files": {
                        "avif": f"assets/img/{m_id}/{prefix}.avif",
                        "webp": f"assets/img/{m_id}/{prefix}.webp",
                        "jpg":  f"assets/img/{m_id}/{prefix}.jpg"
                    },
                    "widths": widths,
                    "alt_ko": alt_ko,
                    "alt_en": alt_en,
                    "credit": {
                        "author": photo_data["author"],
                        "source": source,
                        "url": photo_data["author_url"]
                    }
                }
            else:
                # Gallery images: single size, max width 1600px
                w = min(1600, orig_w)
                h = int(orig_h * (w / orig_w))
                img_resized = img.resize((w, h), Image.Resampling.LANCZOS)
                
                for fmt in ["avif", "webp", "jpg"]:
                    out_path = f"{m_dir}/{prefix}.{fmt}"
                    save_image_with_budget(img_resized, out_path, fmt, base_quality=80, max_size_kb=400)
                    
                # If gallery_1, we ALSO need g1-640 for the index card thumbnail
                if prefix == "g1":
                    w_card = 640
                    h_card = int(orig_h * (w_card / orig_w))
                    img_card = img.resize((w_card, h_card), Image.Resampling.LANCZOS)
                    
                    # Generate only WebP and JPG for the thumbnail
                    save_image_with_budget(img_card, f"{m_dir}/g1-640.webp", "webp", base_quality=75, max_size_kb=100)
                    save_image_with_budget(img_card, f"{m_dir}/g1-640.jpg", "jpg", base_quality=80, max_size_kb=100)
                    
                manifest_entry = {
                    "mountain_id": m_id,
                    "role": role,
                    "files": {
                        "avif": f"assets/img/{m_id}/{prefix}.avif",
                        "webp": f"assets/img/{m_id}/{prefix}.webp",
                        "jpg":  f"assets/img/{m_id}/{prefix}.jpg"
                    },
                    "widths": [],
                    "alt_ko": alt_ko,
                    "alt_en": alt_en,
                    "credit": {
                        "author": photo_data["author"],
                        "source": source,
                        "url": photo_data["author_url"]
                    }
                }
                
    except Exception as e:
        print(f"Error processing image {photo_id}: {e}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_raw_path):
            os.remove(temp_raw_path)
            
    print(f"[{m_id}] Completed processing for {role} (ID: {photo_id})")
    return manifest_entry

def main():
    print(f"Starting image processing pipeline for {len(selected_photos)} photos...")
    
    # Process photos in parallel
    results = []
    # Use max_workers=8 to run parallel downloads and image processing
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_single_photo, photo): photo for photo in selected_photos}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                results.append(res)
                
    # Sort results for stability
    results.sort(key=lambda x: (x["mountain_id"], x["role"]))
    
    # Save manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {MANIFEST_PATH} with {len(results)} entries.")
    
    # Generate CREDITS.md
    generate_credits_file(results)

def generate_credits_file(manifest_entries):
    print("Generating CREDITS.md...")
    
    # Group by mountain
    by_mountain = {}
    for entry in manifest_entries:
        m_id = entry["mountain_id"]
        if m_id not in by_mountain:
            by_mountain[m_id] = []
        by_mountain[m_id].append(entry)
        
    credits_content = """# Photo Credits & Attributions

This document acknowledges and credits the talented photographers whose beautiful work brings the Korea Trails site to life. All photos are used under the free Unsplash License or Pexels License.

"""
    
    # Sort mountains alphabetically/by inventory order
    for m_id in sorted(by_mountain.keys()):
        m_name = mountains_map[m_id]["name_ko"] + " (" + mountains_map[m_id]["name_en"] + ")"
        credits_content += f"## {m_name}\n\n"
        
        for entry in sorted(by_mountain[m_id], key=lambda x: x["role"]):
            role = entry["role"]
            credit = entry["credit"]
            author = credit["author"]
            source = credit["source"]
            url = credit["url"]
            
            role_display = "Hero Header" if role == "hero" else f"Gallery {role.split('_')[1]}"
            credits_content += f"- **{role_display}**: Photo by [{author}]({url}) via [{source}]({source.lower() == 'unsplash' and 'https://unsplash.com' or 'https://pexels.com'}).\n"
            
        credits_content += "\n"
        
    with open(CREDITS_PATH, "w", encoding="utf-8") as f:
        f.write(credits_content)
    print(f"Successfully generated {CREDITS_PATH}.")

if __name__ == "__main__":
    main()
