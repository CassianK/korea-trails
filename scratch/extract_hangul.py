import re

with open('seoraksan-playbook.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

hangul_re = re.compile(r'[가-힣]')

unique_lines = []
for i, l in enumerate(lines):
    if hangul_re.search(l) and not l.strip().startswith('<!--'):
        unique_lines.append((i + 1, l.strip()))

print(f"Found {len(unique_lines)} lines with Hangul.")
for num, content in unique_lines[:100]:
    print(f"{num}: {content}")
