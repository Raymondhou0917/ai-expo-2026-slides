"""Build only reviewed public files; never serve the repository root."""
from pathlib import Path
import json, shutil, re, html
from urllib.parse import quote
r=Path(__file__).resolve().parents[1]; out=r/'dist'; out.mkdir(exist_ok=True)
cfg=json.loads((r/'site-config.json').read_text()); files=json.loads((r/'public-files.json').read_text()); host=cfg['host']
for rel in files:
    p=r/rel
    if not p.is_file() or p.is_symlink() or '..' in Path(rel).parts or any(x.startswith('.') for x in Path(rel).parts):
        raise ValueError('Unsafe or missing public file: '+rel)
    q=out/rel; q.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,q)
urls=[]
for rel in cfg['pages']:
    p=out/rel; s=p.read_text(); title=html.unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1))
    route='/'+rel; route=route[:-10] if route.endswith('index.html') else route
    url='https://'+host+route; urls.append(url)
    desc=re.search(r'<meta name="description" content="([^"]+)"',s)
    desc=html.unescape(desc.group(1)) if desc else title+'：雷蒙三十公開的教學與設計資源。'
    s=re.sub(r'<link\s+rel="canonical"[^>]*>','',s)
    addition='\n<link rel="canonical" href="'+html.escape(url,quote=True)+'">\n'
    for name,val in [('og:title',title),('og:description',desc),('og:url',url),('og:type','website'),('og:locale','zh_TW')]:
        if not re.search(r'<meta[^>]+property="'+name+'"',s): addition+='<meta property="'+name+'" content="'+html.escape(val,quote=True)+'">\n'
    if not re.search(r'<meta[^>]+property="og:image"',s): addition+='<meta property="og:image" content="https://image.lifehacker.tw/brand/logo-raymond30-rounded-v4.png">\n'
    graph={'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':url,'inLanguage':'zh-TW','publisher':{'@type':'Organization','@id':'https://lifehacker.tw/#organization','name':'雷蒙三十','url':'https://lifehacker.tw/'}}
    addition+='<script type="application/ld+json">'+json.dumps(graph,ensure_ascii=False).replace('</','<\\/')+'</script>\n'
    n=[0]
    def heading(m):
        if ' id=' in m.group(1): return m.group(0)
        n[0]+=1; return '<h'+m.group(1)+' id="section-'+str(n[0])+'">'
    s=re.sub(r'<h([12](?:\s[^>]*)?)>',heading,s)
    p.write_text(s.replace('</head>',addition+'</head>',1))
(out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://'+host+'/sitemap.xml\n')
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(u)+'</loc></url>' for u in urls)+'</urlset>\n')
(out/'404.html').write_text('<!doctype html><html lang="zh-TW"><meta charset="utf-8"><meta name="robots" content="noindex"><title>找不到頁面</title><h1>找不到頁面</h1><p><a href="/">回到首頁</a></p></html>')
(out/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\nhttps://:project.pages.dev/*\n  X-Robots-Tag: noindex\nhttps://:deployment.:project.pages.dev/*\n  X-Robots-Tag: noindex\n/*.md\n  Content-Type: text/plain; charset=utf-8\n')
(out/'_redirects').write_text('/ /notion-quiz/ 302\n' if cfg['redirectRoot'] else '')
expected=set(files)|{'robots.txt','sitemap.xml','404.html','_headers','_redirects'}
extra={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}-expected
if extra: raise ValueError('Unexpected output files: '+str(extra))
print('Public build:',len(expected),'files;',len(urls),'indexable pages')
