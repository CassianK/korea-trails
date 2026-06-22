# Korea Trails — 리브랜딩 비주얼 방향 제안서 (Direction Options)

본 문서는 `DESIGN-OVERHAUL.md` §5에 정의된 P1 단계 산출물로, 텍스트 카드 아카이브를 프리미엄 아웃도어 가이드로 탈바꿈하기 위한 **3가지 브랜드 비주얼 방향안**을 제시합니다. 

사용자께서는 아래 제안서 중 **원하는 1개의 방향안**을 지정하여 승인해 주시기 바랍니다. 승인 이후 해당 방향안을 토대로 `design-tokens.json` 및 `design-system.css` 제작에 착수합니다.

---

## [ ] Option A: 클래식 알파인 헤리티지 (Classic Alpine Heritage)
> **콘셉트**: 전통 등산 아카이브와 내셔널 지오그래픽 같은 프리미엄 탐험 저널의 감성을 융합한 아날로그적 신뢰감의 디자인.

```
       [Light Mode]                   [Dark Mode]
  ┌──────────────────────┐       ┌──────────────────────┐
  │  Warm Cream (배경)    │       │  Deep Pine (배경)     │
  │  Forest Green (주색)  │       │  Pine Mint (대비)     │
  │  Ochre Gold (포인트)  │       │  Coal Slate (표면)    │
  └──────────────────────┘       └──────────────────────┘
```

*   **무드**: 신뢰, 클래식, 견고함, 탐험 저널
*   **타이포그래피**: Display Serif(제목: Cabinet Grotesk / Georgia류) + Sans-serif(본문: Satoshi / Inter)
*   **컬러 팔레트 (Light)**:
    *   배경(Bg): Warm Cream (`#FAF8F5`)
    *   표면(Surface): Pure White (`#FFFFFF`)
    *   주색(Primary): Forest Green (`#1B4332`)
    *   보조색(Accent): Ochre Gold (`#D97706`)
    *   텍스트(Text): Deep Charcoal (`#1C2521`)
*   **컬러 팔레트 (Dark)**:
    *   배경(Bg): Deep Obsidian Pine (`#0B1F19`)
    *   표면(Surface): Coal Slate (`#1A2521`)
    *   주색(Primary): Pine Mint (`#48BB78`)
    *   보조색(Accent): Golden Ochre (`#F59E0B`)
    *   텍스트(Text): Warm Gray (`#E2E8F0`)
*   **비주얼 요소**:
    *   두껍고 클래식한 선(Border)과 명확히 구분된 데이터 테이블 그리드.
    *   산 정상이나 숲의 텍스처를 살린 모던 헤리티지 형태의 엠블럼형 로고 디자인.
    *   안정적인 카드 그리드 레이아웃.

---

## [ ] Option B: 슬릭 모던 익스플로러 (Sleek Modern Explorer) - ★추천
> **콘셉트**: 올트레일즈(AllTrails), 스트라바(Strava), 스위스 관광청 앱처럼 극도로 정제되고 첨단 디지털 지도가 강조되는 테크니컬 디자인.

```
       [Light Mode]                   [Dark Mode]
  ┌──────────────────────┐       ┌──────────────────────┐
  │  Snow Slate (배경)    │       │  Pitch Black (배경)   │
  │  High-Tech Teal (주색)│       │  Neon Cyan (포인트)   │
  │  Dark Slate (표면)    │       │  Obsidian (표면)      │
  └──────────────────────┘       └──────────────────────┘
```

*   **무드**: 세련됨, 고기능성, 트렌디, 다이내믹
*   **타이포그래피**: Clean Geometric Sans-serif (Satoshi / Outfit) 전면 적용
*   **컬러 팔레트 (Light)**:
    *   배경(Bg): Snow Slate (`#F8FAFC`)
    *   표면(Surface): Pure White (`#FFFFFF`)
    *   주색(Primary): Technical Teal (`#0EA5E9`)
    *   보조색(Accent): Vibrant Orange (`#F97316`)
    *   텍스트(Text): Dark Slate (`#0F172A`)
*   **컬러 팔레트 (Dark)**:
    *   배경(Bg): Pitch Black (`#09090B`)
    *   표면(Surface): Dark Obsidian (`#18181B`)
    *   주색(Primary): Neon Cyan (`#38BDF8`)
    *   보조색(Accent): Coral Orange (`#FB923C`)
    *   텍스트(Text): Light Silver (`#F4F4F5`)
*   **비주얼 요소**:
    *   유리 투명 효과(Glassmorphism) 및 미세 그림자(Soft shadows)를 극대화한 컴포넌트 레이아웃.
    *   미세 선(Border 1px)과 둥근 모서리(border-radius: 16px)를 적용한 플로팅 카드 그리드.
    *   다크모드 시 네온 느낌의 하이라이트 레이어로 야간 아웃도어 야외 시인성 극대화.

---

## [ ] Option C: 얼시 오가닉 트레일 (Earthy Organic Trail)
> **콘셉트**: 흙, 점토, 나무 등 자연의 요소와 친환경 에코 저널의 따뜻한 느낌을 조합한 편안하고 내추럴한 힐링 테마.

```
       [Light Mode]                   [Dark Mode]
  ┌──────────────────────┐       ┌──────────────────────┐
  │  Soft Sand (배경)     │       │  Warm Coal (배경)     │
  │  Terracotta (주색)    │       │  Amber Gold (포인트)  │
  │  Stone Slate (표면)   │       │  Earth Black (표면)   │
  └──────────────────────┘       └──────────────────────┘
```

*   **무드**: 편안함, 따뜻함, 유대감, 에코 힐링
*   **타이포그래피**: Humanist Sans (Outfit) + Warm Serif Mix
*   **컬러 팔레트 (Light)**:
    *   배경(Bg): Soft Sand (`#FDFBF7`)
    *   표면(Surface): Stone Gray (`#F5F5F4`)
    *   주색(Primary): Terracotta Rust (`#B45309`)
    *   보조색(Accent): Sage Green (`#15803D`)
    *   텍스트(Text): Mud Brown (`#44403C`)
*   **컬러 팔레트 (Dark)**:
    *   배경(Bg): Warm Charcoal (`#1C1917`)
    *   표면(Surface): Earth Black (`#0C0A09`)
    *   주색(Primary): Amber Gold (`#F59E0B`)
    *   보조색(Accent): Emerald Green (`#22C55E`)
    *   텍스트(Text): Clay White (`#E7E5E4`)
*   **비주얼 요소**:
    *   매끄러운 라인보다는 둥글둥글한 알약형 배지 디자인.
    *   유기적인 부드러운 그라디언트 오버레이와 자연 친화적 패턴 사용.

---

## 🗳 선택 및 투표 방식
선호하는 옵션을 선택하여 말씀해 주십시오. (예: **"Option B 선택합니다"** 또는 **"Option A로 진행해 주세요"**)
선택해주시면 즉시 P2 디자인 시스템(토큰, `design-system.css`, 아이콘 팩) 구축을 시작하겠습니다!
