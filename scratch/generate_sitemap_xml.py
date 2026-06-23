import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

# Base URL
BASE_URL = "https://trinos-strategy.github.io/korea-trails"

# Playbook names
mountains = [
    "bukhansan", "chiaksan", "deogyusan", "dobongsan", "duryunsan", "gayasan",
    "gyeryongsan", "hallasan", "jirisan", "juwangsan", "minjusan", "mudeungsan",
    "myeongseongsan", "naejangsan", "odaesan", "seoraksan", "sikjangsan", "sobaeksan",
    "soyosan", "taebaeksan", "unaksan", "wolchulsan", "woraksan", "xueshan",
    "yangmingshan", "yushan"
]

# Pages list
pages = [
    ("index.html", "en/index.html", 1.0),
    ("sitemap.html", "en/sitemap.html", 0.8),
]

for m in mountains:
    pages.append((f"{m}-playbook.html", f"en/{m}-playbook.html", 0.8))

# Build XML
urlset = ET.Element("urlset", {
    "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xmlns:xhtml": "http://www.w3.org/1999/xhtml"
})

today = datetime.date.today().isoformat()

for kr_page, en_page, priority in pages:
    # KR url entry
    url_kr = ET.SubElement(urlset, "url")
    loc_kr = ET.SubElement(url_kr, "loc")
    loc_kr.text = f"{BASE_URL}/{kr_page}"
    
    ET.SubElement(url_kr, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "ko",
        "href": f"{BASE_URL}/{kr_page}"
    })
    ET.SubElement(url_kr, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "en",
        "href": f"{BASE_URL}/{en_page}"
    })
    ET.SubElement(url_kr, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "x-default",
        "href": f"{BASE_URL}/{kr_page}"
    })
    
    lastmod_kr = ET.SubElement(url_kr, "lastmod")
    lastmod_kr.text = today
    changefreq_kr = ET.SubElement(url_kr, "changefreq")
    changefreq_kr.text = "weekly"
    priority_kr = ET.SubElement(url_kr, "priority")
    priority_kr.text = f"{priority:.1f}"

    # EN url entry
    url_en = ET.SubElement(urlset, "url")
    loc_en = ET.SubElement(url_en, "loc")
    loc_en.text = f"{BASE_URL}/{en_page}"
    
    ET.SubElement(url_en, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "ko",
        "href": f"{BASE_URL}/{kr_page}"
    })
    ET.SubElement(url_en, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "en",
        "href": f"{BASE_URL}/{en_page}"
    })
    ET.SubElement(url_en, "xhtml:link", {
        "rel": "alternate",
        "hreflang": "x-default",
        "href": f"{BASE_URL}/{kr_page}"
    })
    
    lastmod_en = ET.SubElement(url_en, "lastmod")
    lastmod_en.text = today
    changefreq_en = ET.SubElement(url_en, "changefreq")
    changefreq_en.text = "weekly"
    priority_en = ET.SubElement(url_en, "priority")
    priority_en.text = f"{priority:.1f}"

# Pretty print XML
xml_str = ET.tostring(urlset, encoding="utf-8")
parsed = minidom.parseString(xml_str)
pretty_xml = parsed.toprettyxml(indent="  ")

# Write to sitemap.xml
with open("/Users/mac/korea-trails/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print("Generated sitemap.xml successfully!")
