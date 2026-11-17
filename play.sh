#!/usr/bin/env bash
# ==============================================================================
# OILS-3: Oops, I Learnt Something! (VTU 2025 Scheme - 3rd Sem CSE Companion)
# Cross-Platform Launcher for macOS, Linux, and Mobile Termux / iSH
# ==============================================================================

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Detect available Python interpreter
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "❌ Python 3 was not detected on your system path."
    echo ""
    echo "👉 Options to run without installing Python locally:"
    echo "   1. Open via GitHub Codespaces (1-click browser terminal):"
    echo "      https://github.com/Ghost5400/OILS-3"
    echo "   2. Install Python 3 via package manager:"
    echo "      - macOS: brew install python"
    echo "      - Ubuntu/Debian: sudo apt update && sudo apt install python3"
    echo "      - Termux (Android): pkg install python"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

"$PY_CMD" "$SCRIPT_DIR/play.py" "$@"

