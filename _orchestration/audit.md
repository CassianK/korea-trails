# Korea Trails Codebase & CSS Design Tokens Audit Report

**Date:** 2026-06-21

This report documents the detailed static analysis of the `korea-trails` codebase, focusing on structure, design tokens (CSS variables), layout insertion coordinates for upcoming upgrades, and visual features of the 26 mountains.

## 1. Global CSS Design Tokens & Variable Mapping

### index.html Design Tokens

| Variable Name | Light Value | Dark Value | Category |
| --- | --- | --- | --- |
| `--color-bg` | `#f7f6f2` | `#0f0e0d` | Color |
| `--color-border` | `#d4d1ca` | `#353432` | Color |
| `--color-divider` | `#dcd9d5` | `#242321` | Color |
| `--color-error` | `#a12c7b` | `#d163a7` | Color |
| `--color-gold` | `#d19900` | `#e8af34` | Color |
| `--color-gold-highlight` | `#e9e0c6` | `#2e2718` | Color |
| `--color-orange` | `#da7101` | `#fdab43` | Color |
| `--color-primary` | `#01696f` | `#4f98a3` | Color |
| `--color-primary-highlight` | `#cedcd8` | `#1e3234` | Color |
| `--color-primary-hover` | `#0c4e54` | `#227f8b` | Color |
| `--color-success` | `#437a22` | `#6daa45` | Color |
| `--color-success-highlight` | `#d4dfcc` | `#263321` | Color |
| `--color-surface` | `#f9f8f5` | `#161514` | Color |
| `--color-surface-2` | `#fbfbf9` | `#1c1b19` | Color |
| `--color-surface-dynamic` | `#e6e4df` | `#2d2c2a` | Color |
| `--color-surface-offset` | `#f3f0ec` | `#1d1c1a` | Color |
| `--color-text` | `#28251d` | `#cdccca` | Color |
| `--color-text-faint` | `#bab9b4` | `#4a4948` | Color |
| `--color-text-muted` | `#7a7974` | `#797876` | Color |
| `--color-warning` | `#964219` | `#bb653b` | Color |
| `--color-warning-highlight` | `#ddcfc6` | `#2a1c12` | Color |
| `--font-body` | `'Satoshi',sans-serif` | `Inherited / Same as Light` | Font |
| `--font-display` | `'Cabinet Grotesk',sans-serif` | `Inherited / Same as Light` | Font |
| `--radius-full` | `9999px` | `Inherited / Same as Light` | Radius |
| `--radius-lg` | `0.75rem` | `Inherited / Same as Light` | Radius |
| `--radius-md` | `0.5rem` | `Inherited / Same as Light` | Radius |
| `--radius-sm` | `0.375rem` | `Inherited / Same as Light` | Radius |
| `--radius-xl` | `1rem` | `Inherited / Same as Light` | Radius |
| `--shadow-lg` | `0 12px 32px oklch(0.2 0.01 80/0.12)` | `0 12px 32px oklch(0 0 0/0.5)` | Shadow |
| `--shadow-md` | `0 4px 12px oklch(0.2 0.01 80/0.08)` | `0 4px 12px oklch(0 0 0/0.4)` | Shadow |
| `--shadow-sm` | `0 1px 2px oklch(0.2 0.01 80/0.06)` | `0 1px 2px oklch(0 0 0/0.3)` | Shadow |
| `--space-1` | `0.25rem` | `Inherited / Same as Light` | Spacing |
| `--space-10` | `2.5rem` | `Inherited / Same as Light` | Spacing |
| `--space-12` | `3rem` | `Inherited / Same as Light` | Spacing |
| `--space-16` | `4rem` | `Inherited / Same as Light` | Spacing |
| `--space-2` | `0.5rem` | `Inherited / Same as Light` | Spacing |
| `--space-3` | `0.75rem` | `Inherited / Same as Light` | Spacing |
| `--space-4` | `1rem` | `Inherited / Same as Light` | Spacing |
| `--space-5` | `1.25rem` | `Inherited / Same as Light` | Spacing |
| `--space-6` | `1.5rem` | `Inherited / Same as Light` | Spacing |
| `--space-8` | `2rem` | `Inherited / Same as Light` | Spacing |
| `--text-2xl` | `clamp(2rem,1.2rem + 2.5vw,3.5rem)` | `Inherited / Same as Light` | Text |
| `--text-base` | `clamp(1rem,0.95rem + 0.25vw,1.125rem)` | `Inherited / Same as Light` | Text |
| `--text-lg` | `clamp(1.125rem,1rem + 0.75vw,1.5rem)` | `Inherited / Same as Light` | Text |
| `--text-sm` | `clamp(0.875rem,0.8rem + 0.35vw,1rem)` | `Inherited / Same as Light` | Text |
| `--text-xl` | `clamp(1.5rem,1.2rem + 1.25vw,2.25rem)` | `Inherited / Same as Light` | Text |
| `--text-xs` | `clamp(0.75rem,0.7rem + 0.25vw,0.875rem)` | `Inherited / Same as Light` | Text |
| `--transition` | `180ms cubic-bezier(0.16,1,0.3,1)` | `Inherited / Same as Light` | Other |

