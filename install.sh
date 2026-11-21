#!/usr/bin/env bash
# Ultimate Faceless Shorts Pipeline - One-Liner Installer for Linux, macOS & Git Bash
set -e

REPO_URL="https://github.com/baerozgaarmard/ultimate-faceless-shorts-pipeline.git"
CLONE_DIR="$HOME/.faceless-shorts-pipeline"

echo "========================================================================"
echo "    ULTIMATE FACELESS SHORTS PIPELINE — ONE-LINER INSTALLER"
echo "========================================================================"

if command -v python3 >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PY_CMD="python"
else
    echo "Error: Python 3 is required. Please install Python 3.10+."
    exit 1
fi

# If already inside the repo directory, run install.py directly
if [ -f "install.py" ] && [ -d "faceless-shorts" ]; then
    $PY_CMD install.py "$@"
    exit 0
fi

# Clone or pull latest into local cache directory
if [ -d "$CLONE_DIR/.git" ]; then
    echo "Updating existing installation in $CLONE_DIR..."
    git -C "$CLONE_DIR" pull --quiet origin main || true
else
    echo "Cloning repository to $CLONE_DIR..."
    git clone --depth 1 "$REPO_URL" "$CLONE_DIR"
fi

cd "$CLONE_DIR"
$PY_CMD install.py "$@"
