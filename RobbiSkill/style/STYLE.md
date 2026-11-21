# Paper Billions Animate Video style: the diorama system

Flat 2D cartoon explainer about money, companies, markets. 16:9, 1920x1080, 30 fps, 8-15 minutes.
All stories, characters, places and props are ORIGINAL. The format rules below were measured on a 15-minute reference of this
genre (244 cuts in 15:00, mean shot 3.65 s, median 3.1 s, 12-21 cuts per minute, ~40 typed black cards).

## 1. The one idea that makes it look right
**Every sentence gets its own tiny world (a "diorama") built around ONE visual metaphor.** Not one room with a hero talking.
"Debt piles up" = a gold balance scale with red $1 DEBT blocks stacking on one pan. "Nobody read the report" = a spending report
with cobwebs on a water cooler. "Orders waited seven years" = a worker with a trolley of servers waiting at a fuel pump under a neon sign "WAIT: ABOUT 7 YEARS".
Ask for each line: *what physical object or place could this sentence be?* Draw that. Then make 4+ things move.

## 2. Anatomy of a diorama shot
| layer | what | made by |
|---|---|---|
| plate | the place, empty of people and writing | Flow image |
| props | objects: bell, truck, box, scale, dog, bag (single figures on green) | Flow image + `key_sprites.py --no-mouth` |
| heroes | recurring characters, mouth closed/open pair, poses | Flow sheet + `key_sprites.py` |
| graphics | text, numbers/counters, stamps, calendars, documents, pins, arrows that draw themselves, bars, inset magnifier | engine layers (code) |
| light | one colour wash or glow per shot (the mood) | `grade` |
| camera | keyframed push/pan, shake on impact | `cam`, `shake` |
| edit | transition in/out, hard cut by default | `tin`, `tout` |
A shot is good when **at least 4 things are moving** (`check_timeline.py` counts them and warns).

## 3. Pacing rules (measured)
- 12-21 cuts per minute; median shot 2.5-4 s; never a scene longer than 7 s without a cut.
- A **typed black card** (white handwriting, typed letter by letter) at every chapter start, every twist/question, and for punchy statements: about one per 30-60 s. Chapter titles are 2-4 words ("The Top", "The Cracks", "Who Gets Hurt").
- A **new place** almost every sentence. The same plate at most 3 shots in a row, and then with a different crop/camera/grade.
- No more than 3 shots with people in a row; alternate with object, map, document, chart, card shots.
- **Recurring devices** give the video a spine: (a) a balloon + stopwatch that shows time vs. price, reused at each big drop; (b) a numbered series ("CRACK 1... CRACK 4") with a round counter badge in the corner and a label top-left; (c) one wall calendar that flips to each date; (d) a colour tag for the day (green = up, red = down).
- Money numbers are big, hand-lettered, glowing red (loss) or green (gain), and count up/down on screen (`counter`). Dates and places appear as small boxed tags bottom-left.
- Heroes are small in the frame (about 25-45 % of its height) and act: walk, sweat, point, sign, hold a prop. Wide shots have tiny crowds.

## 4. Mood = colour (use `grade` and `bgFilter`)
sunset pink/orange = hype and peak · dark green = a company/tech · red + smoke/fire = panic and loss · navy night + one warm lamp = danger, secrets, long nights ·
grey-lilac studio light = a conversation · beige/pale daylight = calm explanation · gold glow = money, ceremonies. The same plate re-lit (day -> night -> red) is a cheap new shot: `"bgFilter":"brightness(.55) saturate(.8)"` plus `grade`.

