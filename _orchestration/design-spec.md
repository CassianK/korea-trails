# Korea Trails Visual Design Specifications & Component Templates

**Date:** 2026-06-21  
**Author:** A1 (Art Director)  
**Status:** Approved for Implementation (Phase 1 Gate)  

---

## 1. Visual Language & Art Direction Principles

To elevate the `korea-trails` codebase from a flat vector-style dashboard to a premium, immersive photographic experience, we establish the following core art direction principles:

1. **Photographic Authenticity & Quality**: 
   Only genuine, natural lighting landscape photos of the respective mountain may be used. Photos must depict typical mountain ridges, peaks, trails, and signature seasonal elements (e.g., autumn foliage on Seoraksan, snow on Hallasan). Avoid over-saturated, AI-generated, or heavily color-filtered stock graphics.
2. **Seamless Theme Integration**:
   Every new photographic component must adapt dynamically to both Light and Dark modes. Instead of hardcoded colors, components must utilize the codebase's existing CSS variables (`--color-*` or `--bg`/`--surface` etc.) to maintain visual harmony.
3. **Contrast & Legibility (A11y)**:
   Any text layered over photographs (e.g., in the Hero Section) must achieve a minimum contrast ratio of **4.5:1 (WCAG AA)**, aiming for **7.1 (WCAG AAA)**. This is enforced using dynamic semi-transparent gradient overlays and optional backdrop filters.
4. **Performance Budgets & Responsive Loading**:
   - **Hero Image (Above-the-Fold)**: Load eagerly (`loading="eager"`), decode asynchronously (`decoding="async"`), and request with high fetch priority (`fetchpriority="high"`). Size must be controlled via responsive `<picture>` tags.
   - **Gallery & Card Images (Below-the-Fold)**: Load lazily (`loading="lazy"`) and decode asynchronously.
5. **No Bundler/Transpiler Rule**:
   All components must be structured in pure vanilla HTML/CSS and dependency-free JavaScript. No npm packages or transpilers.

---

## 2. Design Token Fallback Mapping

Due to the variance in CSS token naming across playbooks (Family A vs. Family B), all CSS specs written in this document must use fallback declarations in the format:  
`var(--primary-token, var(--secondary-token, fallback_value))`.

| Token Role | Family A Variable | Family B Variable | Fallback Value |
|---|---|---|---|
| Page Background | `--color-bg` | `--bg` | `#f7f6f2` (Light) / `#0f0e0d` (Dark) |
| Primary Surface | `--color-surface` | `--surface` | `#f9f8f5` (Light) / `#161514` (Dark) |
| Secondary Surface | `--color-surface-2` | `--surface2` / `--surface-2` | `#fbfbf9` (Light) / `#1c1b19` (Dark) |
| Dynamic Background | `--color-surface-dynamic` | `--surfdyn` | `#e6e4df` (Light) / `#2d2c2a` (Dark) |
| Border Color | `--color-border` | `--border` / `--bor` | `#d4d1ca` (Light) / `#353432` (Dark) |
| Divider Color | `--color-divider` | `--div` | `#dcd9d5` (Light) / `#242321` (Dark) |
| Core Text Color | `--color-text` | `--text` / `--txt` | `#28251d` (Light) / `#cdccca` (Dark) |
| Muted Text Color | `--color-text-muted` | `--muted` | `#7a7974` (Light) / `#797876` (Dark) |
| Faint Text Color | `--color-text-faint` | `--faint` | `#bab9b4` (Light) / `#4a4948` (Dark) |
| Primary Action Color | `--color-primary` | `--blue` / `--green` | `#01696f` (Light) / `#4f98a3` (Dark) |
| Primary Highlight | `--color-primary-highlight` | `--bluebg` / `--greenbg` | `#cedcd8` (Light) / `#1e3234` (Dark) |
| Outer Corner Radius | `--radius-xl` | N/A | `1rem` |
| Block Corner Radius | `--radius-lg` | N/A | `0.75rem` |
| Small Corner Radius | `--radius-md` | N/A | `0.5rem` |

---

## 3. Component Spec 1: Hero Section

