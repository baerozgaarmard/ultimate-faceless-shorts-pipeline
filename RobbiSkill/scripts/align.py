#!/usr/bin/env python3
"""Fit the whole video to the voiceover.

  python align.py <project> [--audio audio/voiceover.mp3]

Needs: script.json {"lines":[{"text": "..."}]} and timeline.json where every shot has  "lines": [first, last]  (0-based line numbers it covers) and optionally  "at": 0.4  (start 40% into its first line, for two shots inside one line).
Does: finds the pauses in the voice, puts every line boundary on the nearest pause, then sets every shot's "duration" so each
shot starts when its first line starts. Shots with  "talk": true  characters get their mouths on for the whole shot.
Writes data/lines.json (line times) and updates timeline.json (a copy is kept as timeline.before_align.json).
"""
import argparse, json, os, re, shutil, subprocess, sys
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--audio'); ap.add_argument('--timings', help='timings.json from tts.py: exact line times, no pause guessing'); a = ap.parse_args()
P = a.project; SR = 16000
script = json.load(open(os.path.join(P, 'script.json'), encoding='utf-8')); lines = [l['text'] if isinstance(l, dict) else l for l in script['lines']]
tlp = os.path.join(P, 'timeline.json'); tl = json.load(open(tlp, encoding='utf-8'))
aud = a.audio or tl.get('audio') or 'audio/voiceover.mp3'; aud = aud if os.path.isabs(aud) else os.path.join(P, aud)
if not os.path.exists(aud): sys.exit(f'voiceover not found: {aud}')
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', aud, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768.0
dur = len(x) / SR; hop = SR // 100; n = len(x) // hop
rms = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1)); thr = max(0.006, 0.035 * rms.max()); loud = rms > thr
idx = np.where(loud)[0]; s0 = idx[0] / 100 if len(idx) else 0.0; e0 = (idx[-1] + 1) / 100 if len(idx) else dur
pauses = []; st = None
for f in range(int(s0 * 100), int(e0 * 100)):
    if not loud[f] and st is None: st = f
    if (loud[f] or f == int(e0 * 100) - 1) and st is not None:
        if (f - st) >= 14: pauses.append(((st + f) / 2 / 100, (f - st) / 100))   # (centre, length) of pauses >= 0.14 s
        st = None
w = [max(1, len(re.sub(r'[^A-Za-z0-9]', '', t))) + (4 if re.search(r'[,;:]$', t) else 0) + (7 if re.search(r'[.?!]$', t) else 0) for t in lines]
tot = sum(w); exp = []; c = s0
for wi in w: exp.append(c + (e0 - s0) * wi / tot); c += (e0 - s0) * wi / tot      # expected END of every line
ends = []; used = set(); prev = s0
TM = json.load(open(a.timings)) if a.timings else None
for i, e in enumerate(exp[:-1]):
    best = None
    for j, (cen, ln) in enumerate(pauses):
        if j in used or cen <= prev + 0.3: continue
        score = abs(cen - e) - 0.25 * min(ln, 0.6)
        if abs(cen - e) < 0.9 and (best is None or score < best[0]): best = (score, j, cen)
    if best: used.add(best[1]); ends.append(best[2]); prev = best[2]
    else: ends.append(max(e, prev + 0.3)); prev = ends[-1]
ends.append(e0)
L = []; s = s0
for i, e in enumerate(ends): L.append({'i': i, 'text': lines[i], 'start': round(s, 3), 'end': round(e, 3)}); s = e
if TM and len(TM) == len(lines):   # exact times from the generated voice: a line runs from its start to the start of the next one
    for i, q in enumerate(TM): L[i]['start'] = q['start'] if i else 0.0; L[i]['end'] = TM[i + 1]['start'] if i + 1 < len(TM) else dur
os.makedirs(os.path.join(P, 'data'), exist_ok=True)
json.dump({'duration': round(dur, 3), 'lines': L}, open(os.path.join(P, 'data', 'lines.json'), 'w'), indent=1)
shutil.copy(tlp, os.path.join(P, 'timeline.before_align.json'))
shots = tl['shots']; first = [sh.get('lines', [None])[0] for sh in shots]
if any(f is None for f in first): sys.exit('every shot needs "lines": [first, last] (the narrated lines it covers). Missing in: ' + ', '.join(sh.get('id', '?') for sh, f in zip(shots, first) if f is None))
starts = [0.0 if i == 0 else L[f]['start'] + float(shots[i].get('at', 0)) * (L[f]['end'] - L[f]['start']) for i, f in enumerate(first)]
for i, sh in enumerate(shots):
    end = starts[i + 1] if i + 1 < len(shots) else dur
    sh['duration'] = round(max(0.5, end - starts[i]), 3)
    for ch in sh.get('chars', []):
        if ch.get('talk'): ch['speakAt'] = [0.05, round(sh['duration'] - 0.08, 3)]
tl['audio'] = os.path.relpath(aud, P).replace('\\', '/')
json.dump(tl, open(tlp, 'w'), indent=1)
print(f'voiceover {dur:.2f} s, speech {s0:.2f}-{e0:.2f} s, {len(pauses)} pauses, {len(lines)} lines, {len(shots)} shots; shot lengths: ' + ' '.join(f"{sh['duration']:.1f}" for sh in shots))
