"""
gen_catalog.py — Generates the syllabus catalog block for open_me.txt.

This tool imports the ground truth experiment definitions from arcade/* and
prints the formatted catalog block for SUBJECTS & EXPERIMENTS COVERED so that
documentation never drifts out of sync with code.

Usage:
    python For_Developers/tools/gen_catalog.py
"""

import os
import sys

# Ensure For_Developers is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FOR_DEV_DIR = os.path.dirname(SCRIPT_DIR)
if FOR_DEV_DIR not in sys.path:
    sys.path.insert(0, FOR_DEV_DIR)

from arcade.dsa.experiments_data import DSA_EXPERIMENTS
from arcade.java.experiments_data import JAVA_EXPERIMENTS
from arcade.git.experiments_data import GIT_EXPERIMENTS


def generate_catalog():
    lines = []
    lines.append("================================================================================")
    lines.append("📚 SUBJECTS & EXPERIMENTS COVERED (VTU 2025 SCHEME - 3RD SEM CSE)")
    lines.append("================================================================================")
    lines.append("")
    
    # 1. DSA
    lines.append("1. 💻 DATA STRUCTURES AND APPLICATIONS (VTU Code: 1BCSL306 / Theory: 1BCS305)")
    lines.append("   -----------------------------------------------------------------------------")
    lines.append(f"   Total Experiments : {len(DSA_EXPERIMENTS)} Full Programs + Interactive ASCII Sandboxes")
    for exp in sorted(DSA_EXPERIMENTS, key=lambda x: x["num"]):
        lines.append(f"   - Exp {exp['num']:02d}: {exp['title']}")
    lines.append("")
    
    # 2. Java
    lines.append("2. ☕ OBJECT-ORIENTED PROGRAMMING WITH JAVA (VTU Code: 1BCS302)")
    lines.append("   -----------------------------------------------------------------------------")
    lines.append(f"   Total Experiments : {len(JAVA_EXPERIMENTS)} Full Programs + OOP Visualizers")
    for exp in sorted(JAVA_EXPERIMENTS, key=lambda x: x["num"]):
        lines.append(f"   - Lab {exp['num']:02d}: {exp['title']}")
    lines.append("")
    
    # 3. Git
    lines.append("3. 🌿 GIT & GITHUB VERSION CONTROL (VTU Code: 1BCSL307A)")
    lines.append("   -----------------------------------------------------------------------------")
    lines.append(f"   Total Experiments : {len(GIT_EXPERIMENTS)} Lab Experiments + Full Interactive Command Sandbox")
    for exp in sorted(GIT_EXPERIMENTS, key=lambda x: x["num"]):
        lines.append(f"   - Exp {exp['num']:02d}: {exp['title']}")
    lines.append("")
    
    # 4. Viva
    lines.append("4. 🎯 COMPREHENSIVE VIVA DRILL VAULT (90+ Questions)")
    lines.append("   -----------------------------------------------------------------------------")
    lines.append("   - 6 Practice Sets with dynamically randomized option shuffling across A/B/C/D")
    lines.append("   - Timed Gauntlet mode with immediate examiner rationales & feedback")
    lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_catalog())

