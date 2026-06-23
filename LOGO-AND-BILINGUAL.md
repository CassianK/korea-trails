# Korea Trails — 로고 리디자인(5종 선택) + 전체 영문화(KR/EN) + 언어 전환기

> **2개 트랙 통합 실행 스펙.** 런타임: Antigravity/Claude Code 서브에이전트. 새 브랜치 `feat/logo-i18n`, 산 단위 커밋, main 직접 푸시 금지, 검증 후 PR.
> 디자인 시스템·기존 템플릿 100% 준수. 두 정지점(로고 선택 / 영문화 파일럿)에서 멈춰 사용자 승인.

---

## 트랙 A — 로고 리디자인 (5종 제시 → 사용자 선택 → 적용)

### A1. 현황 & 목표
현재 로고(단순 산능선 SVG)가 약하다. **임팩트 있고 프리미엄한** 로고로 교체. 단색(헤더·currentColor)·풀컬러·파비콘·OG로 모두 파생 가능해야 함. 다크/라이트 양쪽 가독.

### A2. 5개 방향(에이전트가 각각 SVG로 제작)
1. **Topographic Peak** — 등고선(컨투어)이 겹쳐 봉우리를 이루는 지도학적 마크. 모던·정밀.
2. **Monoline Summit + Trail** — 한 획 선으로 그린 봉우리 + 스위치백 등산로 + 정상 점/태양. 경쾌·미니멀.
3. **Negative-space Wordmark** — "Korea Trails" 워드마크의 한 글자(예: A/K)에 봉우리를 음각. 타이포 중심.
4. **Heritage Badge** — 원형 국립공원 크레스트(산+태양+"KOREA TRAILS" 링). 아웃도어 헤리티지·프리미엄.
5. **K-Peak Monogram** — "K"(또는 KT)를 능선으로 추상화한 앱아이콘형 볼드 마크. 파비콘·소셜 강함.

각 방향: 가로 워드마크 락업 + 아이콘 단독, 단색/풀컬러, 라이트·다크 시안, 파비콘 32px 가독 확인.

### A3. 선택 게이트(정지점 1)
에이전트가 **`logo-options.html` 미리보기 페이지**를 만들어 5종을 (헤더 컨텍스트·라이트/다크·파비콘 크기로) 나란히 렌더 → 사용자가 1개 선택. **선택 전 적용 금지.**

### A4. 적용
선택 로고를 전 페이지(27개) 헤더 SVG + `assets/brand/logo.svg`·`favicon.svg` + OG 카드 마크에 일괄 반영, 기존 로고 제거. design-system 토큰 색 사용.

---

## 트랙 B — 전체 영문화(KR/EN) + 언어 전환기

### B1. 접근 방식 — `/en/` 미러 + hreflang (권장)
전체 콘텐츠 완역이므로 **JS 사전 방식이 아니라 실제 EN 페이지**를 생성한다(긴 본문·SEO에 유리, 빌드리스 호환).
- 구조 미러: `index.html` ↔ `en/index.html`, `<산>-playbook.html` ↔ `en/<산>-playbook.html`.
- 공유 자산(css/img/video/icons)은 상대경로(`../assets/...`)로 참조, 중복 복제 금지.
- 각 페이지 `<html lang>` 정확히(ko/en), `<link rel="alternate" hreflang="ko|en|x-default">` 상호 연결, OG `locale` 설정.

### B2. 언어 전환기(KR/EN)
- 헤더에 **KR/EN 토글** 추가(전 페이지). 현재 페이지의 반대언어 카운터파트로 링크(매핑 규칙: `/en/` 접두).
- 사용자가 선택한 언어를 `localStorage`에 기억해 토글 활성 상태 표시(강제 리다이렉트 없음, 명시적 전환).
- 키보드 접근·`aria-pressed`·포커스 가시성.

### B3. 번역 품질 가드레일(안전 직결)
- **수치·단위·좌표 불변**(거리·시간·표고·요금·배차는 그대로). 숫자 오역 금지.
- **고유명사 일관 로마자(국어의 로마자 표기법)**: Seoraksan, Daecheongbong, Ulsanbawi … 용어집(`_orchestration/glossary.json`) 만들어 전 페이지 일관 적용.
- 위험구간·통제·계절 주의는 의미 손실 없이 정확히 번역(과장·축소 금지).
- 한국 문화·지명은 짧은 영문 보조설명 허용(예: "Daecheongbong (main peak)").

### B4. 범위
index + 활성 플레이북 26개 전부 EN 생성. 트래킹 영상 라벨·교통·체크포인트표·팁·경고·캡션·메타까지 완역. 영상/지도/이미지 자산은 공유(언어 무관).

---

## 단계 & 게이트

