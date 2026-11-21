#!/usr/bin/env python3
"""
Ultimate Faceless Shorts Pipeline - Universal Installer & Style Chooser
Automatically installs faceless-shorts and RobbiSkill into any AI coding agent
(Claude Code, Google Antigravity, OpenCode, Cursor, Windsurf, Codex, etc.)
and interactively guides the user to pick a video style with reference images.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

# Repo metadata
REPO_URL = "https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline.git"
REPO_NAME = "ultimate-faceless-shorts-pipeline"

STYLES = {
    "1": {
        "id": "deep-dive",
        "name": "Deep Dive 3D (High-detail 3D anatomical Medical/Science Explainer)",
        "skill": "faceless-shorts",
        "desc": "High-energy 3D anatomical and physical explainers. Volumetric lighting, 3D cross-sections, floating pins, kinetic camera orbits.",
        "best_for": "What happens if you hold your breath, what happens if you never sleep, why knuckles pop.",
        "sample_prompt": "Make a Deep Dive 3D short: what happens if you crack your knuckles?",
        "ref_rel": os.path.join("references", "faceless-shorts", "deep-dive-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "deep-dive", "style-sheet.png")
    },
    "2": {
        "id": "night-file",
        "name": "Night File 3D (True Crime & Mystery Archives)",
        "skill": "faceless-shorts",
        "desc": "Dark atmospheric 3D room lit by single desk lamps. Manila folders, typewriter documents, red string boards, slow eerie dolly zooms.",
        "best_for": "The man who jumped out of a plane (D.B. Cooper), unsolved heist files, mysterious disappearances.",
        "sample_prompt": "Make a Night File 3D short: the man who vanished at 30,000 feet.",
        "ref_rel": os.path.join("references", "faceless-shorts", "night-file-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "night-file", "style-sheet.png")
    },
    "3": {
        "id": "inside-out",
        "name": "Inside Out (2D X-Ray Diagnostic Explainer)",
        "skill": "faceless-shorts",
        "desc": "Translucent x-ray cutaways with glowing neon highlights tracing internal journeys. Minimalist deep slate backdrops.",
        "best_for": "What happens if you swallow gum, how anesthesia puts you out, swallowed coins.",
        "sample_prompt": "Make an Inside Out short: what happens if you swallow chewing gum?",
        "ref_rel": os.path.join("references", "faceless-shorts", "inside-out-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "inside-out", "style-sheet.png")
    },
    "4": {
        "id": "stick-story",
        "name": "Stick Story (Survival & Protocol Rules)",
        "skill": "faceless-shorts",
        "desc": "Expressive ink stick figures navigating high-stakes situations. Rapid pacing, bold hazard signs, emergency checklist callouts.",
        "best_for": "What if the power went out for 3 days, 3 rules to survive a bear attack, elevator cable snap.",
        "sample_prompt": "Make a Stick Story short: 3 rules to survive an elevator cable snap.",
        "ref_rel": os.path.join("references", "faceless-shorts", "stick-story-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "stick-story", "style-sheet.png")
    },
    "5": {
        "id": "paper-atlas",
        "name": "Paper Atlas (Historical Cartography & Papercraft)",
        "skill": "faceless-shorts",
        "desc": "Textured multi-plane papercraft layers with antique maps, moving marching routes, and historical cutout silhouettes.",
        "best_for": "How one bakery burned down London, the expedition that mapped the Pacific, the lost Roman legion.",
        "sample_prompt": "Make a Paper Atlas short: how one bakery burned down London in 1666.",
        "ref_rel": os.path.join("references", "faceless-shorts", "paper-atlas-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "paper-atlas", "style-sheet.png")
    },
    "6": {
        "id": "tall-tale",
        "name": "Tall Tale 3D (Animated Storytime / History)",
        "skill": "faceless-shorts",
        "desc": "Flat 2D cartoon characters in a bright, sunny, painterly 3D world. Slapstick camera zooms, squash & stretch, funny real history.",
        "best_for": "The girl mailed to grandma via parcel post, the war fought over a bucket, strange true events.",
        "sample_prompt": "Make a Tall Tale 3D short: the girl who was mailed to grandma in 1914.",
        "ref_rel": os.path.join("references", "faceless-shorts", "tall-tale-style-sheet.png"),
        "alt_ref": os.path.join("faceless-shorts", "styles", "tall-tale", "style-sheet.png")
    },
    "7": {
        "id": "robbi-paper-billions",
        "name": "RobbiSkill / Paper Billions (16:9 Diorama & Long-Form Studio)",
        "skill": "RobbiSkill",
        "desc": "Sentence-by-sentence diorama puppet theater. 11 code-drawn sets (office, street, factory, vault, etc.), talking mouth sprites, sound & QA.",
        "best_for": "Business breakdowns, financial empires, deep dives (8-15 min long-form or shorts), tech retrospectives.",
        "sample_prompt": "Make a Paper Billions Animate Video about how Nvidia became a 3 trillion dollar company.",
        "ref_rel": os.path.join("references", "RobbiSkill", "plates", "stage.jpg"),
        "alt_ref": os.path.join("RobbiSkill", "example_flow", "plates", "stage.jpg")
    }
}


def open_file_in_os(path):
    """Open an image or file in the default OS viewer."""
    try:
        p = os.path.abspath(path)
        if not os.path.exists(p):
            return False
        if platform.system() == "Windows":
            os.startfile(p)
        elif platform.system() == "Darwin":
            subprocess.run(["open", p], check=False)
        else:
            subprocess.run(["xdg-open", p], check=False)
        return True
    except Exception:
        return False


def detect_agent_locations():
    """Detect all coding agent skill locations on the user's system."""
    home = Path.home()
    cwd = Path.cwd()

    locations = []

    # 1. Claude Code
    claude_user = home / ".claude" / "skills"
    claude_project = cwd / ".claude" / "skills"
    locations.append({
        "agent": "Claude Code (Global)",
        "path": claude_user,
        "exists": claude_user.parent.exists()
    })
    if claude_project.parent.exists() and claude_project != claude_user:
        locations.append({
            "agent": "Claude Code (Current Project)",
            "path": claude_project,
            "exists": True
        })

    # 2. Google Antigravity
    antigravity_user = home / ".gemini" / "antigravity" / "skills"
    locations.append({
        "agent": "Google Antigravity (Global)",
        "path": antigravity_user,
        "exists": antigravity_user.parent.exists()
    })

    # 3. OpenCode
    opencode_user = home / ".config" / "opencode" / "skills"
    locations.append({
        "agent": "OpenCode (Global)",
        "path": opencode_user,
        "exists": opencode_user.parent.exists()
    })

    # 4. Cursor
    cursor_project = cwd / ".cursor" / "skills"
    locations.append({
        "agent": "Cursor (Current Project)",
        "path": cursor_project,
        "exists": (cwd / ".cursor").exists()
    })

    # 5. Windsurf
    windsurf_project = cwd / ".windsurf" / "skills"
    locations.append({
        "agent": "Windsurf (Current Project)",
        "path": windsurf_project,
        "exists": (cwd / ".windsurf").exists()
    })

    # 6. Current Workspace generic
    generic_project = cwd / "skills"
    locations.append({
        "agent": f"Current Workspace ({cwd.name}/skills)",
        "path": generic_project,
        "exists": True
    })

    return locations