The redesigned hero section replaces the flat gradient background with a full-bleed `<picture>` element and a gradient overlay that adapts to light and dark themes.

### 3.1 HTML Template

To integrate, wrap the original `.hero` contents in `.hero-content`, insert the responsive `<picture>` container, the `.hero-overlay`, and the photographer credit badge.

```html
<section class="hero hero-bleed">
  <!-- Responsive Image Container -->
  <picture class="hero-picture">
    <!-- AVIF sources for high performance -->
    <source type="image/avif" srcset="
      assets/img/seoraksan/hero-640.avif 640w,
      assets/img/seoraksan/hero-1024.avif 1024w,
      assets/img/seoraksan/hero-1600.avif 1600w,
      assets/img/seoraksan/hero-2400.avif 2400w" 
      sizes="100vw">
    <!-- WebP sources -->
    <source type="image/webp" srcset="
      assets/img/seoraksan/hero-640.webp 640w,
      assets/img/seoraksan/hero-1024.webp 1024w,
      assets/img/seoraksan/hero-1600.webp 1600w,
      assets/img/seoraksan/hero-2400.webp 2400w" 
      sizes="100vw">
    <!-- Fallback high-resolution JPG -->
    <img 
      src="assets/img/seoraksan/hero-1600.jpg" 
      srcset="
        assets/img/seoraksan/hero-640.jpg 640w,
        assets/img/seoraksan/hero-1024.jpg 1024w,
        assets/img/seoraksan/hero-1600.jpg 1600w,
        assets/img/seoraksan/hero-2400.jpg 2400w" 
      sizes="100vw"
      alt="설악산 국립공원의 대청봉 기암절벽 풍경" 
      class="hero-img" 
      loading="eager" 
      decoding="async"
      fetchpriority="high">
  </picture>

  <!-- Adaptive Overlay Gradient -->
  <div class="hero-overlay"></div>

  <!-- Hero Text Content -->
  <div class="hero-content">
    <div class="hero-badge">🏔 강원도 속초 · 양양 · 인제 · 고성</div>
    <h1>설악산 등산 코스 가이드</h1>
    <p>대청봉(1,708m)을 품은 대한민국 3대 명산. 초급부터 고급까지 나에게 맞는 코스를 선택하세요.</p>
    <div class="course-selector">
      <button class="course-btn active-beginner" onclick="selectCourse('beginner',this)">🌿 초급 — 울산바위·비룡폭포</button>
      <button class="course-btn" onclick="selectCourse('intermediate',this)">🦶 중급 — 오색 대청봉 왕복</button>
      <button class="course-btn" onclick="selectCourse('advanced',this)">🏔 고급 — 내외설악 관통 종주</button>
    </div>
  </div>

  <!-- Sleek Credit Overlay -->
  <div class="photo-credit hero-credit">
    <span>Photo by <a href="https://unsplash.com/@username" target="_blank" rel="noopener">Photographer</a> / <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a></span>
  </div>
</section>
```

### 3.2 CSS Styles

