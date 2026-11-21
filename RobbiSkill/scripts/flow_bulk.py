#!/usr/bin/env python3
"""Generate images in Google Flow through YOUR Chrome (started with start_chrome.py), paced, resumable, saved to a folder.

  python flow_bulk.py --project "https://flow.google.com/project/XXXX" --prompts prompts.txt --out plates
Options: --cdp http://localhost:9222   --max N   --min-gap 6 --max-gap 12   --rest-every 20 --rest 120   --only 5-12   --dry

prompts.txt, one line per image:   plate_007 | the complete prompt as one paragraph
Already saved files are skipped, so stop and re-run any time. Never touches passwords: you sign in yourself.
Exit codes: 0 done, 2 Flow showed a limit/warning, 3 no image appeared, 4 cannot reach Chrome/Flow.
"""
import argparse, os, random, re, sys, time
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('--project'); ap.add_argument('--prompts', default='prompts.txt'); ap.add_argument('--out', default='plates')
ap.add_argument('--cdp', default='http://localhost:9222'); ap.add_argument('--max', type=int, default=9999)
ap.add_argument('--min-gap', type=float, default=6); ap.add_argument('--max-gap', type=float, default=12)
ap.add_argument('--rest-every', type=int, default=0); ap.add_argument('--rest', type=float, default=120)
ap.add_argument('--only'); ap.add_argument('--dry', action='store_true')
a = ap.parse_args()

items = []
for i, l in enumerate(open(a.prompts, encoding='utf-8').read().splitlines()):
    l = l.strip()
    if not l: continue
    parts = [p.strip() for p in l.split('|', 1)]
    if len(parts) == 2 and re.fullmatch(r'[A-Za-z0-9_-]+', parts[0]): items.append((parts[0].lower(), parts[1]))
    else: items.append((f'img_{i+1:03d}', l))
if a.only:
    lo, _, hi = a.only.partition('-'); lo = int(lo); hi = int(hi or lo)
    items = [it for it in items if lo <= int(re.sub(r'\D', '', it[0]) or 0) <= hi]
os.makedirs(a.out, exist_ok=True)
have = lambda n: any(os.path.exists(os.path.join(a.out, n + e)) for e in ('.jpg', '.png', '.webp'))
todo = [it for it in items if not have(it[0])][: a.max]
print(f'Prompts: {len(items)}, already done: {len(items)-len([i for i in items if not have(i[0])])}, to do now: {len(todo)}')
if a.dry or not todo:
    for n, p in todo[:5]: print(n, '|', p[:90], '...')
    sys.exit(0)
if not a.project: sys.exit('Need --project <Flow project URL>')

BAD = re.compile(r"unusual activity|too many requests|rate limit|limit reached|try again later|something went wrong|can't generate|violat", re.I)
LIST = "()=>[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>800).map(i=>i.src)"

with sync_playwright() as p:
    try:
        br = p.chromium.connect_over_cdp(a.cdp)
    except Exception as e:
        print('Cannot reach Chrome on', a.cdp, '- run start_chrome.py first.', e); sys.exit(4)
    ctx = br.contexts[0]; page = ctx.new_page(); page.goto(a.project, wait_until='domcontentloaded')
    try:
        box = page.get_by_role('textbox', name=re.compile('what do you want to create', re.I)); box.wait_for(timeout=90000)
    except Exception:
        print('The Flow prompt box did not appear. Sign in to Google in that Chrome window and open the project, then re-run.'); sys.exit(4)
    done = 0
    for name, prompt in todo:
        before = set(page.evaluate(LIST)); box.click(); page.keyboard.press('Control+A'); page.keyboard.press('Backspace')
        page.keyboard.insert_text(prompt); time.sleep(1)
        page.get_by_role('button', name=re.compile('start generation', re.I)).click()
        t0 = time.time(); fresh = None
        while time.time() - t0 < 180:
            time.sleep(3); now = page.evaluate(LIST); fresh = next((s for s in now if s not in before), None)
            if fresh: break
            if time.time() - t0 > 15 and BAD.search(page.evaluate('document.body.innerText.slice(0,4000)')):
                print('Flow shows a limit or warning. Stopping to protect your account.'); sys.exit(2)
        if not fresh: print(f'{name}: no image after 3 minutes. Stopping.'); sys.exit(3)
        r = ctx.request.get(fresh); ct = r.headers.get('content-type', '')
        ext = '.png' if 'png' in ct else '.webp' if 'webp' in ct else '.jpg'
        open(os.path.join(a.out, name + ext), 'wb').write(r.body()); done += 1
        print(f'ok {name} ({int(time.time()-t0)} s) [{done}/{len(todo)}]', flush=True)
        if done >= len(todo): break
        if a.rest_every and done % a.rest_every == 0: print(f'resting {a.rest:.0f} s'); time.sleep(a.rest + random.uniform(0, 30))
        else: time.sleep(random.uniform(a.min_gap, a.max_gap))
print('Finished this run. Re-run the same command to continue.')