def check_prerequisites():
    """Check system prerequisites and report status."""
    print("\n🔍 Checking Prerequisites...")
    
    # Python
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        print(f"  [✓] Python: {py_ver} (>= 3.10 required)")
    else:
        print(f"  [!] Python: {py_ver} (Recommend Python 3.10+)")

    # ffmpeg
    try:
        res = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            first_line = res.stdout.split("\n")[0]
            print(f"  [✓] ffmpeg: {first_line[:40]}")
        else:
            print("  [!] ffmpeg: not found or errored. (Install via: 'winget install ffmpeg' or 'brew install ffmpeg')")
    except FileNotFoundError:
        print("  [!] ffmpeg: not found. (Install via: 'winget install ffmpeg' or 'brew install ffmpeg')")

    # Node.js
    try:
        res = subprocess.run(["node", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            print(f"  [✓] Node.js: {res.stdout.strip()}")
        else:
            print("  [i] Node.js: not found (recommended for Chrome headless rendering)")
    except FileNotFoundError:
        print("  [i] Node.js: not found (optional/recommended for Chrome headless rendering)")


def install_skills_to_target(source_base, target_dir):
    """Copy faceless-shorts and RobbiSkill into target skills directory."""
    os.makedirs(target_dir, exist_ok=True)
    
    src_faceless = os.path.join(source_base, "faceless-shorts")
    src_robbi = os.path.join(source_base, "RobbiSkill")

    installed = []

    if os.path.exists(src_faceless):
        dst_faceless = os.path.join(target_dir, "faceless-shorts")
        if os.path.exists(dst_faceless):
            shutil.rmtree(dst_faceless)
        shutil.copytree(src_faceless, dst_faceless)
        installed.append("faceless-shorts")

    if os.path.exists(src_robbi):
        dst_robbi = os.path.join(target_dir, "RobbiSkill")
        if os.path.exists(dst_robbi):
            shutil.rmtree(dst_robbi)
        shutil.copytree(src_robbi, dst_robbi)
        installed.append("RobbiSkill")

    return installed


def interactive_style_picker(source_base):
    """Interactive video style selection with reference image previews."""
    print("\n" + "=" * 68)
    print("  🎨 CHOOSE YOUR VIDEO STYLE — WITH REFERENCE IMAGES")
    print("=" * 68)
    print("Select a style to view its reference image, aesthetic rules, and prompt:\n")

    for num, data in STYLES.items():
        print(f"  [{num}] {data['name']}")
        print(f"      👉 {data['desc'][:90]}...")

    print("  [8] View All Reference Style Sheets & Diorama Plates")
    print("  [Q] Exit to Terminal")
    print("=" * 68)

    while True:
        try:
            choice = input("\nEnter choice (1-8, or Q to exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not choice or choice.lower() == 'q':
            print("Enjoy creating videos! 🚀")
            break

        if choice == "8":
            print("\n🖼️  Opening References folder...")
            ref_path = os.path.join(source_base, "references")
            if os.path.exists(ref_path):
                open_file_in_os(ref_path)
                print(f"Opened: {ref_path}")
            else:
                print("References folder not found at:", ref_path)
            continue

        if choice in STYLES:
            style = STYLES[choice]
            print("\n" + "-" * 60)
            print(f"🎬 SELECTED: {style['name']}")
            print("-" * 60)
            print(f"• Pipeline Skill: {style['skill']}")
            print(f"• Aesthetic:      {style['desc']}")
            print(f"• Best For:       {style['best_for']}")
            print(f"\n📋 SAMPLE AGENT PROMPT:")
            print(f"  >>> \"{style['sample_prompt']}\"")
            print("-" * 60)

            ref_path = os.path.join(source_base, style["ref_rel"])
            if not os.path.exists(ref_path):
                ref_path = os.path.join(source_base, style["alt_ref"])

            if os.path.exists(ref_path):
                print(f"🖼️  Reference Image: {os.path.abspath(ref_path)}")
                opened = open_file_in_os(ref_path)
                if opened:
                    print("   (Reference image launched in your image viewer!)")
            else:
                print(f"   (Reference image path: {style['ref_rel']})")

            print("\n💡 Tip: Paste the sample prompt into your coding agent chat to build!")
            print("-" * 60)
        else:
            print("Invalid choice. Please select 1-8 or Q.")


def main():
    print("""
========================================================================
    ULTIMATE FACELESS SHORTS PIPELINE — UNIVERSAL INSTALLER
    Creators: baerozgaarmard
    Pipelines: Faceless Shorts (6 Styles) + RobbiSkill (Paper Billions)
========================================================================
    """)

    # Determine base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if running from cloned repo or standalone
    if not os.path.exists(os.path.join(script_dir, "faceless-shorts")):
        print("Cloning repository to local cache...")
        cache_dir = os.path.join(Path.home(), ".faceless-shorts-pipeline-cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        subprocess.run(["git", "clone", REPO_URL, cache_dir], check=True)
        source_base = cache_dir
    else:
        source_base = script_dir

    if "--choose-style" in sys.argv or "--styles" in sys.argv:
        interactive_style_picker(source_base)
        return

    check_prerequisites()

    # Detect coding agents
    locations = detect_agent_locations()
    detected = [loc for loc in locations if loc["exists"]]

    print("\n📦 Target AI Coding Agents:")
    for idx, loc in enumerate(detected, 1):
        print(f"  [{idx}] {loc['agent']} -> {loc['path']}")

    print(f"  [A] Install to ALL detected agents (Recommended)")
    print(f"  [C] Specify Custom Directory")

    try:
        sel = input("\nWhere would you like to install? [A]: ").strip().upper()
    except (KeyboardInterrupt, EOFError):
        sel = "A"

    if not sel:
        sel = "A"

    targets_to_install = []
    if sel == "A":
        targets_to_install = [loc["path"] for loc in detected]
    elif sel == "C":
        custom = input("Enter custom skills directory path: ").strip()
        if custom:
            targets_to_install = [Path(custom)]
    elif sel.isdigit() and 1 <= int(sel) <= len(detected):
        targets_to_install = [detected[int(sel) - 1]["path"]]
    else:
        print("Defaulting to ALL detected agents.")
        targets_to_install = [loc["path"] for loc in detected]

    print("\n🚀 Installing skills...")
    for target in targets_to_install:
        installed = install_skills_to_target(source_base, target)
        print(f"  [✓] Installed {', '.join(installed)} into: {target}")

    print("\n🎉 INSTALLATION COMPLETE!")
    
    # Immediately trigger interactive style chooser with reference images
    interactive_style_picker(source_base)


if __name__ == "__main__":
    main()
