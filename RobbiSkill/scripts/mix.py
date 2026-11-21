#!/usr/bin/env python3
"""Sound for the video: your voiceover + soft procedural sound effects + a quiet music bed, all made with numpy (no downloads, no licences).

  python mix.py <project> [--music dark|drive|calm|bed|tense|none|path/to/track.mp3] [--sfx-gain 1.0]

Writes audio/soundtrack.wav and sets "soundtrack" in timeline.json. Effects are placed automatically from the shot types:
cut -> soft whoosh; impact flash -> low thud; numbers/counters -> rising tick-up and pop; clock/stopwatch -> tick-tock; fire -> hiss;
typed card -> quiet key taps; bars/market -> falling sweep; confetti -> sparkle. The music ducks under the voice (smooth side-chain). Final loudness is set to -14 LUFS (YouTube) with a -1.5 dB true-peak limit.
"""
import argparse, json, os, subprocess, sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('--music', default=None); ap.add_argument('--sfx-gain', type=float, default=1.0)
a = ap.parse_args(); P = a.project; SR = 48000
tlp = os.path.join(P, 'timeline.json'); tl = json.load(open(tlp, encoding='utf-8'))
voice = tl.get('audio'); voice = voice if not voice or os.path.isabs(voice) else os.path.join(P, voice)
if not voice or not os.path.exists(voice): sys.exit('voiceover missing (set "audio" in timeline.json)')
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', voice, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
vox = np.frombuffer(raw, dtype=np.float32).copy(); N = len(vox) + SR // 5
rng = np.random.default_rng(5)
def lp(x, f, o=2): b, aa = signal.butter(o, min(f, SR / 2 - 100) / (SR / 2), 'low'); return signal.lfilter(b, aa, x)
def bp(x, f0, f1, o=2): b, aa = signal.butter(o, [f0 / (SR / 2), f1 / (SR / 2)], 'band'); return signal.lfilter(b, aa, x)
def tt(d): return np.arange(int(d * SR)) / SR
def env(n, att=0.004, rel=5.0): e = np.ones(n); na = max(1, int(att * SR)); e[:na] = np.linspace(0, 1, na); e[na:] = np.exp(-np.linspace(0, rel, n - na)) if n > na else 1; return e
def whoosh(d=0.35): n = int(d * SR); x = bp(rng.standard_normal(n), 300, 2400); sw = np.sin(np.pi * np.linspace(0, 1, n)) ** 2; return lp(x * sw, 3500) * 0.35
def thud(): t = tt(0.5); f = 90 * np.exp(-t * 7) + 38; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.003, 6) * 0.9
def pop(f=520): t = tt(0.16); return np.sin(2 * np.pi * f * np.exp(-t * 9) * t) * env(len(t), 0.002, 8) * 0.5
def tick(f=1100, g=0.18): t = tt(0.05); return np.sin(2 * np.pi * f * t) * env(len(t), 0.001, 12) * g
def riser(d): t = tt(d); f = 260 + 700 * (t / d) ** 2; return lp(np.sin(2 * np.pi * np.cumsum(f) / SR), 2600) * np.minimum(1, t / 0.2) * 0.14 * np.exp(-((t - d) ** 2) * 0)
def hiss(d=0.8): n = int(d * SR); return lp(bp(rng.standard_normal(n), 800, 4000), 3800) * env(n, 0.05, 3) * 0.25
def fall(d=1.2): t = tt(d); f = 900 * np.exp(-t * 1.6) + 120; return lp(np.sin(2 * np.pi * np.cumsum(f) / SR), 1800) * np.exp(-t * 1.2) * 0.22
def sparkle(): t = tt(0.5); x = sum(np.sin(2 * np.pi * f * t) * env(len(t), 0.001, 8 + i) for i, f in enumerate((1568, 2093, 2637))) / 3; return lp(x, 4200) * 0.25
def key(): t = tt(0.04); return lp(rng.standard_normal(len(t)) * env(len(t), 0.0005, 14), 2800) * 0.1

