import os
import json
import re

INVENTORY_PATH = "_orchestration/inventory.json"
MANIFEST_PATH = "_orchestration/image-manifest.json"
INDEX_PATH = "index.html"

# Load data
with open(INVENTORY_PATH, "r") as f:
    inventory = json.load(f)
mountains_map = {m["id"]: m for m in inventory}

with open(MANIFEST_PATH, "r") as f:
    manifest_entries = json.load(f)

# Group manifest by mountain
manifest_by_mountain = {}
for entry in manifest_entries:
    m_id = entry["mountain_id"]
    if m_id not in manifest_by_mountain:
        manifest_by_mountain[m_id] = {}
    manifest_by_mountain[m_id][entry["role"]] = entry

# Global CSS for Playbooks
PLAYBOOK_UPGRADE_CSS = """
/* --- UPGRADE: HERO BLEED, GALLERY, LIGHTBOX, CREDITS --- */
.hero-bleed {
  position: relative;
  width: 100%;
  min-height: clamp(340px, 45vh, 520px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--space-12, 3rem) var(--space-6, 1.5rem);
  overflow: hidden;
  border-bottom: 1px solid var(--color-divider, var(--divider, var(--div, #dcd9d5)));
  background-color: var(--color-bg, var(--bg, #f7f6f2));
  
  --hero-overlay-top: rgba(247, 246, 242, 0.35);
  --hero-overlay-bottom: rgba(247, 246, 242, 0.90);
  --hero-text: var(--color-text, var(--text, var(--txt, #28251d)));
  --hero-text-muted: var(--color-text-muted, var(--muted, #7a7974));
  --hero-badge-bg: var(--color-primary-highlight, var(--primary-highlight, #cedcd8));
  --hero-badge-color: var(--color-primary, var(--primary, #01696f));
}

@supports (background-color: color-mix(in srgb, red, blue)) {
  .hero-bleed {
    --hero-overlay-top: color-mix(in srgb, var(--color-bg, var(--bg, #f7f6f2)) 35%, transparent);
    --hero-overlay-bottom: color-mix(in srgb, var(--color-bg, var(--bg, #f7f6f2)) 90%, transparent);
  }
}

[data-theme="dark"] .hero-bleed {
  --hero-overlay-top: rgba(15, 14, 13, 0.35);
  --hero-overlay-bottom: rgba(15, 14, 13, 0.96);
  --hero-text: var(--color-text, var(--text, var(--txt, #cdccca)));
  --hero-text-muted: var(--color-text-muted, var(--muted, #797876));
  --hero-badge-bg: var(--color-primary-highlight, var(--primary-highlight, #1e3234));
  --hero-badge-color: var(--color-primary, var(--primary, #4f98a3));
}

@supports (background-color: color-mix(in srgb, red, blue)) {
  [data-theme="dark"] .hero-bleed {
    --hero-overlay-top: color-mix(in srgb, var(--color-bg, var(--bg, #0f0e0d)) 35%, transparent);
    --hero-overlay-bottom: color-mix(in srgb, var(--color-bg, var(--bg, #0f0e0d)) 96%, transparent);
  }
}

.hero-bleed .hero-picture {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.hero-bleed .hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 35%;
}

.hero-bleed .hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background: linear-gradient(180deg, var(--hero-overlay-top) 0%, var(--hero-overlay-bottom) 100%);
  pointer-events: none;
}

.hero-bleed .hero-content {
  position: relative;
  z-index: 3;
  max-width: 65ch;
  margin: 0 auto;
  pointer-events: auto;
}

.hero-bleed h1 {
  color: var(--hero-text);
  font-family: var(--font-display, sans-serif);
  font-size: var(--text-2xl, 2.5rem);
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: var(--space-4, 1rem);
  text-shadow: 0 1px 2px var(--color-bg, var(--bg, #f7f6f2));
}

[data-theme="dark"] .hero-bleed h1 {
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.hero-bleed p {
  color: var(--hero-text-muted);
  font-size: var(--text-base, 1.1rem);
  line-height: 1.6;
  max-width: 56ch;
  margin: 0 auto var(--space-8, 2rem);
  text-shadow: 0 1px 1px var(--color-bg, var(--bg, #f7f6f2));
}

[data-theme="dark"] .hero-bleed p {
  text-shadow: 0 1px 3px rgba(0,0,0,0.5);
}

.hero-bleed .hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2, 0.5rem);
  background-color: var(--hero-badge-bg);
  color: var(--hero-badge-color);
  padding: var(--space-1, 0.25rem) var(--space-3, 0.75rem);
  border-radius: var(--radius-full, 9999px);
  font-size: var(--text-xs, 0.85rem);
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: var(--space-4, 1rem);
}

.photo-gallery-section {
  max-width: 1100px;
  margin: var(--space-12, 3rem) auto;
  padding: 0 var(--space-6, 1.5rem);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4, 1rem);
  margin-top: var(--space-4, 1rem);
}

.gallery-grid:has(.gallery-item:nth-child(3):last-child) {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 768px) {
  .gallery-grid:has(.gallery-item:nth-child(3):last-child) {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  }
}

.gallery-item {
  position: relative;
  display: block;
  width: 100%;
  aspect-ratio: 3 / 2;
  overflow: hidden;
  border-radius: var(--radius-lg, 0.75rem);
  border: 1px solid var(--color-border, var(--border, var(--bor, #d4d1ca)));
  background-color: var(--color-surface, var(--surface, #f9f8f5));
  padding: 0;
  cursor: pointer;
  box-shadow: var(--shadow-sm, 0 1px 2px rgba(0,0,0,0.06));
}

.gallery-item:focus-visible {
  outline: 3px solid var(--color-primary, var(--primary, #01696f));
  outline-offset: 2px;
}

.gallery-picture, 
.gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition, 180ms ease);
}

.gallery-item:hover .gallery-img {
  transform: scale(1.04);
}

@media (prefers-reduced-motion: reduce) {
  .gallery-item:hover .gallery-img {
    transform: none;
  }
  .gallery-picture, 
  .gallery-img {
    transition: none;
  }
}

.gallery-caption-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: var(--space-4, 1rem) var(--space-4, 1rem) var(--space-3, 0.75rem);
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.75) 100%);
  color: #ffffff;
  text-align: left;
  opacity: 0;
  transition: opacity var(--transition, 180ms ease);
  pointer-events: none;
}

.gallery-item:hover .gallery-caption-overlay,
.gallery-item:focus-within .gallery-caption-overlay {
  opacity: 1;
}

.gallery-caption-text {
  font-size: var(--text-sm, 0.95rem);
  font-weight: 700;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0,0,0,0.8);
}

@media (hover: none) {
  .gallery-caption-overlay {
    opacity: 1;
    background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.65) 100%);
  }
}

.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(15, 14, 13, 0.96);
  z-index: 999;
  display: none;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--transition, 180ms ease);
}

.lightbox[aria-hidden="false"] {
  display: flex;
  opacity: 1;
}

.lightbox-content {
  position: relative;
  max-width: 86vw;
  max-height: 82vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.lightbox-figure {
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-figure picture {
  display: flex;
  justify-content: center;
}

.lightbox-img {
  max-width: 100%;
  max-height: 72vh;
  object-fit: contain;
  border-radius: var(--radius-md, 0.5rem);
  box-shadow: var(--shadow-lg, 0 12px 32px rgba(0,0,0,0.5));
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.lightbox-caption {
  margin-top: var(--space-4, 1rem);
  color: #cdccca;
  font-size: var(--text-base, 1.05rem);
  font-weight: 600;
  text-align: center;
  letter-spacing: 0.02em;
}

.lightbox-close, 
.lightbox-prev, 
.lightbox-next {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-full, 9999px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  z-index: 1005;
  transition: background-color var(--transition, 180ms ease), transform var(--transition, 180ms ease);
}

.lightbox-close:hover, 
.lightbox-prev:hover, 
.lightbox-next:hover {
  background: rgba(255, 255, 255, 0.22);
}

.lightbox-close:focus-visible, 
.lightbox-prev:focus-visible, 
.lightbox-next:focus-visible {
  outline: 3px solid var(--color-primary, var(--primary, #4f98a3));
  outline-offset: 2px;
}

.lightbox-close {
  top: var(--space-6, 1.5rem);
  right: var(--space-6, 1.5rem);
  width: 44px;
  height: 44px;
  font-size: 2rem;
  line-height: 1;
}

.lightbox-prev {
  left: var(--space-6, 1.5rem);
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  font-size: 1.5rem;
}

.lightbox-next {
  right: var(--space-6, 1.5rem);
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  font-size: 1.5rem;
}

@media (max-width: 640px) {
  .lightbox-close {
    top: var(--space-4, 1rem);
    right: var(--space-4, 1rem);
    width: 40px;
    height: 40px;
  }
  .lightbox-prev {
    left: var(--space-3, 0.75rem);
    width: 40px;
    height: 40px;
  }
  .lightbox-next {
    right: var(--space-3, 0.75rem);
    width: 40px;
    height: 40px;
  }
}

.photo-credit {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1, 0.25rem);
  font-family: var(--font-body, sans-serif);
  font-size: clamp(10px, 0.7rem, var(--text-xs));
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-sm, 0.25rem);
  color: rgba(255, 255, 255, 0.8);
  background-color: rgba(15, 14, 13, 0.65);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 10;
  pointer-events: auto;
}

.photo-credit a {
  color: #ffffff;
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color var(--transition, 180ms ease);
}

.photo-credit a:hover {
  color: var(--color-primary, var(--primary, #4f98a3));
}

.photo-credit .credit-divider {
  opacity: 0.5;
  margin: 0 2px;
}

.hero-credit {
  position: absolute;
  bottom: var(--space-4, 1rem);
  right: var(--space-4, 1rem);
}

@media (max-width: 640px) {
  .hero-credit {
    bottom: var(--space-2, 0.5rem);
    right: var(--space-2, 0.5rem);
    padding: 3px 6px;
  }
}

.lightbox-credit {
  position: relative;
  margin-top: var(--space-3, 0.75rem);
  background: none;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  color: #bab9b4;
  font-size: var(--text-xs, 0.85rem);
  justify-content: center;
}

.lightbox-credit a {
  color: #ffffff;
  text-decoration: underline;
}

.lightbox-credit a:hover {
  color: var(--color-primary, var(--primary, #4f98a3));
}
"""

