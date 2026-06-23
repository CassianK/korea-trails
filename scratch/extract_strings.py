import re
from bs4 import BeautifulSoup, NavigableString

with open('seoraksan-playbook.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

hangul_re = re.compile(r'[가-힣]')

text_segments = set()

# Find in text nodes
for text_node in soup.find_all(text=True):
    if text_node.parent and text_node.parent.name in ['script', 'style']:
        continue
    # Skip comments
    if isinstance(text_node, str) and hangul_re.search(text_node):
        val = text_node.strip()
        if val:
            text_segments.add(val)

# Find in attributes
for tag in soup.find_all(True):
    for attr in ['alt', 'title', 'placeholder', 'aria-label']:
        val = tag.get(attr)
        if val and isinstance(val, str) and hangul_re.search(val):
            text_segments.add(val.strip())

print(f"Found {len(text_segments)} unique Korean text segments.")
for s in sorted(list(text_segments))[:20]:
    print(repr(s))
