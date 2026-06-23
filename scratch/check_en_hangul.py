import glob
import re

def check_hangul_in_en():
    en_files = glob.glob("en/**/*.html", recursive=True) + glob.glob("en/**/*.js", recursive=True)
    hangul_re = re.compile(r'[\uac00-\ud7a3\u3130-\u318f\u1100-\u11ff]')
    found = False
    
    for file_path in en_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove script and style tags to avoid false positives (though there shouldn't be Hangul in there anyway)
        # But wait, we want to scan the whole file. Let's see matches:
        matches = hangul_re.findall(content)
        if matches:
            # Let's show context
            print(f"[{file_path}] Found {len(matches)} Hangul characters:")
            # print unique matches
            print(f"  Unique: {set(matches)}")
            found = True
            
    if not found:
        print("No Hangul characters found in any EN files!")
    else:
        print("Found Hangul characters in EN files. Please review.")

if __name__ == "__main__":
    check_hangul_in_en()
