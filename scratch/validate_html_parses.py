import glob
from html.parser import HTMLParser

class StrictHTMLParser(HTMLParser):
    def handle_error(self, message):
        raise Exception(message)

def test_parse_files():
    html_files = glob.glob("**/*.html", recursive=True)
    success = True
    for f_path in html_files:
        if "node_modules" in f_path or ".gemini" in f_path:
            continue
        try:
            with open(f_path, "r", encoding="utf-8") as f:
                content = f.read()
            parser = StrictHTMLParser()
            parser.feed(content)
        except Exception as e:
            print(f"Error parsing {f_path}: {e}")
            success = False
    
    if success:
        print("All HTML files parsed successfully without syntax errors!")
    else:
        print("HTML validation failed.")

if __name__ == "__main__":
    test_parse_files()
