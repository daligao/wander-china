/* Approximate stock shots for now; swap in exact/curated images anytime. */
['changsha','guangzhou','chengdu','beijing','chongqing','hangzhou','harbin','kunming',
 'hohhot','hefei','fuzhou','jinan','guiyang','haikou','changchun','lanzhou','shanghai'
].forEach(c=>{if(CITIES_DATA[c])CITIES_DATA[c].spots.forEach(s=>{s.img='img/'+c+'/'+s.id+'.webp';});});

/* active city — assigned in loadCity() */
let CITY, SP, TM;

function travel(i,j){const t=(TM[i]&&TM[i][j])||(TM[j]&&TM[j][i])||[20,18];
  const m=document.getElementById('prefMode').value;
  if(m==='metro')return t[1]; if(m==='taxi')return t[0]; return Math.min(t[0],t[1]);}

/* life scenes + trip anchors (no fixed location; linked by "nearby", not the matrix) */
const ACT=[
 {id:'breakfast',group:'life',nm:'Breakfast',ic:'🥐',cat:'life',dmin:0.5,pref:'any',meal:'breakfast',price:20,pn:'~¥20 · $3',tip:'Fuel up before the day starts.'},
 {id:'lunch',group:'life',nm:'Lunch',ic:'🍜',cat:'life',dmin:1,pref:'any',meal:'lunch',price:40,pn:'~¥40 · $6',tip:'Eat near where you are; save energy for the afternoon.'},
 {id:'dinner',group:'life',nm:'Dinner',ic:'🍲',cat:'life',dmin:1.5,pref:'any',meal:'dinner',price:60,pn:'~¥60 · $8',tip:'The main local meal — take your time.'},
 {id:'tea',group:'life',nm:'Afternoon tea / boba',ic:'🧋',cat:'life',dmin:0.5,pref:'any',price:20,pn:'~¥20 · $3',tip:'A break to recharge when your feet hurt.'},
 {id:'shopping',group:'life',nm:'Shopping',ic:'🛍️',cat:'life',dmin:2,pref:'any',price:0,pn:'Your call',tip:'Malls / pedestrian streets — browse and snap photos.'},
 {id:'movie',group:'life',nm:'Movie',ic:'🎬',cat:'life',dmin:2.5,pref:'any',price:45,pn:'~¥45 · $6',tip:'Great escape from midday heat or rain.'},
 {id:'ktv',group:'life',nm:'Karaoke (KTV)',ic:'🎤',cat:'life',dmin:2,pref:'night',price:60,pn:'~¥60 · $8',tip:'Classic Chinese night out — sing in a private room.'},
 {id:'nightmarket',group:'life',nm:'Night market / late snacks',ic:'🌃',cat:'life',dmin:1.5,pref:'night',price:50,pn:'~¥50 · $7',tip:'The soul of Chinese nightlife — graze your way through.'},
 {id:'escape',group:'life',nm:'Escape room',ic:'🔦',cat:'life',dmin:2,pref:'any',price:80,pn:'~¥80 · $11',tip:'Book ahead; a local favorite.'},
 {id:'juben',group:'life',nm:'Murder mystery (剧本杀)',ic:'🕵️',cat:'life',dmin:3.5,pref:'any',price:100,pn:'~¥100 · $14',tip:'3–4 hours per game — get a group and reserve.'},
 {id:'show',group:'life',nm:'Live show / gig',ic:'🎫',cat:'life',dmin:2.5,pref:'night',price:150,pn:'Varies',tip:'Theatre / livehouse — book on Damai in advance.'},
 {id:'hotspring',group:'life',nm:'Hot spring',ic:'♨️',cat:'life',dmin:2.5,pref:'night',price:150,pn:'~¥150 · $21',tip:'Deeply relaxing — usually on the city outskirts.'},
 {id:'massage',group:'life',nm:'Massage / foot spa',ic:'💆',cat:'life',dmin:1.5,pref:'night',price:120,pn:'~¥120 · $17',tip:'Cheap and excellent in China — perfect after a long day.'},
 {id:'photo',group:'life',nm:'Photo spot',ic:'📸',cat:'life',dmin:1,pref:'any',price:0,pn:'Free',tip:'Block real time for photos — don\'t rush the shot.'},
 {id:'souvenir',group:'life',nm:'Souvenirs',ic:'🎁',cat:'life',dmin:1,pref:'any',price:100,pn:'Your call',tip:'Buy before you leave; supermarkets beat tourist shops.'},
 {id:'rest',group:'life',nm:'Rest at hotel',ic:'🛌',cat:'life',dmin:1.5,pref:'any',price:0,pn:'—',tip:'Go back and nap when tired — a must with kids or older travelers. Don\'t power through.'},
 {id:'freetime',group:'life',nm:'Free time',ic:'⏳',cat:'life',dmin:1,pref:'any',price:0,pn:'—',tip:'Buffer time — don\'t pack every hour.'},
 {id:'arrive',group:'anchor',nm:'Arrival (airport/station)',ic:'🛬',cat:'life',dmin:0.5,pref:'any',anchor:'start',price:0,pn:'—',tip:'Put this first; add travel time into the city/hotel.'},
 {id:'checkin',group:'anchor',nm:'Hotel check-in',ic:'🏨',cat:'life',dmin:0.5,pref:'any',price:0,pn:'—',tip:'Usually from afternoon; drop bags early and start exploring.'},
 {id:'checkout',group:'anchor',nm:'Hotel check-out',ic:'🧳',cat:'life',dmin:0.5,pref:'any',price:0,pn:'—',tip:'Most hotels check out by 12:00; store bags and keep going.'},
 {id:'depart',group:'anchor',nm:'Departure (to airport/station)',ic:'🛫',cat:'life',dmin:0.5,pref:'any',anchor:'end',price:0,pn:'—',tip:'Put this last; flights arrive 2h early, trains 1h early.'}
];
const NEARBY=10;
function getItem(r){return r.k==='s'?SP[r.i]:ACT[r.i];}
function refKey(r){return r.k+r.i;}
function refDur(r){return r.dur!=null?r.dur:getItem(r).dmin;}

const CAT={landmark:'#e11d48',culture:'#7c3aed',park:'#15803d',mall:'#be185d',kids:'#c2410c',night:'#3730a3',life:'#0e7490',nature:'#166534',history:'#b45309',food:'#db2777',shopping:'#db2777',entertainment:'#7c3aed'};
const CATNM={landmark:'Landmark',culture:'Culture',park:'Park',mall:'Shopping',kids:'Family',night:'Nightlife',life:'Life',nature:'Nature',history:'History',food:'Food',shopping:'Shopping',entertainment:'Fun'};

let days=[[]], curDay=0, dayStarts=['09:00'], filter='all';

/* ---- left wall ---- */
function renderFilters(){
  const cats=['all',...new Set(SP.map(s=>s.cat))];
  document.getElementById('filters').innerHTML=cats.map(c=>
    `<span class="chip ${c===filter?'on':''}" data-c="${c}">${c==='all'?'All':CATNM[c]}</span>`).join('');
  document.querySelectorAll('#filters .chip').forEach(el=>el.onclick=()=>{filter=el.dataset.c;renderFilters();renderWall();});
}
function cardHtml(s,i,kind){
  const dur=s.dmax&&s.dmax!==s.dmin?`${s.dmin}-${s.dmax}h`:`${s.dmin}h`;
  const badges=[`<span class="badge cat" style="background:${CAT[s.cat]}">${CATNM[s.cat]}</span>`,`<span class="badge">${dur}</span>`];
  if(s.pref==='night')badges.push('<span class="badge night">🌙 Night</span>');
  if(s.pref==='day')badges.push('<span class="badge day">☀️ Day</span>');
  if(s.cl)badges.push(`<span class="badge close">🔒 Closed ${s.cl}</span>`);
  if(s.english==='No')badges.push('<span class="badge" style="background:#fef3c7;color:#92400e">🗣️ Chinese only</span>');
  if(s.indoor===true)badges.push('<span class="badge" style="background:#eff6ff;color:#1d4ed8">🏠 Indoor</span>');
  const zoom=kind==='s'?`<button class="nc-zoom" data-detail="${s.id}" draggable="false" title="Details">🔍</button>`:'';
  const img=(kind==='s'&&s.img)?`<img class="nc-img" src="${s.img}" alt="${s.nm}" draggable="false" onerror="this.remove()">`:'';
  const blurb=s.desc||s.tip||'';
  return `<div class="note-card ${kind==='a'?'act':''}" draggable="true" data-kind="${kind}" data-i="${i}">
    ${img}
    <div class="nc-top"><span class="nc-ic">${s.ic}</span><span class="nc-nm">${s.nm}</span>${zoom}</div>
    <div class="nc-meta">${badges.join('')}</div>
    <div class="nc-sub">${blurb}</div>
  </div>`;
}
function renderWall(){
  const wall=document.getElementById('spotWall');
  const spots=SP.map((s,i)=>(filter!=='all'&&s.cat!==filter)?'':cardHtml(s,i,'s')).join('');
  const life=ACT.map((a,i)=>a.group==='life'?cardHtml(a,i,'a'):'').join('');
  const anchor=ACT.map((a,i)=>a.group==='anchor'?cardHtml(a,i,'a'):'').join('');
  wall.innerHTML=spots
    +`<div class="wall-div">🍜 Life scenes (food / fun / shopping / rest)</div>`+life
    +`<div class="wall-div">🛬 Arrival & departure</div>`+anchor;
  document.querySelectorAll('.note-card').forEach(el=>{
    el.addEventListener('dragstart',e=>{
      e.dataTransfer.setData('text/plain',JSON.stringify({from:'wall',kind:el.dataset.kind,i:+el.dataset.i}));
      el.classList.add('dragging');});
    el.addEventListener('dragend',()=>el.classList.remove('dragging'));
  });
  document.querySelectorAll('.nc-zoom').forEach(el=>{
    el.addEventListener('mousedown',e=>e.stopPropagation());
    el.addEventListener('click',e=>{e.stopPropagation();openDetail(el.dataset.detail);});
  });
}

/* ---- day tabs ---- */
const DOW=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function dayDate(i){const v=document.getElementById('startDate').value;if(!v)return null;
  const d=new Date(v);d.setDate(d.getDate()+i);return d;}
