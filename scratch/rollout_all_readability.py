import os
import re
import json
from bs4 import BeautifulSoup

WORKSPACE_DIR = "/Users/mac/korea-trails"

RIDGE_APEX_LOGO_HTML = """<svg class="logo-svg" viewBox="0 0 40 40" width="36" height="36" role="img" aria-label="Korea Trails">
  <defs><linearGradient id="kt-gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f1d98a"/><stop offset=".5" stop-color="#c9a24b"/><stop offset="1" stop-color="#9c7a2e"/>
  </linearGradient></defs>
  <rect width="40" height="40" rx="9" fill="#0e1c34"/>
  <path d="M20 8 L33 31 L7 31 Z" fill="none" stroke="url(#kt-gold)" stroke-width="2.2" stroke-linejoin="round"/>
  <polyline points="11,28 16,21.5 19,24.5 24.5,17 29,28" fill="none" stroke="url(#kt-gold)" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
</svg>"""

SEORAKSAN_STYLE_CSS = """/* COURSE SELECTOR */
.course-selector {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  flex-wrap: wrap;
  margin-top: var(--space-6);
  margin-bottom: var(--space-8);
}
.course-btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: var(--text-sm);
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  cursor: pointer;
  transition: all var(--transition);
}
.course-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.course-btn.active.beginner, .course-btn.active-beginner {
  background: var(--success-highlight);
  color: var(--success);
  border-color: var(--success);
}
.course-btn.active.intermediate, .course-btn.active-intermediate {
  background: var(--color-gold-highlight);
  color: var(--color-gold);
  border-color: var(--color-gold);
}
.course-btn.active.advanced, .course-btn.active-advanced {
  background: var(--warning-highlight);
  color: var(--warning);
  border-color: var(--warning);
}

.intermediate .section-title-icon{background:var(--color-gold-highlight);}
.advanced .section-title-icon{background:var(--color-warning-highlight);}

/* ACCORDION */
.accordion{display:flex;flex-direction:column;gap:var(--space-3);margin-bottom:var(--space-8);}
.acc-item{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-lg);overflow:hidden;}
.acc-header{display:flex;align-items:center;gap:var(--space-4);padding:var(--space-4) var(--space-5);cursor:pointer;user-select:none;width:100%;text-align:left;}
.acc-header:hover{background:var(--color-surface-offset);}
.acc-num{width:28px;height:28px;border-radius:var(--radius-full);display:flex;align-items:center;justify-content:center;font-size:var(--text-xs);font-weight:700;flex-shrink:0;}
.beginner .acc-num{background:var(--color-success-highlight);color:var(--color-success);}
.intermediate .acc-num{background:var(--color-gold-highlight);color:var(--color-gold);}
.advanced .acc-num{background:var(--color-warning-highlight);color:var(--color-warning);}
.acc-title-wrap{flex:1;}
.acc-title{font-weight:700;font-size:var(--text-base);line-height:1.3;}
.acc-meta{font-size:var(--text-xs);color:var(--color-text-muted);margin-top:2px;}
.acc-chevron{color:var(--color-text-faint);transition:transform var(--transition);flex-shrink:0;}
.acc-item.open .acc-chevron{transform:rotate(180deg);}
.acc-body{display:none;padding:0 var(--space-5) var(--space-5);border-top:1px solid var(--color-divider);}
.acc-item.open .acc-body{display:block;}
.acc-desc{font-size:var(--text-sm);color:var(--color-text-muted);line-height:1.7;margin-bottom:var(--space-4);}

/* DIFF BAR */
.diff-bar-wrap{margin-bottom:var(--space-4);}
.diff-label{font-size:var(--text-xs);color:var(--color-text-muted);margin-bottom:var(--space-1);}
.diff-bar-bg{height:6px;background:var(--color-surface-dynamic);border-radius:var(--radius-full);overflow:hidden;}
.diff-bar-fill{height:100%;border-radius:var(--radius-full);}
.diff-easy .diff-bar-fill{background:var(--color-success);}
.diff-medium .diff-bar-fill{background:var(--color-gold);}
.diff-hard .diff-bar-fill{background:var(--color-warning);}
.diff-expert .diff-bar-fill{background:var(--color-error);}

/* TIP / WARN BOX */
.tip-box{background:var(--color-primary-highlight);border-left:3px solid var(--color-primary);border-radius:0 var(--radius-md) var(--radius-md) 0;padding:var(--space-3) var(--space-4);font-size:var(--text-sm);color:var(--color-primary);margin-bottom:var(--space-3);line-height:1.6;}
.warn-box{background:var(--color-warning-highlight);border-left:3px solid var(--color-warning);border-radius:0 var(--radius-md) var(--radius-md) 0;padding:var(--space-3) var(--space-4);font-size:var(--text-sm);color:var(--color-warning);margin-bottom:var(--space-3);line-height:1.6;}

/* CHECKPOINT TABLE */
.cp-table-wrap{overflow-x:auto;margin-bottom:var(--space-8);}
.cp-table{width:100%;border-collapse:collapse;font-size:var(--text-sm);}
.cp-table th{text-align:left;font-weight:700;font-size:var(--text-xs);text-transform:uppercase;letter-spacing:0.06em;color:var(--color-text-muted);padding:var(--space-2) var(--space-4);border-bottom:2px solid var(--color-divider);white-space:nowrap;}
.cp-table td{padding:var(--space-3) var(--space-4);border-bottom:1px solid var(--color-divider);vertical-align:middle;}
.cp-table tr:last-child td{border-bottom:none;}
.cp-table tr:hover td{background:var(--color-surface-offset);}
.badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:var(--radius-full);font-size:var(--text-xs);font-weight:700;}
.badge-summit{background:var(--color-warning-highlight);color:var(--color-warning);}
.badge-shelter{background:var(--color-primary-highlight);color:var(--color-primary);}
.badge-temple{background:var(--color-success-highlight);color:var(--color-success);}
.badge-trailhead{background:var(--color-surface-dynamic);color:var(--color-text-muted);}
.badge-landmark{background:var(--color-gold-highlight);color:var(--color-gold);}

/* MAP SVG */
.map-wrap{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-xl);padding:var(--space-6);margin-bottom:var(--space-8);}
.map-wrap h3{font-family:var(--font-display);font-weight:700;font-size:var(--text-lg);margin-bottom:var(--space-4);}
.map-svg{width:100%;height:auto;max-height:520px;}

/* TIPS GRID */
.tips-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--space-4);margin-bottom:var(--space-8);}
.tip-card{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-lg);padding:var(--space-5);}
.tip-card-icon{font-size:1.5rem;margin-bottom:var(--space-3);}
.tip-card h4{font-weight:700;margin-bottom:var(--space-2);}
.tip-card ul{list-style:none;display:flex;flex-direction:column;gap:var(--space-1);}
.tip-card ul li{font-size:var(--text-sm);color:var(--color-text-muted);padding-left:var(--space-4);position:relative;}
.tip-card ul li::before{content:"·";position:absolute;left:var(--space-2);color:var(--color-text-faint);}

/* RESPONSIVE */
@media(max-width:640px){
  .site-header{padding:var(--space-3) var(--space-4);}
  .main{padding:var(--space-6) var(--space-4);}
  .hero{padding:var(--space-8) var(--space-4) var(--space-6);}
  .tab-bar{padding:0 var(--space-4);}
  .stat-grid{grid-template-columns:repeat(2,1fr);}
  .course-selector{gap:var(--space-2);}
  .course-btn{padding:var(--space-2) var(--space-4);font-size:var(--text-xs);}
}
"""

