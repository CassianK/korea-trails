# Korea Trails — 트래킹 영상 섹션 + 실사 루트 지도 + 백학산 삭제 + 운악산 신설

> **4개 작업 통합 실행 스펙.** 런타임: Antigravity/Claude Code 서브에이전트. 새 브랜치 `feat/tracking-videos-maps`에서 산 단위 커밋, main 직접 푸시 금지, 검증 후 PR.
> 디자인 시스템·템플릿은 기존 통합 플레이북을 100% 준수(새 마크업 발명 금지, 대상 파일 정독).

---

## 작업 1 — 백학산 완전 삭제

- `index.html`의 `MOUNTAINS[]`에서 `baekhaksan` 항목 **완전 제거**(카드 자체 삭제).
- 관련 자산 정리: `assets/img/baekhaksan/`, `assets/video/baekhaksan/`(있으면), `_orchestration/research-baekhaksan.json`, `_assets/asset-manifest.json`·`CREDITS.md`의 baekhaksan 항목 제거.
- 잔존 참조 0 확인(`grep -ri baekhaksan` → 코드/링크 없음). hero 통계 카운트(등록 명산 수) 갱신.

---

## 작업 2 — 산별 "내 트래킹 영상" 유튜브 섹션 (신규 재사용 컴포넌트)

### 2.1 컴포넌트 규격
- 플레이북에 신규 섹션 **"🎬 내 트래킹 영상"** 추가(팁/갤러리 다음, 푸터 앞). 디자인시스템 클래스 재사용(`section-title`/`card`/그리드).
- **데이터 주도**: 아래 `videos.json`에 항목이 있는 산만 섹션 렌더. 없는 산은 섹션 미표시.
- **세로(9:16) 쇼츠 그리드**: 반응형(데스크톱 4~5열, 모바일 2열), 각 항목은 캡션(사용자 라벨) + 썸네일.
- **성능: 파사드(facade) 패턴 필수** — 14개까지 있으므로 iframe을 한꺼번에 로드하지 말 것. 기본은 썸네일 이미지(`https://i.ytimg.com/vi/<ID>/hqdefault.jpg`, object-fit:cover, 9:16 박스) + 재생버튼. **클릭 시에만** `https://www.youtube-nocookie.com/embed/<ID>?autoplay=1` iframe으로 교체.
- 접근성: 각 파사드는 `<button>` + `aria-label="<라벨> 유튜브 쇼츠 재생"`. 키보드 포커스·Enter 재생. `loading="lazy"`.
- 프라이버시: `youtube-nocookie.com` 사용. 자동재생은 클릭 후에만.
- 외부 링크: 각 항목에 원본 쇼츠로 가는 보조 링크(`https://youtube.com/shorts/<ID>`) 제공.

