var N = STEPS.length, i = 0;
var rowEls = [], barEls = [], evEls = [];
function fa(n){return String(n).replace(/[0-9]/g,function(d){return '۰۱۲۳۴۵۶۷۸۹'[d];});}
function H(h){return Math.round(4 + h*3.4);}          /* 0 -> 4px, 9 -> 35px */
function sel(q){return document.querySelectorAll(q);}
function el(id){return document.getElementById(id);}

function init(){
  rowEls = sel('.row'); barEls = sel('.bar'); evEls = sel('.evs');
  alignKeys();
  show(0);
  /* re-measure once the real font has landed, and on resize — hooked ONCE here.
     Re-arming document.fonts.ready from inside alignKeys would spin forever. */
  window.addEventListener('resize', alignKeys);
  if(document.fonts && document.fonts.ready && document.fonts.ready.then){ document.fonts.ready.then(alignKeys); }
}

/* All four branch titles share ONE column width, so their left edges line up flush
   (the user wants them aligned, not ragged). Because the column is uniform, every bar
   also starts at the same x — the titles still sit immediately beside their own bar. */
function alignKeys(){
  var rows = sel('.row'), keys = sel('.row .key'), n = keys.length, max = 0, j, w;
  if(!n || !rows.length) return;
  for(j=0;j<n;j++){ keys[j].style.flex = ''; keys[j].style.width = ''; keys[j].style.maxWidth = ''; }
  if(window.getComputedStyle(rows[0]).flexDirection !== 'row') return;
  for(j=0;j<n;j++){ w = keys[j].getBoundingClientRect().width; if(w > max) max = w; }
  if(!max) return;
  var px = Math.ceil(max) + 'px';
  for(j=0;j<n;j++){ keys[j].style.flex = '0 0 ' + px; keys[j].style.width = px; keys[j].style.maxWidth = px; }
}

function show(k){
  k = Math.max(0, Math.min(N-1, k));
  var st = STEPS[k];
  /* thickness: cumulative; one lane per step, three lanes for the product step */
  for(var r=0;r<4;r++){
    var h = H(st.h[r]);
    barEls[r].style.height = h + 'px';
    rowEls[r].style.setProperty('--bh', h + 'px');
    rowEls[r].classList.toggle('act', st.grow.indexOf(r) > -1);
  }
  /* descriptions: rendered INSIDE the branch they belong to (cumulative history) */
  window._curK = k;
  buildLanes(k);
  if(window.matchMedia('(max-width:700px)').matches){ scrollToActive(st); }
  el('cap').textContent = st.cap || '';
  el('cap').style.opacity = st.cap ? '1' : '0';
  /* year on the grey axis (desktop) and on the phone year-line */
  var yr = st.yr || '';
  var y1 = el('yr'), y2 = el('yrp'), yb = el('yrbar');
  if(y1){ y1.textContent = yr; y1.style.display = yr ? 'block' : 'none'; }
  if(y2){ y2.textContent = yr; }
  if(yb){ yb.classList.toggle('off', !yr); }
  el('hero').classList.toggle('on', !!st.hero);
  el('end').classList.toggle('on', !!st.end);
  el('umb').classList.toggle('on', !!st.umbrella);   /* umbrella shows only on its own step */
  el('combo').classList.toggle('on', !!st.combo);
  renderProd(st);                                    /* dedicated page for each product */
  document.body.classList.toggle('dimmed', !!(st.umbrella || st.end || st.think));
  /* the hero/end cards are opaque covers: nothing behind them may show through */
  el('bar').style.width = ((k+1)/N*100) + '%';
  el('pager').textContent = 'گام ' + fa(k+1) + ' از ' + fa(N);
  var hb = el('home'); if(hb) hb.classList.toggle('show', k > 0);   /* cover needs no home button */
  i = k;
  clearTimeout(window._actT);
  window._actT = setTimeout(function(){
    for(var r3=0;r3<4;r3++){ rowEls[r3].classList.remove('act'); }
  }, 1100);
}

/* Each lane shows ONLY the current step's event title(s) — no stacked history.
   When a step has no event for a branch, that branch simply keeps its bar with no
   title (clean), so titles never pile up on top of each other. */
function buildLanes(k){
  var st = STEPS[k];
  for(var r=0;r<4;r++) evEls[r].innerHTML = '';
  var ev = st.ev || [];
  for(var e=0;e<ev.length;e++){
    var lane = ev[e][0], host = evEls[lane];
    if(!host) continue;
    var chip = document.createElement('div');
    chip.className = 'echip now';
    var m = document.createElement('i'); m.style.background = LANES[lane].color;
    var t = document.createElement('span'); t.textContent = ev[e][1];
    chip.appendChild(m); chip.appendChild(t);
    host.appendChild(chip);
  }
  stackChips();
}

/* Place chips bottom-up above their bar, anchored to the LANE BOTTOM (the bar line).
   Runs after layout so heights are real. */