YANGMINGSHAN_STYLE_CSS = """  /* Header & Navigation */
  .header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: var(--space-3) var(--space-6);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }
  
  .brand {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }
  
  .logo {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--teal, var(--primary)), var(--primary));
    display: grid;
    place-items: center;
    box-shadow: var(--shadow-sm);
  }
  
  .brand h1 {
    font-family: var(--font-display);
    font-size: var(--text-lg);
    font-weight: 800;
    line-height: 1;
  }
  
  .brand p {
    font-size: var(--text-xs);
    color: var(--muted);
    margin-top: 2px;
  }
  
  .theme-btn {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface2);
    color: var(--muted);
    cursor: pointer;
    border: none;
    transition: background-color var(--transition), color var(--transition);
  }
  
  .theme-btn:hover {
    background: var(--border);
    color: var(--text);
  }

  /* Selector & Course Buttons */
  .selector {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-3);
    padding: var(--space-5) 0 var(--space-3);
  }
  
  .course-btn {
    border: 1px solid var(--border);
    background: var(--surface);
    padding: var(--space-3) var(--space-5);
    border-radius: var(--radius-full);
    cursor: pointer;
    font-weight: 700;
    color: var(--text);
    transition: all var(--transition);
  }
  
  .course-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
  }
  
  .course-btn.active.green { background: var(--greenbg); border-color: var(--green); color: #273e16; }
  .course-btn.active.blue { background: var(--bluebg); border-color: var(--blue); color: #1e3a5f; }
  .course-btn.active.red { background: var(--redbg); border-color: var(--red); color: #6a2a18; }

  [data-theme="dark"] .course-btn.active.green { background: var(--greenbg); border-color: var(--green); color: var(--green); }
  [data-theme="dark"] .course-btn.active.blue { background: var(--bluebg); border-color: var(--blue); color: var(--blue); }
  [data-theme="dark"] .course-btn.active.red { background: var(--redbg); border-color: var(--red); color: var(--red); }

  /* Panels & Course Info */
  .panel {
    display: none;
    padding: var(--space-4) 0 var(--space-10);
  }
  
  .panel.active {
    display: block;
  }
  
  .panel-top {
    display: flex;
    gap: var(--space-3);
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: var(--space-5);
  }
  
  .level {
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-full);
    font-size: var(--text-sm);
    font-weight: 800;
  }
  
  .green .level { background: var(--greenbg); color: #273e16; border: 1px solid var(--green); }
  .blue .level { background: var(--bluebg); color: #1e3a5f; border: 1px solid var(--blue); }
  .red .level { background: var(--redbg); color: #6a2a18; border: 1px solid var(--red); }

  [data-theme="dark"] .green .level { background: var(--greenbg); color: var(--green); }
  [data-theme="dark"] .blue .level { background: var(--bluebg); color: var(--blue); }
  [data-theme="dark"] .red .level { background: var(--redbg); color: var(--red); }
  
  .panel-name {
    font-family: var(--font-display);
    font-size: var(--text-xl);
    font-weight: 800;
  }
  
  .panel-sub {
    font-size: var(--text-sm);
    color: var(--muted);
  }

  /* Tabs Customizations (Keep Pill Style matching original design) */
  .tabs {
    display: flex;
    gap: var(--space-2);
    overflow-x: auto;
    padding-bottom: var(--space-2);
    margin: var(--space-4) 0 var(--space-6);
    border-bottom: none;
  }
  
  .tab {
    border: none;
    background: var(--surface2);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-full);
    cursor: pointer;
    white-space: nowrap;
    color: var(--muted);
    font-weight: 700;
    transition: all var(--transition);
  }
  
  .tab:hover {
    background: var(--border);
    color: var(--text);
  }
  
  .green .tab.active { background: var(--greenbg); color: #273e16; border: 1px solid var(--green); }
  .blue .tab.active { background: var(--bluebg); color: #1e3a5f; border: 1px solid var(--blue); }
  .red .tab.active { background: var(--redbg); color: #6a2a18; border: 1px solid var(--red); }

  [data-theme="dark"] .green .tab.active { background: var(--greenbg); color: var(--green); }
  [data-theme="dark"] .blue .tab.active { background: var(--bluebg); color: var(--blue); }
  [data-theme="dark"] .red .tab.active { background: var(--redbg); color: var(--red); }

  /* Grid & KPI Cards Layout */
  .grid6 {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: var(--space-4);
  }
  
  .kpi .num {
    font-family: var(--font-display);
    font-size: var(--text-lg);
    font-weight: 800;
  }
  
  .green .kpi .num { color: var(--green); }
  .blue .kpi .num { color: var(--blue); }
  .red .kpi .num { color: var(--red); }
  
  .kpi .txt {
    font-size: var(--text-xs);
    color: var(--muted);
  }

  /* Section Titles */
  .section-title {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    margin: var(--space-4) 0 var(--space-4);
  }
  
  .section-title h3 {
    font-family: var(--font-display);
    font-size: var(--text-lg);
    font-weight: 800;
  }
  
  .line {
    height: 1px;
    background: var(--border);
    flex: 1;
  }

  /* Course Flow */
  .flow {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
  }
  
  .chip {
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-full);
    background: var(--surface2);
    font-size: var(--text-xs);
    font-weight: 700;
  }
  
  .arr {
    align-self: center;
    color: var(--faint);
  }
  
  .elev svg {
    width: 100%;
    height: 220px;
  }
  
  .desc {
    margin-top: var(--space-4);
    color: var(--muted);
    font-size: var(--text-sm);
  }

  /* Segment Accordions */
  .segments {
    display: grid;
    gap: var(--space-3);
  }
  
  .seg {
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    background: var(--surface);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: all var(--transition);
  }
  
  .seg-head {
    display: flex;
    gap: var(--space-4);
    align-items: center;
    padding: var(--space-4) var(--space-5);
    cursor: pointer;
  }
  
  .seg-no {
    width: 34px;
    height: 34px;
    border-radius: var(--radius-full);
    display: grid;
    place-items: center;
    font-size: var(--text-xs);
    font-weight: 800;
  }
  
  .green .seg-no { background: var(--greenbg); color: var(--green); }
  .blue .seg-no { background: var(--bluebg); color: var(--blue); }
  .red .seg-no { background: var(--redbg); color: var(--red); }
  
  .seg-title {
    font-weight: 800;
    font-size: var(--text-base);
  }
  
  .seg-meta {
    font-size: var(--text-xs);
    color: var(--muted);
    margin-top: 2px;
  }
  
  .seg-arrow {
    margin-left: auto;
    color: var(--muted);
    font-size: 0.85rem;
    transition: transform var(--transition);
  }
  
  .seg-body {
    display: none;
    padding: 0 var(--space-5) var(--space-5);
    border-top: 1px solid var(--border);
  }
  
  .seg.open .seg-body {
    display: block;
  }
  
  .seg.open .seg-arrow {
    transform: rotate(180deg);
  }
  
  .seg-body p {
    margin-top: var(--space-4);
    color: var(--muted);
    font-size: var(--text-sm);
  }
  
  .bar {
    height: 7px;
    background: var(--surface2);
    border-radius: var(--radius-full);
    overflow: hidden;
    margin: var(--space-3) 0;
  }
  
  .fill {
    height: 100%;
  }
  
  .green .fill { background: var(--green); }
  .blue .fill { background: var(--blue); }
  .red .fill { background: var(--red); }
  
  .tip, .warn {
    padding: var(--space-3);
    border-radius: var(--radius-md);
    font-size: var(--text-xs);
    margin-top: var(--space-3);
    line-height: 1.5;
  }
  
  .tip {
    background: var(--surface2);
    color: var(--muted);
  }
  
  .warn {
    background: var(--redbg);
    color: var(--red);
  }

  .table-wrap {
    overflow-x: auto;
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    background: var(--surface);
    box-shadow: var(--shadow-sm);
  }
  
  th, td {
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--border);
    font-size: var(--text-xs);
    text-align: left;
  }
  
  th {
    background: var(--surface2);
    color: var(--muted);
    font-weight: 800;
  }
  
  tr:last-child td {
    border-bottom: none;
  }

  .tips-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-4);
  }
  
  .tipcard h4 {
    font-size: var(--text-sm);
    margin-bottom: var(--space-2);
  }
  
  .tipcard ul {
    padding-left: var(--space-4);
    margin: 0;
  }
  
  .tipcard li {
    margin: var(--space-2) 0;
    color: var(--muted);
    font-size: var(--text-xs);
  }
  
  @media (max-width: 960px) {
    .grid6 { grid-template-columns: repeat(3, 1fr); }
    .tips-grid { grid-template-columns: 1fr 1fr; }
    .stats { grid-template-columns: repeat(2, 1fr); }
  }
  
  @media (max-width: 640px) {
    .grid6 { grid-template-columns: repeat(2, 1fr); }
    .tips-grid { grid-template-columns: 1fr; }
    .stats { grid-template-columns: 1fr; }
    .selector { gap: var(--space-2); }
    .course-btn { padding: var(--space-2) var(--space-4); font-size: var(--text-xs); }
  }
"""

