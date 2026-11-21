# Google Flow prompt templates (fill the <...> parts; keep the fixed words)

Settings in Flow: Nano Banana 2.1, 16:9, x1. One prompt = one image. Always English.

## PLATE STYLE BLOCK (paste verbatim into every plate prompt)
Flat 2D vector illustration like a simple explainer animation: layered shapes with thick dark outlines, simple forms, dark moody gradient lighting, glowing lamps, screens and windows, a gentle vignette. Empty of people and characters. No photorealism, no 3D, no anime, no logos, and no letters, numbers or writing anywhere in the image.

## Plate (a place)
Create one single still image, horizontal 16:9. <PLATE STYLE BLOCK> <the place, in detail: room/street/building, era, props and their state>. <light: one main glowing source and its colour, plus a cool or warm fill>. <wide/medium shot> with a clear empty floor area across the lower middle of the frame.

## Plate (an object, no floor needed)
Create one single still image, horizontal 16:9. <PLATE STYLE BLOCK> One single <object> centered, large and in sharp focus, on a simple <colour> background with soft vignette. <details>.

## Panorama plate (for the camera pan)
Create one single still image, horizontal 16:9. <PLATE STYLE BLOCK> A very wide panoramic <street/market/trading floor> that continues far to the left and right, many separate buildings and props in a row, a clear empty ground strip along the bottom.

## Hero sheet (character, 2 images in one: mouth closed | mouth open)
Create one single still image, horizontal 16:9. A character design sheet on a perfectly flat solid pure green background (#00FF00), nothing else in the frame. Left: one full-body cartoon <WHO> standing, <POSE>, <EXPRESSION>, mouth closed. Right: the same <WHO>, same pose, mouth wide open <talking/gasping/laughing>. Flat 2D vector cartoon in the style of a simple animated explainer: big round head with thick dark outline, flat skin color with very soft cel shading, tiny black dot eyes, short eyebrow lines, small nose, <HAIR>, <OUTFIT with colours>, thick dark outlines, simple fold lines on the clothes, <SHOES>. Evenly lit, no shadow on the ground, no text, no letters, no logos.

CHARACTER DESCRIPTION (keep identical on every sheet of the same character): "<WHO>" + hair + outfit + colours. Example:
"businessman, tidy short dark hair, navy pinstripe suit with white shirt and yellow tie, black shoes".

### Pose ideas (one sheet each)
standing neutral talking · both arms up cheering · holding a fat stack of green dollar bills · holding an empty open wallet, worried ·
both hands on head, panic · pointing at something to the side · shrugging, palms up · hand on chin, thinking · head down, sad · arms crossed, smug.

## Prop (one object, for animation): use key_sprites.py --no-mouth
Props are the engine's actors: bell, truck, box, scale, dog, bag, gavel, vault door, server rack, balloon, megaphone, hand with pen, finger on a button, cobweb, easel, trolley.
One object per image, big, centered. Say the viewpoint ("seen from the side facing right" for things that will drive/slide). Say "no logos, no text".
Template (tested): "Create one single still image, horizontal 16:9. A single <OBJECT with colours and details> on a perfectly flat solid pure green background (#00FF00), nothing else in the frame, centered, large. Flat 2D vector cartoon, thick dark outlines, flat colours with very soft cel shading, evenly lit, no shadow, no text, no letters."
Never use green in the object itself. Then: `python scripts/key_sprites.py sheets/box.jpg box --project . --no-mouth` and use `{"kind":"img","sprite":"sprites/box.json","h":300}`.

## Single prop / extra (older note, same thing)
Create one single still image, horizontal 16:9. A single <object or small person> on a perfectly flat solid pure green background (#00FF00), nothing else in the frame, centered, large. Flat 2D vector cartoon, thick dark outlines, flat colours with very soft cel shading, evenly lit, no shadow, no text.

## Cast sheet for a crowd extra
Same as Hero sheet but a generic <office worker/trader/chef> in a plain outfit, standing neutral (use --no-mouth and `crowd` in the timeline).

## Sock/animal/mascot characters
Use the Hero sheet with "<animal or object puppet>" and describe features (eyes, bandana, fabric). Say "no hands, no legs" when the figure has none.

## Thumbnail (ONE only, no variants) - measured on the reference channel's real thumbnails
What the reference thumbnails have, every time: a HUGE caricature face (50-60 % of the frame, head far bigger than the body, big round eyes, one signature feature like glasses or hair) with an extreme readable emotion (panic: wide eyes, open mouth, sweat drops; or a sly grin) · ONE big simple object the person interacts with and that carries the story (a zipper being pulled with green light, a chip cracking, a giant bell, a candle-lit table), glowing green or red · saturated high-contrast colours, rich warm-dark background with one glowing light and rim light on the face · giant bold sans-serif text across the TOP, 2-4 words, thick black outline, white words + the number in red (loss) or green (gain), baked into the picture · readable on a phone at thumbnail size.
What fails (do not do): dark moody fog, silhouettes, small subjects, tiny chip with legs, side-profile faces, realistic faces, no text, empty top, several objects, thin lines.
Template (face + object + number):
`Create one single YouTube thumbnail image, horizontal 16:9. Style: bold chunky cartoon caricature, thick dark outlines, soft painted shading, saturated high-contrast colours, glossy rim light, slightly exaggerated proportions. SUBJECT: a caricature of <PERSON, signature look> with a HUGE head filling about 55% of the frame on the <left/right>, oversized round expressive eyes, <EMOTION: terrified, mouth open, sweat drops>, both hands <gripping/holding> <ONE OBJECT> that glows <green/red> in the lower centre. BACKGROUND: <rich dark warm setting, simple big shapes, one strong glow behind the head>. TEXT across the top, huge bold white sans-serif block letters with thick black outline, reading exactly: "<WORD(S)>" followed by "<-$NUMBER>" in <red/green>. Maximum 4 words, no other text, no logos, no watermark. Clean, flat-ish, readable at small size.`
Text check: look at the generated image; if any letter is wrong or the number is unreadable, regenerate (add the exact text again). Real faces of real people only as friendly caricature.

## Plate list per sentence (the diorama plan)
For a 10-minute video plan about 40-60 plates, 30-40 props and 8-12 hero sheets. Use each plate 1-3 times with different crops/cameras/grades.
Plate ideas that carry stories: trading floor, boardroom with a huge table, vault, bank street, pawn shop, factory conveyor, warehouse, diner counter, data-center aisle, living room with TV, empty office, stage/studio, courthouse steps, Capitol-like building, harbour with cranes, map of a country/continent (blue sea, beige land, no labels), kitchen, fridge door (for bills on magnets), desert town, train/rail yard, construction site, school classroom, hospital corridor, subway platform, shopping mall, garage startup.
Every plate: lower middle EMPTY, no people, no text, one glowing light source. Prompt side (mood): 'warm golden light', 'cold blue gloomy light with one warm lamp', 'green glow from monitors', 'red emergency light', 'pale daylight'.

## Match the plates (hero and props must look like the same world)
Generate plates first. Then add to EVERY hero and prop prompt a style clause copied from the plate style block: same line weight, same colour palette and texture, same soft shading, "the same illustrated world as the background", on a pure green screen. Keep character proportions simple (slightly large head, small body) so a scale of 0.75-0.95 reads as a figure standing IN the room. If a hero still looks flatter or brighter than the plates, regenerate it with "painterly shading, subtle texture, muted palette" rather than "clean flat vector".