### Playbook Token Heterogeneity & Categorization

The 21 completed playbooks fall into two distinct design system families:

1. **Family A (Standard Token Set - e.g. Seoraksan, Bukhansan, Hallasan, Jirisan, Soyosan, Sobaeksan, Odaesan, Wolchulsan, Woraksan)**:

   - Uses standard prefix `--color-*` (e.g. `--color-bg`, `--color-surface`, etc.) and `--space-*` tokens matching `index.html` structure.

2. **Family B (Legacy Compact Set - e.g. Sikjangsan, Gyeryongsan, Deogyusan, Juwangsan, Myeongseongsan, Naejangsan, Dobongsan, and Taiwan mountains)**:

   - Uses shortened prefixes like `--bg`, `--surface`, `--surface2`, `--border`, `--text`, `--muted`, `--faint` and shortened spacing tokens (e.g. `--s1`, `--s2` or no space tokens at all but raw pixels).


## 2. Layout & Template Anchor Audit

To support Phase 4 UI implementation, we have scanned all 21 completed playbooks to map the exact CSS selectors, container context, and HTML lines for the five upgrade insertion target components.

| Playbook File | Hero Anchor Selector / Context | Course Tabs / Selector | SVG Concept Map Selector | Difficulty Bars Selector | Accordion / Stats Anchor |
| --- | --- | --- | --- | --- | --- |
| `seoraksan-playbook.html` | `section.hero` (Line 211) | None found | `svg` in `.map` or `.elev` (Line 223) | No difficulty bar | `.acc-item` / `.stat-grid` (Line 253) |
| `hallasan-playbook.html` | `section.hero` (Line 184) | None found | `svg` in `.map` or `.elev` (Line 195) | No difficulty bar | `.acc-item` / `.stat-grid` (Line 222) |
| `jirisan-playbook.html` | `header.site-header` & `.hero-card` (Line 174, 220) | `.tabs` / `.tabs-nav` (Line 179) | `svg` in `.map` or `.elev` (Line 186) | `.bar` / `.dbg` (Line 232) | `.acc-item` / `.stat-grid` (Line 297) |
| `bukhansan-playbook.html` | `section.hero` (Line 322) | `.tabs` / `.tabs-nav` (Line 398) | `svg` in `.map` or `.elev` (Line 338) | No difficulty bar | No accordion/stats |
| `sobaeksan-playbook.html` | `section.hero` (Line 139) | `.tabs` / `.tabs-nav` (Line 158) | `svg` in `.map` or `.elev` (Line 150) | `.bar` / `.dbg` (Line 184) | `.acc-item` / `.stat-grid` (Line 176) |
| `gayasan-playbook.html` | `section.hero` (Line 152) | `.tabs` / `.tabs-nav` (Line 172) | `svg` in `.map` or `.elev` (Line 164) | `.bar` / `.dbg` (Line 198) | `.acc-item` / `.stat-grid` (Line 190) |
| `odaesan-playbook.html` | `section.hero` (Line 139) | `.tabs` / `.tabs-nav` (Line 158) | `svg` in `.map` or `.elev` (Line 150) | `.bar` / `.dbg` (Line 184) | `.acc-item` / `.stat-grid` (Line 176) |
| `naejangsan-playbook.html` | `section.hero` (Line 64) | `.tabs` / `.tabs-nav` (Line 95) | `svg` in `.map` or `.elev` (Line 121) | `.bar` / `.dbg` (Line 127) | `.acc-item` / `.stat-grid` (Line 88) |
| `chiaksan-playbook.html` | *Pending (No File)* | *Pending* | *Pending* | *Pending* | *Pending* |
| `deogyusan-playbook.html` | `section.hero` (Line 158) | `.tabs` / `.tabs-nav` (Line 177) | `svg` in `.map` or `.elev` (Line 169) | `.bar` / `.dbg` (Line 203) | `.acc-item` / `.stat-grid` (Line 195) |
| `gyeryongsan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |
| `wolchulsan-playbook.html` | `section.hero` (Line 293) | `.tabs` / `.tabs-nav` (Line 353) | `svg` in `.map` or `.elev` (Line 308) | No difficulty bar | No accordion/stats |
| `mudeungsan-playbook.html` | *Pending (No File)* | *Pending* | *Pending* | *Pending* | *Pending* |
| `baekhaksan-playbook.html` | *Pending (No File)* | *Pending* | *Pending* | *Pending* | *Pending* |
| `duryunsan-playbook.html` | *Pending (No File)* | *Pending* | *Pending* | *Pending* | *Pending* |
| `minjusan-playbook.html` | *Pending (No File)* | *Pending* | *Pending* | *Pending* | *Pending* |
| `sikjangsan-playbook.html` | `section.hero` (Line 27) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 27) | `.bar` / `.dbg` (Line 31) | `.acc-item` / `.stat-grid` (Line 28) |
| `woraksan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |
| `dobongsan-playbook.html` | `section.hero` (Line 157) | None found | `svg` in `.map` or `.elev` (Line 171) | `.bar` / `.dbg` (Line 235) | `.acc-item` / `.stat-grid` (Line 251) |
| `soyosan-playbook.html` | `section.hero` (Line 212) | `.tabs` / `.tabs-nav` (Line 297) | `svg` in `.map` or `.elev` (Line 214) | `.bar` / `.dbg` (Line 317) | No accordion/stats |
| `juwangsan-playbook.html` | `section.hero` (Line 161) | None found | `svg` in `.map` or `.elev` (Line 178) | `.bar` / `.dbg` (Line 274) | No accordion/stats |
| `myeongseongsan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |
| `taebaeksan-playbook.html` | `section.hero` (Line 178) | `.tabs` / `.tabs-nav` (Line 197) | `svg` in `.map` or `.elev` (Line 189) | `.bar` / `.dbg` (Line 223) | `.acc-item` / `.stat-grid` (Line 215) |
| `yushan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |
| `xueshan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |
| `yangmingshan-playbook.html` | `section.hero` (Line 28) | `.tabs` / `.tabs-nav` (Line 29) | `svg` in `.map` or `.elev` (Line 28) | `.bar` / `.dbg` (Line 33) | `.acc-item` / `.stat-grid` (Line 29) |

## 3. Playbook-specific Details & Design Insights

Below is the specific detailed analysis for each mountain's playbook to serve as guide for visual upgrading:

### 설악산 (Seoraksan)
- **ID:** `seoraksan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1708m
- **Region/Country:** 강원 / KR
- **Landmarks:** 대청봉, 공룡능선, 울산바위, 비룡폭포, 오색
- **Season Signature:** 가을 단풍·겨울 설경
- **Search Term Candidates:** `Seoraksan`, `Seoraksan National Park`, `Ulsanbawi`
- **Custom CSS Variables (First 10):** `--color-bg: #f7f6f2`, `--color-surface: #f9f8f5`, `--color-surface-2: #fbfbf9`, `--color-surface-offset: #f3f0ec`, `--color-surface-dynamic: #e6e4df`, `--color-divider: #dcd9d5`, `--color-border: #d4d1ca`, `--color-text: #28251d`, `--color-text-muted: #7a7974`, `--color-text-faint: #bab9b4`

