#!/usr/bin/env python3
"""RobbiSkill: generate the voiceover with a local TTS model (sherpa-onnx + Kokoro) and check it with ASR.
  tts.py say  lines.json out_dir --model DIR     lines.json = [{"id":"s01","text":"...","voice":"narrator"}]
  tts.py check out_dir lines.json --asr DIR      listens back to every wav and reports words that differ
Writes out_dir/<id>.wav, out_dir/voice.wav (all joined, 0.35 s gaps) and out_dir/timings.json ([{id,start,end}])."""
import sys, json, os, re, argparse, wave
import numpy as np
VOICES = {"narrator": 16, "man": 16, "woman": 3, "boy": 17, "old": 15, "villain": 18}   # kokoro sid, see voices list in the model dir
def wav_write(path, a, sr):
    a = np.clip(a, -1, 1); w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype('<i2').tobytes()); w.close()
def say(lines, out, model, speed=1.0, lex=None):
    import sherpa_onnx
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(), kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
        model=f"{model}/model.onnx", voices=f"{model}/voices.bin", tokens=f"{model}/tokens.txt", data_dir=f"{model}/espeak-ng-data", lexicon=",".join(f"{model}/{x}" for x in ("lexicon-us-en.txt",) if os.path.exists(f"{model}/{x}")), dict_dir=f"{model}/dict"),
        num_threads=2, provider="cpu"))
    tts = sherpa_onnx.OfflineTts(cfg); os.makedirs(out, exist_ok=True); allw = []; tim = []; t = 0.0; sr = None
    for L in lines:
        txt = L["text"]
        for k, v in (lex or {}).items(): txt = re.sub(r'\b' + re.escape(k) + r'\b', v, txt)
        sid = L.get("sid", VOICES.get(L.get("voice", "narrator"), 16))
        g = tts.generate(txt, sid=sid, speed=L.get("speed", speed)); a = np.array(g.samples, dtype=np.float32); sr = g.sample_rate
        wav_write(f"{out}/{L['id']}.wav", a, sr)
        gap = np.zeros(int(sr * L.get("gap", .35)), dtype=np.float32)
        tim.append({"id": L["id"], "spoken": txt, "start": round(t, 3), "end": round(t + len(a) / sr, 3)}); allw += [a, gap]; t += (len(a) + len(gap)) / sr
        print(f"  {L['id']}: {len(a)/sr:.2f}s", flush=True)
    wav_write(f"{out}/voice.wav", np.concatenate(allw), sr); json.dump(tim, open(f"{out}/timings.json", "w"), indent=1); print("voice:", f"{out}/voice.wav", f"{t:.1f}s")
def norm(s): return re.findall(r"[a-z0-9']+", s.lower())
def check(out, lines, asr):
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{asr}/encoder.int8.onnx", decoder=f"{asr}/decoder.int8.onnx", joiner=f"{asr}/joiner.int8.onnx", tokens=f"{asr}/tokens.txt", model_type="nemo_transducer", num_threads=2)
    bad = 0; spk = {x['id']: x.get('spoken') for x in json.load(open(f'{out}/timings.json'))}   # compare with what was actually fed to the voice (after respelling)
    for L in lines:
        w = wave.open(f"{out}/{L['id']}.wav"); sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32) / 32768
        s = rec.create_stream(); s.accept_waveform(sr, a); rec.decode_stream(s); heard = norm(s.result.text); want = norm(spk.get(L["id"], L["text"]))
        import difflib
        near = lambda x, pool: any(difflib.SequenceMatcher(None, x, y).ratio() >= (.4 if len(x) <= 3 else .55) for y in pool)
        NUM = {"zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety","hundred","thousand","million","billion","trillion","and","dollars","dollar","percent","cents","euros","pounds"}
        has_digits = any(re.search(r"\d", h) for h in heard)
        miss = [x for x in want if not near(x, heard) and not (has_digits and x in NUM)]; extra = [x for x in heard if not near(x, want) and not x.isdigit()]
        ok = not miss and len(extra) <= 1; bad += not ok
        print(("OK  " if ok else "FIX ") + L["id"] + ("" if ok else f"  not heard={miss} heard instead={extra} (a name or odd word? respell it in the lexicon, then say + check again)"))
    print("all lines clear" if not bad else f"{bad} line(s) need a respelling in the lexicon or a re-read")
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("a"); ap.add_argument("b"); ap.add_argument("--model"); ap.add_argument("--asr"); ap.add_argument("--speed", type=float, default=1.0)
    x = ap.parse_args()
    if x.cmd == "say":
        d = json.load(open(x.a)); lines = d["lines"] if isinstance(d, dict) else d; say(lines, x.b, x.model, x.speed, d.get("lexicon") if isinstance(d, dict) else None)
    else:
        d = json.load(open(x.b)); check(x.a, d["lines"] if isinstance(d, dict) else d, x.asr)
