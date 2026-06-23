import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_DIR = "/Users/mac/korea-trails"

def get_mountain_details(m_id):
    # Hardcoded mapping for accuracy
    names_map = {
        "bukhansan": ("북한산", "Bukhansan National Park"),
        "deogyusan": ("덕유산", "Deogyusan National Park"),
        "dobongsan": ("도봉산", "Dobongsan National Park"),
        "gayasan": ("가야산", "Gayasan National Park"),
        "gyeryongsan": ("계룡산", "Gyeryongsan National Park"),
        "hallasan": ("한라산", "Hallasan National Park"),
        "jirisan": ("지리산", "Jirisan National Park"),
        "juwangsan": ("주왕산", "Juwangsan National Park"),
        "myeongseongsan": ("명성산", "Myeongseongsan Mountain"),
        "naejangsan": ("내장산", "Naejangsan National Park"),
        "odaesan": ("오대산", "Odaesan National Park"),
        "seoraksan": ("설악산", "Seoraksan National Park"),
        "sikjangsan": ("식장산", "Sikjangsan Mountain"),
        "sobaeksan": ("소백산", "Sobaeksan National Park"),
        "soyosan": ("소요산", "Soyosan Mountain"),
        "taebaeksan": ("태백산", "Taebaeksan National Park"),
        "wolchulsan": ("월출산", "Wolchulsan National Park"),
        "woraksan": ("월악산", "Woraksan National Park"),
        "xueshan": ("설산", "Xueshan (Snow Mountain)"),
        "yangmingshan": ("양명산", "Yangmingshan National Park"),
        "yushan": ("위산", "Yushan (Jade Mountain)"),
        "mudeungsan": ("무등산", "Mudeungsan National Park"),
        "chiaksan": ("치악산", "Chiaksan National Park"),
        "baekhaksan": ("백학산", "Baekhaksan Mountain"),
        "duryunsan": ("두륜산", "Duryunsan Provincial Park"),
        "minjusan": ("민주지산", "Minjujisan Mountain")
    }
    
    if m_id in names_map:
        return names_map[m_id][0], names_map[m_id][1]
    return m_id.capitalize(), m_id.capitalize() + " Mountain"

def draw_letter_spacing_text(draw, text, position, font, fill, spacing=10):
    x, y = position
    total_w = 0
    for char in text:
        char_w = draw.textlength(char, font=font)
        total_w += char_w + spacing
    total_w -= spacing
    
    start_x = x - total_w / 2
    curr_x = start_x
    for char in text:
        draw.text((curr_x, y), char, font=font, fill=fill)
        curr_x += draw.textlength(char, font=font) + spacing

def synthesize_og_card(m_id, is_brand=False):
    output_dir = os.path.join(WORKSPACE_DIR, "assets", "img")
    if is_brand:
        output_path = os.path.join(output_dir, "brand-og.png")
    else:
        output_path = os.path.join(output_dir, m_id, "og.png")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
    # 1. Create base canvas: 1200x630, deep navy (#0e1c34)
    navy_color = (14, 28, 52, 255)
    gold_color = (201, 162, 75, 255)       # #c9a24b
    light_gold = (217, 190, 120, 255)      # #d9be78
    
    img = Image.new("RGBA", (1200, 630), navy_color)
    draw = ImageDraw.Draw(img)
    
    # 2. Draw Ridge Apex Logo (Option A)
    # Centered X=600, S=2.5, X0=325, Y0=85
    S = 2.5
    X0 = 325
    Y0 = 85
    
    # Outer Triangle points
    tri_pts = [
        (X0 + 110 * S, Y0 + 26 * S),
        (X0 + 160 * S, Y0 + 116 * S),
        (X0 + 60 * S, Y0 + 116 * S)
    ]
    
    # Draw hollow triangle with stroke width 11
    draw.polygon(tri_pts, outline=gold_color, width=11)
    
    # Polyline ridge points
    ridge_pts = [
        (X0 + 74 * S, Y0 + 109 * S),
        (X0 + 92 * S, Y0 + 84 * S),
        (X0 + 102 * S, Y0 + 95 * S),
        (X0 + 122 * S, Y0 + 69 * S),
        (X0 + 146 * S, Y0 + 109 * S)
    ]
    
    # Draw polyline with stroke width 8
    for i in range(len(ridge_pts) - 1):
        draw.line([ridge_pts[i], ridge_pts[i+1]], fill=gold_color, width=8, joint="round")
        
    # 3. Typography
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 52)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 24)
        brand_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 16)
        ko_title_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 48)
        ko_subtitle_font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 22)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()
        ko_title_font = ImageFont.load_default()
        ko_subtitle_font = ImageFont.load_default()
        
    # Draw KOREA TRAILS brand text (spaced)
    draw_letter_spacing_text(draw, "KOREA TRAILS", (600, 440), brand_font, light_gold, spacing=6)
    
    if is_brand:
        # Brand Card Title
        draw_letter_spacing_text(draw, "대한민국 등산 플레이북", (600, 500), ko_title_font, (255, 255, 255, 255), spacing=2)
        draw_letter_spacing_text(draw, "Korea Trails Playbook Guide", (600, 560), subtitle_font, light_gold, spacing=2)
    else:
        # Mountain Specific Card Title
        ko_name, en_name = get_mountain_details(m_id)
        # Format Korean text with slight spacing
        draw_letter_spacing_text(draw, f"{ko_name} 플레이북", (600, 500), ko_title_font, (255, 255, 255, 255), spacing=3)
        draw_letter_spacing_text(draw, f"{en_name}  |  Course Guide", (600, 560), subtitle_font, light_gold, spacing=1)
        
    # Save image
    img.convert("RGB").save(output_path, "PNG")
    print(f"Synthesized OG Card saved to {output_path}")

def main():
    # 1. Synthesize brand-og.png
    synthesize_og_card("", is_brand=True)
    
    # 2. Synthesize all mountain-specific og.png cards
    mountains = [
        "bukhansan", "deogyusan", "dobongsan", "gayasan", "gyeryongsan", 
        "hallasan", "jirisan", "juwangsan", "myeongseongsan", "naejangsan", 
        "odaesan", "seoraksan", "sikjangsan", "sobaeksan", "soyosan", 
        "taebaeksan", "wolchulsan", "woraksan", "xueshan", "yangmingshan", 
        "yushan", "mudeungsan", "chiaksan", "duryunsan", "minjusan"
    ]
    
    for m in mountains:
        synthesize_og_card(m, is_brand=False)
        
    print("All OG Cards generated successfully!")

if __name__ == "__main__":
    main()
