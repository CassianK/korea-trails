import os
import re
import json
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
        }).encode('utf-8')
    )
    
    with urllib.request.urlopen(req) as res:
        response_data = json.loads(res.read().decode('utf-8'))
        content = response_data['choices'][0]['message']['content']
        return content

def translate_batch(strings, glossary_str):
    prompt = f"""You are an expert translator specializing in outdoor hiking guides.
Translate the following Korean text segments from a hiking playbook for Seoraksan National Park into natural, high-quality English.

Follow these strict rules:
1. Preserve all numbers, units (e.g., km, h, m, 7-1, 1,708m, 1박, 1일차), punctuation, and special symbols exactly.
2. Use official Romanization for names of places, peaks, temples, and routes based on this glossary:
{glossary_str}
For other names, use standard Revised Romanization of Korean (e.g., Heondeulbawi, Sinheungsa, Biseondae).
3. Do not shorten or skip any content. Translate the meaning accurately and professionally.
4. Return the translations as a JSON object where the keys are the original Korean strings and the values are their English translations.
5. Do NOT wrap the JSON in markdown formatting (like ```json ... ```). Output raw JSON only.

Korean strings to translate:
{json.dumps(strings, ensure_ascii=False, indent=2)}"""

    result = call_openrouter(prompt)
    # Clean up markdown if the model included it anyway
    result_clean = result.strip()
    if result_clean.startswith('```'):
        result_clean = re.sub(r'^```(?:json)?\n', '', result_clean)
        result_clean = re.sub(r'\n```$', '', result_clean)
    return json.loads(result_clean.strip())

def main():
    # Load glossary
    glossary = load_glossary()
    glossary_str = json.dumps(glossary, ensure_ascii=False, indent=2)
    
    print("Reading seoraksan-playbook.html...")
    with open('seoraksan-playbook.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    hangul_re = re.compile(r'[가-힣]')
    
    # 1. Extract all unique Korean text segments
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
                
    korean_list = sorted(list(korean_strings))
    print(f"Extracted {len(korean_list)} unique Korean strings to translate.")
    
    # 2. Batch translation using OpenRouter
    translations = {}
    batch_size = 50
    for i in range(0, len(korean_list), batch_size):
        batch = korean_list[i:i+batch_size]
        print(f"Translating batch {i//batch_size + 1}/{(len(korean_list)-1)//batch_size + 1}...")
        try:
            batch_trans = translate_batch(batch, glossary_str)
            translations.update(batch_trans)
        except Exception as e:
            print(f"Error in batch {i//batch_size + 1}: {e}")
            # Retry once
            print("Retrying...")
            batch_trans = translate_batch(batch, glossary_str)
            translations.update(batch_trans)
            
    # 3. Replace in the BeautifulSoup tree
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
                    
    # 4. Perform standard path updates and metadata updates
    # Update lang attribute
    soup.html['lang'] = 'en'
    
    # Toggle language toggle class (KO inactive, EN active)
    lang_toggle = soup.find('div', class_='lang-toggle')
    if lang_toggle:
        ko_btn = lang_toggle.find('button', onclick="changeLanguage('ko')")
        en_btn = lang_toggle.find('button', onclick="changeLanguage('en')")
        if ko_btn and en_btn:
            ko_btn['class'] = 'lang-btn'
            ko_btn['aria-pressed'] = 'false'
            en_btn['class'] = 'lang-btn active'
            en_btn['aria-pressed'] = 'true'
            
    # Update title
    title_tag = soup.find('title')
    if title_tag and title_tag.string == '설악산 등산 플레이북':
        title_tag.string = 'Seoraksan Hiking Playbook'
        
    # Update relative assets paths (prepend ../ to assets/ or _assets/)
    for tag in soup.find_all(True):
        for attr in ['src', 'href', 'poster', 'srcset', 'content']:
            val = tag.get(attr)
            if val and isinstance(val, str):
                if val.startswith('assets/') or val.startswith('_assets/'):
                    tag[attr] = '../' + val
                elif attr == 'srcset':
                    # Handle multiple paths in srcset
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
        if hreflang == 'ko':
            link_tag['href'] = '../' + href
        elif hreflang == 'x-default':
            link_tag['href'] = '../' + href
            
    # Output the translated file
    os.makedirs('en', exist_ok=True)
    with open('en/seoraksan-playbook.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Successfully translated seoraksan-playbook.html to en/seoraksan-playbook.html!")

if __name__ == '__main__':
    main()