```css
/* --- HERO BLEED SECTION --- */
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
  
  /* Fallbacks for older browsers without CSS color-mix */
  --hero-overlay-top: rgba(247, 246, 242, 0.35);
  --hero-overlay-bottom: rgba(247, 246, 242, 0.90);
  --hero-text: var(--color-text, var(--text, var(--txt, #28251d)));
  --hero-text-muted: var(--color-text-muted, var(--muted, #7a7974));
  --hero-badge-bg: var(--color-primary-highlight, var(--primary-highlight, #cedcd8));
  --hero-badge-color: var(--color-primary, var(--primary, #01696f));
}

/* Modern color-mix supports for dynamic transparency mapping based on exact theme color */
@supports (background-color: color-mix(in srgb, red, blue)) {
  .hero-bleed {
    --hero-overlay-top: color-mix(in srgb, var(--color-bg, var(--bg, #f7f6f2)) 35%, transparent);
    --hero-overlay-bottom: color-mix(in srgb, var(--color-bg, var(--bg, #f7f6f2)) 90%, transparent);
  }
}

/* Dark Mode Variable Overrides */
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
  object-position: center 35%; /* Prioritizes mountain ridgeline vertical alignment */
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

/* Ensure readability of headers and descriptions */
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

/* --- OPTIONAL: FLOATING GLASS CARD (Alternative for high-contrast safety) --- */
.hero-bleed .hero-content.glass-card {
  background-color: rgba(249, 248, 245, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--color-border, var(--border, #d4d1ca));
  border-radius: var(--radius-xl, 1rem);
  padding: var(--space-6, 1.5rem) var(--space-8, 2rem);
  box-shadow: var(--shadow-md, 0 4px 12px rgba(0,0,0,0.08));
}

@supports (background-color: color-mix(in srgb, red, blue)) {
  .hero-bleed .hero-content.glass-card {
    background-color: color-mix(in srgb, var(--color-surface, var(--surface, #f9f8f5)) 75%, transparent);
  }
  [data-theme="dark"] .hero-bleed .hero-content.glass-card {
    background-color: color-mix(in srgb, var(--color-surface, var(--surface, #161514)) 75%, transparent);
  }
}

[data-theme="dark"] .hero-bleed .hero-content.glass-card {
  background-color: rgba(22, 21, 20, 0.75);
  border-color: var(--color-border, var(--border, #353432));
}
```

---

## 4. Component Spec 2: Responsive Photo Gallery

The Photo Gallery is standardly integrated at the bottom of the page, directly above the main `<footer>`. This avoids obstructing tab-nav navigation and course details.

### 4.1 HTML Template

```html
<!-- Photo Gallery Grid -->
<section class="photo-gallery-section">
  <h3 class="section-title">
    <span class="section-title-icon">📸</span> 설악산의 사계 &amp; 명소
  </h3>
  
  <div class="gallery-grid">
    <!-- Gallery Image Button 1 -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="설악산 대청봉 가을 단풍 크게 보기" data-index="0" data-credit="Photo by <a href='https://unsplash.com/@photographer1' target='_blank'>Author1</a> on Unsplash">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/seoraksan/g1.avif">
        <source type="image/webp" srcset="assets/img/seoraksan/g1.webp">
        <img src="assets/img/seoraksan/g1.jpg" alt="설악산 대청봉에 물든 화려한 가을 단풍 풍경" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">대청봉 가을 단풍</span>
      </div>
    </button>

    <!-- Gallery Image Button 2 -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="울산바위 전경 크게 보기" data-index="1" data-credit="Photo by <a href='https://unsplash.com/@photographer2' target='_blank'>Author2</a> on Unsplash">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/seoraksan/g2.avif">
        <source type="image/webp" srcset="assets/img/seoraksan/g2.webp">
        <img src="assets/img/seoraksan/g2.jpg" alt="안개 낀 아침 하늘 아래 웅장하게 서 있는 울산바위 암벽" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">울산바위 아침 전경</span>
      </div>
    </button>

    <!-- Gallery Image Button 3 -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="비룡폭포 물줄기 크게 보기" data-index="2" data-credit="Photo by <a href='https://unsplash.com/@photographer3' target='_blank'>Author3</a> on Unsplash">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/seoraksan/g3.avif">
        <source type="image/webp" srcset="assets/img/seoraksan/g3.webp">
        <img src="assets/img/seoraksan/g3.jpg" alt="시원하게 쏟아져 내리는 세찬 비룡폭포의 협곡 물줄기" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">시원한 비룡폭포 계곡</span>
      </div>
    </button>

    <!-- Gallery Image Button 4 (Optional) -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="설악산 공룡능선 운해 크게 보기" data-index="3" data-credit="Photo by <a href='https://unsplash.com/@photographer4' target='_blank'>Author4</a> on Unsplash">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/seoraksan/g4.avif">
        <source type="image/webp" srcset="assets/img/seoraksan/g4.webp">
        <img src="assets/img/seoraksan/g4.jpg" alt="구름바다(운해) 위로 솟아오른 험난하고 신비로운 공룡능선" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">공룡능선 운해</span>
      </div>
    </button>

    <!-- Gallery Image Button 5 (Optional) -->
    <button class="gallery-item" aria-haspopup="dialog" aria-label="대청봉의 겨울 설경 크게 보기" data-index="4" data-credit="Photo by <a href='https://unsplash.com/@photographer5' target='_blank'>Author5</a> on Unsplash">
      <picture class="gallery-picture">
        <source type="image/avif" srcset="assets/img/seoraksan/g5.avif">
        <source type="image/webp" srcset="assets/img/seoraksan/g5.webp">
        <img src="assets/img/seoraksan/g5.jpg" alt="온 세상이 하얗게 덮인 겨울철 설악산 대청봉 정상 주목 군락지" class="gallery-img" loading="lazy" decoding="async">
      </picture>
      <div class="gallery-caption-overlay">
        <span class="gallery-caption-text">대청봉의 설경</span>
      </div>
    </button>
  </div>
</section>
```