### 2.2 임베드 데이터 — `_orchestration/videos.json`
```json
{
  "dobongsan": [
    {"id": "fqzChTcpmjM", "label": "신선대"},
    {"id": "JeCUmWleiK4", "label": "주봉·신선대"},
    {"id": "YMghILiM-4c", "label": "우이암"},
    {"id": "D_P56H5LcWs", "label": "우이령·오봉·석굴암"},
    {"id": "ER2uyn2WmFE", "label": "만월사"},
    {"id": "lHu7jaQ-32w", "label": "냥이 천국"},
    {"id": "IVMQiilgr_M", "label": "정상 고양이"},
    {"id": "h7AtXJMzggI", "label": "고양이 2"},
    {"id": "vnEniq-ljRA", "label": "고양이 3"},
    {"id": "P3zO2XUmo6o", "label": "냥이와 교감"},
    {"id": "kYBnFPkAc2s", "label": "대서 개미왕국 탄생"},
    {"id": "8gGM0qgEvY4", "label": "거북바위"}
  ],
  "bukhansan": [
    {"id": "Vk7J8vaG3Y0", "label": "칼바위"},
    {"id": "IFi9TguP7f0", "label": "대동문·조국문"},
    {"id": "ZPHm7E6kvrA", "label": "능선 구간"},
    {"id": "vaKLvPNpVdw", "label": "중흥사 고양이"},
    {"id": "b5vbksD_0OE", "label": "고양이 2"},
    {"id": "zKM1r8udgDY", "label": "고양이 3"},
    {"id": "pJksnZhdD1A", "label": "백운대 말벌"}
  ],
  "myeongseongsan": [
    {"id": "LYelDwOGetc", "label": "명성산 트래킹"}
  ],
  "soyosan": [
    {"id": "HuzexupXWM0", "label": "소요산 트래킹"},
    {"id": "ASSAHfoC0Q4", "label": "새소리"},
    {"id": "QhETC_XL_h4", "label": "새소리 2"},
    {"id": "2KnijiRywpE", "label": "새소리 3"},
    {"id": "dakqMbjfcP8", "label": "긴꼬리제비나비"},
    {"id": "CJ4KMp_rYqQ", "label": "제비나비 2"},
    {"id": "BsPpue3ox1Y", "label": "청띠신선나비"},
    {"id": "VWT3BQ0w_Yw", "label": "나비 3"},
    {"id": "8bBBvKqGB78", "label": "노린재"},
    {"id": "qBhBODJvVIo", "label": "화장실 점거한 여치들"},
    {"id": "SvXrG-hKFLU", "label": "홍단 딱정벌레"},
    {"id": "yy8X9meEcQM", "label": "꼬마산 개구리"},
    {"id": "yTtuOOH6h4U", "label": "버섯"},
    {"id": "qP09anuR4bA", "label": "버섯 2"}
  ],
  "unaksan": [
    {"id": "Xqn7ifPKOGQ", "label": "거미"},
    {"id": "2k7E12b1cL0", "label": "거미 2"},
    {"id": "AotVM9VuzIA", "label": "거미 3"},
    {"id": "neAIZX4lEJY", "label": "적멸보궁"}
  ]
}
```
> 위 ID는 사용자 제공 쇼츠 URL에서 추출한 정확값. 빌드 시 이 JSON을 단일 출처로 사용(재전사 금지).

---

## 작업 3 — 실사 루트 지도 (영상 있는 산: 도봉·북한·명성·소요·운악)

- **방식**: `SAMPLE-yangmingshan-upgrade.md`의 A‑MAP 설계 그대로 — Leaflet(CDN) + Esri 위성/OpenTopoMap 지형 토글, **실제 등산 루트 폴리라인 + 체크포인트 마커**.
- **좌표 리서치**: 각 산의 기존 체크포인트 표/코스 데이터를 실제 위경도로 확정(공식 지도·KNPS·OSM 교차). 코스별 색상(초/중/고) 계승.
- **삽입**: 기존 "코스 개념도/지도" 섹션을 Leaflet 컨테이너로 교체하되 **기존 SVG는 폴백 보존**(JS 실패·noscript 시 표시).
- 데스크톱/다크/반응형/a11y, lazy init(IntersectionObserver), scrollWheelZoom 포커스 활성, 타일 attribution 표기.
- 산출물: 각 플레이북 지도 교체 + `_orchestration/map-config-<id>.json`(좌표 계약, 양명산 스키마 동일).
- **검증 게이트(중요)**: 좌표가 실제 지형·정상·들머리와 부합하는지 스팟체크(동명이산·오좌표 금지).

---

## 작업 4 — 운악산(雲岳山) 신규 플레이북