function renderTabs(){
  const tabs=document.getElementById('dayTabs');
  let html=days.map((d,i)=>{
    const dt=dayDate(i);const dow=dt?`<span class="dow">${DOW[dt.getDay()]}</span>`:'';
    return `<div class="day-tab ${i===curDay?'on':''}" data-d="${i}">Day ${i+1}${dow}</div>`;
  }).join('');
  html+=`<button class="day-add" id="addDay">＋ Add day</button>`;
  if(days.length>1)html+=`<button class="day-del" id="delDay">Delete day</button>`;
  tabs.innerHTML=html;
  document.querySelectorAll('.day-tab').forEach(el=>el.onclick=()=>{curDay=+el.dataset.d;syncDayStart();renderAll();});
  document.getElementById('addDay').onclick=()=>{days.push([]);dayStarts.push('09:00');curDay=days.length-1;syncDayStart();renderAll();};
  const del=document.getElementById('delDay');if(del)del.onclick=()=>{days.splice(curDay,1);dayStarts.splice(curDay,1);curDay=Math.max(0,curDay-1);syncDayStart();renderAll();};
}
function syncDayStart(){document.getElementById('dayStart').value=dayStarts[curDay];}

/* ---- time math ---- */
function hm(t){const h=Math.floor(t),m=Math.round((t-h)*60);return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;}
function parseHM(s){const[h,m]=s.split(':').map(Number);return h+m/60;}
function computeDay(day){
  let cur=parseHM(dayStarts[curDay]||'09:00');const rows=[];
  day.forEach((ref,k)=>{
    let commute=0,near=false;
    if(k>0){const p=day[k-1];
      if(p.k==='s'&&ref.k==='s')commute=travel(p.i,ref.i)/60;
      else{commute=NEARBY/60;near=true;}
      cur+=commute;}
    const dur=refDur(ref);const arr=cur,leave=cur+dur;cur=leave;
    rows.push({ref,arr,leave,commute,near,dur});
  });
  return rows;
}

/* ---- hard reminders ---- */
function checkDay(rows,dayIdx){
  const flags={};const dt=dayDate(dayIdx);const dow=dt?dt.getDay():null;const seen={};
  const mealWin={breakfast:[6,9.5],lunch:[11,14],dinner:[17,20.5]};
  const mealNm={breakfast:'Breakfast',lunch:'Lunch',dinner:'Dinner'};
  rows.forEach((r,k)=>{
    const s=getItem(r.ref);const f=[];
    if(dow!==null&&s.cl){let closed=false;
      if(s.cl==='Weekdays'&&dow>=1&&dow<=5)closed=true;
      else if(s.cl!=='Weekdays'&&DOW[dow]===s.cl)closed=true;
      if(closed)f.push({level:'d',msg:`closed on ${s.cl==='Weekdays'?'weekdays':s.cl} — can\'t visit this day`});}
    if(s.pref==='night'&&r.leave<18)f.push({level:'w',msg:'a night spot scheduled in daytime — move it past 18:00'});
    if(s.pref==='day'&&r.arr>=19)f.push({level:'w',msg:'a daytime spot pushed to night — experience suffers'});
    if(s.meal&&mealWin[s.meal]){const[a,b]=mealWin[s.meal];
      if(r.arr<a||r.arr>b)f.push({level:'w',msg:`${mealNm[s.meal]} is best ${a}:00–${b}:00, now at ${hm(r.arr)}`});}
    if(r.ref.k==='s'){if(seen[refKey(r.ref)])f.push({level:'w',msg:'this attraction is added twice'});seen[refKey(r.ref)]=1;}
    if(!r.near&&r.commute*60>30)f.push({level:'w',msg:`~${Math.round(r.commute*60)} min from the last stop — a bit far`});
    if(f.length)flags[k]=f;
  });
  return flags;
}

/* ---- right board ---- */
function renderBoard(){
  const day=days[curDay];const rows=computeDay(day);const flags=checkDay(rows,curDay);
  const dz=document.getElementById('dropzone');
  if(!day.length){
    dz.innerHTML=`<div class="dz-empty"><b>🗓️</b>Drag attraction notes here<br>to build Day ${curDay+1}</div>`;
  }else{
    dz.innerHTML=rows.map((r,k)=>{
      const s=getItem(r.ref);const fl=flags[k]||[];
      const flclass=fl.some(x=>x.level==='d')?'flag-danger':fl.length?'flag-warn':'';
      const commuteHtml=k>0?`<div class="commute ${(!r.near&&r.commute*60>30)?'far':''}"><span class="pill">${r.near?'🚶 nearby':'🚇 '+Math.round(r.commute*60)+' min'}</span>${r.near?'walk over':'to next stop'}</div>`:'';
      const flagsHtml=fl.length?`<div class="sb-flags">${fl.map(x=>`<span class="flagline ${x.level}">${x.level==='d'?'🔴':'🟡'} ${x.msg}</span>`).join('')}</div>`:'';
      return commuteHtml+`
      <div class="timeline-item">
        <div class="tl-time"><b>${hm(r.arr)}</b>${hm(r.leave)}</div>
        <div class="tl-dot"><span class="dot" style="background:${CAT[s.cat]};box-shadow:0 0 0 4px ${CAT[s.cat]}22"></span>${k<rows.length-1?'<span class="rail"></span>':''}</div>
        <div class="tl-body">
          <div class="spot-block ${flclass}" draggable="true" data-k="${k}">
            <div class="sb-hd"><span class="sb-ic">${s.ic}</span><span class="sb-nm">${s.nm}</span><span class="sb-x" data-x="${k}">✕</span></div>
            <div class="sb-ctrl">
              <span class="dur-ctrl">Duration
                <button class="dur-btn" data-dur="${k}" data-step="-0.5">−</button><b>${r.dur}h</b>
                <button class="dur-btn" data-dur="${k}" data-step="0.5">＋</button>
              </span>
              <span class="sb-info">${s.pn}</span>
            </div>${flagsHtml}
          </div>
        </div>
      </div>`;
    }).join('');
  }
  bindBlocks();
  const play=rows.reduce((a,r)=>a+r.dur,0);
  const move=rows.reduce((a,r)=>a+r.commute,0);
  const total=play+move;
  document.getElementById('dayStat').innerHTML=
    `${day.length} stops · ${play}h fun + ${move.toFixed(1)}h transit ≈ <b style="color:${total>11?'var(--danger)':'var(--brand-d)'}">${total.toFixed(1)}h</b>`;
  renderAlerts(rows,flags,total);
  renderBudget();
}
function renderBudget(){
  let cost=0;days.forEach(day=>day.forEach(ref=>cost+=(getItem(ref).price||0)));
  document.getElementById('budgetBig').textContent='$'+usd(cost);
  document.getElementById('budgetSmall').textContent=`≈ ¥${cost} · on the ground only (tickets, food, local transit) — no flights or hotels`;
}
function renderAlerts(rows,flags,total){
  const box=document.getElementById('alertList');const list=[];
  if(total>11)list.push({level:'d',msg:`Day ${curDay+1} is packed with ${total.toFixed(1)}h — too much. Split it or drop 1–2 stops.`});
  rows.forEach((r,k)=>{(flags[k]||[]).forEach(f=>list.push({level:f.level,msg:`${getItem(r.ref).nm}: ${f.msg}`}));});
  if(!rows.length){box.innerHTML=`<div class="alert ok">✅ Nothing scheduled yet — drag one in from the left.</div>`;return;}
  if(!list.length){box.innerHTML=`<div class="alert ok">✅ This day looks well-balanced. Ready for a trip sheet!</div>`;return;}
  box.innerHTML=list.map(x=>`<div class="alert ${x.level}">${x.level==='d'?'🔴':'🟡'} ${x.msg}</div>`).join('');
}

/* ---- timeline: delete + reorder ---- */
function bindBlocks(){
  document.querySelectorAll('.sb-x').forEach(el=>el.onclick=e=>{e.stopPropagation();days[curDay].splice(+el.dataset.x,1);renderBoard();});
  document.querySelectorAll('.dur-btn').forEach(el=>el.onclick=e=>{
    e.stopPropagation();const k=+el.dataset.dur;const ref=days[curDay][k];
    const nv=Math.max(0.5,Math.round((refDur(ref)+parseFloat(el.dataset.step))*2)/2);ref.dur=nv;renderBoard();});
  document.querySelectorAll('.spot-block[draggable]').forEach(el=>{
    el.addEventListener('dragstart',e=>{e.dataTransfer.setData('text/plain',JSON.stringify({from:'board',k:+el.dataset.k}));el.classList.add('dragging');});
    el.addEventListener('dragend',()=>el.classList.remove('dragging'));
  });
}
const dz=document.getElementById('dropzone');
dz.addEventListener('dragover',e=>{e.preventDefault();dz.classList.add('over');});
dz.addEventListener('dragleave',()=>dz.classList.remove('over'));
dz.addEventListener('drop',e=>{
  e.preventDefault();dz.classList.remove('over');
  let data;try{data=JSON.parse(e.dataTransfer.getData('text/plain'));}catch(_){return;}
  const items=[...dz.querySelectorAll('.timeline-item')];let pos=days[curDay].length;
  for(let n=0;n<items.length;n++){const rect=items[n].getBoundingClientRect();if(e.clientY<rect.top+rect.height/2){pos=n;break;}}
  if(data.from==='wall'){days[curDay].splice(pos,0,{k:data.kind,i:data.i});}
  else if(data.from==='board'){const [moved]=days[curDay].splice(data.k,1);if(data.k<pos)pos--;days[curDay].splice(pos,0,moved);}
  renderBoard();
});

document.getElementById('dayStart').addEventListener('change',e=>{dayStarts[curDay]=e.target.value;renderBoard();});
document.getElementById('startDate').addEventListener('change',()=>{renderTabs();renderBoard();});
document.getElementById('prefMode').addEventListener('change',renderBoard);
document.getElementById('clearDay').onclick=()=>{days[curDay]=[];renderBoard();};
function renderAll(){renderTabs();renderBoard();}