### 한라산 (Hallasan)
- **ID:** `hallasan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1950m
- **Region/Country:** 제주 / KR
- **Landmarks:** 백록담, 성판악, 관음사, 어리목, 영실
- **Season Signature:** 백록담 설경·봄 진달래
- **Search Term Candidates:** `Hallasan`, `Hallasan National Park Jeju`, `Baengnokdam`
- **Custom CSS Variables (First 10):** `--color-bg: #f5f4f0`, `--color-surface: #f8f7f4`, `--color-surface-2: #fafaf8`, `--color-surface-offset: #f0ede9`, `--color-surface-dynamic: #e5e2dd`, `--color-divider: #d9d6d0`, `--color-border: #d0cdc6`, `--color-text: #26231b`, `--color-text-muted: #787570`, `--color-text-faint: #b6b4af`

### 지리산 (Jirisan)
- **ID:** `jirisan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1915m
- **Region/Country:** 전라 / KR
- **Landmarks:** 천왕봉, 노고단, 성삼재, 백무동, 대피소
- **Season Signature:** 철쭉·운해·겨울 눈꽃
- **Search Term Candidates:** `Jirisan`, `Jirisan National Park`, `Cheonwangbong`
- **Custom CSS Variables (First 10):** `--color-bg: #f7f6f2`, `--color-surface: #f9f8f5`, `--color-surface-2: #fbfbf9`, `--color-surface-offset: #f3f0ec`, `--color-divider: #dcd9d5`, `--color-border: #d4d1ca`, `--color-text: #28251d`, `--color-text-muted: #7a7974`, `--color-text-faint: #bab9b4`, `--color-primary: #01696f`

