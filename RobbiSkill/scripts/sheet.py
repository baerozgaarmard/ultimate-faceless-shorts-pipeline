#!/usr/bin/env python3
"""Contact sheets of a rendered video: a time-stamped frame every STEP seconds, 24 frames per sheet -> review/sheet_01.jpg ...
  python sheet.py <video.mp4> <outdir> [--step 1.0]"""
import argparse, os, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('outdir'); ap.add_argument('--step', type=float, default=1.0); a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.video], capture_output=True, text=True).stdout.strip())
per = max(1, int(24 * a.step)); k = 0; t = 0.0
while t < dur:
    k += 1; out = os.path.join(a.outdir, f'sheet_{k:02d}.jpg')
    vf = f"fps=1/{a.step},scale=384:-1,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.5,tile=6x4"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-t', str(24 * a.step), '-i', a.video, '-vf', vf, '-frames:v', '1', out], check=True)
    print(out); t += 24 * a.step
