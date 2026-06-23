import re
import os
import glob

# Playbooks names
mountains = [
    "bukhansan", "chiaksan", "deogyusan", "dobongsan", "duryunsan", "gayasan",
    "gyeryongsan", "hallasan", "jirisan", "juwangsan", "minjusan", "mudeungsan",
    "myeongseongsan", "naejangsan", "odaesan", "seoraksan", "sikjangsan", "sobaeksan",
    "soyosan", "taebaeksan", "unaksan", "wolchulsan", "woraksan", "xueshan",
    "yangmingshan", "yushan"
]

# All pages (KR + EN)
kr_pages = ["index.html", "sitemap.html"] + [f"{m}-playbook.html" for m in mountains]
en_pages = ["en/index.html", "en/sitemap.html"] + [f"en/{m}-playbook.html" for m in mountains]

def get_footer_html(is_en=False):
    if is_en:
        return """<footer style="border-top:1px solid var(--border); padding: var(--space-8) var(--space-6); background-color: var(--surface); margin-top: var(--space-12);">
<div class="wrap">
  <div class="footer-sitemap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: var(--space-6); text-align: left; margin-bottom: var(--space-8); border-bottom: 1px solid var(--border); padding-bottom: var(--space-8);">
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Gyeonggi/Seoul</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="bukhansan-playbook.html" style="color: var(--muted); text-decoration: none;">Bukhansan</a>
        <a href="dobongsan-playbook.html" style="color: var(--muted); text-decoration: none;">Dobongsan</a>
        <a href="myeongseongsan-playbook.html" style="color: var(--muted); text-decoration: none;">Myeongseongsan</a>
        <a href="soyosan-playbook.html" style="color: var(--muted); text-decoration: none;">Soyosan</a>
        <a href="unaksan-playbook.html" style="color: var(--muted); text-decoration: none;">Unaksan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Gangwon</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="seoraksan-playbook.html" style="color: var(--muted); text-decoration: none;">Seoraksan</a>
        <a href="chiaksan-playbook.html" style="color: var(--muted); text-decoration: none;">Chiaksan</a>
        <a href="odaesan-playbook.html" style="color: var(--muted); text-decoration: none;">Odaesan</a>
        <a href="taebaeksan-playbook.html" style="color: var(--muted); text-decoration: none;">Taebaeksan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Chungcheong</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="sobaeksan-playbook.html" style="color: var(--muted); text-decoration: none;">Sobaeksan</a>
        <a href="gyeryongsan-playbook.html" style="color: var(--muted); text-decoration: none;">Gyeryongsan</a>
        <a href="minjusan-playbook.html" style="color: var(--muted); text-decoration: none;">Minjujisan</a>
        <a href="sikjangsan-playbook.html" style="color: var(--muted); text-decoration: none;">Sikjangsan</a>
        <a href="woraksan-playbook.html" style="color: var(--muted); text-decoration: none;">Woraksan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Jeolla</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="jirisan-playbook.html" style="color: var(--muted); text-decoration: none;">Jirisan</a>
        <a href="naejangsan-playbook.html" style="color: var(--muted); text-decoration: none;">Naejangsan</a>
        <a href="deogyusan-playbook.html" style="color: var(--muted); text-decoration: none;">Deogyusan</a>
        <a href="wolchulsan-playbook.html" style="color: var(--muted); text-decoration: none;">Wolchulsan</a>
        <a href="mudeungsan-playbook.html" style="color: var(--muted); text-decoration: none;">Mudeungsan</a>
        <a href="duryunsan-playbook.html" style="color: var(--muted); text-decoration: none;">Duryunsan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Gyeongsang / Jeju</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="gayasan-playbook.html" style="color: var(--muted); text-decoration: none;">Gayasan</a>
        <a href="juwangsan-playbook.html" style="color: var(--muted); text-decoration: none;">Juwangsan</a>
        <a href="hallasan-playbook.html" style="color: var(--muted); text-decoration: none;">Hallasan</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">Taiwan</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">Yushan</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">Xueshan</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">Yangmingshan</a>
      </div>
    </div>
  </div>

  <p style="font-size: var(--text-xs); color: var(--muted); line-height: 1.8; text-align: center; max-width: 800px; margin: 0 auto;">
    Korea Trails — National Hiking Playbook · National Park Reservation: <a href="https://reservation.knps.or.kr" rel="noopener" target="_blank" style="color: var(--primary); text-decoration: underline;">knps.or.kr</a><br/>
    Some of the hiking photos and tracking videos on this site are original works photographed and produced by Dokyung Kim(김도경), with the videos published on the YouTube channel Dokyung Kim (@DK2560). They may be used for non-commercial purposes only, and credit must be given to the source and author (Dokyung Kim(김도경)) upon use. (CC BY-NC 4.0 standard applied)<br/>
    © 2026 Korea Trails. All Rights Reserved.
  </p>
</div>
</footer>
"""
    else:
        return """<footer style="border-top:1px solid var(--border); padding: var(--space-8) var(--space-6); background-color: var(--surface); margin-top: var(--space-12);">
<div class="wrap">
  <div class="footer-sitemap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: var(--space-6); text-align: left; margin-bottom: var(--space-8); border-bottom: 1px solid var(--border); padding-bottom: var(--space-8);">
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">경기/서울</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="bukhansan-playbook.html" style="color: var(--muted); text-decoration: none;">북한산</a>
        <a href="dobongsan-playbook.html" style="color: var(--muted); text-decoration: none;">도봉산</a>
        <a href="myeongseongsan-playbook.html" style="color: var(--muted); text-decoration: none;">명성산</a>
        <a href="soyosan-playbook.html" style="color: var(--muted); text-decoration: none;">소요산</a>
        <a href="unaksan-playbook.html" style="color: var(--muted); text-decoration: none;">운악산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">강원</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="seoraksan-playbook.html" style="color: var(--muted); text-decoration: none;">설악산</a>
        <a href="chiaksan-playbook.html" style="color: var(--muted); text-decoration: none;">치악산</a>
        <a href="odaesan-playbook.html" style="color: var(--muted); text-decoration: none;">오대산</a>
        <a href="taebaeksan-playbook.html" style="color: var(--muted); text-decoration: none;">태백산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">충청</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="sobaeksan-playbook.html" style="color: var(--muted); text-decoration: none;">소백산</a>
        <a href="gyeryongsan-playbook.html" style="color: var(--muted); text-decoration: none;">계룡산</a>
        <a href="minjusan-playbook.html" style="color: var(--muted); text-decoration: none;">민주지산</a>
        <a href="sikjangsan-playbook.html" style="color: var(--muted); text-decoration: none;">식장산</a>
        <a href="woraksan-playbook.html" style="color: var(--muted); text-decoration: none;">월악산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">전라</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="jirisan-playbook.html" style="color: var(--muted); text-decoration: none;">지리산</a>
        <a href="naejangsan-playbook.html" style="color: var(--muted); text-decoration: none;">내장산</a>
        <a href="deogyusan-playbook.html" style="color: var(--muted); text-decoration: none;">덕유산</a>
        <a href="wolchulsan-playbook.html" style="color: var(--muted); text-decoration: none;">월출산</a>
        <a href="mudeungsan-playbook.html" style="color: var(--muted); text-decoration: none;">무등산</a>
        <a href="duryunsan-playbook.html" style="color: var(--muted); text-decoration: none;">두륜산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">경상 / Jeju</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="gayasan-playbook.html" style="color: var(--muted); text-decoration: none;">가야산</a>
        <a href="juwangsan-playbook.html" style="color: var(--muted); text-decoration: none;">주왕산</a>
        <a href="hallasan-playbook.html" style="color: var(--muted); text-decoration: none;">한라산</a>
      </div>
    </div>
    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">대만</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
        <a href="yushan-playbook.html" style="color: var(--muted); text-decoration: none;">위산</a>
        <a href="xueshan-playbook.html" style="color: var(--muted); text-decoration: none;">설산</a>
        <a href="yangmingshan-playbook.html" style="color: var(--muted); text-decoration: none;">양명산</a>
      </div>
    </div>
  </div>

  <p style="font-size: var(--text-xs); color: var(--muted); line-height: 1.8; text-align: center; max-width: 800px; margin: 0 auto;">
    Korea Trails — 전국 등산 플레이북 · 국립공원 탐방 예약: <a href="https://reservation.knps.or.kr" rel="noopener" target="_blank" style="color: var(--primary); text-decoration: underline;">knps.or.kr</a><br/>
    본 사이트의 일부 등산 사진과 트래킹 영상은 Dokyung Kim(김도경)이 직접 촬영·제작한 저작물이며, 영상은 유튜브 채널 Dokyung Kim (@DK2560)에 게시되어 있습니다. 비상업적 목적에 한해 이용할 수 있으며, 이용 시 반드시 출처와 저작자(Dokyung Kim(김도경))를 표시해야 합니다. (CC BY-NC 4.0 준용)<br/>
    © 2026 Korea Trails. All Rights Reserved.
  </p>
</div>
</footer>
"""