### 북한산 (Bukhansan)
- **ID:** `bukhansan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 836m
- **Region/Country:** 경기 / KR
- **Landmarks:** 백운대, 인수봉, 국망봉, 도선사
- **Season Signature:** 사계절 인수봉 암릉 조망
- **Search Term Candidates:** `Bukhansan`, `Bukhansan National Park Seoul`, `Baegundae`
- **Custom CSS Variables (First 10):** `--color-bg: #f5f7f2`, `--color-surface: #f8faf5`, `--color-surface-2: #fcfdf9`, `--color-surface-offset: #eef2e8`, `--color-surface-dynamic: #e4ead9`, `--color-divider: #d6ddc9`, `--color-border: #c8d1b8`, `--color-text: #1e2a14`, `--color-text-muted: #5a6847`, `--color-text-faint: #9aaa85`

### 소백산 (Sobaeksan)
- **ID:** `sobaeksan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1440m
- **Region/Country:** 충청 / KR
- **Landmarks:** 비로봉, 연화봉, 국망봉, 희방사
- **Season Signature:** 봄철 철쭉 군락·겨울 칼바람 설경
- **Search Term Candidates:** `Sobaeksan`, `Sobaeksan National Park`, `Birobong`
- **Custom CSS Variables (First 10):** `--bg: #f0f2f7`, `--surface: #f4f6fb`, `--surface2: #f8f9fd`, `--surfaceoff: #e4e8f2`, `--surfdyn: #d4daea`, `--div: #c2cad8`, `--bor: #b8c2d4`, `--txt: #1a1e2e`, `--muted: #6a7290`, `--faint: #a8b0c8`

### 가야산 (Gayasan)
- **ID:** `gayasan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1433m
- **Region/Country:** 경상 / KR
- **Landmarks:** 상왕봉, 칠불봉, 해인사, 홍류동계곡
- **Season Signature:** 해인사 가을 단풍·상왕봉 조망
- **Search Term Candidates:** `Gayasan`, `Gayasan National Park`, `Haeinsa`
- **Custom CSS Variables (First 10):** `--bg: #f2f0ea`, `--surface: #f6f5f0`, `--surface2: #fafaf6`, `--surfaceoff: #e8e4dc`, `--surfdyn: #d8d2c6`, `--div: #ccc6ba`, `--bor: #bfb8ab`, `--txt: #1e1a14`, `--muted: #6e6558`, `--faint: #a8a090`

### 오대산 (Odaesan)
- **ID:** `odaesan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1563m
- **Region/Country:** 강원 / KR
- **Landmarks:** 비로봉, 동대산, 두로봉, 월정사, 상원사
- **Season Signature:** 겨울 눈꽃 전나무숲길·가을 사찰단풍
- **Search Term Candidates:** `Odaesan`, `Odaesan National Park`, `Woljeongsa`
- **Custom CSS Variables (First 10):** `--bg: #f2f4f0`, `--surface: #f6f8f4`, `--surface2: #f9faf8`, `--surfaceoff: #e6ece0`, `--surfdyn: #d8e0d0`, `--div: #c8d0c0`, `--bor: #bfc8b6`, `--txt: #1c211a`, `--muted: #727a6a`, `--faint: #aab3a0`