### 4.2 CSS Styles

```css
/* --- PHOTO GALLERY GRID --- */
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

/* Layout adjustments if 3 pictures exist */
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

/* Accessible Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .gallery-item:hover .gallery-img {
    transform: none;
  }
  .gallery-picture, 
  .gallery-img {
    transition: none;
  }
}

/* Captions visible on hover or focus */
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
  pointer-events: none; /* Mouse clicks pass to button */
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

/* Touch devices layout override */
@media (hover: none) {
  .gallery-caption-overlay {
    opacity: 1;
    background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.65) 100%);
  }
}
```

---

## 5. Component Spec 3: Lightweight Lightbox Component

To preview the high-resolution gallery photographs, a lightweight popup modal is placed at the bottom of the body. It relies on standard browser APIs, trapping keyboard focus and adapting to high-contrast themes.

### 5.1 HTML Template (Append to end of `<body>`)

```html
<!-- Lightbox Dialog Overlay -->
<div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="이미지 크게 보기" aria-hidden="true" tabindex="-1">
  <!-- Close Button -->
  <button class="lightbox-close" aria-label="갤러리 닫기">&times;</button>
  
  <!-- Navigation Controls -->
  <button class="lightbox-prev" aria-label="이전 이미지">&#10094;</button>
  <button class="lightbox-next" aria-label="다음 이미지">&#10095;</button>
  
  <!-- Image Frame -->
  <div class="lightbox-content">
    <figure class="lightbox-figure">
      <!-- Injected picture cloned by JS -->
      <figcaption class="lightbox-caption"></figcaption>
    </figure>
    <!-- Attribution Injected Here -->
    <div class="photo-credit lightbox-credit"></div>
  </div>
</div>
```

### 5.2 CSS Styles

```css
/* --- LIGHTBOX COMPONENT --- */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(15, 14, 13, 0.96); /* High-contrast background */
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

/* Lightbox Controls Buttons */
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
```

### 5.3 JavaScript Logic (Vanilla JS, Zero Dependencies)

Place the following script at the bottom of the playbook HTML files (or within existing script tag blocks):

```javascript
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
    
    // Clear old picture elements
    const existingPic = figureContainer.querySelector('picture');
    if (existingPic) existingPic.remove();
    
    // Clone target picture element directly to keep responsive AVIF/WebP sources
    const clonedPic = sourcePicture.cloneNode(true);
    const img = clonedPic.querySelector('img');
    img.className = 'lightbox-img';
    img.removeAttribute('loading'); // Load instantly inside lightbox
    
    figureContainer.insertBefore(clonedPic, captionEl);
    
    // Update labels and credits
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
    
    // Prevent main document scroll while dialog is open
    document.body.style.overflow = 'hidden';
  };
  
  const closeLightbox = () => {
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    // Restore user keyboard focus to the triggering gallery button
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
  
  // Attach event listeners
  galleryItems.forEach((item, idx) => {
    item.addEventListener('click', () => openLightbox(idx));
  });
  
  closeBtn.addEventListener('click', closeLightbox);
  nextBtn.addEventListener('click', showNext);
  prevBtn.addEventListener('click', showPrev);
  
  // Close if user clicks background
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
      closeLightbox();
    }
  });
  
  // Keyboard Events & Accessibility Focus Trap
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
      
      if (e.shiftKey) { // Tab backwards
        if (document.activeElement === firstFocus) {
          lastFocus.focus();
          e.preventDefault();
        }
      } else { // Tab forwards
        if (document.activeElement === lastFocus) {
          firstFocus.focus();
          e.preventDefault();
        }
      }
    }
  });
});
```