def extract_variables(text):
    root_match = re.search(r":root\s*,\s*\[data-theme=\"light\"\]\s*\{(.*?)\}", text, re.DOTALL)
    if not root_match:
        root_match = re.search(r":root\s*\{(.*?)\}", text, re.DOTALL)
    dark_match = re.search(r"\[data-theme=\"dark\"\]\s*\{(.*?)\}", text, re.DOTALL)

    global_vars = {"--bg", "--surface", "--surface2", "--border", "--divider", "--text", "--muted", "--faint", 
                   "--primary", "--primary-hover", "--primary-highlight", "--success", "--success-highlight", 
                   "--warning", "--warning-highlight", "--error", "--error-highlight", "--font-body", "--font-display",
                   "--shadow-sm", "--shadow-md", "--shadow-lg", "--radius-sm", "--radius-md", "--radius-lg", "--radius-xl", "--radius-full",
                   "--transition", "--transition-slow", "--space-1", "--space-2", "--space-3", "--space-4", "--space-5", "--space-6",
                   "--space-8", "--space-10", "--space-12", "--space-16", "--r", "--r2", "--xs", "--sm", "--base", "--lg", "--xl", "--xxl", "--shadow"}

    ignore_vars = global_vars.union({
        "--color-bg", "--color-surface", "--color-surface-2", "--color-surface-offset", "--color-surface-dynamic",
        "--color-divider", "--color-border", "--color-text", "--color-text-muted", "--color-text-faint",
        "--color-text-inverse", "--color-primary", "--color-primary-hover", "--color-primary-highlight",
        "--color-success", "--color-success-highlight", "--color-gold", "--color-gold-highlight",
        "--color-warning", "--color-warning-highlight", "--color-error", "--color-error-highlight",
        "--color-blue", "--color-blue-highlight", "--color-orange", "--color-advanced", "--color-advanced-light",
        "--color-advanced-bg", "--color-beginner", "--color-beginner-light", "--color-beginner-bg",
        "--color-intermediate", "--color-intermediate-light", "--color-intermediate-bg", "--color-accent"
    })

    light_css = ""
    dark_css = ""

    if root_match:
        vars_light = re.findall(r"(--[a-zA-Z0-9_\-]+)\s*:\s*([^;}\n]+)", root_match.group(1))
        local_light = [f"    {k}: {v.strip()};" for k, v in vars_light if k not in ignore_vars]
        if local_light:
            light_css = "  :root {\n" + "\n".join(local_light) + "\n  }\n"

    if dark_match:
        vars_dark = re.findall(r"(--[a-zA-Z0-9_\-]+)\s*:\s*([^;}\n]+)", dark_match.group(1))
        local_dark = [f"    {k}: {v.strip()};" for k, v in vars_dark if k not in ignore_vars]
        if local_dark:
            dark_css = "  [data-theme=\"dark\"] {\n" + "\n".join(local_dark) + "\n  }\n"

    return light_css, dark_css

