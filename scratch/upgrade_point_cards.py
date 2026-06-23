import glob
import os
import re
import copy
from bs4 import BeautifulSoup

point_data = {
    # Unaksan
    "천년고찰 현등사 경내": {"elev": "—", "icon": "icon-location", "desc": "신라 시대 창건된 고찰로 조용한 사찰 분위기"},
    "백일홍 가로수 숲길": {"elev": "—", "icon": "icon-season", "desc": "여름철 붉은 백일홍이 아름답게 피어나는 숲길"},
    "동봉 데크 조망": {"elev": "—", "icon": "icon-mountain", "desc": "포천과 가평 일대 산세가 넓게 펼쳐지는 조망"},
    # Unaksan EN
    "Hyundeungsa Temple grounds, an ancient temple": {"elev": "—", "icon": "icon-location", "desc": "An ancient Silla temple with a quiet and peaceful atmosphere"},
    "Crape Myrtle Tree-lined Forest Path": {"elev": "—", "icon": "icon-season", "desc": "A beautiful forest path lined with blooming crape myrtles in summer"},
    "Dongbong Peak deck view": {"elev": "—", "icon": "icon-mountain", "desc": "Expansive views of the mountain ranges around Pocheon and Gapyeong"},

    # Naejangsan
    "단풍터널": {"elev": "—", "icon": "icon-season", "desc": "가을철 터널처럼 머리 위를 덮는 화려한 아기단풍"},
    "내장사 앞 연못": {"elev": "—", "icon": "icon-location", "desc": "정혜루 아래 연못과 단풍이 어우러지는 반영 명소"},
    "벽련암 숲길": {"elev": "—", "icon": "icon-season", "desc": "서래봉 절벽 아래 고즈넉한 암자로 이어지는 숲길"},
    # Naejangsan EN
    "Maple Tunnel": {"elev": "—", "icon": "icon-season", "desc": "Spectacular baby maple leaves forming a colorful tunnel in autumn"},
    "Pond in front of Naejangsa Temple": {"elev": "—", "icon": "icon-location", "desc": "Scenic reflection pond showcasing autumn foliage below Jeonghye-ru"},
    "Byeongnyeonam Forest Path": {"elev": "—", "icon": "icon-season", "desc": "A quiet forest path leading to a peaceful hermitage below Seoraebong Peak"},

    # Myeongseongsan
    "등룡폭포": {"elev": "—", "icon": "icon-location", "desc": "용이 하늘로 승천했다는 전설이 깃든 웅장한 2단 폭포"},
    "억새밭 중앙 탐방로": {"elev": "—", "icon": "icon-season", "desc": "가을철 은빛 억새가 파도치는 벌판 사이를 걷는 핵심 코스"},
    "산정호수 배경 하산길": {"elev": "—", "icon": "icon-location", "desc": "호수를 내려다보며 가볍게 발걸음을 옮길 수 있는 하산길"},
    # Myeongseongsan EN
    "Deungnyongpokpo Waterfall": {"elev": "—", "icon": "icon-location", "desc": "A majestic double waterfall named after a dragon ascending to heaven"},
    "Miscanthus Field Central Trail": {"elev": "—", "icon": "icon-season", "desc": "Walk through silver miscanthus fields waving like waves in autumn"},
    "Descent route with Sanjeonghosu Lake in the background": {"elev": "—", "icon": "icon-location", "desc": "A scenic path descending with views of the beautiful Sanjeonghosu Lake"},

    # Gyeryongsan
    "은선폭포": {"elev": "—", "icon": "icon-location", "desc": "신선들이 숨어서 놀았다는 전설이 깃든 아름다운 폭포"},
    "관음봉 조망": {"elev": "816m", "icon": "icon-mountain", "desc": "계룡산의 중심 봉우리에서 바라보는 웅장한 능선 조망"},
    "계단 위 암릉감": {"elev": "—", "icon": "icon-warning", "desc": "가파른 계단을 올라 펼쳐지는 스릴 넘치는 암릉 구간"},
    # Gyeryongsan EN
    "Eunseonpokpo Falls": {"elev": "—", "icon": "icon-location", "desc": "A scenic waterfall where taoist hermits were said to hide and play"},
    "Gwanneumbong View": {"elev": "816m", "icon": "icon-mountain", "desc": "Stunning vistas of Gyeryongsan's ridges from the central peak"},
    "Rocky ridge feel above stairs": {"elev": "—", "icon": "icon-warning", "desc": "A thrilling and narrow rocky section after the steep stairs climb"},

    # Woraksan
    "영봉 정상 조망": {"elev": "1097m", "icon": "icon-mountain", "desc": "거대한 암벽으로 이뤄진 월악산 최고봉의 거침없는 전망"},
    "암릉 전망": {"elev": "—", "icon": "icon-mountain", "desc": "충주호와 주변 산군이 파노라마처럼 펼쳐지는 전망"},
    "일출 산행 가능": {"elev": "—", "icon": "icon-clock", "desc": "시야가 트여 있어 이른 아침 동해 방향의 일출 감상 최적"},
    # Woraksan EN
    "Yeongbong Summit View": {"elev": "1097m", "icon": "icon-mountain", "desc": "Stunning panoramic views from the rocky peak of Yeongbong"},
    "Rocky Ridge View": {"elev": "—", "icon": "icon-mountain", "desc": "Breathtaking panorama of Chungjuho Lake and neighboring peaks"},
    "Sunrise Hiking Allowed": {"elev": "—", "icon": "icon-clock", "desc": "Excellent clear views to witness the beautiful sunrise in the morning"},
    "View from Yeongbong Peak Summit": {"elev": "1097m", "icon": "icon-mountain", "desc": "Stunning panoramic views from the rocky peak of Yeongbong"},
    "Rocky ridge view": {"elev": "—", "icon": "icon-mountain", "desc": "Breathtaking panorama of Chungjuho Lake and neighboring peaks"},
    "Sunrise hike possible": {"elev": "—", "icon": "icon-clock", "desc": "Excellent clear views to witness the beautiful sunrise in the morning"},

    # Xueshan
    "전망덱": {"elev": "—", "icon": "icon-location", "desc": "주변 고산지대의 웅장한 실루엣을 한눈에 담는 전망대"},
    "눈물고개 접근부": {"elev": "—", "icon": "icon-warning", "desc": "가파른 비탈길을 오르며 체력 조망이 교차하는 도전 구간"},
    "369산장 풍경": {"elev": "3150m", "icon": "icon-location", "desc": "해발 3,150m 고지대에 위치한 등산객들의 아늑한 쉼터"},
    # Xueshan EN
    "Observation Deck": {"elev": "—", "icon": "icon-location", "desc": "Panoramic deck capturing the grand silhouettes of high peaks"},
    "Nunmulgogae access point": {"elev": "—", "icon": "icon-warning", "desc": "A challenging uphill path testing your physical limits on steep terrain"},
    "369 Hut Scenery": {"elev": "3150m", "icon": "icon-location", "desc": "A cozy high-altitude shelter located 3,150 meters above sea level"},

    # Yangmingshan
    "소유갱 유황 분기공": {"elev": "—", "icon": "icon-warning", "desc": "흰 연기와 유황 냄새가 뿜어져 나오는 화산 지형"},
    "정상 조망": {"elev": "1120m", "icon": "icon-mountain", "desc": "타이베이 분지와 주변 산세를 360도 조망할 수 있는 곳"},
    "짧고 굵은 타이베이 근교 산행": {"elev": "—", "icon": "icon-season", "desc": "대중교통 접근성이 뛰어나며 단시간에 고산 분위기를 느끼는 코스"},
    "정상 2개 연계": {"elev": "—", "icon": "icon-mountain", "desc": "칠성산 주봉과 동봉을 연속으로 정복하는 종주 루트"},
    "냉수갱 온천 분위기": {"elev": "—", "icon": "icon-location", "desc": "무료 족욕탕이 있어 산행 후 발의 피로를 풀기 좋은 온천 구역"},
    "대중교통 연계 편리": {"elev": "—", "icon": "icon-bus", "desc": "타이베이 시내에서 버스로 쉽고 편리하게 들머리 이동 가능"},
    "화산 지형 + 정상": {"elev": "—", "icon": "icon-warning", "desc": "살아있는 화산의 분기공과 칠성산 정상을 잇는 핵심 테마"},
    "몽환호 습지": {"elev": "—", "icon": "icon-location", "desc": "대만 특유의 희귀 수생 식물이 자생하는 안개 낀 습지 호수"},
    "칭티엔강 초원": {"elev": "—", "icon": "icon-season", "desc": "푸른 잔디 언덕 위로 야생 물소들이 한가로이 풀을 뜯는 평원"},
    # Yangmingshan EN
    "Xiaoyoukeng Sulfur Fumarole": {"elev": "—", "icon": "icon-warning", "desc": "An active volcanic terrain with rising steam and sulfur vents"},
    "Summit View": {"elev": "1120m", "icon": "icon-mountain", "desc": "A 360-degree viewpoint overlooking Taipei Basin and green hills"},
    "A Short and Intense Hike in the Taipei Suburbs": {"elev": "—", "icon": "icon-season", "desc": "Excellent public transit access to high mountain feelings in short hours"},
    "2 Peaks Linked": {"elev": "—", "icon": "icon-mountain", "desc": "A traverse route conquering both Qixingshan Main and East Peaks"},
    "Lengshuikeng Hot Spring Atmosphere": {"elev": "—", "icon": "icon-location", "desc": "Hot spring area with free foot baths to relax tired feet after hiking"},
    "Convenient Public Transportation Connections": {"elev": "—", "icon": "icon-bus", "desc": "Easy and cheap bus access directly from downtown Taipei"},
    "Volcanic Landscape + Summit": {"elev": "—", "icon": "icon-warning", "desc": "A core theme connecting active sulfur vents and Qixingshan summit"},
    "Volcanic Terrain + Summit": {"elev": "—", "icon": "icon-warning", "desc": "A core theme connecting active sulfur vents and Qixingshan summit"},
    "Menghuan Lake Wetland": {"elev": "—", "icon": "icon-location", "desc": "Misty wetland lake home to Taiwan's rare quillwort plants"},
    "Menghuan Pond Wetland": {"elev": "—", "icon": "icon-location", "desc": "Misty wetland lake home to Taiwan's rare quillwort plants"},
    "Qingtiangang Grassland": {"elev": "—", "icon": "icon-season", "desc": "Green grassy plateau where wild water buffaloes graze peacefully"},

    # Yushan
    "아주 이른 출발": {"elev": "—", "icon": "icon-clock", "desc": "일출 조망과 안전을 위해 꼭두새벽에 산행을 시작하는 기본 원칙"},
    "기상창 확인": {"elev": "—", "icon": "icon-season", "desc": "고산지대의 급격한 기후 변화를 실시간으로 모니터링하여 대비"},
    "중도 철수 기준 설정": {"elev": "—", "icon": "icon-warning", "desc": "안전을 위해 악천후나 고산병 발생 시 미련 없이 회항할 기준 마련"},
    # Yushan EN
    "Very early start": {"elev": "—", "icon": "icon-clock", "desc": "Start in pre-dawn hours for sunrise viewing and safety margin"},
    "Check weather window": {"elev": "—", "icon": "icon-season", "desc": "Monitor rapid weather changes in the high alpine environment"},
    "Set criteria for mid-course withdrawal": {"elev": "—", "icon": "icon-warning", "desc": "Pre-define when to turn back for safety in case of AMS or storm"},

    # Deogyusan
    "구천동 33경 계곡 경관": {"elev": "—", "icon": "icon-location", "desc": "아름다운 폭포와 소가 줄지어 흐르는 덕유산의 대표 계곡"},
    "중봉·백암봉 능선 조망": {"elev": "—", "icon": "icon-mountain", "desc": "부드러운 능선길을 걸으며 사방으로 거침없이 탁 트인 산세 감상"},
    "무룡산 넓은 고원 능선": {"elev": "1492m", "icon": "icon-season", "desc": "해발 1,400m가 넘는 드넓은 평원 능선에서 만나는 철쭉과 조망"},
    "남덕유산~서봉 절경": {"elev": "1507m", "icon": "icon-mountain", "desc": "덕유산 남부의 거칠고 수려한 암봉들이 펼치는 장엄한 조망"},
    # Deogyusan Seasonal Attractions
    "봄: 철쭉 5월 중순 절정": {"elev": "—", "icon": "icon-season", "desc": "덕유산 능선을 붉게 물들이는 아름다운 철쭉 군락"},
    "여름: 서늘한 능선 피서": {"elev": "—", "icon": "icon-season", "desc": "해발 1,500m대 시원한 바람을 맞으며 걷는 여름 능선 산행"},
    "가을: 단풍 10월 중~하순": {"elev": "—", "icon": "icon-season", "desc": "구천동 계곡과 산자락을 오색빛깔로 물들이는 가을 단풍"},
    "겨울: 눈꽃·상고대 최고": {"elev": "—", "icon": "icon-season", "desc": "주목 군락과 설천봉 일대에 피어나는 환상적인 상고대와 눈꽃"},
    # Deogyusan EN
    "Gucheondong Valley's 33 scenic spots": {"elev": "—", "icon": "icon-location", "desc": "Deogyusan's representative valley with beautiful waterfalls and pools"},
    "Jungbong and Baegambong ridge view": {"elev": "—", "icon": "icon-mountain", "desc": "Expansive panoramic mountain views from the gentle ridge walk"},
    "Muryongsan Peak's wide plateau ridge": {"elev": "1492m", "icon": "icon-season", "desc": "Foliage and open vistas from the plateau ridge over 1,400m high"},
    "Namdeogyusan Peak to Seobong Peak scenery": {"elev": "1507m", "icon": "icon-mountain", "desc": "Majestic views showcasing the rugged peaks of Southern Deogyusan"},
    "Gucheondong 33 Scenic Spots Valley Landscape": {"elev": "—", "icon": "icon-location", "desc": "Deogyusan's representative valley with beautiful waterfalls and pools"},
    "View of Jungbong Peak and Baegambong Peak Ridge": {"elev": "—", "icon": "icon-mountain", "desc": "Expansive panoramic mountain views from the gentle ridge walk"},
    "Muryongsan wide plateau ridge": {"elev": "1492m", "icon": "icon-season", "desc": "Foliage and open vistas from the plateau ridge over 1,400m high"},
    "Namdeogyusan Mountain ~ Seobong Peak Scenic View": {"elev": "1507m", "icon": "icon-mountain", "desc": "Majestic views showcasing the rugged peaks of Southern Deogyusan"},
    # Deogyusan EN Seasonal Attractions
    "Spring: Azaleas peak in mid-May": {"elev": "—", "icon": "icon-season", "desc": "Beautiful azalea colonies coloring Deogyusan's ridges in deep pink"},
    "Summer: Cool ridge for escaping the heat": {"elev": "—", "icon": "icon-season", "desc": "Summer ridge hiking while enjoying cool breezes at 1,500m elevation"},
    "Autumn: Fall foliage mid to late October": {"elev": "—", "icon": "icon-season", "desc": "Beautiful autumn foliage painting Gucheondong Valley and mountain slopes"},
    "Winter: Best for snow flowers and hoarfrost": {"elev": "—", "icon": "icon-season", "desc": "Fantastic rime ice and snow flowers blooming around Seolcheonbong Peak"},

    # Taebaeksan
    "주목 군락: 천제단 일대": {"elev": "—", "icon": "icon-season", "desc": "살아 천년 죽어 천년을 버티는 장엄한 고사 주목 군락"},
    "야생화 군락: 만항재 7~8월": {"elev": "—", "icon": "icon-season", "desc": "여름철 고산 지대에 가득 피어나는 화려한 천상의 야생화 정원"},
    "정암사 수마노탑(국보 332호)": {"elev": "—", "icon": "icon-location", "desc": "삼국유사에 등장하는 자장율사가 세운 유서 깊은 모전석탑"},
    "함백산 정상 풍력발전 단지 조망": {"elev": "1573m", "icon": "icon-mountain", "desc": "함백산 정상에서 펼쳐지는 거대한 바람개비와 광활한 조망"},
    # Taebaeksan EN
    "Yew tree community: Cheonjedan area": {"elev": "—", "icon": "icon-season", "desc": "A majestic colony of ancient yew trees surviving for a thousand years"},
    "Wildflower Colony: Manhangjae Pass, July-August": {"elev": "—", "icon": "icon-season", "desc": "A colorful heavenly garden of alpine wildflowers blooming in summer"},
    "Sumano Pagoda at Jeongamsa Temple (National Treasure No. 332)": {"elev": "—", "icon": "icon-location", "desc": "A historic stone pagoda built by Monk Jajang in the Silla Dynasty"},
    "View of the wind farm complex from the summit of Hambaeksan Mountain": {"elev": "1573m", "icon": "icon-mountain", "desc": "Giant wind turbines and expansive views from the summit of Hambaeksan"},

    # Odaesan
    "봄: 전나무 숲길 신록": {"elev": "—", "icon": "icon-season", "desc": "월정사 전나무 숲길에서 시작되는 연초록빛 상쾌한 아침 산책"},
    "여름: 오대천 계곡 시원함": {"elev": "—", "icon": "icon-season", "desc": "깊고 푸른 계곡을 따라 더위를 시원하게 씻어내는 물소리"},
    "가을: 10월 단풍 절경": {"elev": "—", "icon": "icon-season", "desc": "오대산의 오색 고운 오대단풍이 산 전체를 물들이는 풍경"},
    "겨울: 설경과 전나무 숲": {"elev": "—", "icon": "icon-season", "desc": "눈 덮인 고즈넉한 월정사 전나무 숲길과 설원 비로봉"},
    # Odaesan Seasonal Attractions KR
    "봄: 신록 전나무 상큼한 향기": {"elev": "—", "icon": "icon-season", "desc": "월정사 전나무 숲길에서 시작되는 연초록빛 상쾌한 아침 산책"},
    "여름: 오대천 계곡 시원함": {"elev": "—", "icon": "icon-season", "desc": "깊고 푸른 계곡을 따라 더위를 시원하게 씻어내는 물소리"},
    "가을: 단풍 10월 절정 (국내 손꼽힘)": {"elev": "—", "icon": "icon-season", "desc": "오대산의 오색 고운 오대단풍이 산 전체를 물들이는 풍경"},
    "겨울: 설원 전나무숲 장관": {"elev": "—", "icon": "icon-season", "desc": "눈 덮인 고즈넉한 월정사 전나무 숲길과 설원 비로봉"},
    # Odaesan EN
    "Spring: Fresh green of Fir Forest Path": {"elev": "—", "icon": "icon-season", "desc": "A refreshing morning stroll in the light green forest of Woljeongsa"},
    "Summer: Coolness of Odaecheon Stream Valley": {"elev": "—", "icon": "icon-season", "desc": "The sound of rushing waters washing away summer heat along the valley"},
    "Autumn: Spectacular foliage in October": {"elev": "—", "icon": "icon-season", "desc": "Beautiful autumn colors painting the entire mountain range in October"},
    "Winter: Snowscape and Fir Forest": {"elev": "—", "icon": "icon-season", "desc": "Serene snow-covered fir forest paths and snow-capped Birobong Peak"},
    # Odaesan EN Seasonal Attractions
    "Spring: Fresh scent of new growth fir trees": {"elev": "—", "icon": "icon-season", "desc": "A refreshing morning stroll in the light green forest of Woljeongsa"},
    "Summer: Odaecheon Valley is cool": {"elev": "—", "icon": "icon-season", "desc": "The sound of rushing waters washing away summer heat along the valley"},
    "Autumn: Foliage peaks in October (one of Korea's best)": {"elev": "—", "icon": "icon-season", "desc": "Beautiful autumn colors painting the entire mountain range in October"},
    "Winter: Spectacular snowfield and fir forest": {"elev": "—", "icon": "icon-season", "desc": "Serene snow-covered fir forest paths and snow-capped Birobong Peak"}
}