### 내장산 (Naejangsan)
- **ID:** `naejangsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 763m
- **Region/Country:** 전라 / KR
- **Landmarks:** 신선봉, 내장사, 단풍터널, 백양사
- **Season Signature:** 가을 단풍터널 극치
- **Search Term Candidates:** `Naejangsan`, `Naejangsan National Park`, `Naejangsa`
- **Custom CSS Variables (First 10):** `--bg: #f7f5f1`, `--surface: #fbfaf7`, `--surface2: #f2eee7`, `--border: #ddd7cc`, `--text: #221f18`, `--muted: #736e64`, `--faint: #b9b1a4`, `--green: #3e7d3f`, `--greenbg: #dcebdc`, `--blue: #2d6faa`

### 치악산 (Chiaksan)
- **ID:** `chiaksan`
- **Status:** Pending (No playbook)
- **Altitude:** 1288m
- **Region/Country:** 강원 / KR
- **Landmarks:** 비로봉, 남대봉, 향로봉, 구룡사
- **Season Signature:** 겨울 설경·구룡사 계곡 단풍
- **Search Term Candidates:** `Chiaksan`, `Chiaksan National Park`, `Birobong`

### 덕유산 (Deogyusan)
- **ID:** `deogyusan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1614m
- **Region/Country:** 전라 / KR
- **Landmarks:** 향적봉, 중봉, 설천봉, 구천동계곡, 무주리조트
- **Season Signature:** 겨울 눈꽃 상고대·구천동 계곡
- **Search Term Candidates:** `Deogyusan`, `Deogyusan National Park`, `Hyangjeokbong`
- **Custom CSS Variables (First 10):** `--bg: #f4f3f0`, `--surface: #f8f7f4`, `--surface2: #fafaf8`, `--surfaceoff: #ece6de`, `--surfdyn: #dfd8cc`, `--div: #cec7be`, `--bor: #c5bdb3`, `--txt: #201e19`, `--muted: #7a7570`, `--faint: #b0aba4`

### 계룡산 (Gyeryongsan)
- **ID:** `gyeryongsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 845m
- **Region/Country:** 충청 / KR
- **Landmarks:** 천정봉, 관음봉, 삼불봉, 동학사, 갑사
- **Season Signature:** 봄 벚꽃·가을 갑사 단풍
- **Search Term Candidates:** `Gyeryongsan`, `Gyeryongsan National Park`, `Gapsa`
- **Custom CSS Variables (First 10):** `--bg: #f5f6fb`, `--surface: #fcfcfe`, `--surface2: #e8ebf4`, `--border: #d5dbea`, `--text: #1b2230`, `--muted: #687387`, `--faint: #a2acbd`, `--blue: #637bb4`, `--bluebg: #dfe6f8`, `--green: #5e8572`

### 월출산 (Wolchulsan)
- **ID:** `wolchulsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 809m
- **Region/Country:** 전라 / KR
- **Landmarks:** 천황봉, 구정봉, 사자봉, 구름다리, 도갑사
- **Season Signature:** 가을 억새·봄 야생화 기암절벽
- **Search Term Candidates:** `Wolchulsan`, `Wolchulsan National Park`, `구름다리`
- **Custom CSS Variables (First 10):** `--color-bg: #f7f5f0`, `--color-surface: #faf8f4`, `--color-surface-2: #fcfbf8`, `--color-surface-offset: #f0ece4`, `--color-border: #ddd8ce`, `--color-divider: #e5e0d8`, `--color-text: #1e1b14`, `--color-text-muted: #7a7568`, `--color-text-faint: #bbb5aa`, `--color-text-inverse: #f9f7f3`

### 무등산 (무등산)
- **ID:** `mudeungsan`
- **Status:** Pending (No playbook)
- **Altitude:** 1187m
- **Region/Country:** 전라 / KR
- **Landmarks:** 천왕봉, 지왕봉, 인왕봉, 서석대, 입석대, 규봉암
- **Season Signature:** 서석대·입석대 주상절리 겨울설경
- **Search Term Candidates:** `Mudeungsan`, `Mudeungsan National Park Gwangju`, `Seoseokdae`

### 백학산 (Baekhaksan)
- **ID:** `baekhaksan`
- **Status:** Pending (No playbook)
- **Altitude:** 876m
- **Region/Country:** 경기 / KR
- **Landmarks:** 백학산, 연천
- **Season Signature:** 조용하고 한적한 가을 숲길
- **Search Term Candidates:** `Baekhaksan`, `Baekhaksan Yeoncheon Korea`, `Yeoncheon`