def parse_checkpoint_table(table_el, is_en=False):
    headers = [th.text.strip().lower() for th in table_el.find_all("th")]
    
    name_idx = -1
    elev_idx = -1
    dist_idx = -1
    badge_idx = -1
    features_idx = -1
    day_idx = -1
    
    for i, h in enumerate(headers):
        if "일정" in h or "day" in h or "schedule" in h:
            day_idx = i
        elif "지점" in h or "point" in h or "name" in h:
            name_idx = i
        elif "고도" in h or "해발" in h or "elevation" in h or "elev" in h:
            elev_idx = i
        elif "거리" in h or "distance" in h or "dist" in h:
            dist_idx = i
        elif "종류" in h or "type" in h:
            badge_idx = i
        elif any(x in h for x in ["편의", "시설", "features", "amenities", "memo", "메모", "특징", "비고", "note"]):
            features_idx = i
            
    if name_idx == -1:
        name_idx = 0 if day_idx != 0 else 1
    if elev_idx == -1:
        for i, h in enumerate(headers):
            if any(x in h for x in ["고도", "해발", "elevation", "elev", "height", "m"]):
                elev_idx = i
                break
        if elev_idx == -1: elev_idx = 1
    if dist_idx == -1:
        for i, h in enumerate(headers):
            if any(x in h for x in ["거리", "distance", "dist", "km"]):
                dist_idx = i
                break
        if dist_idx == -1: dist_idx = 2
    if features_idx == -1:
        features_idx = len(headers) - 1
        
    rows_data = []
    tbody = table_el.find("tbody")
    if not tbody:
        tbody = table_el
        
    for tr in tbody.find_all("tr"):
        cells = tr.find_all("td")
        if not cells or len(cells) < 2:
            continue
            
        def get_cell_text(idx):
            if idx >= 0 and idx < len(cells):
                return cells[idx].text.strip()
            return ""
            
        name = get_cell_text(name_idx)
        elevation = get_cell_text(elev_idx)
        distance = get_cell_text(dist_idx)
        features = get_cell_text(features_idx) if (features_idx != -1 and features_idx < len(cells)) else ""
        day_val = get_cell_text(day_idx) if (day_idx != -1 and day_idx < len(cells)) else None
        
        badge_html = ""
        badge_text = ""
        badge_class = ""
        
        if badge_idx != -1 and badge_idx < len(cells):
            badge_span = cells[badge_idx].find("span")
            if badge_span:
                badge_text = badge_span.text.strip()
                badge_class = " ".join(badge_span.get("class", []))
                
        if not badge_text:
            name_lower = name.lower()
            features_lower = features.lower() if features else ""
            if any(x in name_lower or x in features_lower for x in ["출발", "들머리", "시작", "start", "departure", "탐방지원센터", "주차장", "gateway"]):
                badge_text = "Starting Point" if is_en else "출발점"
                badge_class = "badge badge-trailhead"
            elif any(x in name_lower or x in features_lower for x in ["종점", "귀환", "완료", "하산", "end", "return", "ending"]):
                badge_text = "End Point" if is_en else "종점"
                badge_class = "badge badge-trailhead"
            elif any(x in name_lower or x in features_lower for x in ["정상", "주봉", "봉우리", "대청봉", "비로봉", "향적봉", "peak", "summit", "봉"]):
                badge_text = "Summit" if is_en else "정상"
                badge_class = "badge badge-summit"
            elif any(x in name_lower or x in features_lower for x in ["대피소", "산장", "대피", "shelter", "cabin"]):
                badge_text = "Shelter" if is_en else "대피소"
                badge_class = "badge badge-shelter"
            elif any(x in name_lower or x in features_lower for x in ["사찰", "절", "암", "사", "temple", "hermitage"]):
                badge_text = "Temple" if is_en else "사찰"
                badge_class = "badge badge-temple"
            else:
                badge_text = "Landmark" if is_en else "명소"
                badge_class = "badge badge-landmark"
        else:
            badge_text_lower = badge_text.lower()
            if "b-st" in badge_class or "trailhead" in badge_class or any(x in badge_text_lower for x in ["출발", "들머리", "시작", "종점", "귀환", "완료", "start", "end", "return"]):
                badge_class = "badge badge-trailhead"
            elif "b-sk" in badge_class or "shelter" in badge_class or any(x in badge_text_lower for x in ["대피소", "산장", "대피", "쉼터", "shelter"]):
                badge_class = "badge badge-shelter"
            elif "b-pk" in badge_class or "summit" in badge_class or any(x in badge_text_lower for x in ["정상", "주봉", "봉우리", "대청봉", "비로봉", "향적봉", "peak", "summit"]):
                badge_class = "badge badge-summit"
            elif "b-tp" in badge_class or "temple" in badge_class or any(x in badge_text_lower for x in ["사찰", "절", "암", "사", "temple", "hermitage"]):
                badge_class = "badge badge-temple"
            else:
                badge_class = "badge badge-landmark"
                
        badge_html = f'<span class="{badge_class}">{badge_text}</span>'
        
        rows_data.append({
            "name": name,
            "elevation": elevation,
            "distance": distance,
            "features": features,
            "day": day_val,
            "badge_html": badge_html
        })
        
    return rows_data

