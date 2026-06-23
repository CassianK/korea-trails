import os
import re

WORKSPACE_DIR = "/Users/mac/korea-trails"

# 1. Drawer Menu Replacements
ko_drawer_target = """    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
      <a href="index.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        홈
      </a>
      <a href="index.html#mountainGrid" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="m8 3-7 18h22L16 7l-4 7-4-11Z"></path></svg>
        명산 목록
      </a>
      <a href="sitemap.html#regions" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        지역별 탐색
      </a>
      <a href="sitemap.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        사이트맵
      </a>
      </nav>"""

ko_drawer_replacement = """    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
      <a href="index.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        홈
      </a>
      <a href="index.html#mountainGrid" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="m8 3-7 18h22L16 7l-4 7-4-11Z"></path></svg>
        명산 목록
      </a>
      <a href="cycling.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/></svg>
        사이클링
      </a>
      <a href="map.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        인터랙티브 지도
      </a>
      <a href="sitemap.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        사이트맵
      </a>
      </nav>"""

en_drawer_target = """    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
      <a href="../index.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        Home
      </a>
      <a href="../index.html#mountainGrid" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="m8 3-7 18h22L16 7l-4 7-4-11Z"></path></svg>
        Mountain List
      </a>
      <a href="sitemap.html#regions" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        By Region
      </a>
      <a href="sitemap.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        Sitemap
      </a>
      </nav>"""

en_drawer_replacement = """    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
      <a href="../index.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        Home
      </a>
      <a href="../index.html#mountainGrid" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="m8 3-7 18h22L16 7l-4 7-4-11Z"></path></svg>
        Mountain List
      </a>
      <a href="cycling.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/></svg>
        Cycling
      </a>
      <a href="map.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        Interactive Map
      </a>
      <a href="sitemap.html" class="nav-drawer-link">
        <svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
        Sitemap
      </a>
    </nav>"""

# 2. Header Navigation Replacements (Index / Main pages)
ko_header_target = """<nav aria-label="메인 네비게이션" class="header-nav">
<a class="header-nav-link active" href="index.html">홈</a>
<a class="header-nav-link" href="#mountainGrid">명산 탐색</a>
</nav>"""

ko_header_replacement = """<nav aria-label="메인 네비게이션" class="header-nav">
<a class="header-nav-link active" href="index.html">홈</a>
<a class="header-nav-link" href="index.html#mountainGrid">명산 탐색</a>
<a class="header-nav-link" href="cycling.html">사이클링</a>
<a class="header-nav-link" href="map.html">인터랙티브 지도</a>
</nav>"""

en_header_target = """<nav aria-label="Main Navigation" class="header-nav">
<a class="header-nav-link active" href="index.html">Home</a>
<a class="header-nav-link" href="#mountainGrid">Explore Mountains</a>
</nav>"""

en_header_replacement = """<nav aria-label="Main Navigation" class="header-nav">
<a class="header-nav-link active" href="index.html">Home</a>
<a class="header-nav-link" href="index.html#mountainGrid">Explore Mountains</a>
<a class="header-nav-link" href="cycling.html">Cycling</a>
<a class="header-nav-link" href="map.html">Interactive Map</a>
</nav>"""

# 3. Footer Sitemap Replacements
ko_footer_target = """    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">대만</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">위산</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">설산</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">양명산</a>
      </div>
    </div>"""

ko_footer_replacement = """    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">대만</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">위산</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">설산</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">양명산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">테마별</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="cycling.html" style="color: var(--muted); text-decoration: none;">사이클링 코스</a>
        <a href="map.html" style="color: var(--muted); text-decoration: none;">인터랙티브 지도</a>
      </div>
    </div>"""

en_footer_target = """    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Taiwan</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">Yushan</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">Xueshan</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">Yangmingshan</a>
      </div>
    </div>"""

en_footer_replacement = """    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Taiwan</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">Yushan</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">Xueshan</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">Yangmingshan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Themes</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="cycling.html" style="color: var(--muted); text-decoration: none;">Cycling Routes</a>
        <a href="map.html" style="color: var(--muted); text-decoration: none;">Interactive Map</a>
      </div>
    </div>"""

def process_file(filepath):
    is_en = "en/" in filepath
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Update Drawer
    if is_en:
        # Standardize spaces for matching
        norm_target = re.sub(r'\s+', ' ', en_drawer_target)
        # Find matches ignoring whitespace differences
        match = re.search(r'<nav class="nav-drawer-menu".*?</nav>', content, re.DOTALL)
        if match and "cycling.html" not in match.group(0):
            content = content.replace(match.group(0), en_drawer_replacement)
            modified = True
    else:
        match = re.search(r'<nav class="nav-drawer-menu".*?</nav>', content, re.DOTALL)
        if match and "cycling.html" not in match.group(0):
            content = content.replace(match.group(0), ko_drawer_replacement)
            modified = True

    # 2. Update Header Nav (only on index, sitemap, cycling, map)
    if any(x in filepath for x in ["index.html", "sitemap.html"]):
        if is_en:
            if en_header_target in content:
                content = content.replace(en_header_target, en_header_replacement)
                modified = True
        else:
            if ko_header_target in content:
                content = content.replace(ko_header_target, ko_header_replacement)
                modified = True

    # 3. Update Footer
    if is_en:
        if en_footer_target in content:
            content = content.replace(en_footer_target, en_footer_replacement)
            modified = True
    else:
        if ko_footer_target in content:
            content = content.replace(ko_footer_target, ko_footer_replacement)
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    # Process root files
    for f in os.listdir(WORKSPACE_DIR):
        if f.endswith(".html"):
            process_file(os.path.join(WORKSPACE_DIR, f))
            
    # Process en/ files
    en_dir = os.path.join(WORKSPACE_DIR, "en")
    if os.path.exists(en_dir):
        for f in os.listdir(en_dir):
            if f.endswith(".html"):
                process_file(os.path.join(en_dir, f))

if __name__ == "__main__":
    main()