def get_drawer_html(is_en=False):
    if is_en:
        return """
<!-- Navigation Drawer (Hamburger Menu) -->
<div id="navDrawer" class="nav-drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Navigation Menu">
  <div class="nav-drawer-overlay" tabindex="-1"></div>
  <div class="nav-drawer-content">
    <div class="nav-drawer-header">
      <div class="nav-drawer-logo">
        <svg aria-label="Korea Trails" class="logo-svg" height="30" role="img" viewbox="0 0 40 40" width="30">
          <defs><lineargradient id="kt-gold-drawer" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0" stop-color="#f1d98a"></stop><stop offset=".5" stop-color="#c9a24b"></stop><stop offset="1" stop-color="#9c7a2e"></stop>
          </lineargradient></defs>
          <rect fill="#0e1c34" height="40" rx="9" width="40"></rect>
          <path d="M20 8 L33 31 L7 31 Z" fill="none" stroke="url(#kt-gold-drawer)" stroke-linejoin="round" stroke-width="2.2"></path>
          <polyline fill="none" points="11,28 16,21.5 19,24.5 24.5,17 29,28" stroke="url(#kt-gold-drawer)" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></polyline>
        </svg>
        <span class="nav-drawer-logo-text">Korea Trails</span>
      </div>
      <button aria-label="Close Menu" class="nav-drawer-close-btn" id="navDrawerCloseBtn">
        <svg fill="none" height="20" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="20"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>
    
    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
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
      </nav>
    
    <div class="nav-drawer-divider"></div>
    
    <div class="nav-drawer-footer">
      <div class="nav-drawer-section-title">Settings</div>
      <div class="nav-drawer-settings">
        <button aria-label="Toggle Theme" class="drawer-theme-toggle" id="drawerThemeBtn">
          <span class="theme-icon"><svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></span>
          <span class="theme-label">Dark/Light Mode</span>
        </button>
        <div class="drawer-lang-toggle">
          <span class="lang-label">Language</span>
          <div class="lang-toggle">
            <button aria-label="Korean" aria-pressed="false" class="lang-btn" onclick="changeLanguage('ko')">KO</button>
            <button aria-label="English" aria-pressed="true" class="lang-btn active" onclick="changeLanguage('en')">EN</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""
    else:
        return """