def render_timeline(rows_data, is_en=False):
    timeline_html = ['<div class="checkpoint-timeline">']
    for idx, row in enumerate(rows_data):
        item_class = "timeline-item"
        if idx == 0:
            item_class += " start"
        elif idx == len(rows_data) - 1:
            item_class += " end"
            
        if "badge-summit" in row["badge_html"]:
            item_class += " summit"
            
        day_meta_html = ""
        if row["day"]:
            day_label = row["day"]
            if "📅" not in day_label:
                day_label = "📅 " + day_label
            day_meta_html = f'<span class="meta-item">{day_label}</span>\n        '
            
        elevation_label = "Elevation" if is_en else "해발"
        distance_label = "Cumulative" if is_en else "누적"
        features_label = "Amenities" if is_en else "편의시설"
        
        elevation_str = row["elevation"].replace("⛰", "").replace("Elevation", "").replace("고도", "").replace("해발", "").strip()
        distance_str = row["distance"].replace("📏", "").replace("Cumulative", "").replace("누적", "").strip()
        features_str = row["features"].strip()
        if not features_str or features_str in ["—", "-", "none"]:
            features_str = "—"
            
        timeline_html.append(f"""  <div class="{item_class}">
    <div class="timeline-marker">{idx + 1}</div>
    <div class="timeline-content">
      <div class="timeline-header">
        <span class="checkpoint-name">{row["name"]}</span>
        {row["badge_html"]}
      </div>
      <div class="timeline-meta">
        {day_meta_html}<span class="meta-item">⛰ {elevation_label} {elevation_str}</span>
        <span class="meta-item">📏 {distance_label} {distance_str}</span>
      </div>
      <div class="timeline-features">
        <span class="feature-label">{features_label}:</span> {features_str}
      </div>
    </div>
  </div>""")
        
    timeline_html.append('</div>')
    return "\n".join(timeline_html)

