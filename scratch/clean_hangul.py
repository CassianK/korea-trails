import re
import os

replacements = {
    "en/yangmingshan-playbook.html": {
        "/* Leaflet 기본 스타일 보정 */": "/* Leaflet base style adjustment */",
        "/* 마커 툴팁 커스텀 */": "/* Marker tooltip customization */",
        "/* 팝업 창 커스텀 */": "/* Popup window customization */",
        "/* 레이어 컨트롤 커스텀 */": "/* Layer control customization */",
        "/* 줌 컨트롤 커스텀 */": "/* Zoom control customization */",
        "/* 어트리뷰션 바 다크모드 가독성 확보 */": "/* Attribution bar dark mode readability */",
        "/* [다크모드 특화 스타일] */": "/* [Dark mode specific styles] */",
        "/* 오픈토포맵(지형도) 다크모드 시 인버트 필터 적용으로 눈부심 방지 */": "/* OpenTopoMap dark mode invert filter to prevent glare */",
        "// 양명산 Map 구성 데이터 정의": "// Define Yangmingshan Map configuration data",
        "// Beginner 기존 SVG 상속 색": "// Beginner existing SVG inherited color",
        "// Intermediate 기존 SVG 상속 색": "// Intermediate existing SVG inherited color",
        "// Advanced 기존 SVG 상속 색": "// Advanced existing SVG inherited color",
        "// Leaflet CDN 동적 로더 (오프라인 폴백 구조 및 무빌드 통합용)": "// Leaflet CDN dynamic loader (for offline fallback and buildless integration)",
        "// 1. Leaflet CSS 로드": "// 1. Load Leaflet CSS",
        "// 2. Leaflet JS 로드": "// 2. Load Leaflet JS",
        "// 단일 코스 Map 초기화 로직": "// Single course Map initialization logic",
        "// 폴백 SVG 숨기고 Map 엘리먼트 노Departure": "// Hide fallback SVG and show Map element",
        "// Map 인스턴스 생성": "// Create Map instance",
        "scrollWheelZoom: false, // 마우스 스크롤 Medium 의도치 않은 줌 제한": "scrollWheelZoom: false, // Prevent unintentional zoom from mouse scroll",
        "// 베이스 레이어 1: Esri World Imagery (위성 실사 - 기본값)": "// Base layer 1: Esri World Imagery (Satellite - default)",
        "// 베이스 레이어 2: OpenTopoMap (지형도 - 선택 레이어)": "// Base layer 2: OpenTopoMap (Terrain - optional)",
        "className: 'terrain-layer-dark-filter' // 다크모드 대응용 CSS 필터 클래스 바인딩": "className: 'terrain-layer-dark-filter' // Bind CSS filter class for dark mode",
        "// 위성 기본 로드": "// Load satellite by default",
        "// 경로 노드 수집 및 마커 생성": "// Collect route nodes and create markers",
        "// 동일 위치 Medium복 마커 방지 (왕복 코스의 시점/종점 겹침 처리)": "// Prevent duplicate markers at same position",
        "// 이름 파싱 (Xiaoyoukeng -> Xiaoyoukeng)": "// Name parsing",
        "// Point별 Features 상세화": "// Detailed features per point",
        "// circleMarker 기반 깔끔Lower고 모던한 체크Points 마킹": "// Clean and modern checkpoint markers",
        "// 툴팁(영구 표Departure 라벨) 부착": "// Attach tooltips",
        "// 팝업(클릭 시 상세정보 레이어) 구성": "// Configure popups",
        "// 경로 폴리라인 드로잉": "// Draw route polylines",
        '// <svg class="icon-svg"><use href="assets/icons/icons.svg#icon-location"/></svg> Map에 레이어들을 더Lower기 전에 먼저 Map의 구도를 코스 경계에 맞춰 설정 (Leaflet 뷰 투사 에러 방지)': '// Fit Map bounds before adding layers to avoid Leaflet projection errors',
        '// <svg class="icon-svg"><use href="assets/icons/icons.svg#icon-location"/></svg> 이제 안전Lower게 레이어들을 Map에 추가': '// Add layers to Map safely',
        "// Accessibility 보장: 키보드 제스처 및 탭 포커스 핸들링": "// Accessibility: keyboard gestures and tab focus handling",
        "// 전역 관리 변수 바인딩": "// Bind global management variables",
        "// IntersectionObserver 기반 레이지 로딩 & 탭 전동 전환 안정화": "// Lazy loading and tab transition stabilization",
        "// Map 이닛 진행": "// Initialize Map",
        "// 탭 컨텍스트 복구를 위한 resize 보정(Leaflet 0x0 렌더 깨짐 완전방지)": "// Correct resize for tab context recovery",
        "rootMargin: '100px', // 스크롤 도달 100px 전에 비동기 사전 로드": "rootMargin: '100px', // Preload 100px before scroll",
        "// 대상 엘리먼트 구독 등록: display: none인 leaflet-map 대신 카드 컨테이너를 관측": "// Observe card container instead of display:none leaflet-map",
        "// 기존 탭 스위처 이벤트 핸들러 고침/확장 (탭 클릭 시 Leaflet 로드 및 invalidateSize 재트리거 보장)": "// Extend tab switcher event handler",
        '// <svg class="icon-svg"><use href="assets/icons/icons.svg#icon-location"/></svg> Map 탭 클릭 시 렌더 크기 보정 및 동적 초기화 트리거': '// Correct render size and trigger initialization on tab click',
        "// 코스 핏 바운즈 재정렬로 카메라 구도 리셋": "// Reset camera view by fitting bounds",
        "}, 180); // 브라우저 display: block 전환 프레임 대기": "}, 180); // Wait for browser display block transition",
    },
    "en/soyosan-playbook.html": {
        "Summit 인증샷 (proof shot)": "Summit proof shot",
    },
    "en/sobaeksan-playbook.html": {
        "인증샷 (proof shot)": "proof shot",
        "인증샷": "proof shot",
    }
}

def clean_file(filepath, file_replacements):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} - file does not exist.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original_content = content
    for original, replacement in file_replacements.items():
        content = content.replace(original, replacement)
        
    # Also look for any remaining "인증샷" or "인증샷 (proof shot)" and replace it
    content = content.replace("인증샷 (proof shot)", "proof shot")
    content = content.replace("인증샷", "proof shot")
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned remaining Hangul in: {filepath}")
    else:
        print(f"No changes needed in: {filepath}")

def main():
    for filepath, file_replacements in replacements.items():
        clean_file(filepath, file_replacements)
        
if __name__ == '__main__':
    main()