/* ---- detail modal ---- */
function openDetail(id){
  const s=SP.find(x=>x.id===id);if(!s)return;
  const tags=[];
  if(s.pref==='night')tags.push('🌙 Best at night');else if(s.pref==='day')tags.push('☀️ Daytime');else tags.push('🌗 Day or night');
  if(s.cl)tags.push('🔒 Closed '+s.cl);
  tags.push('⭐ ~'+s.dmin+(s.dmax&&s.dmax!==s.dmin?'-'+s.dmax:'')+'h');
  const c=CAT[s.cat]||'#e11d48';
  const hero=s.img
    ? `<div class="dt-photo-wrap"><img class="dt-photo" src="${s.img}" alt="${s.nm}"
         onerror="this.parentElement.outerHTML='<div class=\\'dt-hero\\' style=\\'background:linear-gradient(135deg,${c},${c}bb)\\'><div class=\\'dt-ic\\'>${s.ic}</div><div class=\\'dt-nm\\'>${s.nm}</div><div class=\\'dt-cat\\'>${CATNM[s.cat]||''}</div></div>'">
       <div class="dt-photo-cap"><div class="n">${s.ic} ${s.nm}</div><div class="c">${CATNM[s.cat]||''}${s.nm_cn?' · '+s.nm_cn:''}</div></div></div>`
    : `<div class="dt-hero" style="background:linear-gradient(135deg,${c},${c}bb)">
         <div class="dt-ic">${s.ic}</div><div class="dt-nm">${s.nm}</div><div class="dt-cat">${CATNM[s.cat]||''}</div></div>`;
  const descHtml=s.desc?`<div class="dt-desc">${s.desc}</div>`:'';
  const engLabel=s.english==='Yes'?'✅ Good (signs, staff, menus in English)':s.english==='Partial'?'⚠️ Partial (some English signage, staff may not speak it)':s.english==='No'?'🔴 Chinese only — bring a translation app or guide':'';
  const engRow=s.english?`<div class="dt-row"><b>🗣️ English</b><span>${engLabel}</span></div>`:'';
  const indoorRow=s.indoor!=null?`<div class="dt-row"><b>${s.indoor?'🏠 Indoors':'🌿 Outdoors'}</b><span>${s.indoor?'Covered — good for rainy days':'Open air — check weather before going'}</span></div>`:'';
  document.getElementById('detailBody').innerHTML=`
    ${hero}
    <div class="dt-body">
      <div class="dt-tags">${tags.map(t=>`<span>${t}</span>`).join('')}</div>
      ${descHtml}
      <div class="dt-row"><b>🕐 Hours</b><span>${s.hr}</span></div>
      <div class="dt-row"><b>🎫 Ticket</b><span>${s.pn}</span></div>
      <div class="dt-row"><b>🚇 Metro / Access</b><span>${s.metro}</span></div>
      ${engRow}
      ${indoorRow}
      ${s.tip?`<div class="dt-tips"><b>💡 Insider tips</b><p>${s.tip}</p></div>`:''}
      <div style="margin-top:14px;text-align:center"><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((s.nm_cn?s.nm_cn+' ':'')+s.nm+' '+CITY.nm)}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;background:#4285f4;color:#fff;border-radius:10px;padding:9px 18px;font-weight:700;font-size:13px;text-decoration:none">📍 Open in Google Maps</a></div>
    </div>`;
  document.getElementById('detailMask').classList.add('show');
  // Local preview only: lazily try a Pexels shot. Off in production (uses local img).
  if(!s.img&&LIVE_PHOTOS){pexelsPhoto(`${CITY.nm} ${s.nm}`).then(u=>{
    if(u){s.img=u; if(document.getElementById('detailMask').classList.contains('show'))openDetail(id);}
  });}
}
function closeDetail(){document.getElementById('detailMask').classList.remove('show');}
document.getElementById('detailClose').onclick=closeDetail;
document.getElementById('detailMask').addEventListener('click',e=>{if(e.target.id==='detailMask')closeDetail();});

/* Extract open/close in decimal hours from hr string like "09:00–17:00 (last entry 16:00)" */
function parseHrTimes(hr){
  if(!hr||hr==='—'||/open all day/i.test(hr))return null;
  const m=hr.match(/(\d{1,2}):(\d{2})[–\-](\d{1,2}):(\d{2})/);
  if(!m)return null;
  const open=+m[1]+ +m[2]/60;
  let close=+m[3]+ +m[4]/60;
  if(close<open)close+=24; // crosses midnight (e.g. 11:00–03:00)
  return{open,close};
}

/* =========================================================
   AI BUILD
   Free tier  = local smart auto-arrange (nearest-neighbor + day split).
   Paid tier  = real AI (personalized route, natural-language brief,
                off/peak flight+hotel pricing) via api-proxy.php.
   The seam is callAI() below — wire the DeepSeek/Claude proxy there.
========================================================= */
function smartBuild(maxDays){
  // 1. Build candidate list — respect active filter, skip spots closed on the relevant days
  const startVal = document.getElementById('startDate').value;
  const baseDate = startVal ? new Date(startVal) : null;

  // Separate spots into day-preferred and night-preferred buckets
  const daySpots = [], nightSpots = [];
  SP.forEach((s, i) => {
    if(filter !== 'all' && s.cat !== filter) return; // respect active filter
    if(s.pref === 'night') nightSpots.push(i);
    else daySpots.push(i); // 'day' and 'both' go to day bucket
  });

  // If filter is too narrow and nothing found, fall back to all
  if(daySpots.length + nightSpots.length === 0) {
    SP.forEach((_, i) => daySpots.push(i));
  }

  // 2. Nearest-neighbor order within each bucket, then combine: day first, night second
  function nnOrder(pool) {
    if(!pool.length) return [];
    // Start from the spot with lowest total average travel to others (most central)
    let startIdx = pool[0];
    let minAvg = 1e9;
    pool.forEach(i => {
      const avg = pool.reduce((s, j) => s + (i !== j ? travel(i, j) : 0), 0) / pool.length;
      if(avg < minAvg) { minAvg = avg; startIdx = i; }
    });
    const ord = [startIdx], used = new Set([startIdx]);
    let cur = startIdx;
    while(ord.length < pool.length) {
      let best = -1, bd = 1e9;
      pool.forEach(j => {
        if(used.has(j)) return;
        const d = travel(cur, j);
        if(d < bd) { bd = d; best = j; }
      });
      if(best === -1) break;
      ord.push(best); used.add(best); cur = best;
    }
    return ord;
  }

  const orderedDay = nnOrder(daySpots);
  const orderedNight = nnOrder(nightSpots);
  const fullOrder = [...orderedDay, ...orderedNight];

  // 3. Pack into days, using midpoint duration for realistic estimates
  const MAX_DAY_H = 9; // allow up to 9h active time per day
  const startHr = parseHM(dayStarts[0] || '09:00');
  const nd = [];
  let d = [], load = 0, prev = null, clockHr = startHr;

  const li = ACT.findIndex(a => a.id === 'lunch');
  const di = ACT.findIndex(a => a.id === 'dinner');

  fullOrder.forEach(i => {
    const s = SP[i];
    // Skip spots closed on the day they'd be scheduled (if date set)
    if(baseDate && s.cl) {
      const dayOffset = nd.length; // which day this spot would land on
      const targetDate = new Date(baseDate);
      targetDate.setDate(targetDate.getDate() + dayOffset);
      const dowName = DOW[targetDate.getDay()]; // 'Mon','Tue',etc
      if(dowName === s.cl || (s.cl === 'Weekdays' && targetDate.getDay() > 0 && targetDate.getDay() < 6)) {
        return; // skip this spot — it's closed that day
      }
    }

    const dur = ((s.dmin + (s.dmax || s.dmin)) / 2); // midpoint duration
    const com = prev == null ? 0 : travel(prev, i) / 60;

    // Skip if we'd arrive within 30min of closing, or before opening
    const hrT = parseHrTimes(s.hr);
    if(hrT){
      const arrival = clockHr + com;
      if(arrival >= hrT.close - 0.5) return; // arriving too late
      if(arrival + dur <= hrT.open) return;   // entire visit before it opens
    }

    if(load + com + dur > MAX_DAY_H && d.length) {
      // Finalize current day: insert lunch and optionally dinner
      if(li >= 0 && d.length >= 2) {
        const lunchPos = Math.min(Math.ceil(d.length / 2), d.length);
        d.splice(lunchPos, 0, {k:'a', i:li});
      }
      if(di >= 0 && d.length >= 5) d.push({k:'a', i:di});
      nd.push(d);
      d = []; load = 0; prev = null; clockHr = startHr;
    }

    const c2 = prev == null ? 0 : travel(prev, i) / 60;
    d.push({k:'s', i});
    load += c2 + dur; clockHr += c2 + dur; prev = i;
  });

  if(d.length) {
    // Final day meals
    if(li >= 0 && d.length >= 2) {
      const lunchPos = Math.min(Math.ceil(d.length / 2), d.length);
      d.splice(lunchPos, 0, {k:'a', i:li});
    }
    nd.push(d);
  }

  if(!nd.length || nd.every(day => !day.length)) {
    toast('Nothing to plan — drag some spots in first, or clear the filter.');
    return;
  }

  if(maxDays && nd.length > maxDays) nd.splice(maxDays);

  days = nd;
  dayStarts = nd.map(() => dayStarts[0] || '09:00');
  curDay = 0;
  syncDayStart();
  renderAll();

  const nDays = nd.length;
  const nSpots = nd.reduce((s, day) => s + day.filter(r => r.k === 's').length, 0);
  const closedNote = baseDate ? ' · closed spots auto-skipped' : '';
  toast(`✨ ${nDays}-day plan · ${nSpots} spots${closedNote} — drag to fine-tune!`);

  // Show share strip after a short delay
  setTimeout(showShareStrip, 1200);
}

function getShareText(){
  const nDays = days.filter(d=>d.length).length;
  const nSpots = days.reduce((s,d)=>s+d.filter(r=>r.k==='s').length,0);
  return `Just planned my ${nDays}-day ${CITY.nm} trip using this free AI planner — ${nSpots} spots, auto-scheduled, printable. No sign-up needed 🗺️\nhttps://ordinarymantrying.com/tools/wander-china/planner.html`;
}

function showShareStrip(){
  // Remove existing strip
  document.getElementById('shareStrip')?.remove();
  const nDays = days.filter(d=>d.length).length;
  const shareText = getShareText();
  const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}`;
  const strip = document.createElement('div');
  strip.id = 'shareStrip';
  strip.className = 'share-strip';
  strip.innerHTML = `
    <h3>Nice plan! Share it with your travel crew 🗺️</h3>
    <p>Share once → unlock <b>+5 free</b> AI plans</p>
    <div class="ss-btns">
      <a class="ss-btn" href="${twitterUrl}" target="_blank" onclick="rewardShare()">𝕏 Share on X</a>
      <button class="ss-btn" onclick="copyShareText()">📋 Copy text</button>
      <button class="ss-btn" onclick="nativeShare()">📤 Share…</button>
    </div>
    <div class="ss-copy" onclick="copyShareText()" title="Click to copy">
      💬 "${shareText.replace(/\n/g,'  ')}"
    </div>`;
  document.querySelector('.ai-section').appendChild(strip);
  strip.scrollIntoView({behavior:'smooth', block:'nearest'});
}

function copyShareText(){
  const txt = getShareText();
  navigator.clipboard?.writeText(txt).then(()=>{
    rewardShare();
    toast('📋 Copied! Paste into WhatsApp, iMessage, or anywhere. +5 AI plans unlocked!');
  }).catch(()=>toast('Copy failed — try long-pressing the text instead.'));
}

function nativeShare(){
  const shareText = getShareText();
  if(navigator.share){
    navigator.share({title:'Wander China', text:shareText, url:'https://ordinarymantrying.com/tools/wander-china/planner.html'})
      .then(()=>rewardShare()).catch(()=>{});
  } else {
    copyShareText();
  }
}

function rewardShare(){
  try{
    const shared = localStorage.getItem('wc_shared');
    if(shared) return; // only reward once
    const curr = getAiUses();
    // Reward = subtract 5 from used count (effectively adds 5 free)
    localStorage.setItem(AI_KEY, Math.max(0, curr - 5).toString());
    localStorage.setItem('wc_shared', '1');
    updateAiBadge();
  }catch(e){}
}

// After print: show share prompt
window.addEventListener('afterprint', ()=>{
  setTimeout(()=>{
    const txt = getShareText();
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(txt)}`;
    if(navigator.share){
      navigator.share({title:'Wander China', text:txt, url:'https://ordinarymantrying.com/tools/wander-china/planner.html'})
        .then(()=>rewardShare()).catch(()=>{});
    } else {
      toast('Printed! Share with friends to unlock +5 free plans →');
      setTimeout(showShareStrip, 800);
    }
  }, 500);
});
// Day picker state
let _selectedDays = 3;
document.getElementById('dayPickerBtns').addEventListener('click', e => {
  const btn = e.target.closest('.dpb');
  if (!btn) return;
  _selectedDays = parseInt(btn.dataset.d, 10);
  document.querySelectorAll('.dpb').forEach(b => b.classList.toggle('active', b === btn));
});