def convert_stats_grid(stats_grid_el, is_en=False):
    cards = stats_grid_el.find_all(class_=lambda x: x and any(c in x.split() for c in ["stat-card", "kpi"]))
    if not cards:
        cards = [child for child in stats_grid_el.children if child.name == "div"]
        
    pills_html = []
    for card in cards:
        icon_el = card.find(class_=lambda x: x and any(c in x.split() for c in ["stat-icon", "si"]))
        val_el = card.find(class_=lambda x: x and any(c in x.split() for c in ["stat-value", "sv", "num"]))
        label_el = card.find(class_=lambda x: x and any(c in x.split() for c in ["stat-label", "sl", "txt"]))
        
        icon = icon_el.text.strip() if icon_el else ""
        if not icon and icon_el and icon_el.find("svg"):
            icon = str(icon_el.find("svg"))
            
        value = val_el.text.strip() if val_el else ""
        label = label_el.text.strip() if label_el else ""
        
        if not label or not value:
            divs = card.find_all("div")
            if len(divs) >= 3:
                icon = divs[0].text.strip()
                if not icon and divs[0].find("svg"):
                    icon = str(divs[0].find("svg"))
                value = divs[1].text.strip()
                label = divs[2].text.strip()
            elif len(divs) == 2:
                value = divs[0].text.strip()
                label = divs[1].text.strip()
                
        if not icon:
            label_lower = label.lower()
            if "거리" in label_lower or "distance" in label_lower:
                icon = "📏"
            elif "시간" in label_lower or "일정" in label_lower or "duration" in label_lower or "time" in label_lower or "itinerary" in label_lower:
                icon = "⏱"
            elif "정상" in label_lower or "peak" in label_lower or "summit" in label_lower:
                icon = '<svg class="icon-svg"><use href="assets/icons/icons.svg#icon-mountain"/></svg>' if not is_en else '<svg class="icon-svg"><use href="../assets/icons/icons.svg#icon-mountain"/></svg>'
            elif "고도" in label_lower or "altitude" in label_lower or "elevation" in label_lower:
                icon = "📈"
            elif "칼로리" in label_lower or "calories" in label_lower:
                icon = "🔥"
            elif "난이도" in label_lower or "difficulty" in label_lower:
                icon = "⭐"
            elif "지형" in label_lower or "terrain" in label_lower:
                icon = '<svg class="icon-svg"><use href="assets/icons/icons.svg#icon-mountain"/></svg>' if not is_en else '<svg class="icon-svg"><use href="../assets/icons/icons.svg#icon-mountain"/></svg>'
            elif "접근성" in label_lower or "accessibility" in label_lower:
                icon = "🧭"
            elif "계절" in label_lower or "season" in label_lower:
                icon = "🍂"
            else:
                icon = "🧭"
                
        if "<svg" in icon and "icon-svg" not in icon:
            icon = re.sub(r'<svg\b', '<svg class="icon-svg"', icon)
            
        if "난이도" in label or "difficulty" in label or label.lower() == "difficulty":
            stars_count = 0
            if "★" in value:
                stars_count = value.count("★")
            else:
                val_lower = value.lower()
                if "하" in val_lower or "easy" in val_lower or "low" in val_lower:
                    stars_count = 1
                    if "중하" in val_lower or "medium-low" in val_lower:
                        stars_count = 2
                elif "중" in val_lower or "medium" in val_lower:
                    stars_count = 3
                    if "중상" in val_lower or "medium-high" in val_lower:
                        stars_count = 4
                elif "상" in val_lower or "hard" in val_lower or "high" in val_lower or "expert" in val_lower:
                    stars_count = 5
                    
            if stars_count == 0:
                stars_count = 3
                
            active_class = "active-medium"
            if stars_count <= 2:
                active_class = "active-easy"
            elif stars_count >= 5:
                active_class = "active-hard"
                
            segments_html = []
            for s in range(5):
                if s < stars_count:
                    segments_html.append(f'<span class="segment {active_class}"></span>')
                else:
                    segments_html.append('<span class="segment"></span>')
                    
            segments_str = "\n        ".join(segments_html)
            aria_lbl = f"난이도: {stars_count}단계" if not is_en else f"Difficulty: Level {stars_count}"
            
            value_html = f"""<div class="difficulty-meter" aria-label="{aria_lbl}">
      <div class="meter-segments">
        {segments_str}
      </div>
    </div>"""
            pills_html.append(f"""  <div class="stat-pill">
    <span class="pill-icon">⭐</span>
    <span class="pill-label">{label}</span>
    {value_html}
  </div>""")
        else:
            pills_html.append(f"""  <div class="stat-pill">
    <span class="pill-icon">{icon}</span>
    <span class="pill-label">{label}</span>
    <span class="pill-value">{value}</span>
  </div>""")
            
    summary_html = ['<div class="course-stats-summary">']
    summary_html.extend(pills_html)
    summary_html.append('</div>')
    return "\n".join(summary_html)

def convert_accordion_meta_and_desc(soup, is_en=False):
    items = soup.find_all(class_=lambda x: x and any(c in x.split() for c in ["acc-item", "seg"]))
    for item in items:
        meta_el = item.find(class_=lambda x: x and any(c in x.split() for c in ["acc-meta", "acc-m", "seg-meta"]))
        if meta_el and not meta_el.find(class_="acc-meta-chips") and not meta_el.find(class_="meta-chip"):
            meta_text = meta_el.text.strip()
            parts = [p.strip() for p in re.split(r'[·•|/]', meta_text) if p.strip()]
            if not parts:
                parts = [meta_text]
                
            chips_html = []
            for part in parts:
                emoji = "📍"
                part_lower = part.lower()
                
                if "km" in part_lower or "mile" in part_lower or "거리" in part_lower:
                    emoji = "📏"
                elif any(x in part_lower for x in ["시간", "분", "hr", "min", "h", "m"]) and not any(x in part_lower for x in ["km", "elevation", "해발"]):
                    emoji = "⏱"
                elif any(x in part_lower for x in ["일", "day", "night", "박", "일차"]):
                    emoji = "📅"
                elif any(x in part_lower for x in ["출발", "시작", "start"]):
                    emoji = "🚩"
                elif any(x in part_lower for x in ["종점", "완료", "끝", "귀환", "end", "return"]):
                    emoji = "🏁"
                elif any(x in part_lower for x in ["해발", "고도", "elev", "height"]):
                    emoji = "⛰"
                elif any(x in part_lower for x in ["↑", "올라", "오르막", "ascent", "up", "gain"]):
                    emoji = "📈"
                elif any(x in part_lower for x in ["↓", "내려", "내리막", "descent", "down", "loss"]):
                    emoji = "📉"
                    
                chips_html.append(f'<span class="meta-chip">{emoji} {part}</span>')
                
            if chips_html:
                new_chips_soup = BeautifulSoup(f'<div class="acc-meta-chips">{"".join(chips_html)}</div>', "html.parser").div
                meta_el.replace_with(new_chips_soup)
                
        desc_els = item.find_all(class_=lambda x: x and any(c in x.split() for c in ["acc-desc"]))
        if not desc_els:
            body = item.find(class_=lambda x: x and any(c in x.split() for c in ["acc-body", "seg-body"]))
            if body:
                desc_els = body.find_all("p", recursive=False)
                
        for desc_el in desc_els:
            desc_text = desc_el.text.strip()
            sentences = re.split(r'(?<=[.!?])\s+', desc_text)
            if len(sentences) > 3:
                paragraphs = []
                current_p = []
                for idx, sent in enumerate(sentences):
                    current_p.append(sent)
                    if len(current_p) >= 2 or idx == len(sentences) - 1:
                        paragraphs.append(" ".join(current_p))
                        current_p = []
                        
                for p_text in paragraphs:
                    new_p = soup.new_tag("p", attrs={"class": "acc-desc"})
                    new_p.string = p_text
                    desc_el.insert_before(new_p)
                desc_el.decompose()

