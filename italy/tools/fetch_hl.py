import json, urllib.request, urllib.parse, os, time
UA={'User-Agent':'TravelGuideBuilder/1.0 (personal offline travel guide; see repo README)'}
N=None
M={
'forum':["Via Sacra","Arch of Septimius Severus","Curia Julia","Temple of Saturn","Temple of Caesar","Temple of Vesta","Temple of Antoninus and Faustina","Basilica of Maxentius","Arch of Titus","Column of Phocas"],
'palatine':["Casa Romuli","House of Augustus","Domus Augustana","it:Stadio Palatino","Farnese Gardens","Circus Maximus","Palatine Museum"],
'pantheon':["Pantheon, Rome","Roman concrete",N,"Raphael",N],
'trevi':["Trevi Fountain","Aqua Virgo",N],
'colosseum':[N,N,N,N,N,"Arch of Constantine"],
'stpeters':["it:Cupola di San Pietro","Pietà (Michelangelo)","St. Peter's Baldachin",N,"it:Statua di San Pietro (Arnolfo di Cambio)","Chair of Saint Peter","Tomb of Pope Alexander VII",N],
'vatican_museums':["Laocoön and His Sons","Belvedere Torso","it:Sala Rotonda (Musei Vaticani)","Gallery of Maps","The School of Athens","Sistine Chapel","Vatican Pinacoteca","Bramante Staircase"],
'sistine':["Sistine Chapel ceiling","The Creation of Adam","Libyan Sibyl","The Last Judgment (Michelangelo)","Delivery of the Keys",N],
'castel':["Ponte Sant'Angelo",N,N,"Passetto di Borgo","Castel Sant'Angelo"],
'sansevero':["Veiled Christ","it:Pudicizia (Corradini)","it:Disinganno (Queirolo)",N,"it:Macchine anatomiche",N],
'napoli_sott':[N,N,N,N,N,"it:Teatro romano di Napoli"],
'pompeii':["Temple of Jupiter (Pompeii)","Temple of Apollo (Pompeii)","Stabian Baths","House of the Faun","House of the Vettii","Lupanar (Pompeii)","Via dell'Abbondanza","Amphitheatre of Pompeii","Garden of the Fugitives","Villa of the Mysteries"],
'orvieto_duomo':["Orvieto Cathedral","Miracle of Bolsena","it:Cappella di San Brizio",N,N],
'pozzo':["Pozzo di San Patrizio",N,N],
'orvieto_under':[N,N,N,N],
'civita':["Civita di Bagnoregio","it:Porta Santa Maria (Civita di Bagnoregio)","it:Chiesa di San Donato (Civita di Bagnoregio)","it:Valle dei Calanchi",N,N],
'campo':["Piazza del Campo","Palazzo Pubblico","Fonte Gaia","Palio di Siena","Contrade of Siena"],
'mangia':["Torre del Mangia",N,N,"it:Cappella di Piazza"],
'siena_duomo':["it:Pavimento del Duomo di Siena","Siena Cathedral Pulpit","Piccolomini Library","Piccolomini Altarpiece","it:San Giovanni Battista (Donatello Siena)",N,N,"it:Facciatone"],
'riomaggiore':[N,N,"it:Chiesa di San Giovanni Battista (Riomaggiore)","it:Castello di Riomaggiore","Via dell'Amore"],
'manarola':["Manarola",N,N,"it:Chiesa di San Lorenzo (Manarola)","Sciacchetrà"],
'corniglia':[N,N,N,"it:Chiesa di San Pietro (Corniglia)"],
'vernazza':["Vernazza","it:Castello Doria (Vernazza)","it:Chiesa di Santa Margherita d'Antiochia (Vernazza)",N,N],
'monterosso':["Monterosso al Mare","it:Il Gigante (Monterosso al Mare)","it:Chiesa di San Giovanni Battista (Monterosso al Mare)","it:Convento dei Cappuccini (Monterosso al Mare)",N],
'flo_duomo':["it:Cupola del Brunelleschi",N,N,"Florence Cathedral","Giotto's Campanile","Gates of Paradise",N,"Museo dell'Opera del Duomo (Florence)"],
'uffizi':["Ognissanti Madonna","Portraits of the Duke and Duchess of Urbino","The Birth of Venus","Annunciation (Leonardo)","Doni Tondo","Madonna of the Goldfinch","Venus of Urbino","Medusa (Caravaggio)","Tribuna of the Uffizi",N],
'santacroce':["it:Tomba di Michelangelo","it:Tomba di Galileo Galilei","it:Cenotafio di Dante Alighieri","it:Tomba di Niccolò Machiavelli","Bardi Chapel","Pazzi Chapel","Crucifix (Cimabue, Santa Croce)","Cavalcanti Annunciation",N],
'piazzale':["Piazzale Michelangelo",N,"San Miniato al Monte","it:Giardino delle rose (Firenze)"],
'accademia':["David (Michelangelo)","Awakening Slave","Saint Matthew (Michelangelo)","Palestrina Pietà","The Rape of the Sabine Women (Giambologna)",N,N],
'pontevecchio':[N,"Vasari Corridor","Benvenuto Cellini",N,N],
'burano':["Burano",N,"it:Chiesa di San Martino (Burano)","it:Museo del merletto",N,"it:Bussolà"],
'sangiorgio':["San Giorgio Maggiore, Venice",N,"it:Ultima Cena (Tintoretto San Giorgio)","it:Raccolta della manna (Tintoretto)",N],
'sanmarco':["St Mark's Basilica","Pala d'Oro",N,"Horses of Saint Mark","Portrait of the Four Tetrarchs",N,N,N],
'ducale':["Porta della Carta","it:Scala d'Oro","Paradise (Tintoretto)",N,"it:Bocca di leone",N,N,"Bridge of Sighs",N],
'correr':[N,"Daedalus and Icarus (Canova)","View of Venice (Jacopo de' Barbari)","Two Venetian Ladies","Biblioteca Marciana"],
'piazza_sanmarco':["St Mark's Campanile","St Mark's Clocktower","Caffè Florian","it:Colonne di San Marco e San Todaro","Acqua alta",N],
'lastsupper':["The Last Supper (Leonardo)",N,N,N,N,"it:Crocifissione (Montorfano)","Santa Maria delle Grazie (Milan)"],
'milan_duomo':["Madonnina",N,"it:San Bartolomeo scorticato","it:Santo Chiodo (Milano)",N,"it:Battistero di San Giovanni alle Fonti",N],
'galleria_milan':[N,"Galleria Vittorio Emanuele II",N,"Giuseppe Mengoni",N],
}
# group by language
want={}  # (lang,title) -> [(spot,i)]
for sp,lst in M.items():
    for i,t in enumerate(lst):
        if not t: continue
        lang='en'
        if t.startswith('it:'): lang='it'; t=t[3:]
        want.setdefault((lang,t),[]).append((sp,i))
