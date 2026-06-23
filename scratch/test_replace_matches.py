import re

with open('seoraksan-playbook.html', 'r', encoding='utf-8') as f:
    orig = f.read()

with open('scratch/translate_seoraksan.py', 'r', encoding='utf-8') as f:
    script = f.read()

# We can parse the file line-by-line or find all html.replace calls.
# Let's find all occurrences of: html = html.replace(...)
# We can use a regex that matches multi-line arguments.
matches = re.finditer(r'html\s*=\s*html\.replace\(\s*(["\'\'\'][\s\S]*?["\'\'\'])\s*,\s*(["\'\'\'][\s\S]*?["\'\'\'])\s*\)', script)

failed = 0
passed = 0
for idx, m in enumerate(matches):
    old_raw = m.group(1)
    new_raw = m.group(2)
    try:
        # Use eval to handle escape characters and multi-line quotes
        old_val = eval(old_raw)
        if old_val in orig:
            passed += 1
        else:
            print(f"[{idx}] FAILED to find in seoraksan-playbook.html:")
            print(f"--- START OLD ---\n{old_val}\n--- END OLD ---")
            failed += 1
    except Exception as e:
        print(f"[{idx}] Error evaluating old string {old_raw[:50]}: {e}")

print(f"Total: {passed} passed, {failed} failed")
