#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble the animated timeline deck (self-contained HTML, embedded fonts)."""
import base64, json, os
from timeline_data import LANES, STEPS, UMB_COLOR, OWNER

OUT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(OUT, "index.html")

# Fonts: put Vazirmatn Regular/Bold in ./fonts next to this script, or point FONT_DIR at them.
# (The build embeds the two TTFs as base64, so the output HTML has no external requests.)
FONT_DIR = os.environ.get("FONT_DIR") or os.path.join(OUT, "fonts")
if not os.path.isfile(os.path.join(FONT_DIR, "Vazirmatn-Regular.ttf")):
    raise SystemExit(
        "Font files not found.\n"
        "Put Vazirmatn-Regular.ttf and Vazirmatn-Bold.ttf in ./fonts next to this script,\n"
        "or set FONT_DIR to the directory that holds them."
    )


def b64(name):
    with open(os.path.join(FONT_DIR, name), "rb") as f:
        return base64.b64encode(f.read()).decode()


CSS = """
@font-face{font-family:Vz;src:url(data:font/ttf;base64,%REG%) format('truetype');font-weight:400;font-display:swap}
@font-face{font-family:Vz;src:url(data:font/ttf;base64,%BOLD%) format('truetype');font-weight:700;font-display:swap}
*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#1c1c1e;--grey:#62626a;--paper:#fdfcfb;--c0:#3D6DA8;--c1:#4F7E63;--c2:#7B5FA6;--c3:#2F8CAD;--umb:%UMB%}
html,body{height:100%%}
body{background:var(--paper);color:var(--ink);font-family:Vz,Tahoma;overflow:hidden;direction:rtl}
#bar{position:fixed;top:0;right:0;width:0;height:4px;background:var(--ink);transition:width .35s;z-index:30}
#cap{position:fixed;top:3.2vh;right:8vw;left:8vw;font-size:clamp(18px,2.1vw,30px);font-weight:700;
  text-align:center;opacity:0;transition:opacity .5s}
/* ---- overlays: hero / end ---- */
.ov{position:fixed;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;
  z-index:40;background:var(--paper);padding:0 6vw}
.ov.on{display:flex}
.ov h1{font-size:clamp(38px,6vw,88px);animation:pop .7s}
.ov p{font-size:clamp(17px,2vw,28px);color:var(--grey);margin-top:4vh;text-align:center;animation:pop .7s .25s}
.ov .go{font-size:clamp(14px,1.4vw,19px);color:var(--grey);margin-top:6vh}
/* cover identity: name, role, headline, last-edit date */
.ov .kick{font-size:clamp(12px,1.4vw,21px);color:var(--grey);font-weight:700;
  letter-spacing:.07em;margin-top:0;animation:pop .7s .1s}
.ov .lead{font-size:clamp(16px,1.85vw,26px);color:var(--ink);margin-top:2.4vh;animation:pop .7s .2s}
.ov .sub{font-size:clamp(12.5px,1.4vw,19px);color:var(--grey);margin-top:2.2vh;max-width:70ch;animation:pop .7s .3s}
.ov .meta{font-size:clamp(11.5px,1.15vw,16px);color:var(--grey);margin-top:3.4vh;animation:pop .7s .55s}
/* contact link on the closing page */
#li{display:inline-flex;align-items:center;gap:.5em;margin-top:4.2vh;padding:.6em 1.5em;
  border-radius:999px;background:#0A66C2;color:#fff;text-decoration:none;font-weight:700;
  font-size:clamp(13px,1.5vw,20px);animation:pop .7s .4s}
#li:hover{background:#084f97}
#hlist{list-style:none;display:flex;flex-direction:column;gap:1.6vh;margin-top:4vh}
.hitem{display:flex;align-items:center;gap:.7em;font-size:clamp(14px,1.9vw,24px);font-weight:700;
  animation:pop .7s .4s}
.hitem i{width:13px;height:13px;border-radius:50%;flex:0 0 auto}
.hitem em{font-style:normal;font-weight:400;color:var(--grey);font-size:.76em}
@keyframes pop{from{opacity:0;transform:scale(.96)}to{opacity:1;transform:none}}
/* ---- product pages ---- */
#prod h1{font-size:clamp(26px,4vw,54px)}
#prod .ptag{font-size:clamp(14px,1.8vw,23px);color:var(--grey);margin-top:3vh;max-width:64ch}
#pgrecipe{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:.6em;margin-top:4.2vh}
.rpill{padding:.34em 1.05em;border-radius:999px;color:#fff;font-weight:700;
  font-size:clamp(12px,1.5vw,19px);background:var(--umb);white-space:nowrap}
.rop{font-size:clamp(15px,1.9vw,25px);font-weight:700;color:var(--grey)}
#pgpoints{list-style:none;margin-top:4.2vh;display:flex;flex-direction:column;gap:1.5vh;
  max-width:76ch;text-align:right}
#pgpoints li{font-size:clamp(12.5px,1.45vw,18px);line-height:1.6;padding-right:1.15em;position:relative}
#pgpoints li::before{content:'•';position:absolute;right:0;color:var(--grey)}
#pgrole{margin-top:3.4vh;font-size:clamp(12.5px,1.4vw,18px);font-weight:700;text-align:center}

/* ---- graph: tall lanes; each branch carries its own event chip above the bar.
   NOTE: no vh units here — build rewrites every 'Nvh' into calc(N * var(--u)) and
   --u is 1dvh where supported, so fixed chrome must use % of viewport height.
   top:18% clears the fixed caption (top 3.2%, ~5% tall) so nothing rides under it. ---- */
#graph{position:fixed;top:18%;right:6vw;left:6vw;height:60%}
.row{display:flex;align-items:stretch;height:25%;gap:1.4vw}
.key{flex:0 0 auto;display:flex;flex-direction:column;justify-content:center;align-items:flex-end;gap:.3vh;line-height:1.3}
/* labels hug the LEFT edge of the column; alignKeys() gives all four rows one width,
   so every bar starts at the same x and all four branches come out equal */
.key b,.key em{text-align:left;white-space:normal;overflow-wrap:anywhere}
.key b{font-size:clamp(15px,1.7vw,23px);font-weight:700}
.key em{font-size:clamp(10px,1.05vw,14px);color:var(--grey)}
.lane{position:relative;flex:1;height:100%;border-bottom:1px solid rgba(28,28,30,.10)}
.bar{position:absolute;bottom:0;right:0;left:0;height:5px;background:var(--k);
  border-radius:3px;transition:height .85s cubic-bezier(.35,.1,.9,.3)}
/* event chips live inside their own branch lane, pinned at the far (time) end */
.evs{position:absolute;inset:0;pointer-events:none}
.echip{position:absolute;left:0;display:flex;align-items:center;gap:.45em;width:max-content;max-width:76%;
  padding:.3em .8em;border-radius:10px;background:rgba(253,252,251,.92);
  box-shadow:0 1px 4px rgba(28,28,30,.08);
  font-size:clamp(10.5px,1.1vw,15px);font-weight:700;line-height:1.35;color:var(--ink);
  opacity:.34;transition:opacity .5s}
.echip i{width:8px;height:8px;border-radius:50%;flex:0 0 auto}
.echip.now{opacity:1}
.row.act .lane::after{content:'';position:absolute;left:0;bottom:calc(var(--bh,4px) - 4px);
  width:11px;height:11px;border-radius:50%;background:var(--k)}
.row.act .bar{box-shadow:0 0 0 4px rgba(28,28,30,.07)}
#axis{position:absolute;left:0;right:0;bottom:-10vh;display:flex;align-items:center;gap:1.6vw;
  font-size:clamp(11px,1.1vw,15px);color:var(--grey)}
#axis i{flex:1;height:1px;background:rgba(28,28,30,.22);position:relative}
#axis i::after{content:'';position:absolute;left:0;top:-3.5px;border-top:4px solid transparent;
  border-bottom:4px solid transparent;border-right:7px solid rgba(28,28,30,.38)}
/* year printed in the middle of the grey axis line (paper background cuts the line) */
#yr{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:none;
  background:var(--paper);padding:0 .85em;font-weight:700;color:var(--ink);
  font-size:1.15em;letter-spacing:.02em;white-space:nowrap}
/* phones: the axis is hidden, so the year gets its own slim line above the pager */
#yrbar{display:none}
/* thought step dim, umbrella overlay */
body.dimmed .bar,body.dimmed .key,body.dimmed .chip{filter:grayscale(1);opacity:.32;transition:opacity .8s,filter .8s}
#umb{position:absolute;inset:-16px -8px 0 -8px;padding-right:31%%;background:rgba(44,49,56,.82);border-radius:20px;
  backdrop-filter:blur(7px);transform:translateY(112%%);opacity:0;transition:opacity .25s;z-index:6}
#umb.on{transform:none;opacity:1;transition:transform .95s cubic-bezier(.3,.6,.2,1),opacity .6s}
#umb b{display:block;color:#f4f3f0;font-size:clamp(24px,3.2vw,44px);font-weight:700;text-align:center;margin-top:6vh}
#umb span{display:block;color:rgba(244,243,240,.75);font-size:clamp(14px,1.5vw,20px);text-align:center;margin-top:2vh}
#combo{position:absolute;right:56%%;top:-2vh;bottom:7vh;width:2.5px;background:#14161a;display:none;z-index:9}
#combo.on{display:block}
#combo b{position:absolute;bottom:.6vh;left:-6vw;background:var(--paper);padding:.25em 1.1em;border-radius:10px;
  font-size:clamp(11px,1.2vw,16px);font-weight:700;white-space:nowrap;box-shadow:0 1px 5px rgba(0,0,0,.14)}
/* chrome */
#hint{position:fixed;bottom:2.4vh;right:4vw;font-size:13px;color:var(--grey);z-index:20;transition:opacity 1s}
#hint.gone{opacity:0}
#pager{position:fixed;bottom:2.4vh;left:4vw;font-size:14px;color:var(--grey);z-index:20}
/* ---- home button: back to the cover ---- */
#home{position:fixed;top:2.6vh;left:3vw;z-index:45;font-family:inherit;
  font-size:clamp(11px,1.05vw,14px);font-weight:700;color:var(--ink);
  background:rgba(253,252,251,.88);border:1px solid rgba(28,28,30,.18);border-radius:999px;
  padding:.45em 1.05em;cursor:pointer;backdrop-filter:blur(4px);
  opacity:0;pointer-events:none;transition:opacity .35s}
#home.show{opacity:1;pointer-events:auto}
#home:hover{border-color:rgba(28,28,30,.5)}
@media (max-width:700px){
  /* phone: the stacked deck scrolls; let the browser scroll back to the top */
  html,body{overflow:auto}
  /* fixed chrome on phones: caption + home button occupy ~top 12%. The graph is static
     and scrolls, so it starts BELOW that band — otherwise the first branch title rides
     under the home button. Padding (not margin) keeps #umb inset:0 covering the lanes. */
  /* phones: caption starts at 8vh and can wrap to two lines (~8vh tall), so branches
     start at 18vh. The four rows then spread over the rest of the viewport, so the deck
     fills the screen instead of leaving a dead zone under the last branch. */
  /* phones: #graph is static here, so left/right:6vw no longer applies — the horizontal
     margin must be padding, otherwise bars and labels bleed into the screen edges */
  #graph{top:auto;height:auto;position:static;padding-top:18vh;padding-bottom:15vh;margin-top:0;
    padding-left:5vw;padding-right:5vw;
    min-height:100vh;display:flex;flex-direction:column;justify-content:space-between}
  /* year line on phones: axis is hidden there, so the year sits on its own hairline */
  #yrbar{display:flex;align-items:center;gap:3vw;position:fixed;left:5vw;right:5vw;bottom:8vh;
    z-index:20;font-size:13px;color:var(--grey);transition:opacity .3s}
  #yrbar.off{opacity:0}
  #yrbar i{flex:1;height:1px;background:rgba(28,28,30,.22)}
  #yrbar b{font-weight:700;color:var(--ink);font-size:15px;white-space:nowrap}
  /* the desktop axis is absolute inside a static, stacked graph — hide it on phones and
     let #yrbar carry the year, otherwise a second stray year floats mid-page */
  #axis{display:none}
  .row{flex:1 1 auto;flex-direction:column;align-items:stretch;justify-content:center;gap:0;margin-bottom:0}
  .key{flex-direction:row;align-items:center;justify-content:flex-start;gap:.5em;max-width:100%}
  .key em{display:none}
  /* flex:none is the critical fix: the desktop rule .lane{flex:1} overrides the lane's
     height in the column layout, collapsing it to ~0px so the growing bar rises up
     over the label text. flex:none keeps flex:1 away and the lane keeps its height. */
  .lane{flex:none;height:auto;min-height:2.6vh;border-bottom:none;overflow:hidden}
  .bar{position:static;height:8px !important;border-radius:4px}
  .evs{position:static;display:flex;flex-direction:column;align-items:flex-start;gap:.7vh;padding-top:1vh}
  .echip{position:static !important;bottom:auto !important;left:auto !important;width:auto;max-width:100%;font-size:13px;
    background:rgba(28,28,30,.045);border-radius:10px;padding:.4em .8em}
  .row.act .lane::after{display:none}
  /* phones: the caption must sit BELOW the home button, not on the same band.
     8vh clears the button (top 1.4vh, ~5vh tall) and still leaves the branches below. */
  #cap{top:8vh;right:5vw;left:5vw;font-size:17px}
  #hint{display:none}
  #pager{bottom:2.6vh;font-size:15px}
  #home{top:1.4vh;left:3vw;font-size:12px}
  #umb{padding-right:0}
  #umb{padding:4vh 3vw;display:flex;flex-direction:column;justify-content:center}
  /* the desktop inset(-16px -8px ...) would stick out of the document and create a
     horizontal scrollbar on phones — clamp it to the viewport */
  #graph{clip-path:inset(0)}
  #umb{inset:0}
  #umb b{margin-top:0}
  #umb span{margin-top:2.4vh}
  #combo b{left:auto;right:auto;width:max-content;max-width:60vw}
}
@media print{
  @page{size:A4 landscape;margin:0}
  #bar,#home,#hint,#pager{display:none!important}
  .ov{display:none!important}
  #graph{position:static;height:auto}
}
"""


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