def api(lang,titles):
    q=urllib.parse.urlencode({'action':'query','prop':'pageimages','piprop':'thumbnail','pithumbsize':'640','titles':'|'.join(titles),'format':'json','redirects':1})
    return json.load(urllib.request.urlopen(urllib.request.Request(f'https://{lang}.wikipedia.org/w/api.php?'+q,headers=UA),timeout=30))
res={}
for lang in ('en','it'):
    ts=[t for (l,t) in want if l==lang]
    for i in range(0,len(ts),40):
        chunk=ts[i:i+40]; d=api(lang,chunk)
        mp={}
        for n in d['query'].get('normalized',[]): mp[n['to']]=n['from']
        for r in d['query'].get('redirects',[]): mp[r['to']]=mp.get(r['from'],r['from'])
        for pg in d['query']['pages'].values():
            orig=mp.get(pg['title'],pg['title'])
            th=pg.get('thumbnail',{}).get('source')
            if th: res[(lang,orig)]=(th,pg['title'])
        time.sleep(2)
out={}; miss=[]
existing=json.load(open('img/h/credits.json')) if os.path.exists('img/h/credits.json') else {}
for key,targets in want.items():
    if key not in res: miss.append(key); continue
    url,title=res[key]
    sp,i=targets[0]; fn=f'img/h/{sp}_{i}.jpg'
    if not os.path.exists(fn):
        try:
            data=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read(); open(fn,'wb').write(data); time.sleep(1.2)
        except Exception as e: print('ERR',key,e); continue
    for sp,i in targets: out[f'{sp}_{i}']={'file':fn,'src':url,'title':title,'lang':key[0]}
json.dump(out,open('img/h/credits.json','w'),ensure_ascii=False,indent=1)
print('got',len(out),'missing',len(miss)); print('\n'.join(f'{l}:{t}' for l,t in miss))