### 두륜산 (Duryunsan)
- **ID:** `duryunsan`
- **Status:** Pending (No playbook)
- **Altitude:** 703m
- **Region/Country:** 전라 / KR
- **Landmarks:** 가련봉, 두륜봉, 고계봉, 대흥사
- **Season Signature:** 사계절 동백나무 숲·가을 대흥사 계곡
- **Search Term Candidates:** `Duryunsan`, `Duryunsan Haenam`, `Daeheungsa`

### 민주지산 (Minjujisan)
- **ID:** `minjusan`
- **Status:** Pending (No playbook)
- **Altitude:** 1242m
- **Region/Country:** 충청 / KR
- **Landmarks:** 민주지산, 삼도봉, 석기봉, 물한계곡
- **Season Signature:** 봄 야생화·여울계곡 피서
- **Search Term Candidates:** `Minjujisan`, `Minjujisan Korea`, `Samdobong`

### 식장산 (Sikjangsan)
- **ID:** `sikjangsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 598m
- **Region/Country:** 충청 / KR
- **Landmarks:** 꾀꼬리봉, 국사봉, 독수리봉, 식장산 정상
- **Season Signature:** 도심 대전 야경·독수리봉 가을 조망
- **Search Term Candidates:** `Sikjangsan`, `Sikjangsan Daejeon`, `독수리봉`
- **Custom CSS Variables (First 10):** `--bg: #f5f7f4`, `--surface: #fbfcfb`, `--surface2: #e8eee6`, `--border: #d4ddd1`, `--text: #192218`, `--muted: #687464`, `--faint: #9fac9a`, `--pine: #5c7d63`, `--pinebg: #dce8df`, `--amber: #b68d4e`

### 월악산 (Woraksan)
- **ID:** `woraksan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1097m
- **Region/Country:** 충청 / KR
- **Landmarks:** 영봉, 중봉, 하봉, 덕주사, 신륵사, 보덕암
- **Season Signature:** 가을 단풍·충주호 월악 영봉 조망
- **Search Term Candidates:** `Woraksan`, `Woraksan National Park`, `Yeongbong`
- **Custom CSS Variables (First 10):** `--bg: #f6f4ef`, `--surface: #fcfbf8`, `--surface2: #ece7de`, `--border: #d9d0c3`, `--text: #241f18`, `--muted: #736b60`, `--faint: #afa79b`, `--green: #5f7d53`, `--greenbg: #dbe5d5`, `--blue: #667295`

### 도봉산 (Dobongsan)
- **ID:** `dobongsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 740m
- **Region/Country:** 경기 / KR
- **Landmarks:** 자운봉, 만장봉, 선인봉, 신선대, 망월사
- **Season Signature:** 기암절벽 가을 단풍·사계절 암릉
- **Search Term Candidates:** `Dobongsan`, `Dobongsan Seoul`, `Jaunbong`
- **Custom CSS Variables (First 10):** `--color-bg: #f5f7f2`, `--color-surface: #fff`, `--color-surface-2: #f0f4ee`, `--color-surface-offset: #e8ede5`, `--color-border: #d4dbd0`, `--color-divider: #e2e8df`, `--color-text: #1e2b19`, `--color-text-muted: #5a6e54`, `--color-text-faint: #9aad93`, `--color-beginner: #2d7a3a`

### 소요산 (Soyosan)
- **ID:** `soyosan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 587m
- **Region/Country:** 경기 / KR
- **Landmarks:** 의상대, 공주봉, 자재암, 선녀탕
- **Season Signature:** 자재암 가을 단풍 터널
- **Search Term Candidates:** `Soyosan`, `Soyosan Dongducheon`, `Jajaeam`
- **Custom CSS Variables (First 10):** `--color-bg: #f7f6f2`, `--color-surface: #f9f8f5`, `--color-surface-2: #fbfbf9`, `--color-surface-offset: #f3f0ec`, `--color-surface-dynamic: #e6e4df`, `--color-divider: #dcd9d5`, `--color-border: #d4d1ca`, `--color-text: #28251d`, `--color-text-muted: #7a7974`, `--color-text-faint: #bab9b4`