# Global JS for Lightbox
LIGHTBOX_JS = """
<!-- Lightbox Dialog Overlay -->
<div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="이미지 크게 보기" aria-hidden="true" tabindex="-1">
  <button class="lightbox-close" aria-label="갤러리 닫기">&times;</button>
  <button class="lightbox-prev" aria-label="이전 이미지">&#10094;</button>
  <button class="lightbox-next" aria-label="다음 이미지">&#10095;</button>
  <div class="lightbox-content">
    <figure class="lightbox-figure">
      <figcaption class="lightbox-caption"></figcaption>
    </figure>
    <div class="photo-credit lightbox-credit"></div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
  const galleryItems = document.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('lightbox');
  if (!lightbox || galleryItems.length === 0) return;
  
  const closeBtn = lightbox.querySelector('.lightbox-close');
  const prevBtn = lightbox.querySelector('.lightbox-prev');
  const nextBtn = lightbox.querySelector('.lightbox-next');
  const figureContainer = lightbox.querySelector('.lightbox-figure');
  const captionEl = lightbox.querySelector('.lightbox-caption');
  const creditEl = lightbox.querySelector('.lightbox-credit');
  
  let currentIndex = -1;
  let lastActiveElement = null;
  
  const openLightbox = (index) => {
    currentIndex = index;
    lastActiveElement = document.activeElement;
    
    const item = galleryItems[currentIndex];
    const sourcePicture = item.querySelector('picture');
    const captionText = item.querySelector('.gallery-caption-text')?.textContent || '';
    
    const existingPic = figureContainer.querySelector('picture');
    if (existingPic) existingPic.remove();
    
    const clonedPic = sourcePicture.cloneNode(true);
    const img = clonedPic.querySelector('img');
    img.className = 'lightbox-img';
    img.removeAttribute('loading');
    img.removeAttribute('decoding');
    
    figureContainer.insertBefore(clonedPic, captionEl);
    captionEl.textContent = captionText;
    
    const creditData = item.getAttribute('data-credit') || '';
    if (creditData && creditEl) {
      creditEl.innerHTML = creditData;
      creditEl.style.display = 'block';
    } else if (creditEl) {
      creditEl.style.display = 'none';
    }
    
    lightbox.setAttribute('aria-hidden', 'false');
    lightbox.focus();
    document.body.style.overflow = 'hidden';
  };
  
  const closeLightbox = () => {
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastActiveElement) lastActiveElement.focus();
  };
  
  const showNext = () => {
    let nextIndex = currentIndex + 1;
    if (nextIndex >= galleryItems.length) nextIndex = 0;
    openLightbox(nextIndex);
  };
  
  const showPrev = () => {
    let prevIndex = currentIndex - 1;
    if (prevIndex < 0) prevIndex = galleryItems.length - 1;
    openLightbox(prevIndex);
  };
  
  galleryItems.forEach((item, idx) => {
    item.addEventListener('click', () => openLightbox(idx));
  });
  
  closeBtn.addEventListener('click', closeLightbox);
  nextBtn.addEventListener('click', showNext);
  prevBtn.addEventListener('click', showPrev);
  
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
      closeLightbox();
    }
  });
  
  lightbox.addEventListener('keydown', (e) => {
    if (lightbox.getAttribute('aria-hidden') === 'true') return;
    
    if (e.key === 'Escape') {
      closeLightbox();
    } else if (e.key === 'ArrowRight') {
      showNext();
    } else if (e.key === 'ArrowLeft') {
      showPrev();
    } else if (e.key === 'Tab') {
      const focusableElements = lightbox.querySelectorAll('button');
      const firstFocus = focusableElements[0];
      const lastFocus = focusableElements[focusableElements.length - 1];
      
      if (e.shiftKey) {
        if (document.activeElement === firstFocus) {
          lastFocus.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocus) {
          firstFocus.focus();
          e.preventDefault();
        }
      }
    }
  });
});
</script>
"""