- `MISSING-MOUNTAINS-RESEARCH.md` 파이프라인(리서치→빌드→자산→검증→등록) 적용. 경기 포천·가평, 망경대 약 937m, 현등사·적멸보궁·암릉.
- ⚠️ **사진 자산 없음**: 운악산은 기존 이미지가 없다. `ORCHESTRATION-UPGRADE.md`의 사진 트랙(무료 스톡 API: Unsplash/Pexels)으로 hero·갤러리 실사 사진을 소싱·최적화(AVIF/WebP/JPG·srcset)하고 라이선스·출처 기록. 진위 검증(동명이산·무관 풍경 배제).
- 영상(Ken Burns)·OG 카드·교통 섹션·트래킹 영상 섹션(작업 2의 운악 항목 임베드) 포함.
- 사실 정확성 가드레일 동일: 거리·시간·난이도·교통은 ≥2 권위 소스 교차검증, 불확실은 '확인 필요'.
- 완료 시 `index.html` MOUNTAINS[]에 `done:true`+url 등록(지역 '경기').

---

## 합격 기준 (Definition of Done)

- [ ] 백학산: 카드·자산·참조 완전 삭제, 잔존 0, 통계 카운트 갱신
- [ ] 트래킹 영상 섹션: 5산(도봉·북한·명성·소요·운악)에 정확한 쇼츠 임베드, 파사드(클릭 재생)·9:16·lazy·a11y·nocookie
- [ ] 실사 루트 지도: 5산 Leaflet 위성+지형, 실제 루트 폴리라인·마커, 좌표 스팟체크 통과, JS 폴백 동작
- [ ] 운악산: 스톡 실사 사진 + 플레이북 + 영상/OG + 영상 섹션, 사실 검증, index 등록
- [ ] 전 페이지 무회귀(탭·아코디언·테마·검색/필터), 콘솔 에러·깨진 링크 0, Lighthouse a11y/SEO 유지, CLS<0.1
- [ ] 산 단위 커밋, 독립 검증 GREEN 후 PR·머지

---

## 마스터 킥오프 프롬프트 (오케스트레이터에게 복붙)

```
너는 Korea Trails 'tracking-videos-maps' 트랙의 ORCHESTRATOR다. TRACKING-VIDEOS-AND-MAPS.md를
단일 진실원천으로, 새 브랜치 feat/tracking-videos-maps에서 4개 작업을 수행한다. 하드제약:
빌드리스·다크/라이트·a11y(AA)·무회귀·정보손실0·산 단위 커밋·main 직접 푸시 금지.

순서:
1) 백학산 완전 삭제(카드·자산·참조·통계 카운트). grep으로 잔존 0 확인.
2) '내 트래킹 영상' 섹션 컴포넌트 신설 + _orchestration/videos.json(문서의 ID/라벨 그대로) 임베드.
   파사드 패턴 필수(썸네일+클릭 시에만 youtube-nocookie iframe), 9:16 그리드, lazy, aria-label, 원본 링크.
   데이터 있는 산만 렌더. 도봉(12)·북한(7)·명성(1)·소요(14)·운악(4).
3) 실사 루트 지도(영상 있는 산): SAMPLE-yangmingshan A-MAP 방식(Leaflet 위성+지형, 실제 루트 폴리라인·마커).
   각 산 체크포인트를 실제 좌표로 리서치·확정(공식·KNPS·OSM 교차), 기존 SVG는 폴백 보존, 좌표 스팟체크.
4) 운악산 신규 플레이북: MISSING-MOUNTAINS 파이프라인 + 사진은 ORCHESTRATION-UPGRADE 스톡 소싱(없으므로).
   영상/OG/교통/영상섹션 포함, 사실 ≥2소스 검증, index 등록.

진행 원칙: 먼저 파일럿으로 '도봉산'에 (영상 섹션 + 실사 루트 지도)를 적용한 완성본을 만들어 사용자
확인을 받은 뒤 북한·명성·소요로 확장하고, 운악산은 사진 소싱이 필요하니 별도로 진행한다.
각 산마다 독립 검증(영상 임베드 정확·파사드 동작·지도 좌표 스팟체크·무회귀·콘솔0)을 거치고,
단계 종료 시 결과를 1~2문장으로 보고하라. 시작 전 전체 실행계획을 요약해 승인받아라.
```

---

*Korea Trails 트래킹 영상 + 실사 루트 지도 + 백학산 삭제 + 운악산 신설 · v1.0*
