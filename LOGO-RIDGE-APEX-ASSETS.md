# Korea Trails 로고 — Ridge Apex (확정) · 프로덕션 SVG

> 사용자 선택: **A안 Ridge Apex** (TRINOS 무드 — 딥네이비 #0e1c34 + 메탈릭 골드 그라디언트, 삼각형(산)+능선).
> 아래 마크업을 **그대로** 사용. 골드 그라디언트 id는 페이지당 충돌 없게 접두(`kt-`) 유지.

## 1. 헤더 배지 (logo-svg 교체용 — 밝은 헤더에서도 대비 OK)
기존 각 페이지 헤더의 인라인 `<svg class="logo-svg" ...>`(옛 로고)를 아래로 교체. 옆 `Korea Trails` 워드마크 텍스트는 유지.
```html
<svg class="logo-svg" viewBox="0 0 40 40" width="36" height="36" role="img" aria-label="Korea Trails">
  <defs><linearGradient id="kt-gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f1d98a"/><stop offset=".5" stop-color="#c9a24b"/><stop offset="1" stop-color="#9c7a2e"/>
  </linearGradient></defs>
  <rect width="40" height="40" rx="9" fill="#0e1c34"/>
  <path d="M20 8 L33 31 L7 31 Z" fill="none" stroke="url(#kt-gold)" stroke-width="2.2" stroke-linejoin="round"/>
  <polyline points="11,28 16,21.5 19,24.5 24.5,17 29,28" fill="none" stroke="url(#kt-gold)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
</svg>
```

## 2. favicon.svg (정사각 아이콘)
```html
<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Korea Trails">
  <defs><linearGradient id="kt-gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f1d98a"/><stop offset=".5" stop-color="#c9a24b"/><stop offset="1" stop-color="#9c7a2e"/>
  </linearGradient></defs>
  <rect width="40" height="40" rx="9" fill="#0e1c34"/>
  <path d="M20 8 L33 31 L7 31 Z" fill="none" stroke="url(#kt-gold)" stroke-width="2.6" stroke-linejoin="round"/>
  <polyline points="11,28 16,21.5 19,24.5 24.5,17 29,28" fill="none" stroke="url(#kt-gold)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
</svg>
```

## 3. assets/brand/logo.svg (워드마크 포함 락업 — 소셜/브랜드)
```html
<svg viewBox="0 0 220 150" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Korea Trails">
  <defs><linearGradient id="kt-gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f1d98a"/><stop offset=".5" stop-color="#c9a24b"/><stop offset="1" stop-color="#9c7a2e"/>
  </linearGradient></defs>
  <path d="M110 26 L160 116 L60 116 Z" fill="none" stroke="url(#kt-gold)" stroke-width="4.5" stroke-linejoin="round"/>
  <polyline points="74,109 92,84 102,95 122,69 146,109" fill="none" stroke="url(#kt-gold)" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="110" y="140" text-anchor="middle" fill="#d9be78" font-size="15" font-weight="500" letter-spacing="6" font-family="Georgia,serif">KOREA TRAILS</text>
</svg>
```

## 4. OG/소셜 카드 (brand-og.png 및 산별 og.png)
배경 #0e1c34, 중앙 위 마크(골드 락업), 하단 산이름 + "KOREA TRAILS". 1200×630 재생성.

## 적용 규칙
- 54개 페이지(27 KR + 27 EN) 헤더 = §1 배지로 교체. 옛 인라인 로고/잔여 라벨 0 확인(grep).
- `assets/brand/favicon.svg` = §2, `assets/brand/logo.svg` = §3로 교체.
- `logo-options.html`(내부 미리보기)는 삭제.
- 다크모드: 네이비 타일은 다크에서도 동일(고정 색). 대비 AA 확인. 모노 폴백 필요 시 triangle+ridge를 `currentColor`로.
- 색 토큰: 네이비 `#0e1c34`, 골드 `#c9a24b`(중간값)·하이라이트 `#f1d98a`·딥 `#9c7a2e`, 워드마크 `#d9be78`(네이비 위).
