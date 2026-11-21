#!/usr/bin/env python3
"""Start YOUR normal Chrome with a debugging port so flow_bulk.py can drive it (you stay signed in to Google yourself).
  python start_chrome.py            opens Chrome at https://flow.google.com with port 9222
Uses a separate profile folder (~/.robbi-chrome) so your daily Chrome is untouched; sign in to Google there once.
"""
import os, subprocess, sys, platform
c = [os.environ.get('CHROME', ''), r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
     os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'), '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
     '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser']
chrome = next((p for p in c if p and os.path.exists(p)), None)
if not chrome: sys.exit('Chrome not found. Install Google Chrome or set CHROME=/path/to/chrome')
prof = os.path.join(os.path.expanduser('~'), '.robbi-chrome'); os.makedirs(prof, exist_ok=True)
subprocess.Popen([chrome, '--remote-debugging-port=9222', f'--user-data-dir={prof}', '--no-first-run', 'https://flow.google.com'],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **({'creationflags': 0x00000008} if platform.system() == 'Windows' else {}))
print('Chrome started on port 9222. Sign in to Google in that window if asked, open or create a Flow project, then continue.')
