# RobbiSkill: Paper Billions Animate Video, a skill for Claude and OpenCode

One prompt: topic -> research with sources -> script -> characters and sets drawn in code (Flow images optional) -> your voiceover or a generated one checked by speech recognition -> animated 16:9 video (8-15 min) -> sound -> QA -> YouTube package.
Style: faceless cartoons built as a tiny "diorama" per sentence (own plate, props, moving text/numbers, camera, mood colour). Original characters and scripts.

## Install
Claude Code: folder as `~/.claude/skills/RobbiSkill/` (or `.claude/skills/` in a project).
OpenCode: `~/.config/opencode/skills/RobbiSkill/` (Windows: `C:\Users\<you>\.config\opencode\skills\RobbiSkill\`) or `.opencode/skills/`. Restart the app.

## First run
```
python scripts/setup.py      # checks Python 3.10+, ffmpeg; installs packages. Prints "All set"
python scripts/setup.py --voice   # optional: downloads the built-in voice + speech-recognition models (~850 MB, once)
python scripts/selftest.py   # renders the bundled example. Prints "SELFTEST PASSED"
```
Mac/Linux: `python3`. Install ffmpeg first (Windows: `winget install ffmpeg`; Mac: `brew install ffmpeg`).

## Use
Write: `Make a Paper Billions Animate Video about <topic>` (or paste your own script). Answer the intake, approve the diorama plan ("Build it?"), then it makes plates/props/heroes in Flow, you send your voiceover, it renders, checks contact sheets and gives the MP4 and `package.md`.

## Layout
`SKILL.md` workflow · `style/STYLE.md` the diorama system and layer reference · `style/V2-CODE.md` puppets, sets, night light · `style/flow-prompts.md` optional Flow prompts · `engine/` renderer · `scripts/` tools · `example/` complete code-drawn sample (5 shots, generated voice) · `example_flow/` older sample with Flow images.

## Speed
Measured on a 2-CPU sandbox: about 0.12 s per frame (the browser's software rasterising is the cost), so a 21 s draft took about 1.8 minutes in total and a 10-minute video should take roughly 35-50 minutes, draft or final alike (resolution barely changes it). `render.py` now renders shots in parallel browsers (`--jobs N`, default = number of CPUs, max 6): on this 2-CPU sandbox that gained only about 12%, on a machine with more cores it should help much more (not measured). Shots are cached, so an edit re-renders only the changed shots; the cache is also reset automatically when the engine files change.

## Status (honest)
Tested (Linux, driven by Claude): setup, selftest (render + sound), code puppets, the night light and all 11 sets (each rendered once with a puppet; the last 6 only checked at thumbnail size), a crowd of 12 puppets, generated voice with speech-recognition check on 5 lines, the old Flow pipeline. Not tested: Windows/Mac, a full 10-minute run, a close look at boardroom, map, vault, server, capitol and living (they render but are plainer than office and street), the code-drawn thumbnail, the compare-with-reference step on a real reference, OpenCode with GLM-5.3-Flash. The generated voice is synthetic English; names may need respelling in the lexicon.
