# V2-CODE: puppets, sets, night light, voice (the default way to build)

Everything here is drawn by the engine in code. No images needed. Read STYLE.md for layers, cameras, devices and pacing; they work the same on code shots.

## 1. Cast (in `timeline.json`)
```json
"cast": {"hero": {"skin":"#f1c9a0","suit":"#2b3a67","shirt":"#f4efe2","tie":"#b3283a","hair":"slick","hair_col":"#2a1d14","moustache":true},
         "boss": {"skin":"#e8b98f","suit":"#6b4a30","hair":"bald","glasses":true,"bowtie":"#b3283a"}}
```
Spec fields: `skin skin_d suit suit_d shirt tie bowtie dress hair(bald|slick|short|curly|bob|long|bun|grey) hair_col glasses moustache beard hat hat_col hat_band shoes`. One cast entry = one recognisable person (caricature: hair, glasses, signature clothes). Different people must differ in at least hair + suit colour.

## 2. A puppet in a shot
`"chars":[{"puppet":"hero","x":700,"y":900,"s":1.0,"face":1,"mood":"smug","pose":"gesture","enter":"left","enterAt":0.2}]`
- `x,y` = FEET position (y is the floor line: 880-1000 depending on the set); `s` scale (1.2-1.5 normal, 0.8-1.0 wide or crowd shots, 2.5-3.5 thumbnails); `flip`, `face` (-1..1 looks left/right).
- `mood`: neutral happy grin shock panic worry smug sad angry sleep think laugh. `pose`: idle walk cheer panic clap think point present gesture shrug facepalm hip pocket hold wave push type. `arms:[left,right]` overrides.
- Mouth follows the voice (`mouth:"auto"`, holds each shape ~3 frames like a cut-out puppet). Pose changes snap with a small overshoot. Blinks every ~2.7 s.
- `speaking:true` or `talk` marks who talks; `cut` clips the body below a y (seated behind a desk); `rim`, `lightSide`, `sweat`, `tilt` are accents.
- Other puppet fields work like STYLE.md characters (`attach`, `path`, `swap`, `crowd`).

## 3. Sets and light: `"set":{"kind":"office","time":"night", ...}`
Kinds: `office` (calendar:"MAY 1925"), `street` (sign:"CAFE"), `city` (landmark:"tower"|"skyscraper"), `boardroom`, `stage` (spot, screen, spotX), `trading` (mood:"red"|"green"), `map` (cities:[[x,y],..]), `vault`, `server`, `capitol`, `living` (screen).
- `time`: `night` (navy mood), `dusk` (purple), `day` (no darkening), `red` (crisis). `ambient` overrides the colour; `lighting:false` turns the light layer off.
- The engine darkens the whole picture (characters included) and cuts soft light holes at the lamps/windows/screens, adds glows and light cones. Heroes standing in a light pool are bright; outside it they are dark: that is what removes the "pasted" look. Put the hero near a lamp.
- Extra light for one shot: `"set":{..., "lights":[{"x":..,"y":..,"r":..,"a":0.9}], "glows":[{"x":..,"y":..,"r":..,"c":"#FFD27A","a":.3}], "cones":[{"x":..,"y":..,"w0":..,"w1":..,"len":..,"a":.2}]}`. `flicker` on the shot makes lights breathe.
- New place: add a function to `SETS` in `engine/sets.js` returning `{svg, floorY, lights, glows, cones}` (use the helpers sR sC sP sL sT, ink outline #18161B, thick strokes, flat colours).
- Sets also work inside triptych panels (`panels:[{"set":{...},"chars":[...]}]`).
- Painted Flow plates still work: `"bg":"plates/x.jpg"` (no set). Do not mix both in one shot.

## 4. Voice
See SKILL.md section 6B (`scripts/tts.py say|check`). Speed 0.95-1.0 for a calm narrator. Write numbers as words; respell names in the lexicon until `check` prints "all lines clear".

## 5. Render cost
Sets are heavier than flat plates. Use `--draft` (low res) for reviews; the per-shot cache means only changed shots are redone. See README "Speed" (about 0.12 s per frame on 2 CPUs).
