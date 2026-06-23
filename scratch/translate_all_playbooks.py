import os
import re
import json
import glob
import time
import urllib.request
from bs4 import BeautifulSoup

def load_glossary():
    with open('_orchestration/glossary.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def call_openrouter(prompt):
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is missing")
        
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        data=json.dumps({
            'model': 'google/gemini-2.5-flash',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.1,
            'response_format': {'type': 'json_object'},
        }).encode('utf-8')
    )
    
    with urllib.request.urlopen(req) as res:
        response_data = json.loads(res.read().decode('utf-8'))
        content = response_data['choices'][0]['message']['content']
        return content

def translate_batch(strings, glossary_str):
    prompt = f"""You are an expert translator specializing in outdoor hiking guides.
Translate the following Korean text segments from a hiking playbook for South Korean or Taiwanese mountains into natural, high-quality English.

Follow these strict rules:
1. Preserve all numbers, units (e.g., km, h, m, 7-1, 1,708m, 1박, 1일차), punctuation, and special symbols exactly.
2. Use official Romanization for names of places, peaks, temples, and routes based on this glossary:
{glossary_str}
For other names, use standard Revised Romanization of Korean (e.g., Heondeulbawi, Sinheungsa, Biseondae).
3. Do not shorten or skip any content. Translate the meaning accurately and professionally.
4. Return the translations as a JSON object where the keys are the original Korean strings and the values are their English translations.
5. Do NOT wrap the JSON in markdown formatting (like ```json ... ```). Output raw JSON only.
6. The translated values in the JSON object must be entirely in English and must NOT contain any Korean (Hangul) characters whatsoever. All place names must be fully Romanized (no Hangul in parentheses).

Korean strings to translate:
{json.dumps(strings, ensure_ascii=False, indent=2)}"""

    result = call_openrouter(prompt)
    result_clean = result.strip()
    if result_clean.startswith('```'):
        result_clean = re.sub(r'^```(?:json)?\n', '', result_clean)
        result_clean = re.sub(r'\n```$', '', result_clean)
    
    try:
        return json.loads(result_clean.strip())
    except json.JSONDecodeError:
        # Fallback: try to extract JSON block using regex
        match = re.search(r'\{[\s\S]*\}', result_clean)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        # Print raw response to stderr/stdout for debugging
        print("Raw result that failed JSON decode:")
        print(repr(result_clean))
        raise

def find_theme_button(soup):
    btn = soup.find(attrs={'data-theme-toggle': True})
    if btn: return btn
    btn = soup.find(attrs={'data-thm': True})
    if btn: return btn
    for class_name in ['theme-btn', 'theme-toggle', 'thm-btn', 'theme-btn-toggle']:
        btn = soup.find('button', class_=class_name)
        if btn: return btn
    for btn in soup.find_all('button'):
        label = btn.get('aria-label', '')
        if '테마' in label or '다크' in label or 'Theme' in label or 'Dark' in label:
            return btn
    return None

def inject_toggle_and_scripts_ko(soup, filename):
    # 1. Inject script if not present
    head = soup.head
    if not head:
        head = soup.new_tag('head')
        soup.insert(0, head)
        
    script_exists = soup.find('script', src=re.compile(r'i18n\.js'))
    if not script_exists:
        new_script = soup.new_tag('script', src='assets/js/i18n.js')
        head.append(new_script)
        
    # 2. Inject hreflang alternate links if not present
    alt_exists = soup.find('link', rel='alternate', hreflang='en')
    if not alt_exists:
        links_html = f"""
<link rel="alternate" hreflang="ko" href="{filename}">
<link rel="alternate" hreflang="en" href="en/{filename}">
<link rel="alternate" hreflang="x-default" href="{filename}">"""
        links_soup = BeautifulSoup(links_html, 'html.parser')
        for link in links_soup.find_all('link'):
            head.append(link)
            
    # 3. Inject language toggle if not present
    toggle_exists = soup.find(class_='lang-toggle')
    if not toggle_exists:
        toggle_html = """
<div class="lang-toggle">
  <button class="lang-btn active" onclick="changeLanguage('ko')" aria-label="한국어" aria-pressed="true">KO</button>
  <button class="lang-btn" onclick="changeLanguage('en')" aria-label="English" aria-pressed="false">EN</button>
</div>"""
        toggle_soup = BeautifulSoup(toggle_html, 'html.parser').div
        
        btn = find_theme_button(soup)
        if btn:
            btn.insert_before(toggle_soup)
        else:
            # Fallback to header class or tag
            for header_class in ['hdr', 'header', 'site-header', 'header-actions', 'header-right', 'logo']:
                container = soup.find(class_=header_class)
                if container:
                    container.append(toggle_soup)
                    break
            else:
                header_tag = soup.find(['header', 'nav'])
                if header_tag:
                    header_tag.append(toggle_soup)
                    
