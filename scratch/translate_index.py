import os
import re
import json

# Ensure directories exist
os.makedirs('en', exist_ok=True)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update lang attribute
html = html.replace('<html lang="ko" data-theme="light">', '<html lang="en" data-theme="light">')
html = html.replace('<html data-theme="light" lang="ko">', '<html lang="en" data-theme="light">')

# 2. Update titles and meta tags
html = html.replace(
    '<title>Korea Trails — 한국 & 아시아 명산 등산 플레이북</title>',
    '<title>Korea Trails — Hiking Playbooks of Korea & Asia</title>'
)
html = html.replace(
    '<meta name="description" content="한국과 아시아 명산의 코스 정보, 지도, 교통편, 등산 팁을 제공하는 프리미엄 아웃도어 플레이북 가이드.">',
    '<meta name="description" content="Premium outdoor guide for hiking famous mountains in Korea and Asia. Complete course information, interactive maps, transit directions, and hiking tips.">'
)
html = html.replace(
    '<meta property="og:title" content="Korea Trails — 한국 & 아시아 명산 등산 플레이북">',
    '<meta property="og:title" content="Korea Trails — Hiking Playbooks of Korea & Asia">'
)
html = html.replace(
    '<meta property="og:description" content="한국과 아시아 명산의 코스 정보, 지도, 교통편, 등산 팁을 제공하는 프리미엄 아웃도어 플레이북 가이드.">',
    '<meta property="og:description" content="Premium outdoor guide for hiking famous mountains in Korea and Asia. Complete course information, interactive maps, transit directions, and hiking tips.">'
)

# 3. Add OG locale
if '<meta property="og:locale"' not in html:
    html = html.replace(
        '<meta property="og:type" content="website">',
        '<meta property="og:type" content="website">\n<meta property="og:locale" content="en_US">'
    )

# 4. Update hreflang tags
hreflang_orig = """<link rel="alternate" hreflang="ko" href="index.html">
<link rel="alternate" hreflang="en" href="en/index.html">
<link rel="alternate" hreflang="x-default" href="index.html">"""

hreflang_en = """<link rel="alternate" hreflang="ko" href="../index.html">
<link rel="alternate" hreflang="en" href="index.html">
<link rel="alternate" hreflang="x-default" href="../index.html">"""

html = html.replace(hreflang_orig, hreflang_en)

# 5. Prepend ../ to assets paths (but not to external links or relative html links in en/)
# Let's target src="assets/ and href="assets/ and poster="assets/
html = html.replace('src="assets/', 'src="../assets/')
html = html.replace('href="assets/', 'href="../assets/')
html = html.replace('poster="assets/', 'poster="../assets/')
html = html.replace('use href="assets/', 'use href="../assets/')
html = html.replace('srcset="assets/', 'srcset="../assets/')
html = html.replace('url(\'assets/', 'url(\'../assets/')
html = html.replace('url("assets/', 'url("../assets/')

# Update scripts link
html = html.replace('<script src="../assets/js/i18n.js"></script>', '<script src="../assets/js/i18n.js"></script>')

# 6. Translate layout chrome
html = html.replace('본문 바로가기', 'Skip to main content')
html = html.replace('홈</a>', 'Home</a>')
html = html.replace('명산 탐색</a>', 'Explore Mountains</a>')
html = html.replace('aria-label="메인 네비게이션"', 'aria-label="Main Navigation"')
html = html.replace('aria-label="테마 전환"', 'aria-label="Toggle Theme"')

# Lang toggle active class swap
toggle_ko_active = """    <div class="lang-toggle">
      <button class="lang-btn active" onclick="changeLanguage('ko')" aria-label="한국어" aria-pressed="true">KO</button>
      <button class="lang-btn" onclick="changeLanguage('en')" aria-label="English" aria-pressed="false">EN</button>
    </div>"""

toggle_en_active = """    <div class="lang-toggle">
      <button class="lang-btn" onclick="changeLanguage('ko')" aria-label="Korean" aria-pressed="false">KO</button>
      <button class="lang-btn active" onclick="changeLanguage('en')" aria-label="English" aria-pressed="true">EN</button>
    </div>"""

html = html.replace(toggle_ko_active, toggle_en_active)

