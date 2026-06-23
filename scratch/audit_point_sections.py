import glob
import re
from bs4 import BeautifulSoup

def audit_point_sections():
    files = sorted(glob.glob("*.html") + glob.glob("en/**/*.html", recursive=True))
    keywords = ["포인트", "볼거리 정보", "계절별 볼거리", "Key Points", "Recommended Points", "Points", "Attractions", "Scenic Spot", "Scenic Spots", "Highlights"]
    
    print(f"Auditing {len(files)} files...")
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        soup = BeautifulSoup(content, "html.parser")
        
        # Check headings or list headers
        found_matches = []
        for elem in soup.find_all(text=True):
            text = elem.strip()
            if not text:
                continue
            parent = elem.parent
            if parent.name in ["h2", "h3", "div", "span"] and any(kw.lower() in text.lower() for kw in keywords):
                # check if there's a list (ul or ol) near it
                found_matches.append(text)
                
        # Also check if it already has peak-grid or peak-card
        has_grid = len(soup.find_all(class_="peak-grid"))
        has_card = len(soup.find_all(class_="peak-card"))
        
        if found_matches or has_grid or has_card:
            print(f"[{file_path}]")
            print(f"  Keywords found: {found_matches}")
            print(f"  peak-grid: {has_grid}, peak-card: {has_card}")

if __name__ == "__main__":
    audit_point_sections()
