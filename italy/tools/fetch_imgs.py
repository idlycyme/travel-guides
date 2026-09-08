import json, urllib.request, urllib.parse, os, time
UA={'User-Agent':'TravelGuideBuilder/1.0 (personal offline travel guide; see repo README)'}
titles={
 'colosseum':'Colosseum','forum':'Roman Forum','palatine':'Palatine Hill',
 'stpeters':"St. Peter's Basilica",'stpeters_int':"Saint Peter's Baldachin",'vatican_museums':'Gallery of Maps','sistine':'Sistine Chapel ceiling','bramante':'Bramante Staircase',
 'castel':"Castel Sant'Angelo",'ponte_santangelo':"Ponte Sant'Angelo",
 'sansevero':'Cappella Sansevero','veiled_christ':'Veiled Christ','napoli_sott':'Napoli Sotterranea','pompeii':'Pompeii','pompeii_forum':'Forum (Pompeii)',
 'orvieto':'Orvieto','orvieto_duomo':'Orvieto Cathedral','pozzo':'Pozzo di San Patrizio','civita':'Civita di Bagnoregio',
 'campo':'Piazza del Campo','siena_duomo':'Siena Cathedral','mangia':'Torre del Mangia',
 'manarola':'Manarola','vernazza':'Vernazza','riomaggiore':'Riomaggiore','monterosso':'Monterosso al Mare','corniglia':'Corniglia',
 'flo_duomo':'Florence Cathedral','brunelleschi_dome':"Brunelleschi's dome",'uffizi':'Uffizi','venus':'The Birth of Venus','santacroce':'Basilica of Santa Croce, Florence','piazzale':'Piazzale Michelangelo','accademia':"Galleria dell'Accademia",'david':'David (Michelangelo)','pontevecchio':'Ponte Vecchio',
 'burano':'Burano','sangiorgio':'San Giorgio Maggiore, Venice','sanmarco':"St Mark's Basilica",'ducale':"Doge's Palace",'correr':'Museo Correr','piazza_sanmarco':'Piazza San Marco',
 'lastsupper':'The Last Supper (Leonardo)','grazie':'Santa Maria delle Grazie (Milan)','milan_duomo':'Milan Cathedral','galleria_milan':'Galleria Vittorio Emanuele II',
}
def api(ts):
    q=urllib.parse.urlencode({'action':'query','prop':'pageimages','piprop':'original','titles':'|'.join(ts),'format':'json','redirects':1})
    req=urllib.request.Request('https://en.wikipedia.org/w/api.php?'+q,headers=UA)
    return json.load(urllib.request.urlopen(req,timeout=30))
keys=list(titles)
title2key={}
for k in keys: title2key[titles[k]]=k
results={}
for i in range(0,len(keys),25):
    chunk=[titles[k] for k in keys[i:i+25]]
    d=api(chunk)
    # handle redirects/normalization
    mapping={}
    for n in d['query'].get('normalized',[]): mapping[n['to']]=n['from']
    for r in d['query'].get('redirects',[]): mapping[r['to']]=mapping.get(r['from'],r['from'])
    for pg in d['query']['pages'].values():
        orig=mapping.get(pg['title'],pg['title'])
        k=title2key.get(orig)
        if k: results[k]=(pg['title'],pg.get('original',{}).get('source'))
    time.sleep(2)
out=json.load(open('img/credits.json')) if os.path.exists('img/credits.json') else {}
for k in keys:
    if k in out and os.path.exists(out[k]['file']): continue
    t,url=results.get(k,(None,None))
    if not url: print('NOIMG',k); continue
    url=url.split('?')[0]
    ext=os.path.splitext(url)[1].lower()
    if ext not in ('.jpg','.jpeg','.png'): print('SKIP',k,url); continue
    rel=url.split('/wikipedia/commons/')[1]; name=rel.split('/')[-1]
    turl=f'https://upload.wikimedia.org/wikipedia/commons/thumb/{rel}/1400px-{name}'+('.png' if ext=='.png' else '')
    fn=f'img/{k}'+('.png' if ext=='.png' else '.jpg')
    for attempt,u in enumerate([turl,url]):
        try:
            data=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90).read()
            open(fn,'wb').write(data); out[k]={'file':fn,'src':url,'title':t}
            print('OK',k,len(data)//1024,'KB',t); break
        except Exception as e:
            print('retry' if attempt==0 else 'ERR',k,e); time.sleep(3)
    time.sleep(1.5)
json.dump(out,open('img/credits.json','w'),ensure_ascii=False,indent=1)
print('total',len(out))
