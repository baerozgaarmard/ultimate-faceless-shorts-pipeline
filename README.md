# 🎬 Ultimate Faceless Shorts Pipeline

[![Author: baerozgaarmard](https://img.shields.io/badge/Author-baerozgaarmard-blue.svg)](https://github.com/baerozgaarmard)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![100% Free & Local](https://img.shields.io/badge/Cost-100%25%20Free%20%7C%20No%20API%20Keys-orange.svg)]()
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

> **The definitive autonomous faceless video generation pipeline for AI coding agents.**  
> Combines two production-ready, code-first video engines: **`faceless-shorts`** (6 viral micro-short styles) and **`RobbiSkill`** (Paper Billions diorama puppet studio).  
> **100% local, free, and open.** Zero cloud GPU subscriptions, zero API keys, and zero per-second video generation fees.

---

## ⚡ 1-Command Auto-Install in Any Coding Agent

Install the entire pipeline into **any AI coding agent** (Claude Code, Google Antigravity, OpenCode, Cursor, Windsurf, Codex, etc.) with a single command:

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.ps1 | iex
```

### macOS / Linux / Git Bash
```bash
curl -fsSL https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.sh | bash
```

### Direct Clone & Python
```bash
git clone https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline.git
cd ultimate-faceless-shorts-pipeline
python install.py
```

### 🎯 What the Installer Does Automatically
1. **Detects installed coding agents**:
   - **Google Antigravity** (`~/.gemini/antigravity/skills/`)
   - **Claude Code** (`~/.claude/skills/` and project `.claude/skills/`)
   - **OpenCode** (`~/.config/opencode/skills/` and project `.opencode/skills/`)
   - **Cursor** (`.cursor/skills/`)
   - **Windsurf** (`.windsurf/skills/`)
2. **Copies both skills** (`faceless-shorts` and `RobbiSkill`) cleanly without overwriting other customizations.
3. **Validates prerequisites** (Python 3.10+, ffmpeg, Node.js, Google Chrome).
4. **Launches the Interactive Video Style Selector**:
   - As soon as install finishes, it prompts you to choose your desired video style.
   - Automatically opens and displays the **reference style sheets** on your screen.
   - Provides the exact, ready-to-run prompt to paste into your agent!

---

## 🎨 Choose Your Video Style (7 Distinct Aesthetics)

You can also launch the interactive style picker at any time:
```bash
python choose_style.py
```

| # | Style Name | Pipeline | Best For | Reference Image / Style Sheet |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Deep Dive 3D** | `faceless-shorts` | High-detail 3D anatomical medical & anatomical 3D explainers | [View Style Sheet](references/faceless-shorts/deep-dive-style-sheet.png) |
| **2** | **Night File 3D** | `faceless-shorts` | Unsolved true crime, noir case files & atmospheric mysteries | [View Style Sheet](references/faceless-shorts/night-file-style-sheet.png) |
| **3** | **Inside Out** | `faceless-shorts` | 2D translucent X-ray cutaways with neon diagnostic trails | [View Style Sheet](references/faceless-shorts/inside-out-style-sheet.png) |
| **4** | **Stick Story** | `faceless-shorts` | High-stakes survival protocols & rule breakdowns | [View Style Sheet](references/faceless-shorts/stick-story-style-sheet.png) |
| **5** | **Paper Atlas** | `faceless-shorts` | Historical papercraft layers, parchment maps & battle lines | [View Style Sheet](references/faceless-shorts/paper-atlas-style-sheet.png) |
| **6** | **Tall Tale 3D** | `faceless-shorts` | Flat 2D cartoon characters moving inside a sunny 3D world | [View Style Sheet](references/faceless-shorts/tall-tale-style-sheet.png) |
| **7** | **Paper Billions** | `RobbiSkill` | Sentence-by-sentence diorama puppet theater (16:9 or 9:16) | [View Diorama Assets](references/RobbiSkill/) |

---

## 🖼️ Reference Gallery & Style Sheets

### Pipeline 1: Faceless Shorts (6 Styles)

```
references/faceless-shorts/
├── deep-dive-style-sheet.png      # 3D High-detail 3D anatomical aesthetic (medical / science)
├── night-file-style-sheet.png     # Dark atmospheric 3D true crime archive
├── inside-out-style-sheet.png     # 2D X-ray anatomical reveal with neon glow
├── stick-story-style-sheet.png    # High-energy minimalist stick figure survival
├── paper-atlas-style-sheet.png    # Vintage cartography & layered papercraft
├── tall-tale-style-sheet.png      # 2D flat cartoon people in painterly 3D sets
└── README.md                      # Complete visual styling breakdown
```

### Pipeline 2: RobbiSkill / Paper Billions (Diorama Sets & Puppets)

```
references/RobbiSkill/
├── plates/                        # 2.5D Background Diorama Plates
│   ├── stage.jpg                  # Keynote / Lecture stage diorama
│   ├── office_empty.jpg           # Modern corporate glass-wall office
│   ├── warehouse.jpg              # Industrial supply chain logistics bay
│   ├── exchange.jpg               # Wall Street financial trading floor
│   └── livingroom.jpg             # Domestic living room interior
├── sheets/                        # Cutout Sprite & Prop Sheets
│   ├── bell.jpg, box.jpg, dog.jpg, litter.jpg, scale.jpg, truck.jpg
├── puppets/                       # Character Talking Sprites (Open/Closed Mouths)
│   ├── boss_cash_open.png, boss_cheer_open.png, sock_open.png
└── README.md                      # Diorama architecture & set guide
```

---

## 🛠️ How It Works Under the Hood

### 1. `faceless-shorts` Pipeline Architecture
1. **Script Generation**: Creates concise, hook-driven scripts (`script.json`) with precise word counts and visual pacing.
2. **Local AI Voice**: Synthesizes clean narration locally with **Kokoro-82M** (Apache-2.0 via `kokoro-onnx`). Zero cloud latency.
3. **Whisper Word-Level Alignment**: Extracts exact millisecond word timestamps using **faster-whisper**.
4. **Canvas & 3D Procedural Sets**: Animation drawn purely in code using HTML5 Canvas, WebGL, and Three.js.
5. **Procedural SFX & Ducked Music**: Audio synthesized programmatically (swooshes, pops, impacts, ambient tones) and mixed with ducking.
6. **Headless Chrome Frame Capture**: Headless Chrome renders every frame at deterministic time steps (30 or 60 fps).
7. **FFmpeg Assembly**: Encodes final high-bitrate vertical MP4 (1080x1920) with synchronized word captions.
8. **Contact Sheet QA**: Claude / Antigravity reviews a composite contact sheet of every shot before presenting the video to you.

### 2. `RobbiSkill` (Paper Billions) Architecture
1. **Topic Research & Storyboarding**: Researches topics with real citations, structuring content into sentence-by-sentence dioramas.
2. **11 Built-In Procedural Sets**: Built-in code sets (`office`, `street`, `factory`, `boardroom`, `map`, `vault`, `server`, `capitol`, `living`, `stage`, `exchange`) rendered directly with Canvas/CSS, or loaded from illustrated 2.5D plates.
3. **Code-Drawn Puppets**: Responsive puppets with automatic mouth flap sync driven by phoneme analysis or speech recognition.
4. **Parallel Browser Rendering**: Multi-threaded rendering engine (`--jobs N`) renders shots concurrently with automatic caching.
5. **Multi-Track Audio DSP**: Mixes voiceover, ambient bed, dynamic tickers, and SFX with precise peak limiting.
6. **Package Generation**: Outputs final MP4 alongside `package.md` (titles, description, tags, pinned comment, chapters).

---

## 🚀 Quickstart Examples

### Deep Dive 3D (High-detail 3D anatomical Style)
Tell your coding agent:
> *"Make a Deep Dive 3D short: what happens if you crack your knuckles?"*

### Night File 3D (True Crime Mystery)
Tell your coding agent:
> *"Make a Night File 3D short: the man who jumped out of a plane (D.B. Cooper)."*

### Inside Out (2D X-Ray)
Tell your coding agent:
> *"Make an Inside Out short: what happens if you swallow chewing gum?"*

### Stick Story (Survival Rules)
Tell your coding agent:
> *"Make a Stick Story short: 3 rules to survive an elevator cable snap."*

### Paper Atlas (Historical Cartography)
Tell your coding agent:
> *"Make a Paper Atlas short: how one tiny bakery burned down London in 1666."*

### Tall Tale 3D (Humorous True Story)
Tell your coding agent:
> *"Make a Tall Tale 3D short: the girl who was mailed to grandma in 1914."*

### Paper Billions (RobbiSkill Long-Form / Diorama)
Tell your coding agent:
> *"Make a Paper Billions Animate Video about how Nvidia became a 3 trillion dollar company."*

---

## ⚙️ Prerequisites & System Requirements

- **Python**: 3.10+
- **ffmpeg**: Installed and added to system `PATH`
  - *Windows*: `winget install ffmpeg`
  - *macOS*: `brew install ffmpeg`
  - *Linux*: `sudo apt update && sudo apt install ffmpeg`
- **Node.js**: 20+ (recommended for headless browser rendering)
- **Google Chrome / Chromium**: Installed for headless frame rendering
- **Disk Space**: ~1.5 GB for local TTS (Kokoro) and Whisper models (downloaded on first run)

### Running First-Time Setup & Selftest
```bash
# Setup faceless-shorts dependencies and selftest
cd faceless-shorts
bash scripts/setup.sh
bash scripts/selftest.sh

# Setup RobbiSkill dependencies and selftest
cd ../RobbiSkill
python scripts/setup.py
python scripts/selftest.py
```

---

## 📁 Repository Structure

```
ultimate-faceless-shorts-pipeline/
├── faceless-shorts/               # 6 Micro-Short Styles (3D Anatomical, Noir, X-Ray, Stick, Paper, Toon)
│   ├── SKILL.md                   # Agent skill definition and execution instructions
│   ├── README.md                  # faceless-shorts standalone guide
│   ├── scripts/                   # Setup, voice, whisper words, selftest, and new_video scripts
│   └── styles/                    # 6 style directories (each with STYLE.md, style-sheet.png, example/)
├── RobbiSkill/                    # Paper Billions Diorama Puppet Animation Studio
│   ├── SKILL.md                   # Agent skill definition and diorama execution workflow
│   ├── README.md                  # RobbiSkill standalone guide
│   ├── engine/                    # Canvas/WebGL rendering engine, puppet.js, sets.js, embedded fonts
│   ├── scripts/                   # setup.py, selftest.py, mix.py, align.py, tts.py, etc.
│   ├── style/                     # STYLE.md, flow-prompts.md, V2-CODE.md
│   └── example_flow/              # Illustrated diorama plates, sprite sheets, and audio
├── references/                    # Centralized Reference Showcase
│   ├── faceless-shorts/           # High-resolution style sheet PNGs for all 6 styles
│   └── RobbiSkill/                # Diorama background plates, sprite sheets, and character puppets
├── install.py                     # Universal cross-platform installer & interactive style chooser
├── install.sh                     # One-liner installer for macOS / Linux / Git Bash
├── install.ps1                    # One-liner installer for Windows PowerShell
├── choose_style.py                # Standalone interactive style selector CLI
├── LICENSE                        # MIT License
└── README.md                      # This comprehensive documentation
```

---

## 📄 License & Credits

- **Repository Creator & Owner**: [baerozgaarmard](https://github.com/baerozgaarmard)
- Original animations, sets, stories, sound synthesis, and code are open source under the **MIT License**.
- **Third-Party Open-Source Models & Fonts**:
  - *Kokoro-82M*: Apache-2.0 via `kokoro-onnx`
  - *Faster-Whisper & Whisper small.en*: MIT License
  - *Inter, Caveat, Caveat Brush Fonts*: SIL Open Font License 1.1

---
*Created with ❤️ by **baerozgaarmard** for the autonomous AI developer community.*
