#!/usr/bin/env python3
"""Proves the whole pipeline on this computer (about 2-3 minutes): copies the bundled example, checks it, aligns it to its voiceover,
mixes the sound, renders a draft, makes a contact sheet. Prints SELFTEST PASSED.   python selftest.py"""
import os, shutil, subprocess, sys, tempfile
SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PY = sys.executable
T = os.path.join(tempfile.gettempdir(), 'robbiskill_selftest')
shutil.rmtree(T, ignore_errors=True); shutil.copytree(os.path.join(SK, 'example'), T)
def run(*a):
    print('>', ' '.join(os.path.basename(x) if os.path.isabs(x) else x for x in a), flush=True)
    r = subprocess.run([PY, *a], capture_output=True, text=True); print(r.stdout[-600:]); 
    if r.returncode: print(r.stderr[-1500:]); print('SELFTEST FAILED'); sys.exit(1)
run(os.path.join(SK, 'scripts', 'align.py'), T)
run(os.path.join(SK, 'scripts', 'check_timeline.py'), T)
run(os.path.join(SK, 'scripts', 'mix.py'), T)
run(os.path.join(SK, 'engine', 'render.py'), os.path.join(T, 'timeline.json'), '--draft', '--out', os.path.join(T, 'renders', 'selftest.mp4'))
run(os.path.join(SK, 'scripts', 'sheet.py'), os.path.join(T, 'renders', 'selftest.mp4'), os.path.join(T, 'review'), '--step', '1')
out = os.path.join(T, 'renders', 'selftest.mp4')
d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip())
vol = subprocess.run(['ffmpeg', '-v', 'info', '-i', out, '-af', 'volumedetect', '-vn', '-f', 'null', '-'], capture_output=True, text=True).stderr
mean = [l for l in vol.splitlines() if 'mean_volume' in l]
if d < 10 or not mean or float(mean[0].split()[-2]) < -50: print('SELFTEST FAILED: video too short or silent'); sys.exit(1)
eb = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
li = [l for l in eb.splitlines() if l.strip().startswith('I:')]
lufs = float(li[-1].split()[1]) if li else -99
print(f'loudness {lufs:.1f} LUFS (target -14)')
if not -17 < lufs < -11: print('SELFTEST FAILED: loudness is off target'); sys.exit(1)
print(f'video {out} ({d:.1f} s) | contact sheet: {os.path.join(T, "review", "sheet_01.jpg")}\nOpen both and look at them.\nSELFTEST PASSED')