def generate_short_caption_ko(m_name, role, geo_hint):
    geo_lower = (geo_hint or "").lower()
    
    # Check landmarks in geo_hint
    landmark_map = {
        "ulsanbawi": "울산바위",
        "daecheongbong": "대청봉 정상",
        "공룡능선": "공룡능선 비경",
        "dinosaur ridge": "공룡능선 비경",
        "baengnokdam": "백록담 분화구",
        "백록담": "백록담 분화구",
        "cheonwangbong": "천왕봉 정상",
        "천왕봉": "천왕봉 정상",
        "baegundae": "백운대 만경",
        "백운대": "백운대 만경",
        "insubong": "인수봉 암벽",
        "인수봉": "인수봉 암벽",
        "birobong": "비로봉 설경",
        "비로봉": "비로봉 설경",
        "sanjeong": "산정호수 전경",
        "yushan": "위산 주봉",
        "jade mountain": "위산 주봉",
        "xueshan": "설산 권곡",
        "snow mountain": "설산 권곡",
        "yangmingshan": "양명산 초원",
        "qingtiangang": "칭티엔강 전경"
    }
    
    for key, val in landmark_map.items():
        if key in geo_lower:
            return val
            
    # Fallback template
    role_map = {
        "gallery_1": f"{m_name} 등산코스",
        "gallery_2": f"{m_name} 절경",
        "gallery_3": f"{m_name} 풍경",
        "gallery_4": f"{m_name} 탐방로"
    }
    return role_map.get(role, f"{m_name} 전경")