def translate_playbook(filename, glossary_str):
    print(f"\n==========================================")
    print(f"Processing: {filename}")
    print(f"==========================================")
    
    # 1. Read KO file
    with open(filename, 'r', encoding='utf-8') as f:
        ko_html = f.read()
        
    soup = BeautifulSoup(ko_html, 'html.parser')
    
    # Ensure the KO file has toggle and scripts injected
    inject_toggle_and_scripts_ko(soup, filename)
    
    # Save the updated KO file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    # 2. Extract Korean strings from the updated soup
    hangul_re = re.compile(r'[가-힣]')
    korean_strings = set()
    
    # Text nodes
    for node in soup.find_all(string=True):
        if node.parent and node.parent.name in ['script', 'style']:
            continue
        val = node.strip()
        if val and hangul_re.search(val):
            korean_strings.add(val)
            
    # Attribute values
    for tag in soup.find_all(True):
        for attr in ['alt', 'title', 'placeholder', 'aria-label', 'content']:
            val = tag.get(attr)
            if val and isinstance(val, str) and hangul_re.search(val):
                korean_strings.add(val.strip())
                
    # 2.5 Extract Hangul from script contents and onclick attributes
    for script_tag in soup.find_all('script'):
        if script_tag.string:
            matches_single = re.findall(r"'(.*?([가-힣]+).*?)'", script_tag.string)
            for m in matches_single:
                korean_strings.add(m[0])
            matches_double = re.findall(r'"(.*?([가-힣]+).*?)"', script_tag.string)
            for m in matches_double:
                korean_strings.add(m[0])
                
    for tag in soup.find_all(True):
        onclick = tag.get('onclick')
        if onclick and isinstance(onclick, str) and hangul_re.search(onclick):
            matches_single = re.findall(r"'(.*?([가-힣]+).*?)'", onclick)
            for m in matches_single:
                korean_strings.add(m[0])
            matches_double = re.findall(r'"(.*?([가-힣]+).*?)"', onclick)
            for m in matches_double:
                korean_strings.add(m[0])
                
    # 2.6 Extract Hangul from data-credit attributes
    for tag in soup.find_all(True):
        data_credit = tag.get('data-credit')
        if data_credit and isinstance(data_credit, str) and hangul_re.search(data_credit):
            for m in re.findall(r'[가-힣]+(?:\s+[가-힣]+)*', data_credit):
                korean_strings.add(m.strip())
                
    korean_list = sorted(list(korean_strings))
    print(f"Extracted {len(korean_list)} unique Korean strings.")
    
    if not korean_list:
        print(f"No Korean strings found in {filename}, skipping translation.")
        return
        
    # 3. Translate strings in batches
    translations = {}
    batch_size = 20
    for i in range(0, len(korean_list), batch_size):
        batch = korean_list[i:i+batch_size]
        print(f"  Translating batch {i//batch_size + 1}/{(len(korean_list)-1)//batch_size + 1}...")
        try:
            batch_trans = translate_batch(batch, glossary_str)
            translations.update(batch_trans)
        except Exception as e:
            print(f"  Error in batch: {e}. Retrying in 3 seconds...")
            time.sleep(3)
            batch_trans = translate_batch(batch, glossary_str)
            translations.update(batch_trans)
            
    # 4. Replace strings in tree
    # Text nodes
    for node in soup.find_all(string=True):
        if node.parent and node.parent.name in ['script', 'style']:
            continue
        val = node.strip()
        if val in translations:
            node.replace_with(translations[val])
            
    # Attribute values
    for tag in soup.find_all(True):
        for attr in ['alt', 'title', 'placeholder', 'aria-label', 'content']:
            val = tag.get(attr)
            if val:
                val_strip = val.strip()
                if val_strip in translations:
                    tag[attr] = translations[val_strip]
                    
    # Replace Hangul in script tags
    for script_tag in soup.find_all('script'):
        if script_tag.string:
            script_content = script_tag.string
            for k in sorted(translations.keys(), key=len, reverse=True):
                script_content = script_content.replace(f"'{k}'", f"'{translations[k]}'")
                script_content = script_content.replace(f'"{k}"', f'"{translations[k]}"')
                script_content = script_content.replace(k, translations[k])
            script_tag.string.replace_with(script_content)
            
    # Replace Hangul in onclick attributes
    for tag in soup.find_all(True):
        onclick = tag.get('onclick')
        if onclick and isinstance(onclick, str):
            onclick_new = onclick
            for k in sorted(translations.keys(), key=len, reverse=True):
                onclick_new = onclick_new.replace(k, translations[k])
            tag['onclick'] = onclick_new
            
    # Replace Hangul in data-credit attributes
    for tag in soup.find_all(True):
        data_credit = tag.get('data-credit')
        if data_credit and isinstance(data_credit, str):
            dc_new = data_credit
            for k in sorted(translations.keys(), key=len, reverse=True):
                dc_new = dc_new.replace(k, translations[k])
            tag['data-credit'] = dc_new
                    
    # 5. Apply English specific overrides
    soup.html['lang'] = 'en'
    
    # Toggle switcher active class
    lang_toggle = soup.find('div', class_='lang-toggle')
    if lang_toggle:
        ko_btn = lang_toggle.find('button', onclick="changeLanguage('ko')")
        en_btn = lang_toggle.find('button', onclick="changeLanguage('en')")
        if ko_btn and en_btn:
            ko_btn['class'] = 'lang-btn'
            ko_btn['aria-pressed'] = 'false'
            en_btn['class'] = 'lang-btn active'
            en_btn['aria-pressed'] = 'true'
            
    # Update title to English if it contains Korean playbook text
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = title_tag.string.replace('등산 플레이북', 'Hiking Playbook').replace('플레이북', 'Playbook')
        
    # Prepend ../ to local asset paths
    for tag in soup.find_all(True):
        for attr in ['src', 'href', 'poster', 'srcset', 'content']:
            val = tag.get(attr)
            if val and isinstance(val, str):
                if val.startswith('assets/') or val.startswith('_assets/'):
                    tag[attr] = '../' + val
                elif attr == 'srcset':
                    new_parts = []
                    for part in val.split(','):
                        part = part.strip()
                        if part.startswith('assets/') or part.startswith('_assets/'):
                            new_parts.append('../' + part)
                        else:
                            new_parts.append(part)
                    tag[attr] = ', '.join(new_parts)
                    
    # Update SVG use tags link
    for use_tag in soup.find_all('use'):
        href = use_tag.get('href')
        if href and (href.startswith('assets/') or href.startswith('_assets/')):
            use_tag['href'] = '../' + href
            
    # Update alternate link hrefs
    for link_tag in soup.find_all('link', rel='alternate'):
        hreflang = link_tag.get('hreflang')
        href = link_tag.get('href')
        if hreflang == 'ko' and href:
            link_tag['href'] = '../' + href
        elif hreflang == 'x-default' and href:
            link_tag['href'] = '../' + href
            
    # Save the EN file
    en_filename = os.path.join('en', filename)
    with open(en_filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Saved English playbook to: {en_filename}")

def main():
    glossary = load_glossary()
    glossary_str = json.dumps(glossary, ensure_ascii=False, indent=2)
    
    # Find all playbooks EXCEPT Seoraksan (which is already translated)
    playbooks = sorted(glob.glob('*-playbook.html'))
    playbooks = [p for p in playbooks if p != 'seoraksan-playbook.html']
    
    print(f"Found {len(playbooks)} playbooks to translate.")
    
    os.makedirs('en', exist_ok=True)
    
    for playbook in playbooks:
        # Optimization: Skip if file already exists in en/ and contains 0 Hangul
        en_filename = os.path.join('en', playbook)
        if os.path.exists(en_filename):
            with open(en_filename, 'r', encoding='utf-8') as f:
                en_content = f.read()
            if not re.search(r'[가-힣]', en_content):
                print(f"Skipping {playbook} - already translated and verified.")
                continue

        try:
            translate_playbook(playbook, glossary_str)
        except Exception as e:
            print(f"FAILED to translate {playbook}: {e}")
            # Continue to next playbook to avoid stopping the entire pipeline
            continue

if __name__ == '__main__':
    main()