function stackChips(){
  requestAnimationFrame(function(){
    for(var r=0;r<4;r++){
      var host = evEls[r]; if(!host) continue;
      var chips = host.children;
      /* anchor to the TARGET bar height (final layout), not the mid-transition rendered
         height, so chips never overlap a bar that is still growing under them */
      var bh = H(STEPS[window._curK || 0].h[r]);
      /* chips sit just above their OWN bar, inside their own lane — no extra offset,
         otherwise they ride up into the row above and look like the next branch */
      var y = bh + 10, j, c, hh;
      for(j=chips.length-1;j>=0;j--){
        c = chips[j];
        if(c.style.display === 'none') continue;
        hh = c.offsetHeight;
        c.style.top = 'auto';
        c.style.bottom = Math.round(y) + 'px';
        y += hh + 8;
      }
    }
  });
}

/* Phone: the stacked branches scroll; bring the ACTIVE branch (or the first lane that
   has a chip this step) into view under the fixed caption, so the current event never
   hides behind it. */
function scrollToActive(st){
  requestAnimationFrame(function(){
    var target = null;
    if(st.grow && st.grow.length){ target = rowEls[st.grow[0]]; }
    if(!target){
      for(var r=0;r<4;r++){
        if(st.ev && st.ev.some(function(e){ return e[0]===r; })){ target = rowEls[r]; break; }
      }
    }
    if(!target) return;
    var capEl = el('cap');
    var capH = (parseFloat(window.getComputedStyle(capEl).bottom) || 0) + capEl.offsetHeight + 14;
    var top = window.scrollY + target.getBoundingClientRect().top - capH;
    window.scrollTo({top: Math.max(0, top), behavior: 'auto'});
  });
}

/* Each product page: title, tagline, the three-branch recipe, points.
   The recipe reads right-to-left: electronics + automation + software = product. */
function renderProd(st){
  var page = el('prod');
  if(!page) return;
  page.classList.toggle('on', !!st.pg);
  if(!st.pg) return;
  el('pgtitle').textContent = st.pg.title;
  el('pgtag').textContent = st.pg.tag;
  el('pgrole').textContent = st.pg.role ? ('نقش شاخه‌ها: ' + st.pg.role) : '';
  var ul = el('pgpoints');
  ul.innerHTML = '';
  (st.pg.points || []).forEach(function(t){
    var li = document.createElement('li'); li.textContent = t; ul.appendChild(li);
  });
  var rec = el('pgrecipe');
  rec.innerHTML = '';
  var pill = function(txt, col){
    var s = document.createElement('span'); s.className = 'rpill'; s.textContent = txt;
    if(col) s.style.background = col;
    rec.appendChild(s);
  };
  var op = function(ch){
    var s = document.createElement('span'); s.className = 'rop'; s.textContent = ch;
    rec.appendChild(s);
  };
  pill(LANES[0].key, LANES[0].color); op('+');
  pill(LANES[1].key, LANES[1].color); op('+');
  pill(LANES[3].key, LANES[3].color); op('=');   /* software, not AI */
  pill(st.pg.title, '');
}

document.addEventListener('keydown', function(e){
  if(['ArrowLeft','PageDown',' ','Enter','ArrowDown'].indexOf(e.key) > -1){ show(i+1); e.preventDefault(); }
  if(['ArrowRight','PageUp','ArrowUp','Backspace'].indexOf(e.key) > -1){ show(i-1); e.preventDefault(); }
  if(e.key==='Home'||e.key==='HomeScreen'){ show(0); e.preventDefault(); }   /* Home key -> cover page */
  if(e.key==='f'||e.key==='F'){ var d=document.documentElement;
    if(document.fullscreenElement){document.exitFullscreen();}else if(d.requestFullscreen){d.requestFullscreen();} }
});
var touchUsed=false, x0=null, y0=null;
document.addEventListener('touchstart',function(e){ touchUsed=true; x0=e.touches[0].clientX; y0=e.touches[0].clientY; },{passive:true});
document.addEventListener('touchend',function(e){
  if(x0===null) return;
  var dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
  if(Math.abs(dx)>40 && Math.abs(dx)>Math.abs(dy)){ dx>0 ? show(i-1) : show(i+1); }
  else if(Math.abs(dy)>40){ dy>0 ? show(i-1) : show(i+1); }
  x0=null; setTimeout(function(){touchUsed=false;},700);
},{passive:true});
document.addEventListener('click',function(e){ if(touchUsed) return; show(i+1); });
/* home button: straight back to the cover, never advance a step */
var homeBtn = el('home');
if(homeBtn){
  homeBtn.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); show(0); });
}
setTimeout(function(){ el('hint').classList.add('gone'); },9000);
window.addEventListener('beforeprint', function(){ show(N-1); });

var hsh = (location.hash||'').match(/s(\d+)/);
init();
show(hsh ? parseInt(hsh[1],10)-1 : 0);
