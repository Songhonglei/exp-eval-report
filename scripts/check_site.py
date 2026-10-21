"""Check local report pages, assets, anchors, registry, and aggregate counts."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []; self.ids = []; self.h1 = 0; self.lang = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if 'id' in a: self.ids.append(a['id'])
        if 'href' in a: self.links.append(a['href'])
        if 'src' in a: self.links.append(a['src'])


def main():
    errors = []
    pages = {p.resolve(): Page(p.read_text()) for p in ROOT.rglob('*.html')}
    for path, page in pages.items():
        if page.h1 != 1: errors.append(f'{path.relative_to(ROOT)}: expected one H1')
        if len(page.ids) != len(set(page.ids)): errors.append(f'{path.relative_to(ROOT)}: duplicate anchor')
        if page.lang not in ('zh-CN', 'en'): errors.append(f'{path.relative_to(ROOT)}: missing language')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc: continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir(): target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(ROOT)}: missing {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {link}')
    registry = json.loads((ROOT/'reports.json').read_text())
    assert {r['id'] for r in registry} >= {'orcarouter', 'qwen-image-2-1'}
    assert len([p for p in ROOT.glob('reports/*/report.json')]) == len(registry)
    for report in registry:
        directory = ROOT/'reports'/report['id']
        assert json.loads((directory/'report.json').read_text()) == report
        for lang in report['languages']:
            assert (ROOT/f'reports/{report["id"]}/{lang}/index.html').is_file()
            assert (directory/report['preview'][lang]).is_file()
        assert (directory/report['evidence']['path']).exists()
        assert report['huggingface'].startswith('https://huggingface.co/')
    orca = ROOT/'reports/orcarouter/data'
    rows = {p.name: list(csv.DictReader(p.open())) for p in orca.glob('*.csv')}
    assert sum(len(v) for v in rows.values()) == 14
    assert sum(int(r['requests']) for r in rows['request_counts.csv']) == 160
    qwen = list(csv.DictReader((ROOT/'reports/qwen-image-2-1/evidence/task-summary.csv').open()))
    assert len(qwen) == 25
    for p in ROOT.rglob('*'):
        if '.git' in p.parts or '__pycache__' in p.parts or not p.is_file(): continue
        if p.suffix in {'.html', '.json', '.md', '.csv', '.css', '.js', '.svg'}:
            s = p.read_text()
            if p.suffix == '.md':
                # Markdown sources and evidence indexes are also public entry points.
                for link in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', s):
                    url = urlsplit(link)
                    if url.scheme or url.netloc or not url.path: continue
                    if not (p.parent/unquote(url.path)).exists():
                        errors.append(f'{p.relative_to(ROOT)}: missing Markdown target {link}')
            if '/Users/' in s: errors.append(f'{p.relative_to(ROOT)}: personal absolute path')
            if p.suffix == '.html' and 'https://songhonglei.github.io/orcarouter-local-eval/' in s:
                errors.append(f'{p.relative_to(ROOT)}: outdated Pages URL')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} HTML pages; local HTML/Markdown links and anchors; registry matches manifests and assets; 14 OrcaRouter summary rows; 25 Qwen Image tasks; public-text path checks.')


if __name__ == '__main__': main()