document.getElementById('aiBtn').onclick=()=>{
  const b=document.getElementById('aiBtn');const t=b.textContent;
  b.textContent='⚡ Planning…';b.disabled=true;
  setTimeout(()=>{smartBuild(_selectedDays);b.textContent=t;b.disabled=false;},650);
};

document.getElementById('aiDeepBtn').onclick=async()=>{
  const b=document.getElementById('aiDeepBtn');const t=b.textContent;
  b.textContent='🤖 Asking DeepSeek…';b.disabled=true;
  try{
    const brief=`${_selectedDays}-day trip to ${CITY.nm} for a foreign tourist. Spots available: ${SP.map(s=>s.nm).join(', ')}. Plan exactly ${_selectedDays} days, sequence spots by proximity, mix culture/food/nature. Reply in JSON: {"days":[[spot names for day1],[day2],...]}`;
    const data=await callAI(brief);
    if(data && data.days && Array.isArray(data.days)){
      // Map DeepSeek names back to SP indices
      const nameMap={};SP.forEach((s,i)=>nameMap[s.nm.toLowerCase()]=i);
      const nd=data.days.slice(0,_selectedDays).map(dayNames=>{
        const row=[];
        dayNames.forEach(nm=>{
          const idx=nameMap[nm.toLowerCase()];
          if(idx!=null)row.push({k:'s',i:idx});
        });
        return row;
      }).filter(d=>d.length);
      if(nd.length){
        days=nd;dayStarts=nd.map(()=>dayStarts[0]||'09:00');curDay=0;
        syncDayStart();renderAll();
        toast(`🤖 DeepSeek built a ${nd.length}-day plan — drag to fine-tune!`);
        setTimeout(showShareStrip,1200);
      }else{
        toast('DeepSeek returned no matching spots — try Quick Plan instead.');
        smartBuild(_selectedDays);
      }
    }else{
      throw new Error('bad response');
    }
  }catch(e){
    toast('DeepSeek unavailable — using Quick Plan instead.');
    smartBuild(_selectedDays);
  }
  b.textContent=t;b.disabled=false;
};
/* =========================================================
   REAL TOTAL COST — free estimate, paid deliverable
   Ask departure LATE (only here), pre-guess region from timezone.
   Flight/hotel ranges are heuristics now; callAI() can refine later.
========================================================= */
const FLY={ // region: [label, roundtrip low $, high $]
  na:['North America',750,1400], sa:['South America',900,1700], eu:['Europe',600,1200],
  me:['Middle East',400,900], sas:['South Asia',300,700], sea:['Southeast Asia',150,500],
  ea:['East Asia (Japan/Korea)',200,550], oc:['Oceania',700,1400], af:['Africa',700,1500]};
const STYLE={ // style: [label, hotel/night low, high, food+transit/day low, high]
  budget:['Budget',25,45,15,30], comfort:['Comfort',55,95,30,55], luxury:['Luxury',140,260,60,120]};

/* ── Flight booking tips by region ── */
const FLY_TIPS={
  na:{book:'Book 8–12 weeks before departure',cheap:'January · February · November',airlines:'Air China, United, AA · 1-stop via Tokyo or Seoul is common · non-stop available to Beijing/Shanghai'},
  eu:{book:'Book 6–10 weeks before departure',cheap:'January · March · November',airlines:'Air China, Lufthansa, KLM, British Airways · direct flights to Beijing and Shanghai from major hubs'},
  sea:{book:'Book 3–5 weeks before departure',cheap:'April–May · September',airlines:'AirAsia, Scoot, VietJet for budget · Singapore Airlines, Cathay Pacific for comfort · very competitive fares'},
  ea:{book:'Book 3–5 weeks before departure',cheap:'March · November',airlines:'Peach, Jeju Air, Jin Air · cheapest China routes worldwide from Tokyo/Seoul · flights under $200 possible'},
  oc:{book:'Book 8–12 weeks before departure',cheap:'February · September',airlines:'Qantas, Air China, China Eastern · Hong Kong Cathay Pacific is a popular routing · 10–11 hour flight'},
  sas:{book:'Book 5–8 weeks before departure',cheap:'March · October',airlines:'Air China, IndiGo · Chengdu and Kunming serve as useful gateways to South Asia routes'},
  me:{book:'Book 4–8 weeks before departure',cheap:'February · September',airlines:'Emirates via Shanghai · Air China direct from Dubai, Riyadh, Abu Dhabi · often surprisingly affordable'},
  sa:{book:'Book 10–14 weeks before departure',cheap:'March · September',airlines:'LATAM + Air China via LA or Tokyo · expect 20–25 hour journeys · book early, routes are limited'},
  af:{book:'Book 8–12 weeks before departure',cheap:'January · September',airlines:'Ethiopian Airlines + Air China from Addis Ababa · routes expanding rapidly · stop-over in HK or Bangkok common'},
};