## 5. The layer reference (inside `"layers":[...]` of any shot)
Common fields: `kind, x, y, s (scale), rot, opacity, start, end, in, inDur, out, outDur, loop, kf, attach, flip, z ("under" = behind characters), hud (true = fixed on screen, not moved by the camera), glow, glowColor, shadow, filter`.
- **in**: `pop` · `slideL/R/U/D` · `drop` (bounces) · `fade` · `grow` · `stamp` (slams down) · `swing` · `flipX`. **out**: `fade pop slideL slideR slideU slideD`.
- **loop** (idle motion): `bob shake swing pulse spin float flicker`.
- **kf** keyframes (times relative to the layer start): `[{"t":2.4,"x":2500,"ease":"lin"}]`. Any of x y s rot op. Eases: lin out inout back bounce elastic. Example truck: `"x":-500,"kf":[{"t":2.4,"x":2500,"ease":"lin"}]`.
- **attach**: index of a character in `chars`; the layer follows that character (a prop in a hand).
Kinds:
- `img`: a prop. `"sprite":"sprites/box.json"` (from key_sprites) or `"src":"plates/x.png"`; size `h` or `w`; `anchor` c|bc|bl|br|tl|tc|tr|cl|cr; `wipe:{at,dur}` reveals left to right.
- `text`: `text, size, font (hand|hand6|brush|bold|sans), color, stroke, sw, align, box:{fill,stroke,pad}, glow, typed:true, cps, typeAt, counter:{from,to,fmt B|M|K|time|plain,dec,dur,at,plus,cur}`. Empty `text` + `counter` = a counting number.
- `stamp`: `text, size, color` (readable box, slams with `in:"stamp"`). Good for LOSS, RECORD, DENIED, CLOSED, NOT YET.
- `doc`: a paper/transcript/bill: `w, header, avatar, rows:[{text, hl:true (yellow marker), circle:true (red circle draws on)},{gray:true,w:.7}], cps`.
- `calendar`: `steps:[{at,m,d}]` pages flip; `circleAt` draws the red circle.
- `pin`: map pin drops and bounces: `text` label.
- `poly`: a line/arrow that draws itself: `pts:[[x,y],...]` relative to x,y; `draw:{at,dur}`, `head:"arrow"|"dot"`, `dash:"14 10"`, `stroke, sw`. `path`: same with an SVG path `d`.
- `inset`: a round magnifier showing a zoomed part of a plate: `src, r, zoom, fx, fy` (focus 0-1).
- `bars`: a field of bars: `n, w, h, appear, shrink:{at,dur,to}, colors` (use over a plate; pair with a falling `poly`).
- `rect`, `circle`: simple shapes. `cash, fire, balloon, stopwatch, ekg`: the animated objects (`rows`; stopwatch `dur,to`).
Shot-level: `grade:[{color, alpha, a0, a1, dur, at, blend, radial:[x,y,r]}]` · `bgFilter`, `bgBlur` · `cam:[{t,x,y,z,ease}]` · `shake:[{at,dur,amp}]` ·
`tin / tout` = `whipL whipR whipU whipD fog zoom focus fade flash` (`tinDur`) · `fx:["dust","bokeh","rain","bills","confetti",{"kind":"sparks","at":[x,y]},{"kind":"steam","at":[x,y]}]` · `overlays` (tag, lower, ticker, clock) · `panW,panFrom,panTo` (pan across a very wide plate).

## 6. Characters (heroes) inside a shot
`chars:[{"sprite":"sprites/boss_cheer.json","x":820,"y":1040,"s":1.0,"pose":"cheer","talk":true,"enter":"left"}]`
- `pose` adds motion to the picture: idle cheer panic clap think shrug point wave walk. The picture comes from the sprite sheet: choose the sheet that matches the emotion.
- `swap:[{"t":2.2,"sprite":"sprites/boss_panic.json","pose":"panic"}]` changes the face/pose mid-shot (happy -> panic).
- `path:[{"t":0,"x":300,"y":1020},{"t":1.5,"x":700,"y":1020,"ease":"inout"}]` the hero walks (auto walk pose + auto flip).
- `talk:true` mouth follows the voiceover; `speakAt:[a,b]` for part of the shot. `enter:"left"|"right"` slides in.
- `crowd:{x0,y0,dx,dy,cols,rows,s,char}` many small copies behind.
Feet y 950-1040, hero scale 0.7-1.1; two heroes at least 450 px apart.