<!-- Navigation Drawer (Hamburger Menu) -->
<div id="navDrawer" class="nav-drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Navigation Menu">
  <div class="nav-drawer-overlay" tabindex="-1"></div>
  <div class="nav-drawer-content">
    <div class="nav-drawer-header">
      <div class="nav-drawer-logo">
        <svg aria-label="Korea Trails" class="logo-svg" height="30" role="img" viewbox="0 0 40 40" width="30">
          <defs><lineargradient id="kt-gold-drawer" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0" stop-color="#f1d98a"></stop><stop offset=".5" stop-color="#c9a24b"></stop><stop offset="1" stop-color="#9c7a2e"></stop>
          </lineargradient></defs>
          <rect fill="#0e1c34" height="40" rx="9" width="40"></rect>
          <path d="M20 8 L33 31 L7 31 Z" fill="none" stroke="url(#kt-gold-drawer)" stroke-linejoin="round" stroke-width="2.2"></path>
          <polyline fill="none" points="11,28 16,21.5 19,24.5 24.5,17 29,28" stroke="url(#kt-gold-drawer)" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></polyline>
        </svg>
        <span class="nav-drawer-logo-text">Korea Trails</span>
      </div>
      <button aria-label="메뉴 닫기" class="nav-drawer-close-btn" id="navDrawerCloseBtn">
        <svg fill="none" height="20" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="20"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    </div>
    
    <nav class="nav-drawer-menu" aria-label="Drawer Navigation">
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
      </nav>
    
    <div class="nav-drawer-divider"></div>
    
    <div class="nav-drawer-footer">
      <div class="nav-drawer-section-title">설정</div>
      <div class="nav-drawer-settings">
        <button aria-label="테마 전환" class="drawer-theme-toggle" id="drawerThemeBtn">
          <span class="theme-icon"><svg fill="none" height="18" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="18"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg></span>
          <span class="theme-label">다크/라이트 모드</span>
        </button>
        <div class="drawer-lang-toggle">
          <span class="lang-label">언어 (Language)</span>
          <div class="lang-toggle">
            <button aria-label="한국어" aria-pressed="true" class="lang-btn active" onclick="changeLanguage('ko')">KO</button>
            <button aria-label="English" aria-pressed="false" class="lang-btn" onclick="changeLanguage('en')">EN</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