def get_mountain_name(soup):
    title_text = soup.title.text.strip() if soup.title else ""
    m = re.match(r"^([^\s]+)", title_text)
    if m:
        name = m.group(1)
        name = name.replace("플레이북", "").replace("등산", "").strip()
        return name
    return "명산"

def detect_template_family(content):
    if "site-header" in content or "course-selector" in content or "togAcc" in content:
        return "seoraksan-style"
    return "yangmingshan-style"

def process_playbook(file_name):
    file_path = os.path.join(WORKSPACE_DIR, file_name)
    is_en = file_name.startswith("en/")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update header inline logo
    soup = BeautifulSoup(content, "html.parser")
    header_el = soup.find("header")
    if header_el:
        logo_svg = header_el.find("svg", class_=lambda x: x and "logo-svg" in x)
        if logo_svg:
            new_logo_soup = BeautifulSoup(RIDGE_APEX_LOGO_HTML, "html.parser").svg
            logo_svg.replace_with(new_logo_soup)
            
    for other_svg in soup.find_all("svg", class_=lambda x: x and "logo-svg" in x):
        new_logo_soup = BeautifulSoup(RIDGE_APEX_LOGO_HTML, "html.parser").svg
        other_svg.replace_with(new_logo_soup)

    # 2. Rebrand favicon & OG links in head
    head = soup.head
    if head:
        fav_path = "../assets/brand/favicon.svg" if is_en else "assets/brand/favicon.svg"
        icon_tags = head.find_all("link", rel=re.compile(r"^(shortcut )?icon$", re.I))
        for tag in icon_tags:
            tag["href"] = fav_path
            tag["type"] = "image/svg+xml"
            
        og_img_tag = head.find("meta", attrs={"property": "og:image"})
        tw_img_tag = head.find("meta", attrs={"name": "twitter:image"})
        target_img = "../assets/img/brand-og.png" if is_en else "assets/img/brand-og.png"
        
        m_id = os.path.basename(file_name).replace("-playbook.html", "")
        m_og_path = f"assets/img/{m_id}/og.png"
        if is_en:
            m_og_path = "../" + m_og_path
            
        if os.path.exists(os.path.join(WORKSPACE_DIR, m_og_path.replace("../", ""))):
            target_img = m_og_path
            
        if og_img_tag:
            og_img_tag["content"] = target_img
        if tw_img_tag:
            tw_img_tag["content"] = target_img

    if "seoraksan" in file_name:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Rebranded logo/head for Seoraksan: {file_name}")
        return

    # 3. Readability Redesign upgrades
    template_family = detect_template_family(content)

    # 3a. Update Style & stylesheet link
    head_text = str(soup)
    style_idx = head_text.find("<style>")
    if style_idx != -1:
        link_href = "../assets/css/design-system.css" if is_en else "assets/css/design-system.css"
        if f'href="{link_href}"' not in head_text:
            head_text = head_text[:style_idx] + f'<link rel="stylesheet" href="{link_href}">\n' + head_text[style_idx:]
            
        style_idx = head_text.find("<style>")
        upgrade_comment_match = re.search(r'/\*\s*---\s*UPGRADE:\s*HERO\s*BLEED', head_text)
        if upgrade_comment_match:
            upgrade_idx = upgrade_comment_match.start()
            
            custom_style_block = ""
            if template_family == "yangmingshan-style":
                light_vars, dark_vars = extract_variables(content)
                custom_style_block = f"<style>\n{light_vars}\n{dark_vars}\n{YANGMINGSHAN_STYLE_CSS}\n"
            else:
                custom_style_block = f"<style>\n{SEORAKSAN_STYLE_CSS}\n"
                
            head_text = head_text[:style_idx] + custom_style_block + head_text[upgrade_idx:]

    soup = BeautifulSoup(head_text, "html.parser")

    # 3b. Add skip-link right after <body>
    body = soup.body
    if body:
        skip_link_text = "Skip to main content" if is_en else "본문 바로가기"
        if not soup.find(class_="skip-link"):
            new_skip = soup.new_tag("a", href="#mainContent", attrs={"class": "skip-link"})
            new_skip.string = skip_link_text
            body.insert(0, new_skip)

    # 3c. Wrap course panels in <main id="mainContent">
    first_panel = None
    if template_family == "yangmingshan-style":
        first_panel = soup.find(class_=lambda x: x and "panel" in x.split(), id=lambda x: x in ["beginner", "easy"])
    else:
        first_panel = soup.find(class_=lambda x: x and any(c in x.split() for c in ["course-panel", "panel"]), 
                                id=lambda x: x and any(y in x.lower() for y in ["begin", "easy", "beg"]))
        
    if first_panel and not soup.find("main", id="mainContent"):
        main_wrap = soup.new_tag("main", attrs={"class": "wrap", "id": "mainContent"})
        first_panel.insert_before(main_wrap)
        
        siblings = []
        curr = main_wrap.next_sibling
        while curr:
            next_sib = curr.next_sibling
            
            is_footer = False
            if curr.name in ["footer"]:
                is_footer = True
            elif curr.name == "section" and curr.get("class") and any(c in curr.get("class") for c in ["photo-gallery-section", "footer"]):
                is_footer = True
            elif isinstance(curr, str) and ("FOOTER" in curr or "Photo Gallery" in curr):
                is_footer = True
                
            if is_footer:
                break
                
            if curr.name:
                siblings.append(curr)
            curr = next_sib
            
        for sib in siblings:
            main_wrap.append(sib)

    # 3d. Replace inner <main class="main"> to <div class="main"> in seoraksan-style
    if template_family == "seoraksan-style":
        for inner_main in soup.find_all("main", class_="main"):
            inner_main.name = "div"

    # 3e. Fix Heading Hierarchy
    for title in soup.find_all(class_=re.compile(r"section-title")):
        h_tag = title.find(["h3", "h4"])
        if h_tag:
            h_tag.name = "h2"
            
    for h3 in soup.find_all("h3"):
        if not h3.get("class") or "section-title" not in h3.get("class"):
            h3.name = "h2"
    for h4 in soup.find_all("h4"):
        h4.name = "h3"

    # 3f. Convert stats grids
    for grid in soup.find_all(class_=re.compile(r"(stat-grid|grid6)")):
        new_stats_html = convert_stats_grid(grid, is_en=is_en)
        new_stats_soup = BeautifulSoup(new_stats_html, "html.parser").div
        grid.replace_with(new_stats_soup)

    # 3g. Convert checkpoint tables
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.text.strip().lower() for th in table.find_all("th")]
        is_checkpoint_table = any(any(x in h for x in ["지점", "point", "name", "고도", "elevation"]) for h in headers)
        
        if is_checkpoint_table:
            rows_data = parse_checkpoint_table(table, is_en=is_en)
            if rows_data:
                timeline_html = render_timeline(rows_data, is_en=is_en)
                timeline_soup = BeautifulSoup(timeline_html, "html.parser").div
                
                parent = table.parent
                if parent and parent.name == "div" and any(c in parent.get("class", []) for c in ["cp-table-wrap", "table-wrap", "cp-wrap", "cpt-wrap"]):
                    parent.replace_with(timeline_soup)
                else:
                    table.replace_with(timeline_soup)

    # 3h. Convert accordion meta & description paragraphs
    convert_accordion_meta_and_desc(soup, is_en=is_en)

    # 3i. Inject switcher script if not already present
    has_switcher_script = "window.selectDifficulty =" in str(soup)
    if not has_switcher_script:
        body_close = soup.body
        if body_close:
            override_script = """
<script>
// Unified course switcher override for rebranding compatibility
(function() {
  const switcher = function(lv, btn) {
    document.querySelectorAll('.course-btn').forEach(b => {
      b.classList.remove('active');
    });
    if (btn) {
      btn.classList.add('active');
    } else {
      const targetBtn = document.querySelector('.course-btn.' + lv) || document.querySelector('.course-btn[onclick*="' + lv + '"]');
      if (targetBtn) targetBtn.classList.add('active');
    }
    document.querySelectorAll('.course-panel, .panel').forEach(p => {
      p.classList.remove('active');
    });
    const panel = document.getElementById('panel-' + lv) || 
                  document.getElementById('course-' + lv) || 
                  document.getElementById(lv) ||
                  document.querySelector('.course-panel.' + lv) ||
                  document.querySelector('.panel.' + lv);
    if (panel) {
      panel.classList.add('active');
      setTimeout(() => {
        panel.querySelectorAll('.diff-bar-fill').forEach(b => {
          const w = b.style.width;
          if (w && w !== '0%') {
            b.style.width = '0%';
            requestAnimationFrame(() => requestAnimationFrame(() => { b.style.width = w; }));
          }
        });
      }, 50);
    }
  };
  window.selectDifficulty = window.switchLevel = window.selectLevel = window.selectCourse = window.selC = switcher;
})();
</script>
"""
            body_close.append(BeautifulSoup(override_script, "html.parser"))

    final_content = str(soup)
    final_content = re.sub(r'\[web:\d+\]', '', final_content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"Successfully upgraded playbook: {file_name}")

