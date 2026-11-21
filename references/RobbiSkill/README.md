# RobbiSkill — Paper Billions Diorama System & Visual References

This folder contains visual references, diorama background plates, sprite sheets, and character puppets for **RobbiSkill (Paper Billions Animate Video)**.

---

## 1. The Paper Billions Diorama Architecture
RobbiSkill structures videos into a sequence of sentence-by-sentence **Dioramas**. Each sentence is its own physical-feeling paper set:
- **Background Plate**: 2.5D illustrated scene with depth layers.
- **Props & Objects**: Cutout elements that move, rotate, scale, or pop onto the set.
- **Puppet Characters**: Code-drawn or sprite-sheet characters with synchronized mouth open/closed states.
- **Moving Data / Typography**: Dynamic tickers, money counters, percentages, and handwritten headers (Caveat / Caveat Brush fonts).
- **Camera & Mood Light**: Parallax pan, slow zoom, and day-to-night lighting transitions.

---

## 2. Included Reference Assets

### Background Plates (`plates/`)
| Plate File | Scene Context | Mood / Lighting |
| :--- | :--- | :--- |
| `stage.jpg` | Keynote / Lecture stage | Spotlit theatrical stage with blue-purple auditorium backlight |
| `office_empty.jpg` | Corporate executive office | Modern glass walls, desks, city skyline view |
| `warehouse.jpg` | Logistics / Supply chain facility | Industrial corrugated steel, wooden pallets, overhead bay lamps |
| `exchange.jpg` | Financial stock exchange | Trading terminals, neon green/red market boards |
| `livingroom.jpg` | Cozy domestic interior | Warm sofa, lamp, bookshelf, domestic finance scenario |

### Sprite Sheets & Props (`sheets/`)
| Sheet File | Assets Contained | Usage |
| :--- | :--- | :--- |
| `bell.jpg` | Brass counter bell & ringer | Transaction alerts, service cues |
| `box.jpg` | Cardboard shipping parcels | E-commerce, delivery, packaging scenes |
| `dog.jpg` | Canine companion cutouts | Storytelling, pets, domestic vignettes |
| `litter.jpg` | Waste & recycling bins | Sanitation, environmental or overhead cost stories |
| `scale.jpg` | Golden balance scales | Legal disputes, cost-vs-benefit comparisons |
| `truck.jpg` | Freight & delivery haulers | Transportation, shipping, logistics breakdowns |

### Character Puppets (`puppets/`)
- `boss_cash_open.png` / `boss_cash_closed.png`: Corporate executive puppet with synced mouth states.
- `boss_cheer_open.png`: Celebratory victory reaction puppet.
- `boss_panic_open.png`: Crisis/panic reaction puppet.
- `sock_open.png` / `sock_closed.png`: Mascot sock-puppet narrator with talking states.

---

## 3. The 11 Built-In Procedural Sets (No Images Required!)
RobbiSkill also features 11 completely code-drawn sets built directly into `engine/sets.js` and `engine/puppet.js`:
1. `office` (desks, computer monitors, water cooler, city window)
2. `street` (brick storefronts, streetlamps, pavement, road markings)
3. `factory` (conveyor belts, steam pipes, warning hazard stripes)
4. `boardroom` (mahogany table, executive chairs, presentation chart)
5. `map` (global trade network lines, country nodes, radar rings)
6. `vault` (steel bank vault door, gold brick stacks, security laser)
7. `server` (rack servers, blinking LED lights, cooling fans)
8. `capitol` (neoclassical marble columns, courtroom bench)
9. `living` (cozy living room, rug, armchair, framed wall art)
10. `stage` (spotlights, curtains, auditorium rows)
11. `exchange` (trading floor floorboards, big price displays)
