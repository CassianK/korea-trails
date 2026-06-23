import json
from scratch.translate_all_playbooks import translate_playbook, load_glossary

glossary = load_glossary()
glossary_str = json.dumps(glossary, ensure_ascii=False, indent=2)

try:
    translate_playbook('deogyusan-playbook.html', glossary_str)
except Exception as e:
    import traceback
    traceback.print_exc()