/* ── City-specific breakdown data ── */
const CITY_BD={
  beijing:{
    hood:'Dongcheng district — 15-min walk to Tiananmen, hutong alleys, Line 1/2 metro. Avoid the far-out modern districts.',
    foods:[
      {meal:'Breakfast 早餐',items:'Jianbing (egg crêpe) ¥8 · Baozi steamed buns ¥3/each · Soy milk ¥3',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Zhajiangmian noodles ¥25 · Dumplings (jiaozi) ¥30pp · Food court in mall ¥30',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Peking duck (Da Dong / Quanjude) ¥150pp · Hutong local restaurant ¥60–80pp',lo:10,hi:30},
    ],
    metro:'Day pass ¥20 ($3) · Lines 1 & 2 cover all major sights · Subway app: Alipay Metro',
    tips:['Book Forbidden City exactly 7 days ahead at 8pm via WeChat (passport number required) — sold out within minutes','Mutianyu Great Wall: take official shuttle from Dongzhimen, not the tourist agency buses (30% cheaper)','Eat in hutong alley side streets — same food as tourist spots at 40% of the price','Morning tai chi at Temple of Heaven is free before 8am (you pay only to enter the grounds)']
  },
  shanghai:{
    hood:'Former French Concession (Xuhui) for atmosphere, or Jing\'an for metro access. Pudong is convenient but soulless.',
    foods:[
      {meal:'Breakfast 早餐',items:'Shengjianbao pan-fried buns ¥10 · Youtiao oil stick ¥2 · Soy milk ¥4',lo:2,hi:6},
      {meal:'Lunch 午餐',items:'Xiao Long Bao soup dumplings ¥35 · Wonton noodles ¥20 · Food court ¥30',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Xintiandi restaurant ¥150pp · Shanghainese braised pork ¥70pp · French Concession café ¥80pp',lo:10,hi:30},
    ],
    metro:'9 lines, very efficient · Day pass ¥20 · Pudong→Bund on Line 2 · Maglev from Pudong Airport ¥50',
    tips:['The Bund is magical at sunset (6–8pm) — plan nothing else that evening, just walk and take it in','Yuyuan bazaar restaurants are tourist-priced; the alley one block behind has the same food at half price','Maglev from Pudong Airport: ¥50, 8 minutes. More fun and often faster than taxi','Yu Garden itself is worth seeing; the shops attached to it are not']
  },
  chengdu:{
    hood:'Jinjiang district near Chunxi Road — Lines 1 & 2 intersect here, walk to Kuanzhai Alley and Tianfu Square.',
    foods:[
      {meal:'Breakfast 早餐',items:'Dan Dan mian spicy noodles ¥15 · Steamed bao ¥8 · Century egg congee ¥10',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Mapo tofu set ¥35 · Kung Pao chicken ¥30 · Chuanchuan spicy skewers ¥40',lo:5,hi:10},
      {meal:'Dinner 晚餐',items:'Sichuan hotpot ¥80–150pp all in · Traditional Sichuan tasting menu ¥100pp',lo:12,hi:25},
    ],
    metro:'2 main lines + extensions · Line 3 goes to Panda Base (easiest option)',
    tips:['Chengdu Panda Base opens 7:30am — go first thing; pandas are active and feeding before 10am then sleep all day','Book hotpot at 5pm or 9pm to avoid the 2-hour queue at prime time (6–8pm)','People\'s Park afternoon tea: ¥30 for a pot of tea + watching locals play mahjong — one of the best free afternoons in China','Kuanzhai Alley restaurants are overpriced tourist traps; 2 streets over the same dishes cost half']
  },
  xian:{
    hood:'Near the Bell Tower (Beilin district) or Muslim Quarter (Lianhu district) — most of the city is walkable from here.',
    foods:[
      {meal:'Breakfast 早餐',items:'Roujiamo Chinese burger ¥7 · Persimmon cake ¥8 · Hulatang spiced soup ¥12',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Biangbiang noodles ¥25 · Lamb skewers 10 for ¥20 · Yang rou pao mo mutton stew ¥30',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Muslim Quarter food walk ¥60–80 grazing · Sit-down Shanxi restaurant ¥50pp',lo:8,hi:20},
    ],
    metro:'3 lines · Line 2 from downtown to Terracotta Museum (take dedicated shuttle from Weiyang Palace station)',
    tips:['Terracotta Warriors: buy ONLY from the official website or museum box office — fake "reseller tickets" near entrance are a common scam','Muslim Quarter: arrive at 5–5:30pm, before the 7pm rush. Leave by 8pm when it gets chaotic','Great Mosque (Huajue Lane): one of China\'s most beautiful mosques, rarely crowded in the morning, free to enter inner courtyard','City Wall bike rental ¥60 + ¥200 deposit (fully refunded) — best way to circle the full 14km loop']
  },
  changsha:{
    hood:'Furong district near Orange Island — close to Juzizhou, nightlife, and the main food streets.',
    foods:[
      {meal:'Breakfast 早餐',items:'Rice noodle soup (Changsha style) ¥12 · Stinky tofu ¥6 · Shaobing flat cake ¥5',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Chairman Mao\'s red braised pork ¥35 · Hot & sour soup noodles ¥18',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Hunan cuisine restaurant ¥60–90pp · Wenheyou snack floors ¥50–80 grazing',lo:8,hi:20},
    ],
    metro:'4 lines · Line 2 from airport to city center, most sights on Lines 2 & 4',
    tips:['Wenheyou is a Changsha institution: 7 floors of retro snack stalls in a 1980s-themed building — go for dinner','The Hunan Provincial Museum stinky tofu stall nearby (¥5) is legitimately great — trust the smell','Orange Island: free entry, huge Mao face sculpture worth seeing; best at sunset','Tanghulu (sugar-coated strawberry skewers): ¥10–15 on every street, don\'t miss it']
  },
  guangzhou:{
    hood:'Tianhe or Yuexiu district — Tianhe is modern and metro-connected; Yuexiu is near Chen Clan Ancestral Hall and the old city.',
    foods:[
      {meal:'Breakfast 早餐 (Yum Cha)',items:'Dim sum (har gow, siu mai, cheung fun) at a teahouse — ¥8–15 per plate',lo:6,hi:15},
      {meal:'Lunch 午餐',items:'Wonton noodles ¥20 · Cantonese roast goose ¥50pp · Clay pot rice ¥30',lo:5,hi:12},
      {meal:'Dinner 晚餐',items:'Cantonese seafood restaurant ¥80–150pp · Night market snacks ¥40pp',lo:8,hi:22},
    ],
    metro:'13 lines · one of the best metro systems in China · Canton Tower on Line 3',
    tips:['Yum cha (dim sum breakfast) is a Guangzhou ritual — go to a proper teahouse, not a tourist one, before 10am','Cantonese cooking is the opposite of Sichuan: subtle, light, ingredient-forward. Don\'t expect spice.','Canton Tower observation deck (¥150) has a sky walk — thrilling; the free riverside view from below is equally photogenic','Guangzhou Opera House (Zaha Hadid design) is free to walk around outside; striking building worth seeing']
  },
  hangzhou:{
    hood:'Near West Lake (Xihu district) — walkable to the lake, Hefang Street, and Lingyin Temple. Avoid the new financial district.',
    foods:[
      {meal:'Breakfast 早餐',items:'Longjing tea eggs ¥4 · Steamed glutinous rice cakes ¥8 · Youtiao ¥3',lo:2,hi:6},
      {meal:'Lunch 午餐',items:'Dongpo pork (must-try) ¥45 · West Lake fish in vinegar sauce ¥60 · Dragon Well prawn ¥80pp',lo:6,hi:15},
      {meal:'Dinner 晚餐',items:'Hefang Street food market ¥40–60 grazing · Hangzhou cuisine restaurant ¥70pp',lo:8,hi:20},
    ],
    metro:'4 lines · Line 1 from train station to West Lake',
    tips:['West Lake is free to walk around — save your money and rent a boat (¥80 per boat, split 4 ways) instead of paying for cruises','Longjing tea is famous here; buy directly from a village tea farmer near Longjing Village (cheaper and fresher than shops)','Lingyin Temple: arrive at 8am before tour groups arrive (temple opens at 7:30am)','Dongpo pork: named after the Song dynasty poet who invented it while governing Hangzhou — try it at Lou Wai Lou restaurant']
  },
  nanjing:{
    hood:'Qinhuai River area (Jiangning or Xuanwu district) — walkable to Confucius Temple, Presidential Palace, and Ming walls.',
    foods:[
      {meal:'Breakfast 早餐',items:'Salted duck (must-try in Nanjing) ¥20 portion · Rice gruel with toppings ¥12 · Duck blood soup ¥15',lo:3,hi:6},
      {meal:'Lunch 午餐',items:'Nanjing salted duck full portion ¥45 · Pan-fried beef dumpling ¥20 · Qinhuai snack combination ¥35',lo:5,hi:12},
      {meal:'Dinner 晚餐',items:'Confucius Temple night market ¥50–70 grazing · Hunan-style restaurant ¥60pp',lo:8,hi:20},
    ],
    metro:'4 lines · airport line to city center · Line 2 covers most tourist sites',
    tips:['Salted duck (盐水鸭) is Nanjing\'s most iconic food — order it at a proper duck shop, not a tourist restaurant','Nanjing Massacre Memorial Hall is sobering and important — go with respect; allow 2 full hours and bring water','Ming Xiaoling Mausoleum: the Sacred Way animal sculptures at sunrise are astonishing and almost empty of tourists before 8am','Zifeng Tower observation deck is free on Tuesday afternoons (check latest schedule before going)']
  },
  wuhan:{
    hood:'Wuchang district near Yellow Crane Tower and East Lake · Hankou (old concession area) is another great base.',
    foods:[
      {meal:'Breakfast 早餐',items:'Hot dry noodles (re gan mian) ¥10 — Wuhan\'s signature dish · Tofu pudding ¥5 · Braised egg ¥3',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Three freshwater crab dishes ¥50pp · Lotus root and pork rib soup ¥30 · Duck neck ¥20',lo:5,hi:12},
      {meal:'Dinner 晚餐',items:'Hubei cuisine restaurant ¥60–90pp · Jianghan Road night snacks ¥40–60',lo:8,hi:20},
    ],
    metro:'12 lines · well-connected · Line 4 from Hankou to Wuchang (Yellow Crane Tower)',
    tips:['Hot dry noodles for breakfast is mandatory in Wuhan — locals eat them standing up at street stalls at 7am. Join them.','Yellow Crane Tower is most beautiful at dawn before it\'s crowded; the tower itself is a modern rebuild but the view is real','Wuhan University cherry blossoms (late March–early April): arrive before 8am to beat the crowds of millions','East Lake is bigger than West Lake in Hangzhou but far less crowded — rent a bike and cycle around it in 2–3 hours']
  },
  nanchang:{
    hood:'Donghu district near Tengwang Pavilion · close to Bayi Square and the Gan River promenade.',
    foods:[
      {meal:'Breakfast 早餐',items:'Nanchang mixed rice noodles (mixture of 7 toppings) ¥10 · Glutinous rice balls ¥8',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Three cup chicken (san bei ji) ¥45 · Spicy duck tongue ¥25 · Jiangxi fried noodles ¥18',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Nanchang Old Food Street ¥50–70 grazing · Local Jiangxi restaurant ¥55pp',lo:7,hi:18},
    ],
    metro:'4 lines · Line 2 from airport to city center',
    tips:['Tengwang Pavilion is best in the evening when lit up — the river view from the top is the highlight','Nanchang mixed rice noodles are unique to the city — ask for "ban mian" (mixed without broth) for the authentic version','Red Valley (紅谷滩) district has the modern skyline for night photos; take a ferry across the Gan River for ¥2','The Aviation Museum has a serious collection of old Chinese military aircraft — worth it if you have an afternoon free']
  },
  _default:{
    hood:'Stay near the city center or main train station for easy metro access to sights.',
    foods:[
      {meal:'Breakfast 早餐',items:'Local street food stall · Rice congee or noodles · Typical ¥8–15',lo:2,hi:5},
      {meal:'Lunch 午餐',items:'Local noodle shop or food court in shopping mall',lo:4,hi:10},
      {meal:'Dinner 晚餐',items:'Mid-range local restaurant or nearby night market',lo:7,hi:18},
    ],
    metro:'City metro or bus covers most major sights · DiDi fills the gaps',
    tips:['Eat one block away from tourist sights — same food at 40–60% lower price','Book popular attractions 3–7 days ahead online; queues of 2+ hours without pre-booking are common','DiDi app (Chinese Uber): English interface, all major cities, ¥15–30 per typical city ride','Set up WeChat Pay or Alipay before arrival — many vendors now refuse cash and don\'t accept foreign cards']
  }
};
let costStyle='comfort';
function guessRegion(){const o=new Date().getTimezoneOffset();
  if(o>=240)return'na'; if(o>=120)return'sa'; if(o>=-60)return'eu'; if(o>=-210)return'me';
  if(o>=-360)return'sas'; if(o>=-450)return'sea'; if(o>=-570)return'ea'; return'oc';}
function seasonMult(){const v=document.getElementById('startDate').value;if(!v)return 1;
  const m=new Date(v).getMonth()+1;
  if(m===7||m===8)return 1.25; if(m===10||m===2)return 1.2; if(m===1||m===12)return .9; return 1;}
function openCost(){
  const dcount=Math.max(1,days.some(d=>d.length)?days.length:1);
  const reg=guessRegion();
  document.getElementById('costBody').innerHTML=`
    <div class="cf-field">
      <label for="costRegion">✈️ Where are you flying from?</label>
      <select id="costRegion">${Object.entries(FLY).map(([k,v])=>`<option value="${k}" ${k===reg?'selected':''}>${v[0]}</option>`).join('')}</select>
    </div>
    <div class="cf-field">
      <label for="costNights">🏨 How many nights?</label>
      <input type="number" id="costNights" min="1" max="60" value="${Math.max(1,dcount-1)}">
    </div>
    <div class="cf-field">
      <label>🎚️ Travel style</label>
      <div class="cf-styles" id="costStyles">
        ${Object.entries(STYLE).map(([k,v])=>`<div class="cf-style ${k===costStyle?'on':''}" data-s="${k}">${v[0]}<small>${k==='budget'?'hostels, street food':k==='comfort'?'3-star, mid-range':'4-5 star, fine dining'}</small></div>`).join('')}
      </div>
    </div>
    <button class="cf-go" id="costGo">🤖 Get AI estimate →</button>
    <div class="cr-note" style="margin-top:14px">We only ask now — after you've built your trip. Nothing is stored. ✈️ &amp; 🏨 are seasonal estimates.</div>`;
  document.querySelectorAll('#costStyles .cf-style').forEach(el=>el.onclick=()=>{
    costStyle=el.dataset.s;document.querySelectorAll('#costStyles .cf-style').forEach(x=>x.classList.toggle('on',x.dataset.s===costStyle));});
  document.getElementById('costGo').onclick=renderCostResult;
  document.getElementById('costFoot').textContent='Step 1 of 2 · your answers stay on this device';
  document.getElementById('costMask').classList.add('show');
}
function renderCostResult(){
  const region=document.getElementById('costRegion').value;
  const nights=Math.max(1,+document.getElementById('costNights').value||1);
  const dcount=Math.max(1,days.some(d=>d.length)?days.length:1);
  // capture spot list for AI brief
  const spotList=[];days.forEach(day=>day.forEach(ref=>spotList.push(getItem(ref).nm)));

  // Step 1: show loading animation
  document.getElementById('costBody').innerHTML=`
    <div class="ai-loading">
      <div class="spin">🤖</div>
      <p style="font-weight:700;color:var(--ai-d);margin-top:12px">AI is crunching your trip…</p>
      <div class="ai-steps">
        <div class="ai-step" id="cs1">Checking ${FLY[region]?.[0]||region} flight prices</div>
        <div class="ai-step" id="cs2">Looking up hotel rates for ${nights} nights</div>
        <div class="ai-step" id="cs3">Adding food, transit &amp; ${spotList.length} activities</div>
        <div class="ai-step" id="cs4">Adjusting for season &amp; travel style</div>
      </div>
    </div>`;
  document.getElementById('costFoot').textContent='AI is calculating…';

  // animate steps then show result
  const steps=['cs1','cs2','cs3','cs4'];
  let i=0;
  const tick=setInterval(()=>{
    if(i<steps.length){document.getElementById(steps[i])?.classList.add('done');i++;}
    else{clearInterval(tick);_showCostResult(region,nights,dcount,spotList);}
  },550);
}

function _showCostResult(region,nights,dcount,spotList){
  const isUnlocked=localStorage.getItem('wc_unlock_breakdown')==='1';
  const st=STYLE[costStyle], sm=seasonMult(), fly=FLY[region];
  let attractions=0;days.forEach(day=>day.forEach(ref=>attractions+=(getItem(ref).price||0)));
  attractions=usd(attractions);
  const flyLo=Math.round(fly[1]*sm),flyHi=Math.round(fly[2]*sm);
  const hotLo=st[1]*nights,hotHi=st[2]*nights;
  const fdLo=st[3]*dcount,fdHi=st[4]*dcount;
  const loT=flyLo+hotLo+fdLo+attractions, hiT=flyHi+hotHi+fdHi+attractions;
  const mid=(a,b)=>Math.round((a+b)/2);
  const seasonTxt=sm>1?` · ${sm>=1.25?'peak':'high'} season`:sm<1?' · low season':'';
  const ctx={region,nights,dcount,fly,st,sm,flyLo,flyHi,hotLo,hotHi,fdLo,fdHi,loT,hiT,mid,attractions,seasonTxt};
  if(isUnlocked) _showFullBreakdown(ctx); else _showCostTeaser(ctx);
}

function _shareNum(dcount,fly,loT,hiT){
  const text=`A ${dcount}-day trip to ${CITY.nm} ${CITY.emoji} from ${fly[0]}: ~$${loT.toLocaleString()}–$${hiT.toLocaleString()} all in. Plan yours free: https://ordinarymantrying.com/tools/wander-china/planner.html`;
  if(navigator.share)navigator.share({title:'Wander China',text}).catch(()=>{});
  else{navigator.clipboard?.writeText(text);toast('Copied — share your estimate!');}
}

function _showCostTeaser({region,nights,dcount,fly,flyLo,flyHi,hotLo,hotHi,fdLo,fdHi,loT,hiT,mid,attractions,seasonTxt}){
  const parts=[
    {lb:'✈️ Flights (round trip)',v:mid(flyLo,flyHi),c:'#7c3aed'},
    {lb:'🏨 Hotels ('+nights+' nights)',v:mid(hotLo,hotHi),c:'#0891b2'},
    {lb:'🍜 Food & local transit',v:mid(fdLo,fdHi),c:'#e11d48'},
    {lb:'🎟️ Activities & tickets',v:attractions,c:'#f59e0b'}];
  const max=Math.max(...parts.map(p=>p.v))||1;
  document.getElementById('costBody').innerHTML=`
    <div class="cr-total">
      <div class="n">$${loT.toLocaleString()}–$${hiT.toLocaleString()}</div>
      <div class="u">per person · ${dcount} days / ${nights} nights · from ${fly[0]}${seasonTxt}</div>
    </div>
    <div class="cr-bars-wrap">
      <div class="cr-bars">
        ${parts.map(p=>`<div class="cr-bar"><span class="lb">${p.lb}</span>
          <span class="track"><span class="fill" style="width:${Math.round(p.v/max*100)}%;background:${p.c}"></span></span>
          <span class="v">~$${p.v.toLocaleString()}</span></div>`).join('')}
      </div>
      <div class="cr-bars-overlay"><span class="ol-pill" onclick="doUnlockCost()">🔒 Unlock full breakdown</span></div>
    </div>
    <div class="cr-note">✈️ Your biggest cost is the flight — China on the ground is surprisingly affordable. Unlock to see the full day-by-day budget with real food prices and city-specific tips.</div>
    <div class="cr-unlock">
      <h3>🔓 Full Cost Breakdown — $3</h3>
      <p>What you get: best time to book flights · where to stay in ${CITY.nm} · real food dish prices · day-by-day ticket totals from <em>your plan</em> · 4 money-saving tips for ${CITY.nm}.</p>
      <button class="u-btn" onclick="doUnlockCost()">Unlock for $3 →</button>
    </div>
    <div class="cr-actions">
      <button id="costShare">📤 Share this estimate</button>
      <button id="costBack">↺ Recalculate</button>
    </div>`;
  document.getElementById('costFoot').textContent='Free estimate · unlock full breakdown for $3';
  document.getElementById('costBack').onclick=openCost;
  document.getElementById('costShare').onclick=()=>_shareNum(dcount,fly,loT,hiT);
}

function _showFullBreakdown({region,nights,dcount,fly,st,sm,flyLo,flyHi,hotLo,hotHi,fdLo,fdHi,loT,hiT,mid,attractions,seasonTxt}){
  const ft=FLY_TIPS[region]||FLY_TIPS.na;
  const cityKey=document.getElementById('citySel').value;
  const cbd=CITY_BD[cityKey]||CITY_BD._default;
  const hotelMid=mid(hotLo,hotHi), fdMid=mid(fdLo,fdHi);
  const smCls=sm>=1.25?'peak':sm>=1.1?'high':'good';
  const smTxt=sm>=1.25?'🔴 Peak season — prices 20–25% above base rate':sm>=1.1?'🟡 High season — slight premium applies':'🟢 Good timing — shoulder or low season rates';
  const hotelDesc={
    budget:`Hostels & guesthouses: $25–45/night · Check HostelWorld + Booking.com`,
    comfort:`3-star hotels & boutique guesthouses: $55–95/night · Trip.com often 20–30% cheaper than Booking.com for China hotels`,
    luxury:`4–5 star (Marriott, Hyatt, IHG): $140–260/night · International brands have strong China presence with reliable service`
  };
  // Build day-by-day activity rows from user's actual itinerary
  const dayRows=[];
  days.forEach((day,di)=>{
    if(!day.length)return;
    const ticketItems=day.map(ref=>getItem(ref)).filter(s=>s&&s.price&&!['Lunch','Dinner','Breakfast'].includes(s.nm));
    if(!ticketItems.length)return;
    const cost=usd(ticketItems.reduce((sum,s)=>sum+(s.price||0),0));
    const names=ticketItems.slice(0,3).map(s=>s.nm.split(' ').slice(0,3).join(' ')).join(' + ');
    dayRows.push(`<tr><td>Day ${di+1}</td><td style="color:#374151">${names}</td><td style="text-align:right;font-variant-numeric:tabular-nums"><b>~$${cost}</b></td></tr>`);
  });

  document.getElementById('costBody').innerHTML=`
    <div class="bd-grand">
      <div class="bd-grand-range">$${loT.toLocaleString()} – $${hiT.toLocaleString()}</div>
      <div class="bd-grand-sub">per person · ${dcount} days / ${nights} nights · from ${fly[0]}${seasonTxt}</div>
      <span class="bd-season-tag ${smCls}">${smTxt}</span>
    </div>

    <div class="bd-section">
      <div class="bd-sh">✈️ Flights &nbsp;—&nbsp; ~$${flyLo.toLocaleString()}–$${flyHi.toLocaleString()} round trip</div>
      <div class="bd-dr"><span class="bd-dk">🗓️ Book</span><span class="bd-dv">${ft.book}</span></div>
      <div class="bd-dr"><span class="bd-dk">💰 Cheapest months</span><span class="bd-dv">${ft.cheap}</span></div>
      <div class="bd-dr"><span class="bd-dk">✈️ Airlines</span><span class="bd-dv">${ft.airlines}</span></div>
      <div class="bd-dr"><span class="bd-dk">📱 Tip</span><span class="bd-dv">Set a Google Flights price alert to Beijing, Shanghai, or your entry city — alerts save 15–30% vs buying at random</span></div>
    </div>

    <div class="bd-section">
      <div class="bd-sh">🏨 Hotel &nbsp;—&nbsp; ~$${Math.round(hotelMid/Math.max(nights,1))}/night × ${nights} nights = ~$${hotelMid.toLocaleString()}</div>
      <div class="bd-dr"><span class="bd-dk">📍 Stay in</span><span class="bd-dv">${cbd.hood}</span></div>
      <div class="bd-dr"><span class="bd-dk">🏷️ ${costStyle.charAt(0).toUpperCase()+costStyle.slice(1)} picks</span><span class="bd-dv">${hotelDesc[costStyle]}</span></div>
      <div class="bd-dr"><span class="bd-dk">💡 Book tip</span><span class="bd-dv">Compare Trip.com vs Booking.com side-by-side — Trip.com (local platform) typically lists 15–30% lower rates for China hotels</span></div>
    </div>

    ${dayRows.length?`<div class="bd-section">
      <div class="bd-sh">🎟️ Your planned activities &nbsp;—&nbsp; $${attractions} in entrance fees</div>
      <table class="bd-days-table">
        <thead><tr><th>Day</th><th>Top stops</th><th style="text-align:right">Tickets</th></tr></thead>
        <tbody>${dayRows.join('')}</tbody>
        <tfoot><tr><td colspan="2"><b>Total entrance fees</b></td><td style="text-align:right"><b>$${attractions}</b></td></tr></tfoot>
      </table>
      <div style="font-size:12px;color:var(--sub);margin-top:6px">Based on your actual planned spots — food, transit, shopping not included here</div>
    </div>`:''}

    <div class="bd-section">
      <div class="bd-sh">🍜 Food & drink &nbsp;—&nbsp; ~$${fdLo}–$${fdHi} over ${dcount} days</div>
      ${cbd.foods.map(f=>`<div class="bd-food-row">
        <span class="bd-meal">${f.meal}</span>
        <span class="bd-food-items">${f.items}</span>
        <span class="bd-food-cost">~$${f.lo}–$${f.hi}/day</span>
      </div>`).join('')}
      <div class="bd-food-note">💡 Budget travelers eat well on $15/day; comfort style $30–40/day covers sit-down meals with drinks</div>
    </div>

    <div class="bd-section">
      <div class="bd-sh">🚇 Getting around &nbsp;— included in daily estimate</div>
      <div class="bd-dr"><span class="bd-dk">Metro</span><span class="bd-dv">${cbd.metro}</span></div>
      <div class="bd-dr"><span class="bd-dk">DiDi (Uber)</span><span class="bd-dv">¥15–30 ($2–4) most city rides · English interface · download before you fly</span></div>
      <div class="bd-dr"><span class="bd-dk">Airport</span><span class="bd-dv">Metro/express if available (~¥25–50) · Taxi ¥80–150 depending on distance · avoid unlicensed "black cabs"</span></div>
    </div>

    <div class="bd-tips-box">
      <div class="bd-tips-hd">💡 ${cbd.tips.length} money-saving tips specific to ${CITY.nm}</div>
      <ol class="bd-tips-list">${cbd.tips.map(t=>`<li>${t}</li>`).join('')}</ol>
    </div>

    <div class="cr-actions" style="margin-top:16px">
      <button id="costShare">📤 Share this estimate</button>
      <button id="costBack">↺ Recalculate</button>
    </div>`;
  document.getElementById('costFoot').textContent=`Full breakdown · ${CITY.nm} · ${dcount} days from ${fly[0]}`;
  document.getElementById('costBack').onclick=openCost;
  document.getElementById('costShare').onclick=()=>_shareNum(dcount,fly,loT,hiT);
}
document.getElementById('aiHint').onclick=openCost;

// ── Ko-fi Unlock System ──────────────────────────────────────────────────────
const UNLOCK_PRODUCTS = {
  copy: {
    title: '📋 Unlock Copy Text',
    sub: '$2 one-time · copy your itinerary to WhatsApp, Notes, email',
    kofi: 'https://ko-fi.com/s/22021c2aa4',
    lsKey: 'wc_unlock_copy'
  },
  ai: {
    title: '🤖 Unlock Unlimited AI Builds',
    sub: '$2 one-time · build as many AI trips as you want, any city',
    kofi: 'https://ko-fi.com/s/a55f188bd6',
    lsKey: 'wc_unlock_ai'
  },
  breakdown: {
    title: '💸 Unlock Full Cost Breakdown',
    sub: '$3 one-time · day-by-day budget + cheapest booking windows',
    kofi: 'https://ko-fi.com/s/0c099710a4',
    lsKey: 'wc_unlock_breakdown'
  }
};

let _ulProduct = null;

function openUnlock(product){
  _ulProduct = product;
  const p = UNLOCK_PRODUCTS[product];
  document.getElementById('ulTitle').textContent = p.title;
  document.getElementById('ulSub').textContent = p.sub;
  document.getElementById('ulKofiBtn').href = p.kofi;
  document.getElementById('ulKofiBtn').textContent = '☕ Buy on Ko-fi →';
  document.getElementById('ulCodeInput').value = '';
  document.getElementById('ulError').textContent = '';
  document.getElementById('unlockMask').classList.add('show');
}

document.getElementById('ulVerifyBtn').onclick = async () => {
  const token = document.getElementById('ulCodeInput').value.trim();
  const errEl = document.getElementById('ulError');
  if (!token){ errEl.textContent='Enter your unlock code'; return; }

  const btn = document.getElementById('ulVerifyBtn');
  btn.textContent = 'Checking…'; btn.disabled = true; errEl.textContent = '';

  try {
    const res = await fetch('api/verify.php?token=' + encodeURIComponent(token));
    const data = await res.json();
    if(data.ok){
      const p = UNLOCK_PRODUCTS[data.product];
      if(p) localStorage.setItem(p.lsKey, '1');
      document.getElementById('unlockMask').classList.remove('show');
      applyUnlock(data.product);
      toast('🎉 Unlocked! ' + (p?.title || ''));
    } else {
      errEl.textContent = data.error || 'Invalid code — check your email';
    }
  } catch(e){
    errEl.textContent = 'Connection error — try again';
  }
  btn.textContent = 'Verify →'; btn.disabled = false;
};

function applyUnlock(product){
  if(product === 'copy'){
    // copy & print are now always free — nothing extra to do
    navigator.clipboard?.writeText(buildTripTxt())
      .then(()=>toast('📋 Copied!')).catch(()=>{});
  }
  if(product === 'ai'){
    document.getElementById('aiPaywall')?.remove();
    window._aiUnlocked = true;
    updateAiBadge();
  }
  if(product === 'breakdown'){
    document.querySelector('.cr-bars-overlay')?.remove();
    document.querySelector('.cr-unlock')?.remove();
  }
}

// Restore unlocks from previous sessions
(function restoreUnlocks(){
  if(localStorage.getItem('wc_unlock_ai')==='1') window._aiUnlocked=true;
})();

// Auto-detect payment from Ko-fi tab (storage event fires across tabs on same domain)
window.addEventListener('storage', e => {
  if(e.key === 'wc_just_unlocked' && e.newValue){
    applyUnlock(e.newValue);
    const labels = {copy:'📋 Copy Text',ai:'🤖 AI Build Unlimited',breakdown:'💸 Full Cost Breakdown'};
    toast('🎉 ' + (labels[e.newValue]||'Feature') + ' unlocked — enjoy!');
    // close unlock modal if open
    document.getElementById('unlockMask')?.classList.remove('show');
  }
});

/* placeholder for real AI call (paid). Returns a plan or throws. */
async function callAI(brief){
  const res=await fetch('api-proxy.php',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({task:'plan',city:CITY.nm,brief,spots:SP.map(s=>s.nm)})});
  if(!res.ok)throw new Error('AI unavailable');
  return res.json();
}

/* ---- trip sheet ---- */
function buildSheetDayHtml(day, di){
  const dt=dayDate(di);
  const dowStr=dt?`(${dt.toLocaleDateString('en-US',{month:'short',day:'numeric'})}, ${DOW[dt.getDay()]})`:'';
  const saved=curDay;curDay=di;const rows=computeDay(day);curDay=saved;
  let dayCost=0;
  const rowsHtml=rows.map((r,k)=>{
    const s=getItem(r.ref);dayCost+=(s.price||0);
    const commute=k>0?`<small>${r.near?'🚶 walk nearby':'🚇 ~'+Math.round(r.commute*60)+' min to get here'}</small>`:'';
    return `<div class="sheet-row"><div class="t">${hm(r.arr)}–${hm(r.leave)}</div>
      <div class="c"><b>${s.ic} ${s.nm}</b> <small>${s.metro&&s.metro!=='—'?s.metro+' · ':''}${s.pn}</small><small>💡 ${s.tip}</small>${commute}</div></div>`;
  }).join('');
  return {html:`<div class="sheet-day" id="sheet-day-${di}"><h3>Day ${di+1} ${dowStr} · tickets ≈ $${usd(dayCost)}</h3>${rowsHtml}</div>`, cost:dayCost};
}

document.getElementById('genBtn').onclick=()=>{
  const body=document.getElementById('sheetBody');
  let grandCost=0, dayChunks=[];
  days.forEach((day,di)=>{
    if(!day.length)return;
    const {html,cost}=buildSheetDayHtml(day,di);
    grandCost+=cost; dayChunks.push({html,di});
  });
  if(!dayChunks.length){toast('Nothing scheduled yet — drag a few notes in first.');return;}
  document.getElementById('sheetTitle').textContent=`My ${CITY.nm} trip`;
  document.getElementById('sheetSub').textContent=`${CITY.emoji} ${CITY.nm} · ${CITY.district} · built with Wander China`;
  document.getElementById('sheetCost').textContent=`Tickets & activities ≈ $${usd(grandCost)} (¥${grandCost}) per person`;

  // Always show all days — copy & print are free
  body.innerHTML=dayChunks.map(c=>c.html).join('');
  document.getElementById('sheetMask').classList.add('show');
};
function buildTripTxt(){
  let txt=`【My ${CITY.nm} trip】\n`;
  days.forEach((day,di)=>{if(!day.length)return;
    const saved=curDay;curDay=di;const rows=computeDay(day);curDay=saved;
    txt+=`\n===== Day ${di+1} =====\n`;
    rows.forEach((r,k)=>{const s=getItem(r.ref);
      if(k>0)txt+=r.near?`  🚶 nearby\n`:`  🚇 ~${Math.round(r.commute*60)} min\n`;
      txt+=`${hm(r.arr)}-${hm(r.leave)} ${s.nm} (${s.pn})\n`;});
  });
  return txt;
}
document.getElementById('copyBtn').onclick=()=>{
  const txt=buildTripTxt();
  navigator.clipboard?.writeText(txt).then(()=>toast('📋 Copied! Paste into WhatsApp, Notes, or email.'))
    .catch(()=>{toast('Copy failed — try long-pressing the text instead.');});
};
function doCopyUnlock(){ openUnlock('copy'); }
function doUnlockCost(){ openUnlock('breakdown'); }
function doPrint(){
  if(localStorage.getItem('wc_shared')==='1'){
    window.print();
    return;
  }
  // Not shared yet — show share-to-print prompt
  const txt = getShareText();
  const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(txt)}`;
  const existing = document.getElementById('printSharePrompt');
  if(existing){ existing.scrollIntoView({behavior:'smooth',block:'nearest'}); return; }
  const gate = document.createElement('div');
  gate.id = 'printSharePrompt';
  gate.className = 'share-strip';
  gate.style.margin = '14px 0 0';
  gate.innerHTML = `
    <h3>🖨️ 打印前先分享一下吧！</h3>
    <p>分享给朋友 → 解锁打印 + 额外 <b>+5次</b> 免费 AI 规划</p>
    <div class="ss-btns">
      <a class="ss-btn" href="${twitterUrl}" target="_blank" onclick="rewardShare();setTimeout(()=>{document.getElementById('printSharePrompt')?.remove();window.print();},400)">𝕏 Twitter 分享</a>
      <button class="ss-btn" onclick="copyShareTextAndPrint()">📋 复制文案后打印</button>
      <button class="ss-btn" onclick="nativeShareThenPrint()">📤 分享...</button>
    </div>
    <div class="ss-copy" onclick="copyShareTextAndPrint()" title="点击复制后打印">
      💬 "${txt.replace(/\n/g,'  ')}"
    </div>
    <div style="text-align:center;margin-top:10px"><a style="font-size:11px;color:rgba(255,255,255,.35);cursor:pointer" onclick="rewardShare();document.getElementById('printSharePrompt')?.remove();window.print()">直接打印（不分享）</a></div>`;
  document.getElementById('sheetBody').appendChild(gate);
  gate.scrollIntoView({behavior:'smooth', block:'nearest'});
}
function copyShareTextAndPrint(){
  const txt = getShareText();
  navigator.clipboard?.writeText(txt).then(()=>{
    rewardShare();
    document.getElementById('printSharePrompt')?.remove();
    toast('📋 文案已复制！粘贴后分享，正在打印…');
    setTimeout(()=>window.print(), 600);
  }).catch(()=>toast('复制失败，请手动复制后再打印'));
}
function nativeShareThenPrint(){
  const txt = getShareText();
  if(navigator.share){
    navigator.share({title:'Wander China',text:txt,url:'https://ordinarymantrying.com/tools/wander-china/planner.html'})
      .then(()=>{ rewardShare(); document.getElementById('printSharePrompt')?.remove(); setTimeout(()=>window.print(),400); })
      .catch(()=>{});
  } else {
    copyShareTextAndPrint();
  }
}
document.getElementById('shareTripBtn').onclick=()=>{
  const nStops=days.reduce((a,d)=>a+d.filter(r=>r.k==='s').length,0);
  const nDays=days.filter(d=>d.length).length;
  const text=`My ${nDays}-day ${CITY.nm} ${CITY.emoji} trip — ${nStops} stops, planned in minutes. Build yours free:`;
  if(navigator.share)navigator.share({title:`My ${CITY.nm} trip`,text,url:location.href}).catch(()=>{});
  else{navigator.clipboard?.writeText(text+' '+location.href);toast('Link copied — share your trip!');}
};

/* ---- toast ---- */
let toastT;
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('show'),2600);}

/* ---- city loading + init ---- */
const CITY_GUIDE_SLUGS=['beijing','changchun','changsha','chengdu','chongqing','fuzhou','guangzhou','guiyang','haikou','hangzhou','harbin','hefei','hohhot','jinan','kunming','lanzhou','shanghai'];
function loadCity(key){
  const cd=CITIES_DATA[key]||CITIES_DATA.changsha;
  CITY=cd.meta;SP=cd.spots;TM=cd.tm||[];
  days=[[]];dayStarts=['09:00'];curDay=0;filter='all';
  document.getElementById('cityTag').textContent=CITY.nm;
  document.getElementById('citySel').value=(CITIES_DATA[key]?key:'changsha');
  // update "already here" panel
  const activeKey2=CITIES_DATA[key]?key:'changsha';
  document.getElementById('hereBarCity').textContent=CITY.nm;
  document.getElementById('hereSectionCity').textContent=CITY.nm;
  const isChangsha=activeKey2==='changsha';
  document.getElementById('hereChangsha').style.display=isChangsha?'':'none';
  document.getElementById('hereOther').style.display=isChangsha?'none':'';
  const gl=document.getElementById('hereGuideLink');
  if(gl)gl.href=`cities/${activeKey2}.html`;
  const guideLink=document.getElementById('cityGuideLink');
  const dragHint=document.getElementById('dragHint');
  const activeKey=CITIES_DATA[key]?key:'changsha';
  SP.forEach(s=>{if(!s.img)s.img=`../img/${activeKey}/${s.id}.webp`;});
  if(CITY_GUIDE_SLUGS.includes(activeKey)){
    guideLink.href=`cities/${activeKey}.html`;
    guideLink.style.display='inline-block';
    if(dragHint)dragHint.style.display='none';
  }else{
    guideLink.style.display='none';
    if(dragHint)dragHint.style.display='';
  }
  syncDayStart();renderFilters();renderWall();renderAll();
}
(function init(){
  // city selector
  const sel=document.getElementById('citySel');
  sel.innerHTML=Object.keys(CITIES_DATA).map(k=>`<option value="${k}">${CITIES_DATA[k].meta.emoji} ${CITIES_DATA[k].meta.nm}</option>`).join('');
  sel.onchange=()=>loadCity(sel.value);
  // default date = day after tomorrow
  const d=new Date();d.setDate(d.getDate()+2);
  document.getElementById('startDate').value=d.toISOString().slice(0,10);
  // pick city from ?city= or localStorage (handed over by the quiz)
  const params=new URLSearchParams(location.search);
  let key=(params.get('city')||'').toLowerCase().replace(/[^a-z]/g,'');
  if(!key){try{key=(localStorage.getItem('wc_city')||'').toLowerCase().replace(/[^a-z]/g,'');}catch(e){}}
  const known=!!CITIES_DATA[key];
  loadCity(known?key:'changsha');
  if(key&&!known)setTimeout(()=>toast(`Full planner for "${key}" is coming — meet ${CITY.nm} for now 🌶️`),400);
  // Auto-build demo plan on first visit so users see what the tool produces immediately
  const isFirstVisit=!sessionStorage.getItem('wc_built');
  const isFromQuiz=params.get('from')==='quiz';
  if(isFirstVisit&&!isFromQuiz){
    sessionStorage.setItem('wc_built','1');
    setTimeout(()=>{
      if(!days.some(d=>d.length)){
        smartBuild();
        setTimeout(()=>toast('✨ Sample plan — tap any spot for details, or rebuild with AI Build!'),900);
      }
    },200);
  }
  // quiz handoff banner
  if(params.get('from')==='quiz'){
    setTimeout(()=>{
      const meta=CITY;
      const banner=document.getElementById('quizBanner');
      const txt=document.getElementById('quizBannerText');
      txt.innerHTML=`🎯 Quiz matched you with <strong>${meta.emoji||''} ${meta.nm}</strong> <span class="qb-hint">— Drag attractions from the left panel onto your timeline to build your trip ✨</span>`;
      banner.classList.add('show');
    },300);
  }
  // ---- City Explorer ----
  const FULL_SET=new Set(['changsha','guangzhou','chengdu','beijing','chongqing','hangzhou',
    'harbin','kunming','hohhot','hefei','fuzhou','jinan','guiyang','haikou','changchun','lanzhou']);
  const ceGrid=document.getElementById('ceGrid');
  function renderCeGrid(){
    ceGrid.innerHTML='';
    Object.entries(CITIES_DATA).forEach(([id,cd])=>{
      const m=cd.meta;
      const isFull=FULL_SET.has(id);
      const isActive=id===(CITY&&CITY._id||key||'changsha');
      const card=document.createElement('div');
      card.className='ce-card'+(isActive?' active':'');
      card.dataset.city=id;
      card.innerHTML=`<span class="ce-emoji">${m.emoji||'🏙️'}</span>
        <div class="ce-nm">${m.nm}</div>
        <div class="ce-cn">${m.nm_cn}</div>
        <span class="ce-badge ${isFull?'full':'lite'}">${isFull?'Full guide':'Coming soon'}</span>`;
      card.onclick=()=>{
        if(days.some(d=>d.length)&&!confirm(`Switch to ${m.nm}? Your current plan will reset.`))return;
        days=[[]];dayStarts=['09:00'];curDay=0;
        loadCity(id);
        document.querySelectorAll('.ce-card').forEach(c=>c.classList.toggle('active',c.dataset.city===id));
        window.scrollTo({top:0,behavior:'smooth'});
        toast(`Switched to ${m.emoji||''} ${m.nm} — drag spots to build your day!`);
      };
      ceGrid.appendChild(card);
    });
  }
  renderCeGrid();

  // store active city id on meta for ce-grid active detection
  const _origLoad=loadCity;
  // patch CITY._id after load
  const _afterLoad=()=>{if(CITY)CITY._id=Object.keys(CITIES_DATA).find(k=>CITIES_DATA[k].meta===CITY)||''};
  _afterLoad();
  // auto-open here section if URL has ?mode=here
  if(new URLSearchParams(location.search).get('mode')==='here'){
    setTimeout(()=>{const s=document.getElementById('hereSection');if(s){s.classList.add('open');s.scrollIntoView({behavior:'smooth',block:'start'});}},400);
  }
  // hide loading overlay
  const loader=document.getElementById('pageLoader');
  if(loader)setTimeout(()=>loader.classList.add('done'),50);
})();

function toggleHere(){
  const sec=document.getElementById('hereSection');
  if(!sec)return;
  sec.classList.toggle('open');
  if(sec.classList.contains('open'))sec.scrollIntoView({behavior:'smooth',block:'start'});
}

// ---- AI Build usage counter (10 free, then paywall) ----
const AI_KEY='wc_ai_uses';
function getAiUses(){try{return parseInt(localStorage.getItem(AI_KEY)||'0',10);}catch(e){return 0;}}
function incAiUses(){try{localStorage.setItem(AI_KEY,getAiUses()+1);}catch(e){}}
const FREE_AI=10;

// show remaining uses badge near AI button
(function(){
  const sec=document.querySelector('.ai-section');
  if(!sec)return;
  const badge=document.createElement('div');
  badge.className='ai-uses';
  badge.id='aiUsesBadge';
  sec.appendChild(badge);
  updateAiBadge();
})();
function updateAiBadge(){
  const b=document.getElementById('aiUsesBadge');if(!b)return;
  const used=getAiUses(),left=Math.max(0,FREE_AI-used);
  const shared = localStorage.getItem('wc_shared') === '1';
  b.innerHTML=left>0
    ?`<b>${left}</b> free AI plans · ${shared?'':'share to get +5 bonus'}`
    :`Free uses exhausted — <b>share to get +5</b> or unlock unlimited $2`;
}

// Intercept the existing aiBtn click to add the counter
document.getElementById('aiBtn').addEventListener('click',function handler(e){
  if(!window._aiUnlocked && getAiUses()>=FREE_AI){
    e.stopImmediatePropagation();
    const existing=document.getElementById('aiPaywall');
    if(existing){existing.scrollIntoView({behavior:'smooth',block:'nearest'});return;}
    const gate=document.createElement('div');
    gate.id='aiPaywall';
    gate.className='copy-gate';
    gate.style.marginTop='14px';
    gate.innerHTML=`<div class="cg-emoji">🤖</div>
      <h3>You've used all ${FREE_AI} free AI plans</h3>
      <p>You're clearly a planner. Unlock unlimited AI trip-building for all 31 cities.</p>
      <button class="cg-btn" onclick="document.getElementById('aiPaywall').remove();openUnlock('ai')">🔓 Unlock unlimited — $2</button>`;
    document.querySelector('.ai-section').appendChild(gate);
    gate.scrollIntoView({behavior:'smooth',block:'nearest'});
    return;
  }
  incAiUses();
  setTimeout(updateAiBadge,100);
},true);
