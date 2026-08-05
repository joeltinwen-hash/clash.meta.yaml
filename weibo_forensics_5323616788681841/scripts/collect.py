#!/usr/bin/env python3
import requests, csv, hashlib, os, time, json, re, urllib.parse, subprocess
from pathlib import Path
BASE=Path('weibo_forensics_5323616788681841')
UA_LIST={
 'desktop':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
 'mobile':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Weibo'
}
queries=['5323616788681841','AX9xdpfY','1034:5323616443629696','5323616443629696','R9UnAAqxH','8345249001','最近都在推荐这个余音绕梁竹知了，说是1000块钱以内最好玩的玩具，确实挺好玩的。','最近都在推荐这个余音绕梁竹知了','1000块钱以内最好玩的玩具','余音绕梁竹知了','确实挺好玩的','石头日谈 竹知了','王澎程 竹知了','石头日谈 AX9xdpfY','涉嫌侵权，已经投诉了啊','BV1Yu3T6zEeJ','BV1KD3g6uE6t','2066003943059203398']
platforms={
 'bing':'https://www.bing.com/search?q={q}', 'baidu':'https://www.baidu.com/s?wd={q}', 'sogou':'https://www.sogou.com/web?query={q}', 'so360':'https://www.so.com/s?q={q}',
 'weibo_site':'https://www.bing.com/search?q={q}+site%3Aweibo.com+OR+site%3Am.weibo.cn', 'sina_site':'https://www.bing.com/search?q={q}+site%3Asina.cn',
 'zhihu_site':'https://www.bing.com/search?q={q}+site%3Azhihu.com', 'bilibili_site':'https://www.bing.com/search?q={q}+site%3Abilibili.com',
 'tieba_site':'https://www.bing.com/search?q={q}+site%3Atieba.baidu.com', 'xiaohongshu_site':'https://www.bing.com/search?q={q}+site%3Axiaohongshu.com',
 'douyin_site':'https://www.bing.com/search?q={q}+site%3Adouyin.com', 'toutiao_site':'https://www.bing.com/search?q={q}+site%3Atoutiao.com',
 'qqnews_site':'https://www.bing.com/search?q={q}+site%3Aqq.com', 'wechat_site':'https://www.bing.com/search?q={q}+site%3Amp.weixin.qq.com',
 'shopping':'https://www.bing.com/search?q={q}+%E8%B4%AD%E4%B9%B0+OR+%E5%95%86%E5%93%81', 'bing_images':'https://www.bing.com/images/search?q={q}'
}
core_urls=['https://m.weibo.cn/detail/5323616788681841','https://www.sina.cn/news/detail/5323616788681841.html','https://www.sina.cn/media/8345249001','https://www.sina.cn/news/detail/5318734828801903.html','http://t.cn/AX9xdpfY','https://t.cn/AX9xdpfY','https://video.weibo.com/show?fid=1034:5323616443629696','https://weibo.com/tv/show/1034:5323616443629696','https://www.sina.cn/media/1749821214','https://www.bilibili.com/video/BV1Yu3T6zEeJ','https://www.bilibili.com/video/BV1KD3g6uE6t','https://www.zhihu.com/question/2066003943059203398']
rows=[]; qrows=[]
def save_response(url, method='GET', allow=True, ua='desktop', tag=''):
    ts=time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    safe=re.sub(r'[^A-Za-z0-9_.-]+','_', (tag or urllib.parse.urlparse(url).netloc+urllib.parse.urlparse(url).path)[:120])
    try:
        r=requests.request(method,url,headers={'User-Agent':UA_LIST[ua]},allow_redirects=allow,timeout=25)
        body=r.content if method!='HEAD' else b''
        ext='html' if 'html' in r.headers.get('content-type','') else 'json' if 'json' in r.headers.get('content-type','') else 'bin'
        sub='raw/html' if ext=='html' else 'raw/json' if ext=='json' else 'raw/http'
        path=BASE/sub/f'{ts}_{safe}_{method}_{ua}.{ext}'
        path.write_bytes(body)
        h=hashlib.sha256(body).hexdigest()
        chain=' > '.join([x.url for x in r.history]+[r.url])
        hdr=BASE/'raw/http'/f'{ts}_{safe}_{method}_{ua}_headers.txt'
        hdr.write_text('\n'.join([f'URL: {url}',f'FINAL: {r.url}',f'STATUS: {r.status_code}',f'CHAIN: {chain}','']+[f'{k}: {v}' for k,v in r.headers.items()]),encoding='utf-8')
        rows.append([ts,url,method,ua,r.status_code,chain,r.headers.get('content-type',''),len(body),h,str(path), 'unknown', 'yes/partial'])
        return r, path
    except Exception as e:
        rows.append([ts,url,method,ua,'ERROR',str(e),'',0,'','', 'unknown','no']); return None,None
# core requests variants
for u in core_urls:
  for method in ['GET','HEAD']:
    for allow in [False,True]:
      for ua in ['desktop','mobile']:
        save_response(u,method,allow,ua, 'core_'+u)
# searches
for q in queries:
  for pname,tpl in platforms.items():
    url=tpl.format(q=urllib.parse.quote('"'+q+'"'))
    r,p=save_response(url,'GET',True,'desktop','search_'+pname+'_'+q)
    text=(r.text[:5000] if r is not None else '')
    hits=[]
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text, re.S|re.I):
        title=re.sub('<.*?>',' ',m.group(2)); href=m.group(1)
        if any(x in title+href for x in ['竹知了','532361','AX9xdpfY','R9Un','石头','王澎程','BV1','知乎']): hits.append((title.strip()[:120],href[:200]))
    qrows.append([time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),pname,q,url,'unknown',json.dumps(hits,ensure_ascii=False)[:1000],'' if r is not None and r.status_code<400 else 'blocked/error'])
# archives
arch_urls=[]
for u in core_urls:
    arch_urls += [f'https://web.archive.org/cdx?url={urllib.parse.quote(u,safe="")}&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200', f'https://arquivo.pt/wayback/cdx?url={urllib.parse.quote(u,safe="")}&output=json', f'https://archive.today/{u}']
for u in arch_urls: save_response(u,'GET',True,'desktop','archive_'+u)
# write csvs
with open(BASE/'evidence/evidence.csv','w',newline='',encoding='utf-8') as f: csv.writer(f).writerows([['utc_time','url','method','user_agent','status','redirect_chain','content_type','size','sha256','local_path','login_required','independent_review']]+rows)
with open(BASE/'evidence/query_log.csv','w',newline='',encoding='utf-8') as f: csv.writer(f).writerows([['utc_time','platform','query','url','result_count','key_hits','blocked_reason']]+qrows)
(BASE/'evidence/urls.txt').write_text('\n'.join(core_urls+arch_urls),encoding='utf-8')
# hashes all files except hashes
with open(BASE/'evidence/hashes.sha256','w',encoding='utf-8') as f:
    for p in sorted(BASE.rglob('*')):
        if p.is_file() and p.name!='hashes.sha256':
            f.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p)+'\n')
