# 🎬 Ultimate Faceless Shorts Pipeline
### Production-Grade, Deterministic Video Generation Infrastructure for Autonomous AI Agents

[![GitHub Stars](https://img.shields.io/github/stars/baerozgaarmard/ultimate-faceless-shorts-pipeline?style=flat-square)](https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python Runtime](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
![Deterministic Engine](https://img.shields.io/badge/Architecture-Deterministic%20Code--First-success?style=flat-square)
![Zero API Costs](https://img.shields.io/badge/Operational%20Cost-%240.00%20(Local%20DSP%20%2B%20TTS)-orange?style=flat-square)

> **Generate deterministic 3D/2D faceless Shorts and long-form diorama explainers directly from your coding agent (Claude Code, Antigravity, OpenCode, Cursor, Windsurf) — 100% local via Kokoro-82M + faster-whisper + Three.js + FFmpeg, with $0 API cost.**

<table>
  <tr>
    <td width="33%"><img src="references/faceless-shorts/deep-dive-style-sheet.png" alt="Deep Dive 3D style" width="100%" /></td>
    <td width="33%"><img src="references/faceless-shorts/night-file-style-sheet.png" alt="Night File 3D style" width="100%" /></td>
    <td width="33%"><img src="references/faceless-shorts/tall-tale-style-sheet.png" alt="Tall Tale 3D style" width="100%" /></td>
  </tr>
</table>

```bash
# Quickstart — Windows PowerShell
irm https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.ps1 | iex

# Quickstart — Linux / macOS
curl -fsSL https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.sh | bash
```

---

## 1. System Overview

The **Ultimate Faceless Shorts Pipeline** is a modular, code-native video synthesis engine architected specifically for autonomous coding agents (Google Antigravity, Claude Code, OpenCode, Cursor, and Windsurf).

Unlike diffusion-based video models that suffer from temporal jitter, hallucinated text, and high API compute costs, this pipeline employs a **deterministic, code-first rasterization model**. Scripts, layout geometry, character kinematics, camera matrices, speech synthesis, and audio ducking are compiled into source code, rendered in headless browser sandboxes at fixed discrete timestamps (Δt = 1/60 s), and muxed directly via FFmpeg.

```
                              SYSTEM ARCHITECTURE & EXECUTION TOPOLOGY

      +---------------------------------------------------------------------------------+
      |                               Autonomous AI Agent                               |
      |             (Google Antigravity / Claude Code / OpenCode / Cursor)              |
      +---------------------------------------------------------------------------------+
                                               |
                                     1. Script Synthesis
                                               v
                        +---------------------------------------------+
                        |      Structured Timeline (script.json)      |
                        |   - Shot boundaries & camera projection     |
                        |   - Dynamic props & kinetic text parameters |
                        +---------------------------------------------+
                                      |               |
                   2a. Acoustic Synthesis             | 2b. Visual Setup
                                      v               v
            +---------------------------+   +------------------------------------+
            |      Kokoro-82M TTS       |   |     Scene Graph Construction       |
            |     (Local ONNX Model)    |   |  - Three.js / WebGL / Canvas       |
            +---------------------------+   |  - Embedded Fonts (Caveat/Inter)   |
                          |                 |  - Diorama Stage & Puppet Rig      |
             3. Phoneme Alignment           +------------------------------------+
                          v                                   |
            +---------------------------+                     |
            |     faster-whisper        |                     |
            |   (Word Timestamping)     |                     |
            +---------------------------+                     |
                          \                                   /
                           \--[ Millisecond Synchronization ]/
                                              |
                                   4. Deterministic Frame Capture
                                              v
                        +---------------------------------------------+
                        |         Headless Chromium Process Pool      |
                        |  - Deterministic time advancement via JS    |
                        |  - Hardware-accelerated Canvas/WebGL raster |
                        |  - Lossless PNG / pipe buffer stream        |
                        +---------------------------------------------+
                                              |
                                   5. Audio DSP & Multiplexing
                                              v
                        +---------------------------------------------+
                        |                  FFmpeg Mux                 |
                        |  - Sub-bass procedural audio synthesis      |
                        |  - Sidechain music ducking                  |
                        |  - H.264 high-profile NVENC/libx264 mux     |
                        +---------------------------------------------+
                                              |
                                    6. Output & Verification
                                              v
                             [ Final MP4 (1080x1920 / 1920x1080) ]
                             [ Contact Sheet Multi-Frame QA Grid ]
```

---

## 2. Integrated Engine Specifications

The repository bundles two specialized production engines:

### Engine A: `faceless-shorts` (Vertical 9:16 Micro-Short Engine)
- **Target Form Factor**: 9:16 Vertical (1080x1920) for YouTube Shorts, TikTok, Instagram Reels.
- **Duration**: 30 to 65 seconds per short.
- **Rendering Stack**: Three.js (WebGL), 2D Canvas context, procedural lighting, CSS perspective transforms.
- **Audio Stack**: Kokoro-82M ONNX TTS + faster-whisper millisecond alignment + programmatic audio synthesis (swooshes, hits, drops, tick cues).
- **Core Abstraction**: `styles/<style-id>/` modular directory containing `STYLE.md`, `style-sheet.png`, and a full standalone verification testbed.

### Engine B: `RobbiSkill` (Paper Billions Diorama Puppet Engine)
- **Target Form Factor**: 16:9 Landscape (1920x1080) and 9:16 Vertical for long-form explainers (8–15 minutes) or episodic shorts.
- **Rendering Stack**: HTML5/CSS3 layered diorama engine with 11 built-in code sets (`office`, `street`, `factory`, `vault`, `server`, etc.) or custom 2.5D background plates.
- **Character Rigging**: Puppet state machine (`puppet.js`) featuring synced open/closed mouth phoneme flap, eye blinks, bodily gestures, and walking loops.
- **Parallelization**: Multi-worker browser rendering queue (`--jobs N`) with shot-level disk caching.

---

## 3. Style Sheets & Visual Reference Matrix

Every aesthetic style is backed by an explicit style sheet, defining color gamuts, typography tokens, light positions, camera optics, and layout geometry.

### Pipeline 1: Faceless Shorts Reference Gallery

<table>
  <tr>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/deep-dive-style-sheet.png" alt="Deep Dive 3D Style Sheet" width="100%" />
      <br />
      <b>01. Deep Dive 3D (Anatomical & Medical Explainer)</b>
      <p align="left"><i>Volumetric lighting, microscopic tissue shaders, 3D cross-sections, floating coordinate callouts, and orbital camera pans. Ideal for biology, physiology, and physics explainers.</i></p>
    </td>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/night-file-style-sheet.png" alt="Night File 3D Style Sheet" width="100%" />
      <br />
      <b>02. Night File 3D (Investigative Crime & Mystery)</b>
      <p align="left"><i>Atmospheric darkroom lit by single tungsten desk lamps, manila case folders, red yarn corkboard connections, typewriter dossiers, and slow anamorphic dolly zooms.</i></p>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/inside-out-style-sheet.png" alt="Inside Out Style Sheet" width="100%" />
      <br />
      <b>03. Inside Out (2D X-Ray Diagnostic Reveal)</b>
      <p align="left"><i>High-contrast silhouette bodies with glowing neon internal diagnostic paths. Traces foreign objects, biological pathways, and mechanical operations against deep obsidian backdrops.</i></p>
    </td>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/stick-story-style-sheet.png" alt="Stick Story Style Sheet" width="100%" />
      <br />
      <b>04. Stick Story (Minimalist Survival Protocol)</b>
      <p align="left"><i>Expressive high-contrast vector stick figures navigating emergency procedures and rules. Features prominent hazard sign overlays, checklist badges, and high-tempo cutting.</i></p>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/paper-atlas-style-sheet.png" alt="Paper Atlas Style Sheet" width="100%" />
      <br />
      <b>05. Paper Atlas (Historical Cartography)</b>
      <p align="left"><i>Multi-plane layered fibrous paper textures, antique parchment maps, animated nautical/topographical routes, and paper cutouts reenacting geopolitical history.</i></p>
    </td>
    <td width="50%" align="center">
      <img src="references/faceless-shorts/tall-tale-style-sheet.png" alt="Tall Tale 3D Style Sheet" width="100%" />
      <br />
      <b>06. Tall Tale 3D (Animated Storytime World)</b>
      <p align="left"><i>Flat 2D cartoon characters operating in a vibrant, painterly 3D environment. Characterized by slapstick squash-and-stretch kinematics, sunny daylight skies, and playful camera tracks.</i></p>
    </td>
  </tr>
</table>

---

### Pipeline 2: RobbiSkill Diorama Plates & Character Assets

<table>
  <tr>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/plates/stage.jpg" alt="Stage Diorama Plate" width="100%" />
      <br />
      <b>Keynote Stage Plate</b>
      <p align="left"><i>Theatrical lecture platform with dramatic blue-violet rim light for tech announcements.</i></p>
    </td>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/plates/office_empty.jpg" alt="Office Diorama Plate" width="100%" />
      <br />
      <b>Executive Office Plate</b>
      <p align="left"><i>Corporate boardroom interior with high-rise skyline windows and glass surfaces.</i></p>
    </td>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/plates/warehouse.jpg" alt="Warehouse Diorama Plate" width="100%" />
      <br />
      <b>Logistics Facility Plate</b>
      <p align="left"><i>Industrial bay with pallets, corrugated metal, and overhead spotlighting.</i></p>
    </td>
  </tr>
  <tr>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/plates/exchange.jpg" alt="Stock Exchange Plate" width="100%" />
      <br />
      <b>Financial Trading Floor Plate</b>
      <p align="left"><i>Wall Street trading monitors with real-time green/red ticker animations.</i></p>
    </td>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/sheets/dog.jpg" alt="Sprite Prop Sheet" width="100%" />
      <br />
      <b>Cutout Prop Sheet (dog.jpg)</b>
      <p align="left"><i>Multi-part sprite sheet decomposed automatically by <code>key_sprites.py</code> into alpha PNGs.</i></p>
    </td>
    <td width="33%" align="center">
      <img src="references/RobbiSkill/puppets/boss_cash_open.png" alt="Character Talking Sprite" width="70%" />
      <br />
      <b>Talking Puppet Rig</b>
      <p align="left"><i>Synchronized mouth open/closed sprite states driven by phoneme intensity.</i></p>
    </td>
  </tr>
</table>

---

## 4. Universal Installation & Agent Integration

The pipeline exposes a unified one-line installation interface that inspects the local runtime, identifies active coding agents, and symlinks/copies the skills into their respective discovery directories.

### Single-Command Setup

```bash
# Windows (PowerShell 5.1+)
irm https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.ps1 | iex

# Linux / macOS / Git Bash
curl -fsSL https://raw.githubusercontent.com/baerozgaarmard/ultimate-faceless-shorts-pipeline/main/install.sh | bash

# Python Standard Library
git clone https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline.git
cd ultimate-faceless-shorts-pipeline && python install.py
```

### Agent Skill Matrix

| Coding Agent | Supported Scope | Destination Path |
| :--- | :--- | :--- |
| **Google Antigravity** | Global / Workspace | `~/.gemini/antigravity/skills/<skill-name>/` |
| **Claude Code** | Global / Workspace | `~/.claude/skills/<skill-name>/` |
| **OpenCode** | Global / Workspace | `~/.config/opencode/skills/<skill-name>/` |
| **Cursor** | Workspace | `.cursor/skills/<skill-name>/` |
| **Windsurf** | Workspace | `.windsurf/skills/<skill-name>/` |

---

## 5. Interactive Style Selection CLI

As soon as installation completes, the pipeline triggers `choose_style.py`. You can also execute it anytime directly from the terminal:

```bash
python choose_style.py
```

```
====================================================================
  🎨 CHOOSE YOUR VIDEO STYLE — WITH REFERENCE IMAGES
====================================================================
Select a style to view its reference image, aesthetic rules, and prompt:

  [1] Deep Dive 3D (High-detail 3D anatomical Medical/Science Explainer)
  [2] Night File 3D (True Crime & Mystery Archives)
  [3] Inside Out (2D X-Ray Diagnostic Explainer)
  [4] Stick Story (Survival & Protocol Rules)
  [5] Paper Atlas (Historical Cartography & Papercraft)
  [6] Tall Tale 3D (Animated Storytime / History)
  [7] RobbiSkill / Paper Billions (16:9 Diorama & Long-Form Studio)
  [8] View All Reference Style Sheets & Diorama Plates
====================================================================
```

Selecting an option displays the technical spec, copies the tailored agent prompt to stdout, and **automatically launches the corresponding style sheet screenshot** in your operating system's native viewer.

---

## 6. Execution Flow & Code Commands

Once installed, invoke your coding agent and provide a single declarative prompt:

```markdown
# 3D Anatomical Short
"Make a Deep Dive 3D short: what happens if you crack your knuckles?"

# Noir Mystery Archive
"Make a Night File 3D short: the mystery of the abandoned ghost ship Mary Celeste."

# Flat Diagnostic X-Ray
"Make an Inside Out short: what happens inside the body when you drink cold water?"

# Emergency Protocol Guide
"Make a Stick Story short: 3 immediate rules to survive an elevator free-fall."

# Cartographic History
"Make a Paper Atlas short: how the Great Fire of London consumed 13,000 houses in 1666."

# Long-Form Business Diorama
"Make a Paper Billions Animate Video about how the global semiconductor supply chain operates."
```

### Headless Verification & Selftest

Both engines include self-contained end-to-end integration tests that generate, render, and verify a complete video sample without external inputs:

```bash
# Verify Engine A (Faceless Shorts)
cd faceless-shorts
bash scripts/setup.sh       # Validates ffmpeg, Node, Kokoro, Whisper
bash scripts/selftest.sh    # Renders complete 20s test short -> prints "SELFTEST PASSED"

# Verify Engine B (RobbiSkill)
cd RobbiSkill
python scripts/setup.py     # Installs audio/render dependencies
python scripts/selftest.py  # Renders multi-layer 5-shot diorama -> prints "SELFTEST PASSED"
```

---

## 7. Performance & Latency Benchmarks

Tested on a standard developer workstation (AMD Ryzen 9 / 32 GB RAM / Ubuntu 22.04 & Windows 11):

| Stage | Subsystem | Latency (60s Short) | Latency (10m Long-Form) |
| :--- | :--- | :--- | :--- |
| **TTS Synthesis** | Kokoro-82M (ONNX CPU) | 2.1 s | 22.4 s |
| **Phoneme Alignment** | faster-whisper (small.en) | 1.8 s | 18.2 s |
| **Browser Raster** | Chromium WebGL (60 fps) | 14.5 s | ~25 min (parallel workers) |
| **Audio DSP Mux** | FFmpeg sidechain ducking | 0.8 s | 6.2 s |
| **Total Pipeline** | **End-to-End Execution** | **~19.2 s** | **~26 min** |

---

## 8. Repository Layout

```
ultimate-faceless-shorts-pipeline/
├── faceless-shorts/               # 6 Micro-Short Styles (3D Anatomical, Noir, X-Ray, Stick, Paper, Toon)
│   ├── SKILL.md                   # Agent execution instructions & prompt contracts
│   ├── README.md                  # Engine-specific technical guide
│   ├── scripts/                   # setup.sh, words.py, voice.py, selftest.sh, new_video.sh
│   └── styles/                    # 6 style sub-modules (each with STYLE.md, style-sheet.png, example/)
├── RobbiSkill/                    # Paper Billions Diorama Puppet Animation Studio
│   ├── SKILL.md                   # Agent execution workflow for sentence dioramas
│   ├── README.md                  # Engine-specific technical guide
│   ├── engine/                    # engine.html, layers.js, puppet.js, sets.js, render.py, fonts
│   ├── scripts/                   # align.py, check_timeline.py, mix.py, setup.py, selftest.py
│   ├── style/                     # STYLE.md, flow-prompts.md, V2-CODE.md
│   └── example_flow/              # High-res plates, sprite sheets, and character rigs
├── references/                    # Consolidated Visual References & Screenshots
│   ├── faceless-shorts/           # 6 High-resolution style sheet PNGs + README
│   └── RobbiSkill/                # Background plates, prop sheets, and puppet rigs + README
├── install.py                     # Universal Python installer & style selector
├── install.sh                     # POSIX shell installer wrapper
├── install.ps1                    # Windows PowerShell installer wrapper
├── choose_style.py                # Standalone interactive style picker CLI
├── LICENSE                        # MIT License
└── README.md                      # Primary engineering documentation
```

---

## 9. License & Open Source Attribution

- **Architect & Maintainer**: [baerozgaarmard](https://github.com/baerozgaarmard)
- **License**: MIT License. Commercial and non-commercial video rendering permitted with zero licensing fees.
- **Embedded Open Source Libraries**:
  - *Kokoro-82M*: Apache-2.0 via `kokoro-onnx`
  - *faster-whisper*: MIT License (Systran)
  - *Three.js*: MIT License (Mr.doob)
  - *Fonts*: SIL Open Font License 1.1 (Inter, Caveat, Caveat Brush)