---

## 6. Component Spec 4: Mountain Card Thumbnail (index.html)

For `index.html`, each mountain card receives a header-level landscape thumbnail representing the mountain.

### 6.1 HTML Template (JavaScript Grid Dynamic Render)

Modify the `renderCard` template inside `index.html`'s scripts to prepending `.card-thumbnail-wrap`:

```javascript
const renderCard = m => `
  <div class="mountain-card">
    <!-- Card Top Photographic Thumbnail -->
    <div class="card-thumbnail-wrap">
      <picture>
        <source srcset="assets/img/\${m.id}/g1-640.webp" type="image/webp">
        <img 
          src="assets/img/\${m.id}/g1-640.jpg" 
          alt="\${m.name} 등산로 전경" 
          class="card-thumbnail" 
          loading="lazy" 
          decoding="async">
      </picture>
    </div>
    
    <!-- Original Card Header -->
    <div class="card-header">
      <div class="card-title-row">
        <span class="card-name">\${m.name}</span>
        <span class="card-alt">\${m.alt}</span>
      </div>
      <div style="display:flex;align-items:center;gap:var(--space-2);">
        <span class="card-region">\${m.region}</span>
        <span class="diff-badge \${DIFF_CLASS[m.diff]}">\${DIFF_LABEL[m.diff]}</span>
        \${m.done ? '<span style="font-size:var(--text-xs);background:var(--color-orange);color:#fff;padding:2px 8px;border-radius:var(--radius-full);font-weight:700;">플레이북 ✓</span>' : ''}
      </div>
    </div>
    
    <!-- Original Card Body & Footer -->
    <div class="card-body">
      ...
    </div>
  </div>
`;
```

### 6.2 CSS Styles

```css
/* --- MOUNTAIN CARD THUMBNAIL --- */
.card-thumbnail-wrap {
  position: relative;
  width: 100%;
  height: 160px; /* Fixed height for consistent dashboard layout alignment */
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

/* Reduced Motion Override */
@media (prefers-reduced-motion: reduce) {
  .mountain-card:hover .card-thumbnail {
    transform: none;
  }
}

/* Dynamic Placeholder Fallback (if image fails to load or for pending mountains) */
.card-thumbnail-wrap.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, 
    var(--color-primary-highlight, var(--bluebg, #cedcd8)) 0%, 
    var(--color-surface-offset, var(--surfaceoff, #f3f0ec)) 100%
  );
  color: var(--color-primary, var(--primary, #01696f));
  font-size: 2.2rem;
  font-family: var(--font-display, sans-serif);
  font-weight: 800;
}
```

---

## 7. Component Spec 5: Photo Credits Caption Layouts

Licensing compliance (Unsplash / Pexels Terms of Service) dictates that we must document attribution and host images locally (no hotlinking). Below are the credit overlay layouts for different contexts.

### 7.1 Hero Section Credit Overlay (Standard)

```html
<div class="photo-credit hero-credit">
  <span class="credit-author">Photo by <a href="https://unsplash.com/@username" target="_blank" rel="noopener">Hong Gil-dong</a></span>
  <span class="credit-divider">/</span>
  <span class="credit-source"><a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a></span>
</div>
```

```css
/* --- PHOTO CREDITS STYLING --- */
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

/* Position specifically in Hero Bottom Right */
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
```

### 7.2 Lightbox Credit Overlay (Framed Style)

```html
<div class="photo-credit lightbox-credit">
  <span>Photo by <a href="https://unsplash.com/@username" target="_blank" rel="noopener">Hong Gil-dong</a> on Unsplash</span>
</div>
```

```css
/* Lightbox Credit Overrides (removes backdrop and uses subtle text look) */
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
```