## 7. Other shot types (full-screen, still fully supported)
`numbers` (paper background with big numbers, cash, fire, balloon, stopwatch, ekg), `chart` (bars), `linechart` (+ studio monitor), `market` (hundreds of bars + falling line),
`triptych` (2-4 vertical panels; each panel is a real scene: `bg, cx, cy, k, layers, chars, from, at`; `panelW:[.35,.65]`), `card` (typed black card; `by:"word"`).
Cards may carry `tin:"flash"`.

## 8. Device library (recipes; each = one metaphor)
| the sentence says | build this |
|---|---|
| a date / "months later" | `calendar` flipping + `tag` text; fog transition for a time jump |
| big money raised/lost | `text` counter glowing + `cash` pile dropping + `bills` fx, camera push |
| money burning | numbers shot: `cash` + `fire` + red counter + `sparks` |
| price vs cost | gold `scale` prop, `$3` and `$2` texts on the pans, `stamp` LOSS |
| a stock crashes | `bars` shrinking + red `poly` drawing with a dot head + red counter + red `grade` growing + `shake` |
| a company | a company-character: a prop with a face (apple, box, chip) or its building plate; a hero in front |
| a document / quote | `doc` with typed rows, yellow marker, red circle; or a stamped bill |
| a place far away | map plate + `pin` + dashed `poly` route + `inset` magnifier into a detail |
| a deadline/time pressure | balloon + stopwatch recurring device |
| "nobody noticed/read" | cobwebs/dust, a `doc` on a shelf, a sleeping clerk |
| a decision | hero + two props + a hand/finger prop pressing a button (close-up of the finger as a character) |
| comparison A vs B | `triptych` with 2 panels, different mood grade in each |
| power/authority | a building with a face, `stamp` DENIED, a gavel prop slamming (`shake`) |
| rumour/headline | newswire machine printing a `doc`, ticker overlay, tweet card typed live |
| twist / question | black typed `card`, then `flash` into the next shot |
| everything is fine (irony) | ekg object, calm plate, then whip into red |
| a crowd reacts | `crowd`, confetti or red SELL tags popping on desks |

## 9. QA checklist (read every contact sheet, frame by frame)
- Does the picture show what the sentence says at that second? Do numbers on screen equal the script's numbers?
- 4+ things moving; the camera is never still; a new place most shots.
- Props in front of the plate read clearly: not hidden behind a hero, not cut by the frame (camera moves cut the edges: keep key text `hud:true`).
- Text readable on a phone: size >= 56 for words, >= 40 for tags; strong stroke on busy plates; stamps have a pale box.
- No people or writing inside plates; heroes keep the same face across sheets; hero feet on the floor.
- Sound: voice clear above music; effects soft.

## 10. Characters must sit in the scene (not look pasted)
A hero looks pasted when: different drawing style than the plate, big and centred, no shadow, other light, no interaction. Rules:
- **Style**: draw heroes in the plates' style (same outline weight, palette, texture). See flow-prompts.md "Match the plates".
- **Size/place**: scale 0.75-0.95 normal, 0.5-0.7 wide shots; stand off-centre (x 450-750 or 1150-1450), feet on the floor line of that plate; keep the lower middle of plates empty. `horizon` on a shot makes heroes shrink as they stand higher (farther).
- **Light**: automatic. The engine tints heroes and props (`LIGHTSTYLE`) from the shot's `grade` colour and `bgFilter` brightness. Override per shot: `"light":{"color":"#2a6a8a","amount":.3,"brightness":.8,"rim":"#ffb347","rimSide":"left"}`; `"light":false` turns it off. A warm lamp in the plate = warm rim on the hero.
- **Shadow**: two-layer contact shadow under heroes and under props with `anchor:"bc"` (`ground:false` to skip). Film grain overlay ties layers together (`"grain":false` to skip).
- **Interaction**: hero holds a prop (`attach`), walks to something (`path`), reacts (`swap` face), looks at the number. A hero doing nothing in the middle is the failure case.