def rebrand_landing_logo(file_name):
    file_path = os.path.join(WORKSPACE_DIR, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    header_el = soup.find("header")
    if header_el:
        logo_svg = header_el.find("svg", class_=lambda x: x and "logo-svg" in x)
        if logo_svg:
            new_logo_soup = BeautifulSoup(RIDGE_APEX_LOGO_HTML, "html.parser").svg
            logo_svg.replace_with(new_logo_soup)
            
    for other_svg in soup.find_all("svg", class_=lambda x: x and "logo-svg" in x):
        new_logo_soup = BeautifulSoup(RIDGE_APEX_LOGO_HTML, "html.parser").svg
        other_svg.replace_with(new_logo_soup)
        
    is_en = file_name.startswith("en/")
    head = soup.head
    if head:
        fav_path = "../assets/brand/favicon.svg" if is_en else "assets/brand/favicon.svg"
        icon_tags = head.find_all("link", rel=re.compile(r"^(shortcut )?icon$", re.I))
        for tag in icon_tags:
            tag["href"] = fav_path
            tag["type"] = "image/svg+xml"
            
        og_img_tag = head.find("meta", attrs={"property": "og:image"})
        tw_img_tag = head.find("meta", attrs={"name": "twitter:image"})
        target_img = "../assets/img/brand-og.png" if is_en else "assets/img/brand-og.png"
        
        if og_img_tag:
            og_img_tag["content"] = target_img
        if tw_img_tag:
            tw_img_tag["content"] = target_img
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Rebranded logo for landing page: {file_name}")

def main():
    # 1. Rebrand index.html and en/index.html
    rebrand_landing_logo("index.html")
    rebrand_landing_logo("en/index.html")
    
    # 2. Upgrade all playbooks by scanning workspace directory
    # Find all *-playbook.html in workspace root
    playbooks = [f for f in os.listdir(WORKSPACE_DIR) if f.endswith("-playbook.html") and f != "logo-options.html"]
    
    for file_name in sorted(playbooks):
        # Process KR version
        process_playbook(file_name)
        
        # Process EN version if it exists
        en_file_name = "en/" + file_name
        if os.path.exists(os.path.join(WORKSPACE_DIR, en_file_name)):
            process_playbook(en_file_name)
            
    print("\nAll playbooks and landing pages successfully rebranded and upgraded!")

if __name__ == "__main__":
    main()
