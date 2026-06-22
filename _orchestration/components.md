# Korea Trails — 컴포넌트 시스템 마크업 규격 (Components)

본 문서는 `design-system.css`에 구축된 클래스를 기반으로 메인 랜딩 및 플레이북에서 재사용할 공통 HTML 컴포넌트의 표준 마크업 구조와 웹 접근성(a11y) 가이드를 기술합니다.

---

## 1. 브랜드 헤더 (Brand Header)
*   **클래스**: `.site-header`, `.logo-wrap`, `.logo-svg`, `.logo-text`, `.header-right`, `.theme-btn`
*   **HTML 골격**:
```html
<header class="site-header">
  <div class="logo-wrap">
    <svg class="logo-svg" viewBox="0 0 36 36" fill="none" aria-label="Korea Trails">
      <rect width="36" height="36" rx="8" fill="var(--primary)"/>
      <path d="M4 28 L10 16 L15 22 L20 12 L25 20 L30 10" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <circle cx="30" cy="10" r="2.5" fill="white"/>
    </svg>
    <a href="index.html" class="logo-text">Korea Trails</a>
  </div>
  <div class="header-right">
    <button class="theme-btn" id="themeBtn" aria-label="테마 전환 (라이트/다크)">◐</button>
  </div>
</header>
```
*   **접근성 (a11y)**:
    *   `<header>` 시맨틱 랜드마크 사용.
    *   테마 전환 버튼에 명확한 `aria-label` 부여.

---

## 2. 플레이북 코스 선택 탭 (Course Selector Tabs)
*   **클래스**: `.tabs`, `.tab`, `.tabpane`
*   **HTML 골격**:
```html
<div class="tabs" role="tablist" aria-label="코스별 안내">
  <button class="tab active" role="tab" aria-selected="true" aria-controls="pane-overview" data-tab="overview">📋 개요</button>
  <button class="tab" role="tab" aria-selected="false" aria-controls="pane-route" data-tab="route">🗺 경로 안내</button>
  <button class="tab" role="tab" aria-selected="false" aria-controls="pane-map" data-tab="map">📍 지도</button>
  <button class="tab" role="tab" aria-selected="false" aria-controls="pane-tips" data-tab="tips">💡 팁 & 주의</button>
</div>

<div class="tabpane active" id="pane-overview" role="tabpanel" tabindex="0">
  <!-- 개요 콘텐츠 -->
</div>
<div class="tabpane" id="pane-route" role="tabpanel" tabindex="0">
  <!-- 경로 안내 콘텐츠 -->
</div>
```
*   **접근성 (a11y)**:
    *   `role="tablist"`, `role="tab"`, `role="tabpanel"` 관계 설정.
    *   활성화 상태에 따른 `aria-selected="true|false"` 동적 갱신 (JS 연동).
    *   키보드 탭 진입을 위한 `tabindex="0"` 부여.

---

## 3. 체크포인트 테이블 (Checkpoint Table)
*   **클래스**: `.table-wrap`, `table`, `th`, `td`
*   **HTML 골격**:
```html
<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th scope="col">지점</th>
        <th scope="col">고도</th>
        <th scope="col">누적거리</th>
        <th scope="col">특징</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>소유갱 (들머리)</td>
        <td>약 800m</td>
        <td>0km</td>
        <td>108 버스 정류장, 분기공</td>
      </tr>
    </tbody>
  </table>
</div>
```
*   **접근성 (a11y)**:
    *   테이블 열 헤더에 `scope="col"` 명시.
    *   `.table-wrap`에 `overflow-x: auto`를 부여하여 모바일 스크롤 시 접근성 유지.

---

## 4. 구간 상세 아코디언 (Segment Accordion)
*   **클래스**: `.accordion`, `.accordion-header`, `.accordion-content`
*   **HTML 골격**:
```html
<div class="accordion">
  <button class="accordion-header" aria-expanded="false" aria-controls="sect-1">
    <span>1구간: 소유갱 ➔ 칠성산 주봉</span>
  </button>
  <div class="accordion-content" id="sect-1" aria-hidden="true">
    <p>소유갱 들머리에서 출발하여 유황 연기가 솟아오르는 등산로를 따라 경사를 오릅니다...</p>
  </div>
</div>
```
*   **접근성 (a11y)**:
    *   헤더는 실제 `<button>` 태그로 작성하여 키보드 포커스 및 Enter/Space 키 동작 보장.
    *   열림/닫힘 상태에 따른 `aria-expanded="true|false"` 및 콘텐츠의 `aria-hidden="true|false"` 동적 변경.

---

## 5. 지표 통계 요약 (Stats KPI Card Grid)
*   **클래스**: `.stats`, `.stat`, `.l`, `.v`
*   **HTML 골격**:
```html
<div class="stats">
  <div class="stat">
    <div class="l">최고 고도</div>
    <div class="v">1,120m</div>
  </div>
  <div class="stat">
    <div class="l">총 거리</div>
    <div class="v">3.2km</div>
  </div>
  <div class="stat">
    <div class="l">소요 시간</div>
    <div class="v">1시간 40분</div>
  </div>
</div>
```

---

## 6. 지도 컨테이너 & 폴백 SVG
*   **클래스**: `.card.map`, `.map-fallback`, `.leaflet-map`
*   **HTML 골격**:
```html
<div class="card map" style="position: relative;">
  <!-- JS 비활성/오프라인 시 나타날 폴백 SVG -->
  <svg class="map-fallback" viewBox="0 0 760 420" aria-hidden="true">
    <!-- SVG 도형 및 경로 -->
  </svg>
  <!-- JS 로드 성공 시 노출될 실사 지도 컨테이너 -->
  <div class="leaflet-map" id="map-beginner" style="display: none; width: 100%; height: 400px;" role="application" aria-label="실사 지도 서비스"></div>
</div>
```