### 주왕산 (Juwangsan)
- **ID:** `juwangsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 721m
- **Region/Country:** 경상 / KR
- **Landmarks:** 주왕산, 주방천계곡, 주왕굴, 용추폭포, 절골계곡
- **Season Signature:** 기암 절경과 주방천 폭포 단풍
- **Search Term Candidates:** `Juwangsan`, `Juwangsan National Park`, `Jubang valley`
- **Custom CSS Variables (First 10):** `--color-bg: #f5f3ef`, `--color-surface: #faf9f7`, `--color-surface-2: #ffffff`, `--color-surface-offset: #ece9e3`, `--color-divider: #dbd8d1`, `--color-border: #ccc9c1`, `--color-text: #1e1c18`, `--color-text-muted: #6b6860`, `--color-text-faint: #a8a69f`, `--color-text-inverse: #f5f3ef`

### 명성산 (Myeongseongsan)
- **ID:** `myeongseongsan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 922m
- **Region/Country:** 경기 / KR
- **Landmarks:** 명성산, 삼각봉, 억새군락지, 산정호수
- **Season Signature:** 가을 은빛 물억새 군락·산정호수
- **Search Term Candidates:** `Myeongseongsan`, `Myeongseongsan Pocheon`, `Sanjeong lake`
- **Custom CSS Variables (First 10):** `--bg: #f5f4ef`, `--surface: #fbfaf7`, `--surface2: #efebe4`, `--border: #ddd7cd`, `--text: #1f1c17`, `--muted: #716b61`, `--faint: #b4ab9d`, `--green: #427b49`, `--greenbg: #dbe9dd`, `--blue: #2f6ba3`

### 태백산 (Taebaeksan)
- **ID:** `taebaeksan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1567m
- **Region/Country:** 강원 / KR
- **Landmarks:** 장군봉, 천제단, 문수봉, 유일사, 당골광장, 주목군락
- **Season Signature:** 겨울 천제단 설경·주목 상고대
- **Search Term Candidates:** `Taebaeksan`, `Taebaeksan National Park`, `Cheonjedan`
- **Custom CSS Variables (First 10):** `--bg: #f6f5f1`, `--surface: #f9f8f5`, `--surface2: #fbfaf8`, `--surfaceoff: #efe8e0`, `--surfdyn: #e3d9ce`, `--div: #d5cdc4`, `--bor: #ccc4ba`, `--txt: #22201a`, `--muted: #7a7470`, `--faint: #b5b0aa`

### 위산 (Yushan)
- **ID:** `yushan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 3952m
- **Region/Country:** 대만 / TW
- **Landmarks:** 위산 주봉, 배운산장, 타타카 들머리
- **Season Signature:** 고산 일출·사계절 야생화·운해
- **Search Term Candidates:** `Yushan`, `Yushan Taiwan`, `Yushan main peak`
- **Custom CSS Variables (First 10):** `--bg: #f6f3ee`, `--surface: #fcfaf7`, `--surface2: #eee8e0`, `--border: #ddd4c8`, `--text: #211d18`, `--muted: #72685b`, `--faint: #afa394`, `--green: #6a7d4c`, `--greenbg: #e5eadc`, `--blue: #456e96`

### 설산 (Xueshan)
- **ID:** `xueshan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 3886m
- **Region/Country:** 대만 / TW
- **Landmarks:** 설산 주봉, 369산장, 흑삼림, 설산동봉
- **Season Signature:** 빙하 권곡 설경·사계절 숲
- **Search Term Candidates:** `Xueshan`, `Xueshan Taiwan`, `369 Cabin`
- **Custom CSS Variables (First 10):** `--bg: #f3f5f7`, `--surface: #fbfcfd`, `--surface2: #e9eef2`, `--border: #d4dde4`, `--text: #192129`, `--muted: #65707a`, `--faint: #a5afb9`, `--green: #5f7c8c`, `--greenbg: #deeaef`, `--blue: #496aa3`

### 양명산 (Yangmingshan)
- **ID:** `yangmingshan`
- **Status:** Completed (Playbook exists)
- **Altitude:** 1120m
- **Region/Country:** 대만 / TW
- **Landmarks:** 칠성산 주봉, 소유갱, 냉수갱, 칭티엔강
- **Season Signature:** 봄철 진달래·유황 온천 화산 경관
- **Search Term Candidates:** `Yangmingshan`, `Yangmingshan Taiwan`, `Qixingshan`
- **Custom CSS Variables (First 10):** `--bg: #f4f5f1`, `--surface: #fcfcfa`, `--surface2: #eef1ea`, `--border: #d8ddd2`, `--text: #1d221b`, `--muted: #667061`, `--faint: #a7b0a2`, `--green: #4f7d4a`, `--greenbg: #dfeadf`, `--blue: #326f95`