def coin(): t = tt(0.35); return (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t) * (t > 0.07)) * env(len(t), 0.001, 7) * 0.22
def flip(): n = int(0.14 * SR); return lp(bp(rng.standard_normal(n), 1500, 6000), 5000) * env(n, 0.002, 7) * 0.3
def stamp(): th = thud() * 0.9; cl = lp(bp(rng.standard_normal(int(0.12 * SR)), 300, 3000), 3000) * env(int(0.12 * SR), 0.001, 9) * 0.5; th[: len(cl)] += cl; return th
def swoosh_up(): n = int(0.5 * SR); x = bp(rng.standard_normal(n), 500, 5000); sw = np.linspace(0, 1, n) ** 2 * np.linspace(1, 0, n) ** .5; return lp(x * sw, 6000) * 0.4
def snap(): n = int(0.09 * SR); return lp(bp(rng.standard_normal(n), 900, 4500), 4500) * env(n, 0.001, 10) * 0.28
def boom(): t = tt(1.4); f = 60 * np.exp(-t * 2.5) + 32; return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2) + lp(rng.standard_normal(len(t)), 300) * np.exp(-t * 4) * .4) * 0.9
def bell(): t = tt(1.6); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate((880, 1760, 2637))) * 0.12
sfx = np.zeros(N)
def put(x, t, g=1.0):
    i = int(t * SR); 
    if i < 0 or i >= N: return
    j = min(N, i + len(x)); sfx[i:j] += x[: j - i] * g * a.sfx_gain

t0 = 0.0
for si, sh in enumerate(tl['shots']):
    d = float(sh['duration']); ty = sh.get('type', 'scene')
    if si > 0: put(whoosh(), max(0, t0 - 0.12), 0.8)
    if sh.get('flash'): put(thud(), t0, 0.9)
    if ty in ('numbers', 'triptych', 'market', 'chart'):
        for it in sh.get('items', []):
            st = float(it.get('start', 0.3)); put(pop(), t0 + st, 0.8)
            if it.get('counter'): put(riser(float(it['counter'].get('dur', 1.2))), t0 + st, 1.0)
        for o in sh.get('objects', []):
            if o.get('kind') == 'fire': put(hiss(min(1.2, d)), t0 + 0.3, 0.7)
            if o.get('kind') == 'stopwatch':
                for k in range(int(float(o.get('dur', 3)) * 2)): put(tick(900 if k % 2 else 1300), t0 + float(o.get('start', 0)) + k * 0.5, 0.8)
        if ty == 'market': put(fall(min(2.5, d)), t0 + 0.2, 0.9)
        if ty == 'chart':
            for b in sh.get('chart', {}).get('bars', []): put(pop(380), t0 + float(b.get('start', 0.5)) + 0.6, 0.7)
    if ty == 'card':
        txt = sh.get('text', ''); st = float(sh.get('start', 0.3)); cps = max(14, len(txt) / max(0.6, d - st - 0.7))
        for k in range(0, len(txt), 2): put(key(), t0 + st + k / cps, 1.0)
    for l in sh.get('layers', []) + [c for p in sh.get('panels', []) for c in p.get('layers', [])]:
        st = t0 + float(l.get('start', 0)); k = l.get('kind', 'text'); ent = l.get('in', 'pop')
        if k == 'stamp' or ent == 'stamp': put(stamp(), st, 1.0)
        elif k == 'cash': put(coin(), st + 0.1, 0.8); put(coin(), st + 0.22, 0.6)
        elif k == 'calendar':
            for q in l.get('steps', [])[1:]: put(flip(), t0 + float(q.get('at', 0)), 0.9)
        elif k == 'text' and (l.get('text') or l.get('counter')):
            put(pop(640 if len(l.get('text', '')) < 14 else 480), st, 0.55 if not l.get('counter') else 0.7)
            if l.get('counter'): put(riser(float(l['counter'].get('dur', 1.2))), st, 1.0)
        elif k in ('balloon', 'fire', 'stopwatch', 'ekg', 'bars', 'poly', 'doc', 'pin', 'inset'): put(swoosh_up() if k in ('inset', 'doc', 'pin') else pop(420), st, 0.6)
        if k == 'fire': put(hiss(min(1.2, d)), st, 0.6)
    for c in sh.get('chars', []):
        if c.get('enter'): put(snap(), t0 + float(c.get('enterAt', 0.1)), 0.8)
    for f in sh.get('fx', []):
        k = f if isinstance(f, str) else f.get('kind')
        if k == 'confetti': put(sparkle(), t0 + 0.2, 0.9)
        if k == 'bills': put(sparkle(), t0 + 0.1, 0.5)
    for o in sh.get('overlays', []):
        if o.get('kind') in ('tag', 'lower', 'label'): put(pop(700), t0 + float(o.get('start', 0)), 0.5)
        if o.get('kind') == 'clock':
            for k in range(int((float(o.get('end', d)) - float(o.get('start', 0))) * 3)): put(tick(1500, 0.1), t0 + float(o.get('start', 0)) + k / 3, 0.6)
    t0 += d