def process_file(file_path):
    is_en = file_path.startswith("en/")
    home_link = "../index.html" if is_en else "index.html"
    rel_path = "../" if is_en else ""

    print(f"Processing: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Avoid processing if sitemap footer or drawer script is already present
    if "nav-drawer.js" in content and "footer-sitemap" in content:
        print(f"  Already processed (skipped).")
        return False

    # 1. Update logo to link
    # Style A: <div class="header-logo">
    logo_style_a = r'(<div class="header-logo">)(.*?)(</div>\s*(<div class="header-actions">|<div class="lang-toggle">))'
    # Style B: <div class="logo-wrap"> with <a class="logo-text"
    # We'll first change <a class="logo-text" to <span class="logo-text" to avoid nesting.
    content = re.sub(
        r'<div class="logo-wrap">(.*?)<a class="logo-text" href="index.html">(.*?)</a>(.*?)</div>',
        rf'<a class="logo-wrap" href="{home_link}">\1<span class="logo-text">\2</span>\3</a>',
        content,
        flags=re.DOTALL
    )
    # If logo-wrap has a span:
    content = re.sub(
        r'<div class="logo-wrap">(.*?)</div>',
        rf'<a class="logo-wrap" href="{home_link}">\1</a>',
        content,
        flags=re.DOTALL
    )

    # Style C: <div class="brand">
    content = re.sub(
        r'<div class="brand">(.*?)</div>(\s*<div class="lang-toggle">)',
        rf'<a class="brand" href="{home_link}">\1</a>\2',
        content,
        flags=re.DOTALL
    )

    # Convert header-logo div to anchor link (Style A)
    def logo_repl_a(match):
        prefix = match.group(1).replace('<div', '<a')
        prefix = prefix.replace('class="header-logo"', f'class="header-logo" href="{home_link}"')
        content_inner = match.group(2)
        suffix = match.group(3).replace('</div>', '</a>')
        return prefix + content_inner + suffix

    content, count_a = re.subn(logo_style_a, logo_repl_a, content, flags=re.DOTALL)

    # 2. Add Hamburger Button to header
    # Check if hamburger button is already there
    if "menuToggleBtn" not in content:
        # Determine insertion point
        btn_aria = "Open Navigation Menu" if is_en else "메뉴 열기"
        btn_html = f"""  <button aria-label="{btn_aria}" aria-expanded="false" aria-controls="navDrawer" class="menu-toggle-btn" id="menuToggleBtn">
    <svg fill="none" height="20" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="20"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
  </button>\n"""

        if '<div class="header-actions">' in content:
            content = content.replace(
                '</div>\n</header>',
                f'{btn_html}</div>\n</header>'
            ).replace(
                '</div></header>',
                f'{btn_html}</div></header>'
            )
        elif '<div class="header-right">' in content:
            content = content.replace(
                '</div>\n</header>',
                f'{btn_html}</div>\n</header>'
            ).replace(
                '</div></header>',
                f'{btn_html}</div></header>'
            )
        else:
            # Fallback insertion
            if '</div></header>' in content:
                content = content.replace('</div></header>', f'{btn_html}</div></header>')
            else:
                content = content.replace('</header>', f'{btn_html}</header>')

    # 3. Handle Footer Replacement or Insertion
    footer = get_footer_html(is_en)
    # Check if there is an existing footer
    if "<footer" in content:
        # Replace the entire footer block
        content = re.sub(
            r'<footer.*?>.*?</footer>',
            footer,
            content,
            flags=re.DOTALL
        )
    else:
        # No footer, we will insert it right before the </body> replace structure
        # (This is handled together with Drawer and Script)
        pass

    # 4. Insert Drawer and Script tag
    drawer = get_drawer_html(is_en)
    script_tag = f"""<script src="{rel_path}assets/js/nav-drawer.js"></script>"""

    # If footer was not inserted via replacement, insert it now
    if "<footer" not in content:
        insert_block = f"\n{footer}\n{drawer}\n{script_tag}\n</body>"
    else:
        insert_block = f"\n{drawer}\n{script_tag}\n</body>"

    content = content.replace('</body>', insert_block)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Processed successfully!")
    return True

if __name__ == "__main__":
    # Test on one file first if desired, but we can process all safely.
    # We will process sitemap pages and index pages, then all playbooks.
    all_target_files = kr_pages + en_pages
    processed_count = 0
    for file_path in all_target_files:
        if os.path.exists(file_path):
            if process_file(file_path):
                processed_count += 1
        else:
            print(f"File not found: {file_path}")

    print(f"Finished. Processed {processed_count} files.")
