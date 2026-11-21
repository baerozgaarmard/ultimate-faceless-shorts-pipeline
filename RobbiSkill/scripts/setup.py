#!/usr/bin/env python3
"""One-time setup, safe to re-run. Prints 'All set' when the machine can make videos.
Checks Python 3.10+, ffmpeg, Chrome; installs playwright + numpy + pillow; downloads Playwright's Chromium (the renderer).
Works on Windows, macOS and Linux (plain Python, no bash).
"""
import os, platform, shutil, subprocess, sys

ok = True
def say(k, v): print(f'{k:<12} {v}')

if sys.version_info >= (3, 10): say('python', f'ok ({platform.python_version()})')
else: say('python', 'MISSING: need Python 3.10+ (python.org)'); ok = False

if shutil.which('ffmpeg') and shutil.which('ffprobe'): say('ffmpeg', 'ok')
else:
    hint = {'Windows': 'winget install Gyan.FFmpeg', 'Darwin': 'brew install ffmpeg'}.get(platform.system(), 'sudo apt install ffmpeg')
    say('ffmpeg', f'MISSING: install it ({hint}), then open a NEW terminal'); ok = False

def chrome_path():
    c = [os.environ.get('CHROME', ''), r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
         os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
         '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/snap/bin/chromium']
    return next((p for p in c if p and os.path.exists(p)), None)
cp = chrome_path()
if cp: say('chrome', f'ok ({cp})')
else: say('chrome', 'not found: needed only for the automatic Google Flow mode (install Chrome, or use the manual prompts mode)')

def have(mod):
    try: __import__(mod); return True
    except Exception: return False
need = [m for m, mod in (('playwright', 'playwright'), ('numpy', 'numpy'), ('scipy', 'scipy'), ('pillow', 'PIL')) if not have(mod)]
if need:
    print('installing:', ' '.join(need))
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', *need])
    if r.returncode != 0:
        r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', *need])
    if r.returncode != 0: say('python-libs', 'FAILED: run  ' + sys.executable + ' -m pip install ' + ' '.join(need)); ok = False
if all(have(m) for m in ('playwright', 'numpy', 'scipy', 'PIL')): say('python-libs', 'ok')
else: ok = False

if have('playwright'):
    r = subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], capture_output=True, text=True)
    if r.returncode == 0: say('chromium', 'ok (renderer)')
    else: say('chromium', 'FAILED: ' + (r.stderr or r.stdout)[-300:]); ok = False

# optional: the built-in voice (only with  setup.py --voice ; about 850 MB, one time)
if '--voice' in sys.argv:
    import tarfile, urllib.request
    md = os.path.join(os.path.expanduser('~'), '.robbiskill', 'models'); os.makedirs(md, exist_ok=True)
    if not have('sherpa_onnx'):
        r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'sherpa-onnx']) .returncode or 0
        if r: subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--break-system-packages', 'sherpa-onnx'])
    for name, rel in (('kokoro-multi-lang-v1_0', 'tts-models'), ('sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8', 'asr-models')):
        if os.path.isdir(os.path.join(md, name)): say(name, 'already there'); continue
        tgz = os.path.join(md, name + '.tar.bz2'); print('downloading', name, '...')
        try:
            urllib.request.urlretrieve(f'https://github.com/k2-fsa/sherpa-onnx/releases/download/{rel}/{name}.tar.bz2', tgz)
            with tarfile.open(tgz) as tf: tf.extractall(md)
            os.remove(tgz); say(name, 'ok')
        except Exception as e: say(name, f'FAILED ({e}). The voice option is not available; use your own recording.'); 
    say('voice-models', md)
print('All set' if ok else 'Fix the items above, then run setup.py again.')
sys.exit(0 if ok else 1)