# Hero section translation
html = html.replace(
    '<h1 class="hero-title-giant">한국과 아시아의 명산을<br>정복하세요</h1>',
    '<h1 class="hero-title-giant">Conquer the Peaks of<br>Korea & Asia</h1>'
)
html = html.replace(
    '한눈에 비교하는 거리와 고도 정보, 다크모드 대응 실사 지도, 그리고 대중교통 정보까지 탑재된 완성형 명산 가이드북.',
    'The ultimate outdoor guide with elevation profiles, dark-mode compatible maps, and detailed public transit information.'
)
html = html.replace('placeholder="산 이름, 고도, 지역 또는 설명 검색..."', 'placeholder="Search mountain name, elevation, region, or description..."')
html = html.replace('aria-label="명산 검색"', 'aria-label="Search mountains"')

# Hero stats translation
html = html.replace('등록 명산</div>', 'Registered Peaks</div>')
html = html.replace('플레이북 완성</div>', 'Playbooks Completed</div>')
html = html.replace('난이도 세분화</div>', 'Difficulty Range</div>')
html = html.replace('대중교통 & 지도</div>', 'Transit & Maps</div>')

# Filter bar translation
html = html.replace('aria-label="지역 필터"', 'aria-label="Filter by Region"')
html = html.replace('<option value="all">지역: 전체</option>', '<option value="all">Region: All</option>')
html = html.replace('<option value="korea">대한민국 전체</option>', '<option value="korea">South Korea</option>')
html = html.replace('<option value="강원">강원</option>', '<option value="Gangwon">Gangwon</option>')
html = html.replace('<option value="경기">경기/서울</option>', '<option value="Gyeonggi">Gyeonggi/Seoul</option>')
html = html.replace('<option value="충청">충청</option>', '<option value="Chungcheong">Chungcheong</option>')
html = html.replace('<option value="경상">경상</option>', '<option value="Gyeongsang">Gyeongsang</option>')
html = html.replace('<option value="전라">전라</option>', '<option value="Jeolla">Jeolla</option>')
html = html.replace('<option value="제주">제주</option>', '<option value="Jeju">Jeju</option>')
html = html.replace('<option value="대만">대만</option>', '<option value="Taiwan">Taiwan</option>')

html = html.replace('aria-label="난이도 필터"', 'aria-label="Filter by Difficulty"')
html = html.replace('<option value="all">난이도: 전체</option>', '<option value="all">Difficulty: All</option>')
html = html.replace('<option value="easy">초급</option>', '<option value="easy">Beginner</option>')
html = html.replace('<option value="medium">중급</option>', '<option value="medium">Intermediate</option>')
html = html.replace('<option value="hard">고급</option>', '<option value="hard">Advanced</option>')
html = html.replace('<option value="expert">전문가</option>', '<option value="expert">Expert</option>')

html = html.replace('aria-label="플레이북 상태 필터"', 'aria-label="Filter by Playbook Status"')
html = html.replace('<option value="all">플레이북: 전체</option>', '<option value="all">Playbook: All</option>')
html = html.replace('<option value="done">완성됨 (17)</option>', '<option value="done">Completed (26)</option>')
html = html.replace('<option value="pending">준비 중 (9)</option>', '<option value="pending">Coming Soon (0)</option>')

html = html.replace('aria-label="정렬 순서"', 'aria-label="Sort By"')
html = html.replace('<option value="elevation-desc">높은 고도 순</option>', '<option value="elevation-desc">Elevation (Highest)</option>')
html = html.replace('<option value="elevation-asc">낮은 고도 순</option>', '<option value="elevation-asc">Elevation (Lowest)</option>')
html = html.replace('<option value="name-asc">가나다 이름 순</option>', '<option value="name-asc">Name (A-Z)</option>')
html = html.replace('<option value="difficulty-asc">낮은 난이도 순</option>', '<option value="difficulty-asc">Difficulty (Lowest)</option>')
html = html.replace('<option value="difficulty-desc">높은 난이도 순</option>', '<option value="difficulty-desc">Difficulty (Highest)</option>')

# Accordion Map translation
html = html.replace('인터랙티브 전국 지도 펼치기 (한국 & 아시아)', 'Show Interactive National Map (Korea & Asia)')

# Footer translation
html = html.replace(
    'Korea Trails — 전국 등산 플레이북 · 국립공원 탐방 예약: <a href="https://reservation.knps.or.kr" target="_blank" rel="noopener">knps.or.kr</a>',
    'Korea Trails — National Hiking Playbook · National Park Reservation: <a href="https://reservation.knps.or.kr" target="_blank" rel="noopener">knps.or.kr</a>'
)
html = html.replace('© 2026 Korea Trails. All Rights Reserved.', '© 2026 Korea Trails. All rights reserved.')