| Phase | 내용 | 게이트 |
|---|---|---|
| A1 로고 5종 | 5개 SVG + logo-options.html | **사용자 1개 선택(정지점1)** |
| A2 로고 적용 | 27p 헤더·파비콘·OG 반영 | 단색/컬러·다크/라이트·파비콘 렌더 OK |
| B1 i18n 파일럿 | en/index + en/seoraksan + 토글 | **사용자 번역품질·전환기 확인(정지점2)** |
| B2 영문화 확장 | 나머지 25 EN 생성 | 페이지별 hreflang·자산경로·무회귀 |
| QA | 통합 검증 | 아래 합격기준 GREEN |

> 파일럿: 로고 선택 후, 영문화는 index+설악산 EN 1쌍으로 품질·전환기 검증 뒤 확장.

---

## 합격 기준 (Definition of Done)

- [ ] 사용자 선택 로고 1종, 27p 헤더·favicon.svg·OG 일괄 반영(벡터·단색/컬러·다크/라이트)
- [ ] index + 26 플레이북의 EN 카운터파트(`/en/`) 전부 생성, 콘텐츠 완역
- [ ] KR/EN 토글 전 페이지 동작(상호 매핑), localStorage 기억, aria·키보드
- [ ] hreflang(ko/en/x-default)·`<html lang>`·OG locale 정확, 공유 자산 경로 정상(깨짐 0)
- [ ] 수치·단위 불변, 고유명사 로마자 일관(glossary), 위험·통제 정확 번역
- [ ] EN 페이지에 미번역 한글 잔존 0(고유명사 로마자 제외), 무회귀(지도·영상·검색/필터), 콘솔 에러 0
- [ ] Lighthouse a11y/SEO 유지, 산 단위 커밋, 검증 GREEN 후 PR·머지

---

## 마스터 킥오프 프롬프트 (오케스트레이터에게 복붙)

```
너는 Korea Trails 'logo-i18n' 트랙의 ORCHESTRATOR다. LOGO-AND-BILINGUAL.md를 단일 진실원천으로,
새 브랜치 feat/logo-i18n에서 두 트랙을 수행한다. 하드제약: 빌드리스·다크/라이트·a11y(AA)·무회귀·
정보손실0·산 단위 커밋·main 직접 푸시 금지. 디자인 시스템·기존 템플릿 100% 준수.

[트랙 A — 로고]
1) 임팩트 있는 로고 5개 방향을 각각 SVG로 제작(문서 A2: Topographic Peak / Monoline Summit+Trail /
   Negative-space Wordmark / Heritage Badge / K-Peak Monogram). 각 단색(currentColor)+풀컬러, 라이트/다크,
   파비콘 32px 가독.
2) logo-options.html 미리보기 페이지에 5종을 헤더 컨텍스트·라이트/다크·파비콘 크기로 나란히 렌더하고
   ★여기서 멈춰 사용자에게 1개를 선택받는다(정지점1).
3) 선택 로고를 전 페이지(27개) 헤더 SVG + assets/brand/logo.svg·favicon.svg + OG 마크에 일괄 반영,
   기존 로고 제거.

[트랙 B — 전체 영문화 + 언어 전환기]
4) /en/ 미러 구조로 실제 EN 페이지 생성(JS 사전 방식 금지): index.html↔en/index.html,
   <산>-playbook.html↔en/<산>-playbook.html. 공유 자산은 ../assets 상대경로로 참조(복제 금지).
5) 헤더에 KR/EN 토글 추가(전 페이지, 상호 카운터파트 링크, localStorage 기억, aria-pressed·키보드).
   각 페이지 <html lang>, hreflang(ko/en/x-default) 상호연결, OG locale 설정.
6) 번역 가드레일: 수치·단위·좌표 불변, 고유명사는 _orchestration/glossary.json 기반 일관 로마자
   (국어 로마자 표기법: Seoraksan, Daecheongbong 등), 위험·통제·계절 주의 정확 번역, 미번역 한글 잔존 0.
7) ★먼저 index+설악산 EN 1쌍과 토글을 만들어 사용자에게 번역품질·전환기를 확인받은 뒤(정지점2)
   나머지 25개로 확장한다.

검증: EN 페이지 hreflang·자산경로·미번역 한글 스캔·무회귀(지도/영상/검색/필터)·콘솔0·Lighthouse 유지.
각 단계·게이트 종료 시 결과를 1~2문장 보고하고, 정지점에서는 반드시 멈춰 승인받아라.
시작 전 전체 실행계획을 요약해 승인받아라.
```

---

## 운용 메모 (사용자)
- 로고는 **5종 미리보기에서 직접 고른 뒤** 적용됩니다(잘못된 대량 반영 방지).
- 영문화는 26개 완역이라 큰 작업 → **설악산 EN 파일럿으로 번역 톤·전환기**를 먼저 확인하세요.
- 유지보수: 이후 KR 본문 수정 시 EN 카운터파트도 함께 갱신해야 함(글로서리·hreflang 일관).
- 파일럿(로고 5종 + 설악산 EN)이 나오면 코드로 검수해 확장 게이트를 함께 판단하겠습니다.

---

*Korea Trails 로고 리디자인 + 전체 영문화(KR/EN) + 언어 전환기 · v1.0*