mus = a.music or tl.get('music') or 'dark'
music = np.zeros(N)
if mus == 'none': pass
elif mus in ('dark', 'drive', 'calm', 'bed', 'tense'):
    mus2 = {'bed': 'calm', 'tense': 'dark'}.get(mus, mus)
    BPM = {'dark': 84, 'drive': 104, 'calm': 72}[mus2]; beat = 60.0 / BPM; t = np.arange(N) / SR
    N2 = {'dark': [(57, 0), (53, 0), (48, 0), (55, 0)], 'drive': [(57, 0), (50, 0), (53, 0), (52, 0)], 'calm': [(48, 0), (55, 0), (53, 0), (52, 0)]}[mus2]  # root MIDI per bar (minor feel)
    mf = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    def saw(f, d, det=0.004):
        tt_ = np.arange(int(d * SR)) / SR; return sum(2 * ((tt_ * f * (1 + k * det)) % 1) - 1 for k in (-1, 0, 1)) / 3
    def pluck(f, d=0.5):
        tt_ = np.arange(int(d * SR)) / SR; return (np.sin(2 * np.pi * f * tt_) + .35 * np.sin(2 * np.pi * 2 * f * tt_)) * np.exp(-tt_ * 7)
    def kick():
        tt_ = np.arange(int(.3 * SR)) / SR; f = 110 * np.exp(-tt_ * 22) + 42; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt_ * 9)
    def hat():
        n = int(.05 * SR); return hp_(rng.standard_normal(n), 7000) * np.exp(-np.arange(n) / SR * 70)
    def hp_(x, f): b_, a_ = signal.butter(2, f / (SR / 2), 'high'); return signal.lfilter(b_, a_, x)
    pad = np.zeros(N); bass = np.zeros(N); lead = np.zeros(N); perc = np.zeros(N)
    bars = int(N / SR / (beat * 4)) + 2
    minor = [0, 3, 7, 10]
    for bar in range(bars):
        root, _ = N2[bar % 4]; t0b = bar * beat * 4; i0 = int(t0b * SR)
        if i0 >= N: break
        # pad: root-third-fifth-seventh chord, slow swell, an octave up
        L = int(beat * 4.2 * SR); ch = sum(saw(mf(root + 12 + iv), beat * 4.2) for iv in (0, 3, 7)) * 0.05
        sw = np.minimum(1, np.arange(L) / (SR * beat * 1.6)) * np.minimum(1, (L - np.arange(L)) / (SR * beat * 1.0)); j = min(N, i0 + L); pad[i0:j] += (ch * sw)[: j - i0]
        # sub bass: root on 1, a push on the '& of 2'
        for off, dur_, g in ((0, beat * 1.4, 1.0), (beat * 2.5, beat * .9, .7)):
            tt_ = np.arange(int(dur_ * SR)) / SR; nb = (np.sin(2 * np.pi * mf(root - 12) * tt_) + .25 * np.sin(2 * np.pi * mf(root) * tt_)) * np.minimum(1, tt_ / .01) * np.exp(-tt_ * 1.6) * 0.34 * g
            i = i0 + int(off * SR); j = min(N, i + len(nb))
            if i < N: bass[i:j] += nb[: j - i]
        # arpeggio pluck, eighth notes, 3 notes cycling, quieter at the start of the video
        for k in range(8):
            iv = minor[[0, 2, 1, 2, 0, 3, 1, 2][k] % 4] + 24; pl = pluck(mf(root + iv)) * 0.12; i = i0 + int(k * beat * .5 * SR); j = min(N, i + len(pl))
            if i < N: lead[i:j] += pl[: j - i]
        # percussion
        if mus2 != 'calm' or bar % 2:
            for k in range(4):
                kk = kick() * (0.55 if mus2 == 'dark' else 0.7); i = i0 + int(k * beat * SR); j = min(N, i + len(kk))
                if i < N and (mus2 == 'drive' or k in (0, 2)): perc[i:j] += kk[: j - i]
        for k in range(8):
            h_ = hat() * (0.09 if k % 2 else 0.05); i = i0 + int(k * beat * .5 * SR); j = min(N, i + len(h_))
            if i < N and mus2 != 'calm': perc[i:j] += h_[: j - i]
    # simple reverb on pad+lead: decaying noise impulse, 1.8 s
    ir = rng.standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 2.4); ir = lp(ir, 5000); ir /= np.abs(ir).sum() * 0.12
    wet = signal.fftconvolve(lead + pad * .6, ir)[:N]
    energy = 0.55 + 0.45 * np.clip(t / 25.0, 0, 1)                    # builds over the first 25 s
    music = lp(pad, 2200, 2) * 1.0 + lp(bass, 400, 2) * 1.0 + lead * 0.8 + wet * 0.5 + perc * 0.8
    music = music * energy * 0.45
