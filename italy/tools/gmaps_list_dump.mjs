// Dump all places from a shared Google Maps list (the /maps/placelists/list/<id> page).
// The public getlist API only returns the first 10 items, so this drives headless Chrome
// over the DevTools protocol, scrolls the side panel until everything is loaded, and prints
// the panel text (name / rating / category / your note, one per line).
//
// 1) start Chrome:  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
//       --remote-debugging-port=9333 --user-data-dir=/tmp/gm-prof --window-size=1400,1000 about:blank &
// 2) node tools/gmaps_list_dump.mjs <listId> > list_lines.json
//    listId is the value after 11m2!2s in the resolved short link, e.g. Ma6iPjHlRIG9yxpHlqcVFQ
// 3) kill Chrome. Parse list_lines.json (lines array) into name/rating/category triplets.
const [,, listId, portArg] = process.argv; const port = portArg || 9333;
if(!listId){ console.error('listId required'); process.exit(1); }
const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
let page = targets.find(t => t.type === 'page');
if(!page) page = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method:'PUT'})).json();
const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pending = {}; ws.onmessage = e => { const m = JSON.parse(e.data); if(m.id && pending[m.id]){ pending[m.id](m); delete pending[m.id]; } };
const send = (method, params={}) => new Promise(res => { const i = ++id; pending[i] = res; ws.send(JSON.stringify({id:i, method, params})); });
const evalJs = async expr => (await send('Runtime.evaluate', {expression: expr, awaitPromise: true, returnByValue: true})).result?.result?.value;
const sleep = ms => new Promise(r => setTimeout(r, ms));
await send('Page.enable');
await send('Network.setUserAgentOverride', {userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'});
await send('Page.navigate', {url: `https://www.google.com/maps/placelists/list/${listId}?hl=zh-TW`});
await sleep(6000);
await evalJs(`(()=>{const b=[...document.querySelectorAll('button')].find(x=>/accept|同意|接受|Accetta/i.test(x.textContent)); if(b) b.click();})()`);
await sleep(1500);
const res = await evalJs(`(async()=>{
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  const cands=[...document.querySelectorAll('div')].filter(d=>d.scrollHeight>d.clientHeight+100 && /auto|scroll/.test(getComputedStyle(d).overflowY) && /\\d\\.\\d\\(/.test(d.innerText));
  cands.sort((a,b)=>b.scrollHeight-a.scrollHeight);
  const panel=cands[0]; if(!panel) return JSON.stringify({err:'no panel'});
  let last=-1, same=0, lines=[];
  for(let i=0;i<300;i++){
    panel.scrollTop=panel.scrollHeight; await sleep(600);
    lines=panel.innerText.split('\\n').map(s=>s.trim()).filter(Boolean);
    const n=lines.filter(l=>/^\\d\\.\\d\\(/.test(l)).length;
    if(n===last){ same++; if(same>8) break; } else { same=0; last=n; }
  }
  return JSON.stringify({ratings:last, lines});
})()`);
console.log(res); ws.close();
