import json,re,math,os,time,urllib.request
from PIL import Image, ImageDraw, ImageFont
UA={'User-Agent':'TravelGuideBuilder/1.0 (personal offline travel guide; see repo README)'}
G=json.loads(re.search(r'window\.GUIDE = (.*);\s*$',open('data.js').read(),re.S).group(1))
C=G['coords']; S=G['spots']
W,Hh=1400,1000; TILE=256
def ll2px(lat,lon,z): n=2**z; x=(lon+180)/360*n*TILE; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n*TILE; return x,y
def dist(a,b):
    R=6371; p1,p2=math.radians(a[0]),math.radians(b[0]); dp=p2-p1; dl=math.radians(b[1]-a[1]); h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2; return 2*R*math.asin(math.sqrt(h))
cache={}
def tile(z,x,y):
    fn=f'.tiles/{z}_{x}_{y}.png'
    os.makedirs(os.path.dirname(fn),exist_ok=True)
    if not os.path.exists(fn):
        u=f'https://{"abc"[(x+y)%3]}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png'
        for a in range(3):
            try: open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()); break
            except Exception as e: time.sleep(2)
        time.sleep(0.25)
    return Image.open(fn).convert('RGB')
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
fontS=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',20)
fontA=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
def render(markers,out):
    lats=[m['ll'][0] for m in markers]; lons=[m['ll'][1] for m in markers]
    clat,clon=(min(lats)+max(lats))/2,(min(lons)+max(lons))/2
    def fitz(ms):
        la=[m['ll'][0] for m in ms]; lo=[m['ll'][1] for m in ms]
        for z in range(16,11,-1):
            xs=[ll2px(a,b,z) for a,b in zip(la,lo)]
            if max(x for x,_ in xs)-min(x for x,_ in xs)<W-200 and max(y for _,y in xs)-min(y for _,y in xs)<Hh-200: return z
        return 12
    spots_=[m for m in markers if m['kind']=='spot'] or markers
    sc=(sum(m['ll'][0] for m in spots_)/len(spots_), sum(m['ll'][1] for m in spots_)/len(spots_))
    while fitz(markers)<14 and any(m['kind']!='spot' for m in markers):
        far=max((m for m in markers if m['kind']!='spot'), key=lambda m:dist(m['ll'],sc)); markers.remove(far)
    z=fitz(markers)
    if len(markers)==1: z=15
    lats=[m['ll'][0] for m in markers]; lons=[m['ll'][1] for m in markers]
    clat,clon=(min(lats)+max(lats))/2,(min(lons)+max(lons))/2
    cx,cy=ll2px(clat,clon,z); x0,y0=cx-W/2,cy-Hh/2
    img=Image.new('RGB',(W,Hh),(240,240,240))
    for tx in range(int(x0//TILE),int((x0+W)//TILE)+1):
        for ty in range(int(y0//TILE),int((y0+Hh)//TILE)+1):
            try: img.paste(tile(z,tx,ty),(int(tx*TILE-x0),int(ty*TILE-y0)))
            except Exception as e: pass
    d=ImageDraw.Draw(img)
    col={'spot':(138,59,42),'eat':(217,119,6),'store':(34,139,84),'hotel':(30,90,180)}
    # draw
    for m in markers:
        x,y=ll2px(*m['ll'],z); x-=x0; y-=y0; r=21
        d.ellipse([x-r,y-r,x+r,y+r],fill=col[m['kind']],outline='white',width=3)
        tw=d.textlength(m['label'],font=font if len(m['label'])<3 else fontS)
        d.text((x-tw/2,y-15),m['label'],fill='white',font=font if len(m['label'])<3 else fontS)
    d.rectangle([0,Hh-26,W,Hh],fill=(255,255,255)); d.text((8,Hh-24),'© OpenStreetMap contributors · tiles OSM France',fill=(90,90,90),font=fontA)
    img.save(out,'JPEG',quality=80,optimize=True); return {'z':z,'x0':x0,'y0':y0,'w':W,'h':Hh}
result={}
for day in G['days']:
    spots=[i for i in day['spots'] if not S[i].get('kind')]
    eats=[i for i in day['spots'] if S[i].get('kind')=='eat']
    if not eats: eats=[i for i,sp in S.items() if sp.get('kind')=='eat' and sp['city']==day['city']]
    storeKeys=set(G.get('storeKeys',[]))
    hotel=(day.get('plan') or {}).get('hotel')
    pts=[]
    for n,i in enumerate(spots,1):
        if i in C: pts.append({'kind':'spot','label':str(n),'name':S[i]['name'],'id':i,'ll':C[i]})
    letters='abcdefghijklmnopqrstuvwxyz'; li=0
    for e in eats:
        for k,h in enumerate(S[e]['highlights']):
            key=f'{e}_{k}'
            if key in C: pts.append({'kind':'store' if key in storeKeys else 'eat','label':letters[li%26],'name':h[0],'id':key,'ll':C[key]}); li+=1
    for st in G.get('stores',[]):
        if st['city']==day['city']: pts.append({'kind':'store','label':letters[li%26],'name':st['name'],'id':'store','ll':st['ll']}); li+=1
    if hotel and hotel['id'] in C: pts.append({'kind':'hotel','label':'H','name':hotel['name'],'id':hotel['id'],'ll':C[hotel['id']]})
    if not pts: continue
    # cluster (single-link, 8 km)
    clusters=[]
    for p in pts:
        for c in clusters:
            if any(dist(p['ll'],q['ll'])<8 for q in c): c.append(p); break
        else: clusters.append([p])
    clusters=[c for c in clusters if len(c)>=2 or any(p['kind']=='spot' for p in c)]
    clusters.sort(key=lambda c:-sum(p['kind']=='spot' for p in c))
    maps=[]
    for n,c in enumerate(clusters[:2]):
        fn=f"img/maps/{day['date'].replace('/','-')}_{n}.jpg"
        geo=render(c,fn)
        maps.append({'file':fn.replace('img/',''),'geo':geo,'markers':[{k:v for k,v in p.items() if k!='ll'} for p in c]})
        print(day['date'],fn,'z',geo['z'],len(c),'markers')
    result[day['date']]=maps
json.dump(result,open('maps.json','w'),ensure_ascii=False,indent=1)