else:
    mp = mus if os.path.isabs(mus) else os.path.join(P, mus)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-i', mp, '-t', str(N / SR), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    mm = np.frombuffer(r, dtype=np.float32); music[: len(mm)] = mm[:N] * 0.35
hop = SR // 50; ve = np.abs(np.pad(vox, (0, N - len(vox))))[: (N // hop) * hop].reshape(-1, hop).mean(axis=1)
ve = np.convolve(ve, np.ones(8) / 8, 'same'); ve = np.clip(ve / (np.percentile(ve, 95) + 1e-9), 0, 1)
env_ = np.zeros_like(ve); c_ = 0.0                                              # side-chain: fast attack (~60 ms), slow release (~500 ms)
for i, v in enumerate(ve): c_ = v if v > c_ else c_ + (v - c_) * 0.04; env_[i] = c_
duck = np.repeat(1 - 0.5 * env_, hop); duck = np.pad(duck, (0, N - len(duck)), constant_values=1)
fade = np.minimum(1, np.minimum(np.arange(N) / (SR * 1.0), (N - np.arange(N)) / (SR * 1.5)))
v_ = np.pad(vox, (0, N - len(vox))); b_, a_ = signal.butter(2, 70 / (SR / 2), 'high'); v_ = signal.lfilter(b_, a_, v_)   # clean the low rumble of the voice
v_ = np.tanh(v_ * 1.6) / np.tanh(1.6)                                           # gentle level evening (soft clip) before loudness normalisation
mix = v_ * 1.0 + sfx * 0.7 + music * duck * fade
mix = lp(mix, 16000, 1)
os.makedirs(os.path.join(P, 'audio'), exist_ok=True); out = os.path.join(P, 'audio', 'soundtrack.wav')
mix = mix / (np.abs(mix).max() + 1e-9) * 0.9; tmp = out + '.tmp.wav'; wavfile.write(tmp, SR, (mix * 32767).astype(np.int16))
ln = subprocess.run(['ffmpeg', '-v', 'info', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
try:
    js = json.loads(ln[ln.rindex('{'):]); af = f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true"
except Exception: af = 'loudnorm=I=-14:TP=-1.5:LRA=7'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-af', af, '-ar', str(SR), '-ac', '1', out], check=True); os.remove(tmp)
tl['soundtrack'] = 'audio/soundtrack.wav'; json.dump(tl, open(tlp, 'w'), indent=1)
print(f'ok {out}: {len(vox)/SR:.1f} s voice, music={mus}, sfx cues placed')
