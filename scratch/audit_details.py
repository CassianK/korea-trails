import glob
import re
from bs4 import BeautifulSoup

targets = [
    "unaksan-playbook.html",
    "naejangsan-playbook.html",
    "myeongseongsan-playbook.html",
    "gyeryongsan-playbook.html",
    "woraksan-playbook.html",
    "xueshan-playbook.html",
    "yangmingshan-playbook.html",
    "yushan-playbook.html",
    "deogyusan-playbook.html",
    "taebaeksan-playbook.html",
    "odaesan-playbook.html",
    "soyosan-playbook.html",
    "sikjangsan-playbook.html"
]

def find_points_section(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    
    # We want to search for specific sections or keywords
    keywords = ["추천 포인트", "포인트", "매력 포인트", "운영 포인트", "볼거리 정보", "계절별 볼거리",
                "Recommended Points", "Key Attractions", "Points", "Attraction Points", "Operational Points",
                "Attractions Information", "Season Attractions", "볼거리"]
    
    found_sections = []
    
    # Search for H2 or H3 containing these keywords
    for h in soup.find_all(["h2", "h3", "div"]):
        text = h.get_text().strip()
        if any(kw.lower() == text.lower() or text.endswith(kw) or text.startswith(kw) for kw in keywords):
            # check sibling list
            sibling = h.find_next_sibling()
            if sibling and sibling.name in ["ul", "ol"]:
                found_sections.append((h.name, text, str(sibling)[:300]))
            else:
                # check parent/child structures
                parent = h.parent
                if parent and parent.name == "div" and "card" in parent.get("class", []):
                    ul = parent.find("ul") or parent.find("ol")
                    if ul:
                        found_sections.append((h.name, text + " (in card)", str(ul)[:300]))
                        
    return found_sections

for target in targets:
    for prefix in ["", "en/"]:
        path = prefix + target
        try:
            sections = find_points_section(path)
            if sections:
                print(f"=== {path} ===")
                for sec in sections:
                    print(f"  Header: {sec[0]} | {sec[1]}")
                    print(f"  List: {sec[2]}\n")
        except FileNotFoundError:
            pass