def clean_double_nested_containers(soup):
    """
    Finds and resolves L2 .peak-grid wrapped in .tipcard or .tc-card
    """
    modified = False
    
    # Target all div classes containing tipcard or tc-card
    for parent in soup.find_all("div", class_=lambda c: c and any(cls in c.split() for cls in ["tipcard", "tc-card"])):
        grid = parent.find(class_="peak-grid")
        if grid:
            heading = parent.find(["h2", "h3"])
            grid_extracted = grid.extract()
            if heading:
                heading_extracted = heading.extract()
                parent.insert_before(heading_extracted)
            parent.insert_before(grid_extracted)
            parent.decompose()
            modified = True
            
    return modified

def standardize_soyosan(file_path):
    print(f"Standardizing Soyosan: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    is_en = file_path.startswith("en/")
    icon_prefix = "../" if is_en else ""
    
    grids = soup.find_all(class_=re.compile(r"peak-grid|peaks-grid"))
    for grid in grids:
        grid["class"] = ["peak-grid"]
        cards = grid.find_all(class_="peak-card")
        for card in cards:
            card["class"] = ["peak-card"]
            alt_div = card.find(class_="peak-alt")
            if alt_div:
                alt_div["class"] = ["peak-elev"]
                
            elev_div = card.find(class_="peak-elev")
            name_div = card.find(class_="peak-name")
            icon_id = "icon-mountain"
            
            if name_div:
                svg = name_div.find("svg")
                if svg:
                    use = svg.find("use")
                    if use and "href" in use.attrs:
                        href = use.attrs["href"]
                        match = re.search(r"#(icon-\w+)", href)
                        if match:
                            icon_id = match.group(1)
                    svg.decompose()
                name_text = name_div.get_text().strip()
                name_div.string = name_text
                
            feat_div = card.find(class_="peak-features")
            if feat_div:
                feat_div.decompose()
                
            desc_div = card.find(class_="peak-desc")
            card.clear()
            
            # 1. peak-icon
            icon_wrapper = soup.new_tag("div", attrs={"class": "peak-icon"})
            new_svg = soup.new_tag("svg", attrs={"class": "icon-svg"})
            new_use = soup.new_tag("use", attrs={"href": f"{icon_prefix}assets/icons/icons.svg#{icon_id}"})
            new_svg.append(new_use)
            icon_wrapper.append(new_svg)
            card.append(icon_wrapper)
            
            # 2. peak-elev
            if elev_div:
                card.append(elev_div)
            else:
                new_elev = soup.new_tag("div", attrs={"class": "peak-elev"})
                new_elev.string = "—"
                card.append(new_elev)
                
            # 3. peak-name
            if name_div:
                card.append(name_div)
                
            # 4. peak-desc
            if desc_div:
                card.append(desc_div)
                
    clean_double_nested_containers(soup)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

def standardize_sikjangsan(file_path):
    print(f"Standardizing Sikjangsan: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    is_en = file_path.startswith("en/")
    icon_prefix = "../" if is_en else ""
    
    grids = soup.find_all(class_="peak-grid")
    for grid in grids:
        cards = grid.find_all(class_=re.compile(r"peak-card"))
        for card in cards:
            m_span = card.find("span", class_="m")
            h2 = card.find("h2")
            p = card.find("p")
            
            elev_val = m_span.get_text().strip() if m_span else "—"
            name_val = h2.get_text().strip() if h2 else ""
            desc_val = p.get_text().strip() if p else ""
            
            card.clear()
            card["class"] = ["peak-card"]
            
            # 1. peak-icon
            icon_wrapper = soup.new_tag("div", attrs={"class": "peak-icon"})
            new_svg = soup.new_tag("svg", attrs={"class": "icon-svg"})
            new_use = soup.new_tag("use", attrs={"href": f"{icon_prefix}assets/icons/icons.svg#icon-mountain"})
            new_svg.append(new_use)
            icon_wrapper.append(new_svg)
            card.append(icon_wrapper)
            
            # 2. peak-elev
            new_elev = soup.new_tag("div", attrs={"class": "peak-elev"})
            new_elev.string = elev_val
            card.append(new_elev)
            
            # 3. peak-name
            new_name = soup.new_tag("div", attrs={"class": "peak-name"})
            new_name.string = name_val
            card.append(new_name)
            
            # 4. peak-desc
            new_desc = soup.new_tag("div", attrs={"class": "peak-desc"})
            new_desc.string = desc_val
            card.append(new_desc)
            
    clean_double_nested_containers(soup)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

def upgrade_playbook_lists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    is_en = file_path.startswith("en/")
    icon_prefix = "../" if is_en else ""
    
    keywords = [
        "추천 포인트", "포인트", "매력 포인트", "운영 포인트", "볼거리 정보", "계절별 볼거리", "계절별 매력", "볼거리",
        "Recommended Points", "Key Attractions", "Points", "Attraction Points", "Operational Points",
        "Attractions Information", "Season Attractions", "Photo Point", "Photo Spot", "Seasonal Attractions",
        "Attraction Information", "Attractions"
    ]
    
    modified = False
    
    # Find all headings
    for h in soup.find_all(["h2", "h3"]):
        heading_text = "".join(t for t in h.find_all(text=True) if t.parent.name not in ["svg", "use"]).strip()
        
        # Check if heading text matches keywords
        if any(kw.lower() == heading_text.lower() or heading_text.endswith(kw) or heading_text.startswith(kw) for kw in keywords):
            parent = h.parent
            parent_card = None
            if parent and parent.name == "div" and any(cls in parent.get("class", []) for cls in ["card", "tipcard", "tc-card"]):
                parent_card = parent
                ul = parent.find("ul") or parent.find("ol")
            else:
                sibling = h.find_next_sibling()
                if sibling and sibling.name in ["ul", "ol"]:
                    ul = sibling
                else:
                    ul = None
            
            if ul:
                new_grid = soup.new_tag("div", attrs={"class": "peak-grid"})
                li_items = ul.find_all("li")
                for li in li_items:
                    li_text = li.get_text().strip()
                    
                    data = point_data.get(li_text)
                    if not data:
                        if ":" in li_text:
                            parts = li_text.split(":", 1)
                            name = parts[0].strip()
                            desc = parts[1].strip()
                        elif "：" in li_text:
                            parts = li_text.split("：", 1)
                            name = parts[0].strip()
                            desc = parts[1].strip()
                        else:
                            name = li_text
                            desc = f"{name}의 세부 볼거리 정보" if not is_en else f"Detailed scenery of {name}"
                            
                        data = point_data.get(name)
                        if not data:
                            elev = "—"
                            icon = "icon-location"
                            lower_name = name.lower()
                            if any(k in lower_name for k in ["봉", "정상", "peak", "summit", "산"]):
                                icon = "icon-mountain"
                            elif any(k in lower_name for k in ["계곡", "폭포", "waterfall", "falls", "lake", "호", "연못"]):
                                icon = "icon-location"
                            elif any(k in lower_name for k in ["봄", "여름", "가을", "겨울", "spring", "summer", "autumn", "winter", "season", "단풍", "숲"]):
                                icon = "icon-season"
                            elif any(k in lower_name for k in ["주의", "대비", "위험", "warning", "caution"]):
                                icon = "icon-warning"
                        else:
                            elev = data["elev"]
                            icon = data["icon"]
                            desc = data["desc"]
                    else:
                        name = li_text
                        elev = data["elev"]
                        icon = data["icon"]
                        desc = data["desc"]
                        
                    new_card = soup.new_tag("div", attrs={"class": "peak-card"})
                    
                    # 1. Icon
                    icon_wrapper = soup.new_tag("div", attrs={"class": "peak-icon"})
                    new_svg = soup.new_tag("svg", attrs={"class": "icon-svg"})
                    new_use = soup.new_tag("use", attrs={"href": f"{icon_prefix}assets/icons/icons.svg#{icon}"})
                    new_svg.append(new_use)
                    icon_wrapper.append(new_svg)
                    new_card.append(icon_wrapper)
                    
                    # 2. Elevation
                    new_elev = soup.new_tag("div", attrs={"class": "peak-elev"})
                    new_elev.string = elev
                    new_card.append(new_elev)
                    
                    # 3. Name
                    new_name = soup.new_tag("div", attrs={"class": "peak-name"})
                    new_name.string = name
                    new_card.append(new_name)
                    
                    # 4. Description
                    new_desc = soup.new_tag("div", attrs={"class": "peak-desc"})
                    new_desc.string = desc
                    new_card.append(new_desc)
                    
                    new_grid.append(new_card)
                    
                ul.replace_with(new_grid)
                modified = True
                
                if parent_card:
                    h_clone = soup.new_tag(h.name)
                    for attr in h.attrs:
                        h_clone[attr] = h[attr]
                    for child in h.contents:
                        h_clone.append(copy.copy(child))
                        
                    parent_card.insert_before(h_clone)
                    parent_card.insert_before(new_grid)
                    parent_card.decompose()
                    modified = True
                    
    # Always run nested container cleanup post-processing to clean previously missed parent cards
    cleaned = clean_double_nested_containers(soup)
    if cleaned:
        modified = True
        
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Upgraded/Cleaned {file_path}")

def run_upgrades():
    playbooks = [
        "unaksan-playbook.html",
        "naejangsan-playbook.html",
        "myeongseongsan-playbook.html",
        "gyeryongsan-playbook.html",
        "woraksan-playbook.html",
        "xueshan-playbook.html",
        "yangmingshan-playbook.html",
        "yushan-playbook.html",
        "deogyusan-playbook.html",
        "taebaeksan-playbook.html",
        "odaesan-playbook.html"
    ]
    
    for playbook in playbooks:
        for prefix in ["", "en/"]:
            path = prefix + playbook
            if os.path.exists(path):
                upgrade_playbook_lists(path)
                
    # Standardize Soyosan
    for prefix in ["", "en/"]:
        path = prefix + "soyosan-playbook.html"
        if os.path.exists(path):
            standardize_soyosan(path)
            
    # Standardize Sikjangsan
    for prefix in ["", "en/"]:
        path = prefix + "sikjangsan-playbook.html"
        if os.path.exists(path):
            standardize_sikjangsan(path)

if __name__ == "__main__":
    run_upgrades()
