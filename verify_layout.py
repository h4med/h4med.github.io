#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout verifier v2 for the timeline deck.
Desktop: chips are absolute inside lanes -> check containment + pairwise overlap.
Phone:   #graph scrolls; only in-viewport geometry vs fixed chrome (cap/pager) is checked."""
import os, sys
from playwright.sync_api import sync_playwright

HTML = "file://" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
STEPS_TOTAL = 22
CHECK_STEPS = list(range(1, STEPS_TOTAL + 1))
SIZES = [("phone-390x844", 390, 844), ("phone-360x740", 360, 740), ("phone-414x896", 414, 896),
         ("desktop-1440x900", 1440, 900)]

JS = r"""
() => {
  const R = e => { const b = e.getBoundingClientRect(); return {t:Math.round(b.top),b:Math.round(b.bottom),l:Math.round(b.left),r:Math.round(b.right)}; };
  const cap = document.getElementById('cap'), pager = document.getElementById('pager');
  const out = {mobile: window.matchMedia('(max-width:700px)').matches,
               cap: null, pager: R(pager), rows: [], vh: innerHeight};
  if (getComputedStyle(cap).opacity !== '0' && cap.textContent) out.cap = R(cap);
  [...document.querySelectorAll('.row')].forEach((row, idx) => {
    const lane = row.querySelector('.lane'), bar = row.querySelector('.bar');
    const chips = [...row.querySelectorAll('.echip')].filter(c => getComputedStyle(c).display !== 'none');
    out.rows.push({r: idx, lane: R(lane), bar: R(bar),
      chips: chips.map(c => ({txt: c.textContent.slice(0,22), rect: R(c), now: c.classList.contains('now')}))});
  });
  return out;
}
"""

def overlap(a, b):
    w = min(a['r'], b['r']) - max(a['l'], b['l'])
    h = min(a['b'], b['b']) - max(a['t'], b['t'])
    return (w * h) if (w > 0 and h > 0) else 0

def check(snap):
    issues = []
    mobile, vh = snap['mobile'], snap['vh']
    # fixed chrome: the caption sits at top:3.2% of viewport; anything under it is graph area
    CHROME_BOTTOM = int(vh * 0.075)
    for rec in snap['rows']:
        lane, bar = rec['lane'], rec['bar']
        if not mobile and (bar['b'] - bar['t']) < 6:
            continue  # transition still animating the bar height: geometry not final
        vis = [c for c in rec['chips'] if c['rect']['t'] >= 0 and c['rect']['b'] <= vh]
        for c in rec['chips']:
            cr = c['rect']
            if cr['b'] < 0 or cr['t'] > vh:
                continue  # scrolled off-screen on phone: fine
            if not mobile:
                if cr['t'] < min(CHROME_BOTTOM, lane['t']) - 1:
                    issues.append(f"row{rec['r']} chip '{c['txt']}' escapes into fixed chrome")
                if cr['b'] > bar['t'] + 1:
                    issues.append(f"row{rec['r']} chip '{c['txt']}' overlaps bar")
            # visible chip vs caption / pager (fixed chrome on both layouts)
            if snap['cap'] and overlap(cr, snap['cap']) > 30:
                issues.append(f"row{rec['r']} chip '{c['txt']}' overlaps caption")
            if overlap(cr, snap['pager']) > 30:
                issues.append(f"row{rec['r']} chip '{c['txt']}' overlaps pager")
        for i in range(len(vis)):
            for j in range(i+1, len(vis)):
                a, b = vis[i]['rect'], vis[j]['rect']
                if overlap(a, b) > 20:
                    issues.append(f"row{rec['r']} chips overlap: '{vis[i]['txt']}' / '{vis[j]['txt']}'")
        # cross-row collisions among visible chips (desktop rows are adjacent bands)
        for other in snap['rows']:
            if other['r'] == rec['r']: continue
            for c in vis:
                for oc in [x for x in other['chips'] if x['rect']['t'] >= 0 and x['rect']['b'] <= vh]:
                    if overlap(c['rect'], oc['rect']) > 20:
                        issues.append(f"row{rec['r']} chip '{c['txt']}' hits row{other['r']} chip '{oc['txt']}'")
    return issues

results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, vw, vh in SIZES:
        page = browser.new_page(viewport={'width': vw, 'height': vh})
        page.goto(HTML)
        page.wait_for_timeout(700)
        for s in CHECK_STEPS:
            page.evaluate(f"show({s-1})")
            page.wait_for_timeout(1500)
            vis = page.evaluate("() => ({hero: document.getElementById('hero').classList.contains('on'), end: document.getElementById('end').classList.contains('on'), prod: document.getElementById('prod').classList.contains('on'), umb: document.getElementById('umb').classList.contains('on')})")
            if any(vis.values()):
                results.append((name, s, ['skip-overlay']))
                continue
            snap = page.evaluate(JS)
            results.append((name, s, check(snap)))
        # end page: linkedin link
        page.evaluate(f"show({STEPS_TOTAL-1})")
        page.wait_for_timeout(400)
        href = page.evaluate("() => { const a=document.getElementById('li'); return a ? a.href : null; }")
        results.append((name, 'end-link', [] if href and 'hamed-davandeh' in href else ['MISSING LINKEDIN']))
        # step 21 content: ChirpStack + UNS present, Billing gone
        page.evaluate("show(20)")
        page.wait_for_timeout(600)
        txt = page.evaluate("() => document.body.innerText")
        ok = ('ChirpStack' in txt) and ('معماری UNS' in txt) and ('Billing' not in txt)
        results.append((name, 'step21-content', [] if ok else ['CONTENT MISMATCH']))
        page.close()
    browser.close()

bad = [(n,s,i) for n,s,i in results if i and i[0] != 'skip-overlay']
for n,s,i in bad:
    print(f"[FAIL] {n} step {s}:")
    for x in i: print('   -', x)
print(f"\n{len(results)} checks, {len(bad)} failures")
sys.exit(1 if bad else 0)
