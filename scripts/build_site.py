"""Build the bilingual static report collection. No inference or network access."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import hashlib
import json
import posixpath
import re

import markdown

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://songhonglei.github.io/exp-eval-report'
REPOSITORY = 'https://github.com/Songhonglei/exp-eval-report'
CATEGORIES = {'models': {'zh': '模型', 'en': 'Models'},
              'skills': {'zh': 'Skill', 'en': 'Skills'},
              'open-source': {'zh': '开源项目', 'en': 'Open source'}}


def relative(target, page):
    trailing = target.endswith('/')
    result = posixpath.relpath(target.rstrip('/'), str(Path(page).parent))
    return result + ('/' if trailing else '')


def asset_url(target, page):
    version = hashlib.sha256((ROOT / target).read_bytes()).hexdigest()[:12]
    return relative(target, page) + '?v=' + version


def anchor(url, label, **attrs):
    extra = ''.join(f' {escape(key.rstrip("_"))}="{escape(value, quote=True)}"' for key, value in attrs.items())
    return f'<a href="{escape(url, quote=True)}"{extra}>{escape(label)}</a>'


def page_head(title, description, page, lang, alternate):
    url = BASE + '/' + page.replace('index.html', '')
    other = BASE + '/' + alternate.replace('index.html', '')
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | exp-eval-report</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{'zh-CN' if lang == 'zh' else 'en'}" href="{url}">
<link rel="alternate" hreflang="{'en' if lang == 'zh' else 'zh-CN'}" href="{other}">
<meta property="og:type" content="{'website' if page in ('index.html', 'en/index.html') else 'article'}">
<meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#163b66">
<link rel="stylesheet" href="{asset_url('assets/site.css', page)}">
<script src="{asset_url('assets/site.js', page)}" defer></script>
</head><body id="top">
<a class="skip" href="#main">{'跳到正文' if lang == 'zh' else 'Skip to content'}</a>'''


def header(page, lang, alternate):
    return f'''<header class="site-header">{anchor(relative('index.html' if lang == 'zh' else 'en/index.html', page), 'exp-eval-report', class_='brand')}
<nav aria-label="{'网站导航' if lang == 'zh' else 'Site navigation'}">
{anchor(relative('index.html' if lang == 'zh' else 'en/index.html', page), '报告目录' if lang == 'zh' else 'Reports')}
{anchor(relative(alternate, page), 'English' if lang == 'zh' else '中文', hreflang='en' if lang == 'zh' else 'zh-CN')}
{anchor(REPOSITORY, 'GitHub')}</nav></header>'''


def footer(page, lang):
    return f'''<footer class="site-footer"><span>exp-eval-report</span><span>{'实验条件、证据与结论一并记录' if lang == 'zh' else 'Conditions, evidence, and conclusions kept together'}</span>{anchor('#top', '回到顶部' if lang == 'zh' else 'Back to top')}</footer></body></html>'''


def write_page(page, content):
    target = ROOT / page
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def load_reports():
    reports = []
    for path in sorted((ROOT / 'reports').glob('*/report.json')):
        report = json.loads(path.read_text())
        assert report['id'] == path.parent.name
        assert report['category'] in CATEGORIES
        for lang in ['zh', 'en']:
            assert lang in report['title'] and lang in report['description']
        reports.append(report)
    assert len({report['id'] for report in reports}) == len(reports)
    return reports


def build_portal(reports, lang):
    page = 'index.html' if lang == 'zh' else 'en/index.html'
    alternate = 'en/index.html' if lang == 'zh' else 'index.html'
    title = '模型与工具的实验报告' if lang == 'zh' else 'Experiments with models and tools'
    intro = ('汇集模型、Skill 与开源项目的本地实验、评测和工程记录。每份报告保留测试条件、实际观察与适用范围，提供中英文阅读入口。' if lang == 'zh' else
             'Local experiments, evaluations, and engineering notes on models, skills, and open-source projects. Each report keeps its conditions, observations, and scope together, with Chinese and English editions.')
    body = page_head(title, intro, page, lang, alternate) + header(page, lang, alternate)
    body += f'''<main id="main"><section class="portal-hero"><div><div><h1>{title}</h1><p>{intro}</p></div>
<div class="portal-context"><h2>{'多项目，独立记录' if lang == 'zh' else 'Separate reports for separate projects'}</h2><p>{'上游项目保留各自仓库。这里按报告归档正文、图表与公开证据，并链接 Hugging Face 英文内容。' if lang == 'zh' else 'Upstream projects retain their own repositories. This collection organizes the articles, figures, and public evidence, with links to the English material on Hugging Face.'}</p></div></div></section>
<section class="portal" aria-label="{'报告列表' if lang == 'zh' else 'Report collection'}"><div class="filters"><div class="filter-buttons" role="group" aria-label="{'按类别筛选' if lang == 'zh' else 'Filter by category'}">'''
    for key, label in [('all', '全部' if lang == 'zh' else 'All')] + [(key, value[lang]) for key, value in CATEGORIES.items()]:
        body += f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
    body += f'''</div><label class="search" for="report-search">{'搜索报告' if lang == 'zh' else 'Find a report'}<input id="report-search" type="search" placeholder="{'标题、项目或技术' if lang == 'zh' else 'Title, project, or technology'}" autocomplete="off"></label></div><div id="report-list">'''
    for report in reports:
        base = 'reports/' + report['id'] + '/'
        target = relative(base + lang + '/', page)
        search = ' '.join(list(report['title'].values()) + list(report['description'].values()) + report['topics'])
        body += f'''<article class="report-row" data-report="{report['id']}" data-category="{report['category']}" data-search="{escape(search, quote=True)}">
<a class="report-preview" href="{target}" tabindex="-1" aria-hidden="true"><img src="{relative(base + report['preview'][lang], page)}" alt="" width="230" height="150"></a>
<div><div class="report-meta"><time datetime="{report['experiment_date']}">{report['experiment_date']}</time><span>{CATEGORIES[report['category']][lang]}</span><span>{'中文 / English'}</span></div>
<h2>{anchor(target, report['title'][lang])}</h2><p>{escape(report['description'][lang])}</p><div class="report-links">
{anchor(relative(base+'zh/', page), '中文报告', class_='read')}{anchor(relative(base+'en/', page), 'English report', class_='read')}
{anchor(report['huggingface'], 'Hugging Face（英文）' if lang == 'zh' else 'Hugging Face')}
<span class="topics">{''.join('<span class="topic">'+escape(topic)+'</span>' for topic in report['topics'])}</span></div></div></article>'''
    body += f'''</div><p id="empty-results" class="empty" role="status" hidden>{'目前没有符合筛选条件的报告。可切换类别或清空搜索。' if lang == 'zh' else 'No reports match this selection. Choose another category or clear the search.'}</p>
<div class="portal-note"><p>{'后续报告可按模型、Skill 或开源项目分类加入，每份独立保存来源、正文与证据。' if lang == 'zh' else 'New model, skill, and open-source project reports can be added independently, with their own sources, articles, and evidence.'}</p>{anchor(REPOSITORY+'/blob/main/CONTRIBUTING.md', '新增报告指南' if lang == 'zh' else 'Add a report')}</div></section></main>'''
    if lang == 'zh':
        body += r'''<script>if(/^#section-\d+$/.test(location.hash)){location.replace('reports/orcarouter/zh/'+location.hash)}</script>'''
    write_page(page, body + footer(page, lang))


def build_report(report, lang):
    identifier = report['id']
    page = f'reports/{identifier}/{lang}/index.html'
    alternate = f'reports/{identifier}/{"en" if lang == "zh" else "zh"}/index.html'
    source = ROOT / f'reports/{identifier}/ARTICLE.{"zh-CN" if lang == "zh" else "en"}.md'
    text = source.read_text()
    text = re.sub(r'\A# [^\n]+\n+', '', text, count=1)
    renderer = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'toc_depth': '2'}})
    body = renderer.convert(text)
    toc = renderer.toc
    if identifier == 'orcarouter':
        old_ids = re.findall(r'<h2 id="([^"]+)"', body)
        for i, old in enumerate(old_ids, 1):
            body = body.replace(f'id="{old}"', f'id="section-{i}"', 1)
            toc = toc.replace(f'href="#{old}"', f'href="#section-{i}"')

    def rewrite(match):
        attr, value = match.groups()
        if value.startswith(('#', '/')) or urlsplit(value).scheme:
            return match.group(0)
        return f'{attr}="../{value}"'

    body = re.sub(r'(href|src)="([^"]+)"', rewrite, body)
    body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)"\s*/?></p>',
                  r'<figure class="report-figure"><a href="\2"><img alt="\1" src="\2" loading="lazy"></a></figure>', body)
    body = re.sub(r'(</figure>)\s*<p>(?:<em>)?((?:图\s*\d+|Figure\s+\d+).*?)(?:</em>)?</p>',
                  lambda m: m.group(1).replace('</figure>', '<figcaption>'+m.group(2).removesuffix('</em>')+'</figcaption></figure>'), body)
    hint = '表格可左右滑动' if lang == 'zh' else 'Scroll sideways to view the table'
    body = body.replace('<table>', '<div class="table-wrap" role="region" tabindex="0" data-scroll-hint="'+hint+'" aria-label="'+('数据表；'+hint if lang == 'zh' else 'Data table; '+hint)+'"><table>').replace('</table>', '</table></div>')
    title = report['title'][lang]
    evidence_url = report['evidence'].get('url', '../'+report['evidence']['path'])
    full = page_head(title, report['description'][lang], page, lang, alternate) + header(page, lang, alternate)
    full += f'''<main id="main"><section class="article-hero"><div><p class="breadcrumbs">{anchor(relative('index.html' if lang == 'zh' else 'en/index.html', page), '报告目录' if lang == 'zh' else 'Report collection')}<span>{CATEGORIES[report['category']][lang]}</span><time datetime="{report['experiment_date']}">{report['experiment_date']}</time></p>
<h1>{escape(title)}</h1><p class="summary">{escape(report['description'][lang])}</p><nav class="article-actions" aria-label="{'报告资源' if lang == 'zh' else 'Report resources'}">
{anchor(relative(alternate, page), 'English edition' if lang == 'zh' else '中文版本')}
{anchor(report['huggingface'], 'Hugging Face 英文内容' if lang == 'zh' else 'Read on Hugging Face')}
{anchor('../'+source.name, 'Markdown 正文' if lang == 'zh' else 'Markdown source')}
{anchor(evidence_url, '公开证据' if lang == 'zh' else 'Public evidence')}
</nav></div></section><div class="article-layout"><aside><details class="tocbox"><summary>{'本页目录' if lang == 'zh' else 'On this page'}</summary><nav aria-label="{'文章目录' if lang == 'zh' else 'Article contents'}">{toc}</nav></details></aside><article>{body}
<nav class="article-footer" aria-label="{'继续阅读' if lang == 'zh' else 'Continue reading'}">{anchor(relative('index.html' if lang == 'zh' else 'en/index.html', page), '返回全部报告' if lang == 'zh' else 'All reports')}{anchor(report['huggingface'], 'Hugging Face')}{anchor(REPOSITORY+'/tree/main/reports/'+identifier, 'GitHub')}</nav></article></div></main>'''
    write_page(page, full + footer(page, lang))


def report_readme(report):
    p = ROOT / 'reports' / report['id'] / 'README.md'
    p.write_text(f'''# {report['title']['en']}

{report['description']['zh']}

{report['description']['en']}

| Language | GitHub Pages | Markdown |
|---|---|---|
| 中文 | [阅读报告]({BASE}/reports/{report['id']}/zh/) | [中文正文](ARTICLE.zh-CN.md) |
| English | [Read report]({BASE}/reports/{report['id']}/en/) | [English article](ARTICLE.en.md) |

[English material on Hugging Face]({report['huggingface']})

Experiment date: {report['experiment_date']}. {report['evidence']['description']['en']}

Metadata: [report.json](report.json). Reports retain their original measurement scope and limitations. Publication changes do not represent new model experiments.
''')


def main():
    reports = load_reports()
    for lang in ['zh', 'en']:
        build_portal(reports, lang)
        for report in reports:
            build_report(report, lang)
    for report in reports:
        report_readme(report)
    (ROOT / 'reports.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2)+'\n')
    (ROOT / '.nojekyll').touch()
    print(f'Built 2 portal pages and {len(reports) * 2} report pages.')


if __name__ == '__main__':
    main()