import re
CSS = re.sub(r"(\d+(?:\.\d+)?)vh", r"calc(\1 * var(--u))", CSS)
UA = ":root{--u:1vh}\n@supports (height:100dvh){:root{--u:1dvh}}\n"
css = (UA + CSS.replace("%REG%", b64("Vazirmatn-Regular.ttf"))
          .replace("%BOLD%", b64("Vazirmatn-Bold.ttf"))
          .replace("%UMB%", UMB_COLOR)
          .replace("%%", "%"))   # CSS has no %-formatting: unescape the doubled percent signs

rows = []
for r, L in enumerate(LANES):
    rows.append(
        f'<div class="row" data-r="{r}" style="--k:{L["color"]}">'
        f'<div class="key"><b>{esc(L["key"])}</b><em>{esc(L["sub"])}</em></div>'
        f'<div class="lane"><div class="bar" style="background:{L["color"]}"></div>'
        f'<div class="evs"></div></div></div>')

hlist = "".join(
    f'<li class="hitem"><i style="background:{L["color"]}"></i>{esc(L["key"])}'
    f'<em>{esc(L["sub"])}</em></li>' for L in LANES)

js = open(os.path.join(OUT, "timeline.js"), encoding="utf-8").read()

html = (
    '<!DOCTYPE html><html dir="rtl" lang="fa"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="mobile-web-app-capable" content="yes">'
    '<title>' + OWNER['name'] + ' | ' + OWNER['lead'] + '</title>'
    '<meta name="description" content="' + OWNER['name'] + ' — ' + OWNER['lead'] + '">'
    '<meta property="og:title" content="' + OWNER['name'] + ' | ' + OWNER['lead'] + '">'
    '<meta property="og:description" content="مروری بر مسیر حرفه‌ای: چهار شاخه‌ی موازی که در پایان زیر چتر مهندسی سیستم جمع شدند.">'
    '<style>' + css + '</style></head><body>'
    '<div id="bar"></div>'
    '<button id="home" type="button" title="صفحه‌ی اول" aria-label="بازگشت به صفحه‌ی اول">⌂ صفحه‌ی اول</button>'
    '<div id="hero" class="ov">'
    '<h1>' + OWNER['name'] + '</h1>'
    '<p class="lead">' + OWNER['lead'] + '</p>'
    '<p class="sub">مروری بر مسیر حرفه‌ای: چهار شاخه‌ی موازی که در پایان زیر چتر مهندسی سیستم جمع شدند.</p>'
    '<ul id="hlist">' + hlist + '</ul>'
    '<p class="meta">آخرین ویرایش: ' + OWNER['last_edit'] + '</p>'
    '<p class="go">کلیک، اسپیس یا کلید ← برای شروع</p></div>'
    '<div id="cap"></div>'
    '<div id="graph"><div id="umb"><b>مهندسی سیستم</b><span>چتری که هر چهار شاخه را در بر می‌گیرد؛ از نیازمندی تا نگه‌داشت</span></div>'
    '<div id="combo"><b>ترکیب شاخه‌ها</b></div>' + "".join(rows) +
    '<div id="axis"><span>از دانشگاه فردوسی</span><i></i><span>تا امروز</span><b id="yr"></b></div></div>'
    '<div id="yrbar"><i></i><b id="yrp"></b><i></i></div>'
    '<div id="prod" class="ov"><h1 id="pgtitle"></h1><p class="ptag" id="pgtag"></p>'
    '<div id="pgrecipe"></div><ul id="pgpoints"></ul><p id="pgrole"></p></div>'
    '<div id="end" class="ov"><h1>پایان</h1>'
    '<p>' + OWNER['name'] + ' — ' + OWNER['lead'] + '</p>'
    '<a id="li" href="' + OWNER['linkedin'] + '" target="_blank" rel="noopener">'
    '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" aria-hidden="true">'
    '<path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg>'
    ' لینکدین: hamed-davandeh</a>'
    '<p class="meta">آخرین ویرایش: ' + OWNER['last_edit'] + '</p></div>'
    '<div id="hint">کلیک، اسپیس یا کلید ← : بعدی &nbsp;·&nbsp; کلید → : قبلی &nbsp;·&nbsp; Home : صفحه‌ی اول &nbsp;·&nbsp; f : تمام‌صفحه</div>'
    '<div id="pager"></div>'
    '<script>var STEPS=' + json.dumps(STEPS, ensure_ascii=False) + ';var LANES=' +
    json.dumps(LANES, ensure_ascii=False) + ';</script>'
    '<script>' + js + '</script></body></html>')

open(HTML, "w", encoding="utf-8").write(html)
print("html:", HTML, os.path.getsize(HTML), "bytes | steps:", len(STEPS), "lanes:", len(LANES))