def update_playbook_html(file_path, m_id):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (does not exist)")
        return
        
    m = mountains_map[m_id]
    m_name = m["name_ko"]
    
    print(f"Upgrading playbook: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Check if already upgraded
    if "hero-bleed" in html:
        print(f"Playbook {file_path} is already upgraded. Skipping.")
        return
        
    # 1. Inject Styles
    style_close_idx = html.find("</style>")
    if style_close_idx != -1:
        html = html[:style_close_idx] + PLAYBOOK_UPGRADE_CSS + html[style_close_idx:]
    else:
        print(f"Error: </style> tag not found in {file_path}")
        return
        
    # 2. Inject Hero Section
    # Find either <section class="hero"> or <header class="site-header"> (for jirisan)
    hero_pattern_section = re.compile(r'<section class="hero">([\s\S]*?)</section>')
    hero_pattern_header = re.compile(r'<header class="site-header">([\s\S]*?)</header>')
    
    is_jirisan = (m_id == "jirisan")
    hero_match = hero_pattern_header.search(html) if is_jirisan else hero_pattern_section.search(html)
    
    if hero_match:
        inner_content = hero_match.group(1)
        hero_photo = manifest_by_mountain[m_id]["hero"]
        
        # Build picture tag
        alt_ko = hero_photo["alt_ko"]
        alt_en = hero_photo["alt_en"]
        credit = hero_photo["credit"]
        author = credit["author"]
        source = credit["source"]
        author_url = credit["url"]
        
        picture_tag = f"""
  <!-- Background Picture -->
  <picture class="hero-picture">
    <source type="image/avif" srcset="assets/img/{m_id}/hero-640.avif 640w, assets/img/{m_id}/hero-1024.avif 1024w, assets/img/{m_id}/hero-1600.avif 1600w, assets/img/{m_id}/hero-2400.avif 2400w" sizes="100vw">
    <source type="image/webp" srcset="assets/img/{m_id}/hero-640.webp 640w, assets/img/{m_id}/hero-1024.webp 1024w, assets/img/{m_id}/hero-1600.webp 1600w, assets/img/{m_id}/hero-2400.webp 2400w" sizes="100vw">
    <img src="assets/img/{m_id}/hero-1600.jpg" srcset="assets/img/{m_id}/hero-640.jpg 640w, assets/img/{m_id}/hero-1024.jpg 1024w, assets/img/{m_id}/hero-1600.jpg 1600w, assets/img/{m_id}/hero-2400.jpg 2400w" sizes="100vw" alt="{alt_ko} / {alt_en}" class="hero-img">
  </picture>
  <div class="hero-overlay"></div>
"""
        
        credit_tag = f"""
  <!-- Hero Credit Overlay -->
  <div class="photo-credit hero-credit">
    <span class="credit-author">Photo by <a href="{author_url}" target="_blank" rel="noopener">{author}</a></span>
    <span class="credit-divider">/</span>
    <span class="credit-source"><a href="https://{source.lower()}.com" target="_blank" rel="noopener">{source}</a></span>
  </div>
"""

        # Repackage Hero Section
        if is_jirisan:
            upgraded_hero = f"""<header class="site-header hero-bleed">
  {picture_tag}
  <div class="hero-content">
    {inner_content}
  </div>
  {credit_tag}
</header>"""
            html = hero_pattern_header.sub(upgraded_hero, html, 1)
        else:
            upgraded_hero = f"""<section class="hero hero-bleed">
  {picture_tag}
  <div class="hero-content">
    {inner_content}
  </div>
  {credit_tag}
</section>"""
            html = hero_pattern_section.sub(upgraded_hero, html, 1)
    else:
        print(f"Error: Hero tag match not found in {file_path}")
        return
        
    # 3. Inject Photo Gallery Section
    # Construct gallery HTML
    gallery_items_html = ""
    for idx in range(1, 5):
        role = f"gallery_{idx}"
        photo = manifest_by_mountain[m_id][role]
        alt_ko = photo["alt_ko"]
        alt_en = photo["alt_en"]
        credit = photo["credit"]
        author = credit["author"]
        source = credit["source"]
        author_url = credit["url"]
        
        # Get source metadata for the caption matching
        matching_selected = next(p for p in manifest_entries if p["mountain_id"] == m_id and p["role"] == role)
        geo_hint = matching_selected.get("geo_hint", "")
        short_caption = generate_short_caption_ko(m_name, role, geo_hint)
        
        gallery_items_html += f"""
    <!-- Gallery Image Button {idx} -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="{alt_en} 크게 보기" data-index="{idx-1}" data-credit="Photo by <a href='{author_url}' target='_blank' rel='noopener'>{author}</a> on {source}">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/{m_id}/g{idx}.avif">
        <source type="image/webp" srcset="assets/img/{m_id}/g{idx}.webp">
        <img src="assets/img/{m_id}/g{idx}.jpg" alt="{alt_ko}" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">{short_caption}</span>
      </div>
    </button>
"""

    gallery_section_html = f"""
<!-- Photo Gallery Grid -->
<section class="photo-gallery-section">
  <h3 class="section-title" style="margin-bottom:var(--space-4);font-family:var(--font-display);font-size:var(--text-lg);font-weight:800;">
    <span class="section-title-icon">📸</span> {m_name}의 사계 &amp; 명소
  </h3>
  <div class="gallery-grid">
    {gallery_items_html}
  </div>
</section>
"""

    # Inject right before <!-- FOOTER --> or <footer> or last <script> tag
    footer_idx = html.find("<!-- FOOTER -->")
    if footer_idx == -1:
        footer_idx = html.find("<footer")
    if footer_idx == -1:
        # Fallback to last <script> tag
        script_matches = list(re.finditer(r'<script\b[^>]*>', html))
        if script_matches:
            footer_idx = script_matches[-1].start()
            
    if footer_idx != -1:
        html = html[:footer_idx] + gallery_section_html + html[footer_idx:]
    else:
        print(f"Error: Footer or script tag not found in {file_path}")
        return
        
    # 4. Inject Lightbox overlay & scripts
    body_close_idx = html.rfind("</body>")
    if body_close_idx != -1:
        html = html[:body_close_idx] + LIGHTBOX_JS + html[body_close_idx:]
    else:
        print(f"Error: </body> tag not found in {file_path}")
        return
        
    # Save the updated file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully upgraded: {file_path}")

def upgrade_index_html():
    print(f"Upgrading index page: {INDEX_PATH}")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
        
    if "card-thumbnail-wrap" in html:
        print("Index page already upgraded. Skipping.")
        return
        
    # Inject CSS before </style>
    card_css = """
/* --- MOUNTAIN CARD THUMBNAIL --- */
.card-thumbnail-wrap {
  position: relative;
  width: 100%;
  height: 160px;
  overflow: hidden;
  background-color: var(--color-surface-offset, var(--surfaceoff, #f3f0ec));
  border-bottom: 1px solid var(--color-divider, var(--divider, var(--div, #dcd9d5)));
}

.card-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform var(--transition, 180ms ease);
}

.mountain-card:hover .card-thumbnail {
  transform: scale(1.04);
}

@media (prefers-reduced-motion: reduce) {
  .mountain-card:hover .card-thumbnail {
    transform: none;
  }
}
"""
    style_close_idx = html.find("</style>")
    if style_close_idx != -1:
        html = html[:style_close_idx] + card_css + html[style_close_idx:]
        
    # Modify renderCard function in scripts
    old_render_part = """const renderCard = m => `
  <div class="mountain-card">
    <div class="card-header">"""

    new_render_part = """const renderCard = m => `
  <div class="mountain-card">
    <!-- Card Top Photographic Thumbnail -->
    <div class="card-thumbnail-wrap">
      <picture>
        <source srcset="assets/img/${m.id}/g1-640.webp" type="image/webp">
        <img 
          src="assets/img/${m.id}/g1-640.jpg" 
          alt="${m.name} 등산로 전경" 
          class="card-thumbnail" 
          loading="lazy" 
          decoding="async">
      </picture>
    </div>
    <div class="card-header">"""

    if old_render_part in html:
        html = html.replace(old_render_part, new_render_part)
    else:
        print("Warning: old renderCard template not exact match. Attempting alternative replacement.")
        pattern = re.compile(r'const\s+renderCard\s*=\s*m\s*=>\s*`\s*<div\s+class="mountain-card">\s*<div\s+class="card-header">')
        if pattern.search(html):
            html = pattern.sub(new_render_part, html, 1)
        else:
            print("Error: Could not replace renderCard template in index.html")
            return
            
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully upgraded index.html")

def main():
    # Upgrade playbooks
    for m in inventory:
        m_id = m["id"]
        file_name = m.get("file")
        if file_name:
            update_playbook_html(file_name, m_id)
            
    # Upgrade index.html
    upgrade_index_html()

if __name__ == "__main__":
    main()
