"""Check every maintained JavaScript file and inline HTML script with Node."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
class Scripts(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=False);self.active=False;self.parts=[];self.scripts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script':
            attrs=dict(attrs);self.active='src' not in attrs and attrs.get('type','') in ('','text/javascript','module');self.parts=[]
    def handle_data(self,data):
        if self.active:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.active:self.scripts.append(''.join(self.parts));self.active=False

def main():
    count=0
    for path in (ROOT/'templates').rglob('*.js'):
        subprocess.run(['node','--input-type=module','--check'],input=path.read_text(),check=True,capture_output=True,text=True);count+=1
    with tempfile.TemporaryDirectory(prefix='reference-js-') as directory:
        for html in (ROOT/'templates').rglob('*.html'):
            parser=Scripts();parser.feed(html.read_text())
            for i,script in enumerate(parser.scripts):
                file=Path(directory)/f'inline-{count}.js';file.write_text(script)
                r=subprocess.run(['node','--check',str(file)],capture_output=True,text=True)
                assert r.returncode==0,(str(html.relative_to(ROOT)),i,r.stderr);count+=1
    font=ROOT/'templates/html/assets/fonts/pretendard/PretendardVariable.woff2'
    assert hashlib.sha256(font.read_bytes()).hexdigest()=='9599f12fd42fc0bce1cd50b47a0c022e108d7aa64dd0d1bb0ed44f3282d900b4'
    print(f'PASS {count} JavaScript sources / inline scripts; official font hash')
if __name__=='__main__':main()
