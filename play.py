#!/usr/bin/env python3
# pyright: reportMissingImports=false
"""
NOVA-3: (3rd Sem Engineering)
Authors: Mohammed Nouman MN , 
Repository: MdNoouman36/NOVA-3

Master Arcade Hub for all three 3rd-Sem engineering lab subjects:
  - Git Mastery
  - DSA Lab Studio (1BCSL306 — 12 Experiments, VTU 2025 Scheme)
  - Java OOP Lab Studio (1BCS302 — 10 Experiments, VTU 2025 Scheme)
"""

import os
import sys

# Ensure For_Developers and root directory are on Python search path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DIR = os.path.join(SCRIPT_DIR, "For_Developers")
for p in (SCRIPT_DIR, DEV_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import time
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul 2>&1")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def _configure_console():
    # Auto-launch into a dedicated spacious window on Windows
    if sys.platform == "win32" and "--new-window" not in sys.argv and "--no-window" not in sys.argv:
        script_path = os.path.abspath(__file__)
        try:
            subprocess.Popen(
                [sys.executable, script_path, "--new-window"],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                cwd=SCRIPT_DIR
            )
            print("\n\033[92m[*] Launching 'NOVA-3: Master Arcade Hub' in a new dedicated window! 🚀\033[0m\n")
            sys.exit(0)
        except Exception:
            pass

    if sys.platform == "win32":
        try:
            os.system("title 🎮 NOVA-3: Next-Gen Open Virtual Assistant (NOVA-3) (3rd Sem Master Arcade)")
            os.system("mode con: cols=112 lines=42 >nul 2>&1")
        except Exception:
            pass

# ── Arcade Submodule Imports ────────────────────────────────────────────────
try:
    from arcade.core import Color, clear_screen, prompt_input  # type: ignore
    from arcade.constants import CODE_DSA_LAB, CODE_DSA_THEORY, CODE_JAVA, CODE_GIT  # type: ignore
    from arcade.session import (  # type: ignore
        _SESSION, _show_session_header, _end_of_session_summary,
        _show_trophy_case, _init_profile_dialog, BANNER, _BADGES, _clear_local_db,
    )
    from arcade.git.studio import mode_git_studio  # type: ignore
    from arcade.dsa.studio import mode_dsa_studio  # type: ignore
    from arcade.java.studio import mode_java_studio  # type: ignore
    from arcade.vault import _show_code_vault  # type: ignore
    from arcade.viva_bank import run_viva_drill_session  # type: ignore
    from arcade.dialogues import print_dialogue  # type: ignore
except ImportError:
    from For_Developers.arcade.core import Color, clear_screen, prompt_input  # type: ignore
    from For_Developers.arcade.constants import CODE_DSA_LAB, CODE_DSA_THEORY, CODE_JAVA, CODE_GIT  # type: ignore
    from For_Developers.arcade.session import (  # type: ignore
        _SESSION, _show_session_header, _end_of_session_summary,
        _show_trophy_case, _init_profile_dialog, BANNER, _BADGES, _clear_local_db,
    )
    from For_Developers.arcade.git.studio import mode_git_studio  # type: ignore
    from For_Developers.arcade.dsa.studio import mode_dsa_studio  # type: ignore
    from For_Developers.arcade.java.studio import mode_java_studio  # type: ignore
    from For_Developers.arcade.vault import _show_code_vault  # type: ignore
    from For_Developers.arcade.viva_bank import run_viva_drill_session  # type: ignore
    from For_Developers.arcade.dialogues import print_dialogue  # type: ignore

def mode_quickfire_drill_hub():
    """
    Submenu for Option [Q]:
    Choose lab -> Choose Set (Set 1 or Set 2, 15 questions each, 6 total practice sets).
    """
    while True:
        clear_screen()
        print(f"\n{Color.YELLOW}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   ⚡ QUICK-FIRE VIVA DRILL — VTU High-Yield Practice Sets (6 Total Sets)    ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print_dialogue("viva")
        print("  Select your lab to get the 15 most important viva questions (2 sets per lab):\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 🐙  {Color.BOLD}Git Lab ({CODE_GIT}){Color.RESET}        (2 Sets · 30 Top Viva Questions)")
        print(f"  {Color.GREEN}[2]{Color.RESET} 🌳  {Color.BOLD}DSA Lab ({CODE_DSA_LAB}){Color.RESET}           (2 Sets · 30 Top Viva Questions)")
        print(f"  {Color.CYAN}[3]{Color.RESET} ☕  {Color.BOLD}Java OOP Lab ({CODE_JAVA}){Color.RESET}     (2 Sets · 30 Top Viva Questions)")
        print(f"  {Color.DIM}[0]{Color.RESET} ⬅️   Back to Main Menu\n")

        lab_choice = prompt_input(f"{Color.BOLD}Choose Lab [1 - 3, 0=Back]: {Color.RESET}").strip()
        if lab_choice in ("0", "B", "BACK", "EXIT", "Q"):
            return

        subject_map = {"1": "git", "2": "dsa", "3": "java"}
        subj_key = subject_map.get(lab_choice)
        if not subj_key:
            continue

        subj_names = {
            "git": "Git Lab (1BCSL307A)",
            "dsa": "DSA Lab (1BCSL306)",
            "java": "Java OOP Lab (1BCS302)"
        }

        while True:
            clear_screen()
            print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"║  🎯 {subj_names[subj_key]} — Select Practice Set (15 Questions Each)       ║")
            print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
            print(f"  {Color.YELLOW}[1]{Color.RESET} 📘  {Color.BOLD}Set 1 — Core Fundamentals & Lab Exam Favorites{Color.RESET} (15 Qs)")
            print(f"  {Color.GREEN}[2]{Color.RESET} 📙  {Color.BOLD}Set 2 — Tricky Follow-Ups & Examiner Traps{Color.RESET}     (15 Qs)")
            print(f"  {Color.DIM}[0]{Color.RESET} ⬅️   Back to Lab Selection\n")

            set_choice = prompt_input(f"{Color.BOLD}Choose Practice Set [1 or 2, 0=Back]: {Color.RESET}").strip()
            if set_choice in ("0", "B", "BACK"):
                break
            if set_choice in ("1", "2"):
                run_viva_drill_session(subj_key, set_choice)
                break

def main():
    _init_profile_dialog()
    while True:
        clear_screen()
        print(BANNER)
        _show_session_header()

        print(f"{Color.BOLD}VTU 3RD SEM LAB MODULES & CONCEPT STUDIOS:{Color.RESET}")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 🐙  {Color.BOLD}Git Lab Studio{Color.RESET}  {Color.DIM}(1BCSL307A · 12 Experiments){Color.RESET}")
        print(f"      {Color.DIM}↳ 12 VTU Lab Experiments, Block Explanations, Command Library, Sandbox & Socratic Viva{Color.RESET}")

        print(f"\n  {Color.GREEN}[2]{Color.RESET} 🌳  {Color.BOLD}DSA Lab Studio{Color.RESET}  {Color.DIM}({CODE_DSA_LAB} · 12 Experiments){Color.RESET}")
        print(f"      {Color.DIM}↳ Interactive Memory Sandboxes, 3-Part Block Logic, Disaster Scenarios & Viva{Color.RESET}")

        print(f"\n  {Color.CYAN}[3]{Color.RESET} ☕  {Color.BOLD}Java OOP Lab Studio{Color.RESET}  {Color.DIM}(1BCS302 · 10 Experiments){Color.RESET}")
        print(f"      {Color.DIM}↳ 10 Experiments with 3-Part Block Logic Breakdown, Disaster Scenarios & Viva{Color.RESET}")

        print(f"\n  {Color.MAGENTA}[4]{Color.RESET} ⚡  {Color.BOLD}Quick Reference & In-Terminal Code Vault{Color.RESET}")
        print(f"      {Color.DIM}↳ Instant in-terminal access to all lab source files and experiments at once...{Color.RESET}")

        print(f"\n  {Color.YELLOW}[Q]{Color.RESET} 🎓  {Color.BOLD}High-Yield Viva Practice Hub{Color.RESET}  {Color.DIM}(6 Sets · 90 Top Viva Questions with Socratic Hints){Color.RESET}")

        trophies_count = len(_SESSION.get("trophies", []) or _SESSION.get("badges", []))
        print(f"\n  {Color.MAGENTA}[T]{Color.RESET} 🏆  {Color.BOLD}Educational Milestones (Trophies){Color.RESET}  {Color.DIM}({trophies_count}/{len(_BADGES)} Achieved){Color.RESET}")

        print(f"\n  {Color.DIM}[R]{Color.RESET} 🔄  {Color.DIM}Start Fresh / Reset Local Progress{Color.RESET}")
        print(f"  {Color.DIM}[5]{Color.RESET} 🏃  Exit to Terminal  {Color.DIM}(choose whether to save progress){Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Enter your choice [1 - 5, Q, T, R]: {Color.RESET}").strip().upper()

        if choice == "1":
            mode_git_studio()
        elif choice == "2":
            mode_dsa_studio()
        elif choice == "3":
            mode_java_studio()
        elif choice == "4":
            _show_code_vault()
        elif choice == "Q":
            mode_quickfire_drill_hub()
        elif choice == "T":
            _show_trophy_case()
        elif choice == "R":
            clear_screen()
            print(f"\n{Color.YELLOW}{Color.BOLD}🔄 START FRESH / RESET LOCAL SAVE{Color.RESET}\n")
            print("  This will clear your saved progress and badges on this device so you can start over from scratch.\n")
            confirm = prompt_input(f"  {Color.RED}Are you sure you want to reset local progress? [y/N]: {Color.RESET}").strip().upper()
            if confirm in ("Y", "YES"):
                _clear_local_db()
                print(f"\n  {Color.GREEN}✔ Save cleared! Starting completely fresh! ❤️{Color.RESET}\n")
            else:
                print(f"\n  {Color.CYAN}Reset cancelled. Your saved progress is safe!{Color.RESET}\n")
            time.sleep(1.0)
        elif choice in ("5", "0", "EXIT"):
            _end_of_session_summary()
            break

if __name__ == "__main__":
    _configure_console()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}See you soon buddy! We're in this together ❤️{Color.RESET}\n")
    except Exception as e:
        print(f"\n{Color.RED}Something went wrong: {e}{Color.RESET}\n")
        import traceback
        traceback.print_exc()
        prompt_input("\nPress Enter to exit...")
