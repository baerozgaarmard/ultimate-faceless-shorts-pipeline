#!/usr/bin/env python3
"""Create a project folder:  python new_video.py <name> [--dir <parent>]   (default parent: ~/robbi-videos)"""
import argparse, json, os, shutil, sys
ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('--dir', default=os.path.join(os.path.expanduser('~'), 'robbi-videos'))
a = ap.parse_args()
P = os.path.join(a.dir, a.name)
if os.path.exists(P): sys.exit(f'{P} already exists: pick another name')
for d in ('plates', 'sprites', 'sheets', 'audio', 'renders', 'review'): os.makedirs(os.path.join(P, d))
json.dump({'name': a.name, 'stage': 'intake', 'voice_file': None, 'notes': []}, open(os.path.join(P, 'project.json'), 'w'), indent=1)
print(P)