# Extra landing page translations
html = html.replace('alt="설악산 대청봉의 기암괴석과 웅장한 아침 안개"', 'alt="Seoraksan Daecheongbong Peak granite rocks and majestic morning fog"')
html = html.replace('배경영상: AI 생성', 'Background Video: AI Generated')
html = html.replace('<div class="hero-stat-value">4단계</div>', '<div class="hero-stat-value">4 Levels</div>')
html = html.replace('<div class="hero-stat-label">난이도별 가이드</div>', '<div class="hero-stat-label">Difficulty Levels</div>')
html = html.replace("const DIFF_LABEL = { easy: '초급', medium: '중급', hard: '고급', expert: '전문가' };", "const DIFF_LABEL = { easy: 'Beginner', medium: 'Intermediate', hard: 'Advanced', expert: 'Expert' };")
html = html.replace('고도: <strong>${m.alt}</strong>', 'Elevation: <strong>${m.alt}</strong>')
html = html.replace('난이도: <strong>${DIFF_LABEL[m.diff]}</strong>', 'Difficulty: <strong>${DIFF_LABEL[m.diff]}</strong>')
html = html.replace('플레이북 바로가기', 'View Playbook')
html = html.replace('⏳ 준비 중', '⏳ Coming Soon')

# 7. Localized MOUNTAINS data list
mountains_en_js = """window.MOUNTAINS = [
  // ── South Korea ──
  {id:'seoraksan',     name:'Seoraksan',     alt:'1,708m', region:'Gangwon', dist:'10km', time:'7-9 hours',  diff:'hard',   done:true,  url:'seoraksan-playbook.html',     desc:'Seoraksan Daecheongbong Peak. Korea\\\'s premier rocky mountain trail including the Dinosaur Ridge. Breathtaking views in all four seasons.', lat: 38.1189, lng: 128.4650},
  {id:'hallasan',      name:'Hallasan',      alt:'1,950m', region:'Jeju', dist:'9km',  time:'8-10 hours', diff:'hard',   done:true,  url:'hallasan-playbook.html',      desc:'The highest peak in South Korea. View the Baekrokdam crater lake via the Seongpanak or Gwaneumsa trails. Draws over a million hikers annually.', lat: 33.3617, lng: 126.5292},
  {id:'jirisan',       name:'Jirisan',       alt:'1,915m', region:'Jeolla', dist:'24km', time:'2 Days (1 Night)', diff:'expert', done:true,  url:'jirisan-playbook.html',       desc:'The largest mountainous national park in South Korea. A 25km ridge trek from Nogodan to Cheonwangbong Peak. Features 4 national park visitor trails.', lat: 35.3369, lng: 127.7306},
  {id:'bukhansan',     name:'Bukhansan',     alt:'836m',   region:'Gyeonggi', dist:'8km',  time:'4-5 hours',  diff:'medium', done:true,  url:'bukhansan-playbook.html',     desc:'National park north of Seoul. Majestic granite peaks of Baegundae and Insubong. Highly accessible from downtown Seoul.', lat: 37.6586, lng: 126.9778},
  {id:'sobaeksan',     name:'Sobaeksan',     alt:'1,440m', region:'Chungcheong', dist:'12km', time:'6-7 hours',  diff:'medium', done:true,  url:'sobaeksan-playbook.html',     desc:'The scenic ridge connecting Yeonhwabong and Birobong. Renowned for its royal azalea fields in spring. Trail passes via Jungnyeong Pass.', lat: 36.9427, lng: 128.4722},
  {id:'gayasan',       name:'Gayasan',       alt:'1,433m', region:'Gyeongsang', dist:'10km', time:'5-6 hours',  diff:'medium', done:true,  url:'gayasan-playbook.html',       desc:'A sacred mountain housing the historic Haeinsa Temple. Experience the spiritual energy of the Tripitaka Koreana at Sangwangbong Peak.', lat: 35.8236, lng: 128.1219},
  {id:'odaesan',       name:'Odaesan',       alt:'1,563m', region:'Gangwon', dist:'11km', time:'5-6 hours',  diff:'medium', done:true,  url:'odaesan-playbook.html',       desc:'Integrate your hike with historic temple visits to Woljeongsa and Sangwonsa. The high plateau ridge of Birobong Peak is highly impressive.', lat: 37.7989, lng: 128.5639},
  {id:'naejangsan',    name:'Naejangsan',    alt:'763m',   region:'Jeolla', dist:'8km',  time:'4-5 hours',  diff:'easy',   done:true,  url:'naejangsan-playbook.html',    desc:'South Korea\\\'s top autumn foliage destination. The Naejangsa maple tunnel is nationwide famous. Cable car service is available.', lat: 35.4336, lng: 126.8856},
  {id:'chiaksan',      name:'Chiaksan',      alt:'1,288m', region:'Gangwon', dist:'11.5km',time:'6 hours',    diff:'hard',   done:true,  url:'chiaksan-playbook.html',      desc:'Wonju\\\'s Chiaksan. The steep ascent to Birobong Peak is one of the most challenging trails in Gangwon Province.', lat: 37.3686, lng: 128.0531},
  {id:'deogyusan',     name:'Deogyusan',     alt:'1,614m', region:'Jeolla', dist:'12km', time:'6-7 hours',  diff:'medium', done:true,  url:'deogyusan-playbook.html',     desc:'Hyangjeokbong Peak. Famous for its beautiful winter snowscapes and ski slopes. Connected with Muju Deogyusan Resort.', lat: 35.8617, lng: 127.7472},
  {id:'gyeryongsan',   name:'Gyeryongsan',   alt:'845m',   region:'Chungcheong', dist:'7km',  time:'4 hours',    diff:'easy',   done:true,  url:'gyeryongsan-playbook.html',   desc:'A famous mountain in the Chungcheong region. Rocky ridges of Sambulbong and Gwaneumbong Peaks, with Gapsa and Donghaksa temples.', lat: 36.3533, lng: 127.2081},
  {id:'wolchulsan',    name:'Wolchulsan',    alt:'809m',   region:'Jeolla', dist:'7km',  time:'4-5 hours',  diff:'hard',   done:true,  url:'wolchulsan-playbook.html',    desc:'Known as the Geumgangsan of the south. Dramatic granite rock formations around Cheonhwangbong Peak, featuring a thrilling suspension bridge.', lat: 34.7892, lng: 126.6975},
  {id:'mudeungsan',    name:'Mudeungsan',    alt:'1,187m', region:'Jeolla', dist:'12.4km', time:'6 hours',  diff:'medium', done:true,  url:'mudeungsan-playbook.html',    desc:'The guardian mountain of Gwangju. Stunning columnar joint formations of Seoseokdae and Ipseokdae. Designated a national park in 2013.', lat: 35.1336, lng: 127.0089},
  {id:'duryunsan',     name:'Duryunsan',     alt:'703m',   region:'Jeolla', dist:'5.9km', time:'4 hours 30 mins',diff:'medium', done:true,  url:'duryunsan-playbook.html',     desc:'A scenic mountain set behind Haenam\\\'s Daeheungsa Temple. Ocean views of the South Sea from Garyeonbong Peak. Cable car available.', lat: 34.4817, lng: 126.6231},
  {id:'minjusan',      name:'Minjujisan',    alt:'1,242m', region:'Chungcheong', dist:'8km',   time:'3 hours 30 mins',diff:'medium', done:true,  url:'minjusan-playbook.html',      desc:'Minjujisan in Yeongdong, Chungbuk. Samdobong Peak marks the three-way border of Chungcheong, Jeolla, and Gyeongsang provinces.', lat: 36.0356, lng: 127.8719},
  {id:'sikjangsan',    name:'Sikjangsan',    alt:'598m',   region:'Chungcheong', dist:'6km',  time:'3 hours',    diff:'easy',   done:true,  url:'sikjangsan-playbook.html',    desc:'Sikjangsan on the east of Daejeon. Perfect for a day hike near the city, offering panoramic night views of downtown Daejeon.', lat: 36.3117, lng: 127.4819},
  {id:'woraksan',      name:'Woraksan',      alt:'1,097m', region:'Chungcheong', dist:'9km',  time:'5-6 hours',  diff:'hard',   done:true,  url:'woraksan-playbook.html',      desc:'Overlooking the beautiful scenic vistas of Chungjuho Lake. The rocky ridge trail up Yeongbong Peak offers an exhilarating challenge.', lat: 36.8833, lng: 128.0931},
  {id:'dobongsan',     name:'Dobongsan',     alt:'740m',   region:'Gyeonggi', dist:'7km',  time:'3-4 hours',  diff:'medium', done:true,  url:'dobongsan-playbook.html',     desc:'A popular rocky peak behind Seoul\\\'s Dobong-gu. Majestic granite formations of Jaunbong and Manjangbong Peaks in Bukhansan National Park.', lat: 37.6992, lng: 127.0156},
  {id:'soyosan',       name:'Soyosan',       alt:'587m',   region:'Gyeonggi', dist:'6km',  time:'3 hours',    diff:'easy',   done:true,  url:'soyosan-playbook.html',       desc:'Soyosan in Dongducheon, Gyeonggi. Renowned for Jajaeam Hermitage valley and autumn colors. A favorite day hike in the Seoul metro area.', lat: 37.9436, lng: 127.0789},
  {id:'juwangsan',     name:'Juwangsan',     alt:'721m',   region:'Gyeongsang', dist:'8km',  time:'4-5 hours',  diff:'easy',   done:true,  url:'juwangsan-playbook.html',     desc:'Juwangsan in Cheongsong. Explore deep valleys of Jubangcheon and waterfalls. The historic Juwanggul Cave offers a mystical atmosphere.', lat: 36.4022, lng: 129.0628},
  {id:'myeongseongsan',name:'Myeongseongsan',alt:'922m',   region:'Gyeonggi', dist:'8km',  time:'4-5 hours',  diff:'medium', done:true,  url:'myeongseongsan-playbook.html',desc:'Bordering Pocheon and Cheorwon. Famous for its sprawling silver grass fields in autumn, overlooking scenic Sanjeong Lake.', lat: 38.1067, lng: 127.3117},
  {id:'unaksan',       name:'Unaksan',       alt:'937.5m', region:'Gyeonggi', dist:'4km',  time:'2 hours 30 mins',diff:'hard',   done:true,  url:'unaksan-playbook.html',       desc:'One of Gyeonggi\\\'s five sacred peaks, bordering Gapyeong and Pocheon. Spectacular crags, historic Hyeongdeungsa Temple, and autumn foliage.', lat: 37.9163, lng: 127.3188},
  {id:'taebaeksan',    name:'Taebaeksan',    alt:'1,567m', region:'Gangwon', dist:'10km', time:'5-6 hours',  diff:'medium', done:true,  url:'taebaeksan-playbook.html',    desc:'Cheonjedan altar on the high plateau. Famous for winter snowscapes and ancient yew trees. A key section of the Baekdudaegan ridge.', lat: 37.0983, lng: 128.9136},
  // ── Taiwan ──
  {id:'yushan',        name:'Yushan (Jade Mountain)', alt:'3,952m', region:'Taiwan', dist:'11km', time:'2 Days (1 Night)', diff:'expert', done:true,  url:'yushan-playbook.html',        desc:'The highest peak in Taiwan and Northeast Asia. Summit sunrise attempt after staying at Paiyun Lodge. Permit required.', lat: 23.4700, lng: 120.9575},
  {id:'xueshan',       name:'Xueshan (Snow Mountain)', alt:'3,886m', region:'Taiwan', dist:'11km', time:'2 Days (1 Night)', diff:'expert', done:true,  url:'xueshan-playbook.html',       desc:'Taiwan\\\'s second-highest peak. Scenic glacial cirques, ancient black forest, and alpine vegetation. Accessible from Taichung/Lishan.', lat: 24.3850, lng: 121.2319},
  {id:'yangmingshan',  name:'Yangmingshan',  alt:'1,120m',region:'Taiwan',dist:'8km', time:'4-5 hours',  diff:'easy',   done:true,  url:'yangmingshan-playbook.html',  desc:'Volcanic national park near Taipei. Panoramas of the active fumaroles at Qixing Mountain. Famous for spring azaleas and sulfur hot springs.', lat: 25.1672, lng: 121.5742},
];"""

# Replace the MOUNTAINS array in JS
# We find window.MOUNTAINS = [ ... ];
pattern = re.compile(r'window\.MOUNTAINS\s*=\s*\[[\s\S]*?\];')
html = pattern.sub(mountains_en_js, html)

with open('en/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated en/index.html successfully!")
