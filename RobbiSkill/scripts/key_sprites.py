#!/usr/bin/env python3
"""Cut a Flow character sheet (hero on flat green, left = mouth closed, right = mouth open) into engine sprites.

  python key_sprites.py sheets/boss_cheer.jpg boss_cheer [--project .] [--no-mouth]

Writes <project>/sprites/boss_cheer_closed.png, boss_cheer_open.png and boss_cheer.json (what timeline.json points to):
  "sprite": "sprites/boss_cheer.json"
--no-mouth: the sheet holds ONE figure (a prop, a crowd member, an animal): only the _closed file is made.
Removes the green background, despills the green edge, crops tight. Prints a warning if the green key looks dirty.
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser(); ap.add_argument('sheet'); ap.add_argument('name'); ap.add_argument('--project', default='.'); ap.add_argument('--no-mouth', action='store_true')
ap.add_argument('--size', type=float, default=0.98, help='scale of the on-screen height relative to the sheet pixels (1.0 = 640 px for a standing hero)')
a = ap.parse_args()
im = Image.open(a.sheet).convert('RGB'); W, H = im.size
arr = np.array(im).astype(float); r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
gd = g - np.maximum(r, b)
# the background green is the most common strongly-green colour: check it is really there
bg_share = float((gd > 90).mean())
if bg_share < 0.25: print(f'WARNING: only {bg_share:.0%} of the sheet is green. Regenerate it on a flat pure green (#00FF00) background.', file=sys.stderr)
alpha = np.clip((90 - gd) / 60, 0, 1)
arr[..., 1] = np.where(alpha < 1, g - np.clip(gd, 0, None) * 0.9, g)
rgba = Image.fromarray(np.dstack([arr.clip(0, 255), alpha * 255]).astype('uint8'), 'RGBA')
halves = [(0, 0, W, H)] if a.no_mouth else [(0, 0, W // 2, H), (W // 2, 0, W, H)]
outdir = os.path.join(a.project, 'sprites'); os.makedirs(outdir, exist_ok=True)
sizes = []
for nm, box in zip(('closed', 'open'), halves):
    c = rgba.crop(box); bb = c.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    if not bb: sys.exit(f'nothing found in the {nm} half: is the character on a green background?')
    c = c.crop(bb); c.save(os.path.join(outdir, f'{a.name}_{nm}.png')); sizes.append(c.size)
w, h = sizes[0]
info = {'closed': f'sprites/{a.name}_closed.png', 'ar': round(w / h, 4), 'h': round(h * a.size)}
if not a.no_mouth: info['open'] = f'sprites/{a.name}_open.png'
json.dump(info, open(os.path.join(outdir, f'{a.name}.json'), 'w'), indent=1)
print(f'ok {a.name}: {w}x{h}px, on-screen height ~{info["h"]}px at s=1')
