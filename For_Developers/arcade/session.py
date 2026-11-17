# pyright: reportMissingImports=false
"""
arcade.session — User profile, local database, educational milestones, and learning progress.
"""
import os
import json
import time

try:
    from arcade.core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, typewrite,
    )
    import arcade.core as _core_mod  # type: ignore
    from arcade.dialogues import print_dialogue  # type: ignore
except (ImportError, ValueError):
    from .core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, typewrite,
    )
    from . import core as _core_mod  # type: ignore
    from .dialogues import print_dialogue  # type: ignore

DB_PATH = os.path.join(PROJECT_ROOT, "oils_local_db.json")

_SESSION = {
    "experiments_done": [],
    "visualizers_explored": [],
    "viva_practiced": 0,
    "trophies": [],
    "badges": [],
    "correct": 0,
    "wrong": 0,
    "start_time": time.time()
}

_BADGES = {
    "git_basics":        {"name": "🐙 Git Foundations", "desc": "Mastered repository setup, staging, commits & status workflow."},
    "git_branches":      {"name": "🌿 Branch & Merge Navigator", "desc": "Mastered branch creation, merging, and merge conflict resolution."},
    "git_recovery":      {"name": "🚨 Git Rescue Specialist", "desc": "Mastered stash, reset, revert, and disaster recovery commands."},
    "git_lab_complete":  {"name": "📦 Git Lab Scholar", "desc": "Explored all 12 official Git Lab experiments & commands (1BCSL307A)."},
    "dsa_memory":        {"name": "🧠 Pointer & Memory Master", "desc": "Explored Stack vs Heap, malloc(), dangling pointers, and free()."},
    "dsa_linear":        {"name": "📦 Stack & Queue Architect", "desc": "Mastered Stack LIFO, Circular Queues, and Infix to Postfix evaluation."},
    "dsa_linked":        {"name": "🔗 Linked List Virtuoso", "desc": "Mastered Singly, Doubly, and Polynomial Linked List operations."},
    "dsa_trees":         {"name": "🌲 BST & Tree Explorer", "desc": "Mastered Binary Search Tree insertion, search & Inorder traversals."},
    "dsa_graphs_hash":   {"name": "🕸️ Graph & Hash Navigator", "desc": "Mastered Hash collisions, Linear Probing, and DFS graph traversals."},
    "dsa_lab_complete":  {"name": "🌳 DSA Lab Scholar", "desc": "Completed all 12 verified Data Structures lab programs (1BCSL306)."},
    "java_oop_core":     {"name": "☕ OOP Core Architect", "desc": "Mastered Classes, Inheritance, Encapsulation & Dynamic Dispatch."},
    "java_concurrency":  {"name": "🧵 Thread & Concurrency Specialist", "desc": "Mastered Multithreading lifecycle, Thread extension, start() and sleep()."},
    "java_lab_complete": {"name": "☕ Java Lab Scholar", "desc": "Completed all 10 verified Java OOP lab programs (1BCS302)."},
    "quickfire_ace":     {"name": "⚡ Quickfire Ace", "desc": "Scored 13+ in a comprehensive viva drill practice set."},
    "vault_dweller":     {"name": "📚 Vault Dweller", "desc": "Explored verified source files in the in-terminal Code Vault."}
}

_TROPHIES = _BADGES

_VISUALIZERS = {
    "DSA-V1": "Stack Memory Sandbox",
    "DSA-V2": "Linear Queue Sandbox",
    "DSA-V3": "Circular Queue Sandbox",
    "DSA-V4": "Singly Linked List Sandbox",
    "DSA-V5": "Circular Linked List Sandbox",
    "DSA-V6": "Binary Search Tree Sandbox",
    "DSA-V7": "Hash Table Sandbox",
}
VISUALIZERS = _VISUALIZERS

def _save_to_local_db():
    """Saves user progress right to their local device — no cloud/backend needed!"""
    try:
        data = {
            "experiments_done": sorted(list(set(_SESSION.get("experiments_done", [])))),
            "visualizers_explored": sorted(list(set(_SESSION.get("visualizers_explored", [])))),
            "viva_practiced": _SESSION.get("viva_practiced", 0),
            "trophies": sorted(list(set(_SESSION.get("trophies", []) or _SESSION.get("badges", [])))),
            "badges": sorted(list(set(_SESSION.get("badges", []) or _SESSION.get("trophies", [])))),
            "last_saved": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def _clear_local_db():
    """Removes the local database file and resets session to start fresh."""
    _SESSION["experiments_done"] = []
    _SESSION["visualizers_explored"] = []
    _SESSION["viva_practiced"] = 0
    _SESSION["trophies"] = []
    _SESSION["badges"] = []
    _SESSION["correct"] = 0
    _SESSION["wrong"] = 0
    if os.path.isfile(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

def _load_from_local_db():
    """Loads existing progress from the local device database on startup."""
    if os.path.isfile(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            _SESSION["experiments_done"] = data.get("experiments_done", [])
            _SESSION["visualizers_explored"] = data.get("visualizers_explored", [])
            _SESSION["viva_practiced"] = data.get("viva_practiced", 0)
            tr = data.get("trophies") or data.get("badges", [])
            _SESSION["trophies"] = tr
            _SESSION["badges"] = tr
            return True
        except Exception:
            pass
    return False

def _unlock_trophy(trophy_id):
    """Unlocks an educational milestone and notifies the student warmly."""
    if trophy_id in _TROPHIES and trophy_id not in _SESSION["trophies"]:
        _SESSION["trophies"].append(trophy_id)
        if trophy_id not in _SESSION["badges"]:
            _SESSION["badges"].append(trophy_id)
        _save_to_local_db()
        t = _TROPHIES[trophy_id]
        print(f"\n  {Color.MAGENTA}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"  ║  🏆  EDUCATIONAL MILESTONE ACHIEVED: {t['name']:<31}║")
        print(f"  ║  ↳ {t['desc']:<62}║")
        print(f"  ╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

def _unlock_badge(badge_id):
    """Alias for unlocking educational milestones."""
    _unlock_trophy(badge_id)

def _check_milestone_badges():
    """Evaluates real learning milestones across Git, DSA, and Java."""
    exps = set(_SESSION.get("experiments_done", []))
    vis = set(_SESSION.get("visualizers_explored", []))

    # Git Milestones
    git_count = len([e for e in exps if str(e).startswith("GIT-")])
    if git_count >= 1:
        _unlock_trophy("git_basics")
    if git_count >= 6:
        _unlock_trophy("git_branches")
    if git_count >= 12:
        _unlock_trophy("git_lab_complete")

    # DSA Milestones
    if "DSA-V1" in vis or "DSA-1" in exps:
        _unlock_trophy("dsa_memory")
    if any(e in exps for e in ("DSA-3", "DSA-4", "DSA-7")) or any(v in vis for v in ("DSA-V1", "DSA-V2", "DSA-V3")):
        _unlock_trophy("dsa_linear")
    if any(e in exps for e in ("DSA-5", "DSA-8")) or any(v in vis for v in ("DSA-V4", "DSA-V5")):
        _unlock_trophy("dsa_linked")
    if any(e in exps for e in ("DSA-6", "DSA-10")) or "DSA-V6" in vis:
        _unlock_trophy("dsa_trees")
    if any(e in exps for e in ("DSA-9", "DSA-11", "DSA-12")) or "DSA-V7" in vis:
        _unlock_trophy("dsa_graphs_hash")

    dsa_count = len([e for e in exps if str(e).startswith("DSA-")])
    if dsa_count >= 12:
        _unlock_trophy("dsa_lab_complete")

    # Java Milestones
    if any(e in exps for e in ("JAVA-1", "JAVA-2", "JAVA-3", "JAVA-4")):
        _unlock_trophy("java_oop_core")
    if any(e in exps for e in ("JAVA-7", "JAVA-8")):
        _unlock_trophy("java_concurrency")

    java_count = len([e for e in exps if str(e).startswith("JAVA-")])
    if java_count >= 10:
        _unlock_trophy("java_lab_complete")

def _init_profile_dialog():
    """Asks user on startup if they want to resume saved progress or start fresh."""
    if not os.path.isfile(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        saved_exps = len(data.get("experiments_done", []))
        saved_vis = len(data.get("visualizers_explored", []))
        saved_trophies = len(data.get("trophies", []) or data.get("badges", []))
        if saved_exps == 0 and saved_vis == 0 and saved_trophies == 0:
            return

        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}{'═'*78}{Color.RESET}")
        print("  💾 SAVED LAB PROGRESS FOUND ON THIS DEVICE")
        print(f"{Color.CYAN}{Color.BOLD}{'═'*78}{Color.RESET}\n")
        print_dialogue("general")

        exps = set(data.get("experiments_done", []))
        git_done = len([e for e in exps if str(e).startswith("GIT-")])
        dsa_done = len([e for e in exps if str(e).startswith("DSA-")])
        java_done = len([e for e in exps if str(e).startswith("JAVA-")])

        print(f"    🐙 Git Lab Progress      : {Color.GREEN}{git_done}/12 Experiments{Color.RESET}")
        print(f"    🌳 DSA Lab Progress      : {Color.GREEN}{dsa_done}/12 Programs{Color.RESET}")
        print(f"    ☕ Java Lab Progress     : {Color.GREEN}{java_done}/10 Programs{Color.RESET}")
        print(f"    🎬 Visualizers Explored  : {Color.CYAN}{saved_vis}/{len(_VISUALIZERS)} Concepts{Color.RESET}")
        print(f"    🏆 Milestones Achieved   : {Color.MAGENTA}{saved_trophies}/{len(_BADGES)} Milestones{Color.RESET}")
        if data.get("last_saved"):
            print(f"    🕒 Last Saved            : {Color.DIM}{data.get('last_saved')}{Color.RESET}")
        print()
        print(f"  {Color.GREEN}{Color.BOLD}[Enter / C]{Color.RESET}  Continue your learning journey")
        print(f"  {Color.YELLOW}{Color.BOLD}[F]{Color.RESET}          Start fresh (Reset saved progress)\n")

        choice = prompt_input(f"  {Color.BOLD}Your choice [Enter to continue, or 'F' to start fresh]: {Color.RESET}").strip().upper()
        if choice in ("F", "FRESH", "RESET", "NEW"):
            _clear_local_db()
            print(f"\n  {Color.YELLOW}✨ Progress reset! Starting fresh! ❤️{Color.RESET}")
            time.sleep(1.0)
        else:
            _load_from_local_db()
            print(f"\n  {Color.GREEN}✔ Welcome back! Loaded your saved lab progress.{Color.RESET}")
            time.sleep(0.7)
    except Exception:
        pass

_FUNNY_PRAISES = [
    "Spot on buddy! You nailed the core logic! ❤️",
    "Great job! That's exactly how it works in memory. 🧠✨",
    "Brilliant catch! You're really mastering this concept step by step. 🌱",
    "Clean and confident! Keep this momentum going, we've got this! 🙌",
    "Awesome! Your conceptual foundation is getting super solid. 💡",
    "You're making genuine progress, one experiment at a time! 🚀",
    "Look at that — you're getting really comfortable with this! 👏",
    "Step by step, everything is starting to make sense! 🧩",
    "Perfect answer buddy! The examiner will love this clarity. 🌟",
    "You're building real engineering intuition! 💎",
]

_FUNNY_ROASTS = [
    "No worries at all buddy! Learning code takes patience — let's review why this works. ❤️",
    "You're close! Take a breath, trace the logic step-by-step, and it will click. 💡",
    "Mistakes are just steps on the way to mastery! Let's break down the concept together. 🌱",
    "Don't worry buddy, tricky concepts take a moment. We will face it together! 🤝",
    "Good try! Look at the underlying principle and you'll see why the other option fits. 🔍",
    "Every small attempt gets you closer to cracking your lab exam! Keep your spirits high! ✨",
    "Take your time buddy! Nobody masters memory and syntax in a single day. ☕",
    "No stress at all! Let's check the explanation below to make it crystal clear. 📖",
]

_MEME_QUOTES = [
    "\"It compiles. Ship it.\" — Every CS student ever 🚀",
    "\"Why does it work? I don't know and I'm scared to ask.\" 😰",
    "\"Undefined behaviour: a love story.\" 💔",
    "\"I'll fix it in production.\" — Famous last words 💀",
    "\"It works on my machine!\" — The classic alibi 🤷",
    "\"Just one more bug, then I'll sleep.\" (3 AM) 🌙",
    "\"git commit -m 'final_FINAL_v3_ACTUALLY_FINAL'\" 😭",
    "\"The code doesn't have bugs, it has undocumented features.\" 🐛✨",
    "\"Semicolon? What semicolon? Oh THAT semicolon!\" 🤦",
    "\"sudo make me a sandwich.\" — The engineer's prayer 🥪",
    "\"It's not a bug, it's a feature request from reality.\" 🌟",
    "\"Have you tried turning it off and on again?\" — Also engineering. 🔄",
    "\"Documentation? We don't do that here.\" 📚🚫",
    "\"rm -rf / — just kidding... mostly.\" 💣",
    "\"malloc(sizeof(clue)) returned NULL.\" — Classic student moment 😂",
    "\"The best code is simple code.\" — Smart thinker 🧠",
    "\"Take it one concept at a time. Nobody learns it in a day!\" ⏳",
    "\"// TODO: understand this when I wake up\" — real comment energy 📝",
]

def _record_concept_mastered(concept_name=""):
    """Records that a concept or question was successfully understood."""
    _SESSION["correct"] = _SESSION.get("correct", 0) + 1
    _SESSION["viva_practiced"] = _SESSION.get("viva_practiced", 0) + 1
    _check_milestone_badges()
    _save_to_local_db()

def _award_xp(points=0, reason=""):
    """Compatibility wrapper that records learning progress."""
    _record_concept_mastered(reason)

def _break_streak(reason=""):
    """Compatibility wrapper that records a learning attempt."""
    _SESSION["wrong"] = _SESSION.get("wrong", 0) + 1
    _SESSION["viva_practiced"] = _SESSION.get("viva_practiced", 0) + 1
    _save_to_local_db()

def _make_progress_bar(done_count, total_count, width=40):
    """Returns an ASCII progress bar string."""
    pct = int((done_count / total_count) * 100) if total_count > 0 else 0
    pct = min(100, pct)
    filled = int(pct / 100 * width)
    bar = Color.GREEN + "█" * filled + Color.DIM + "░" * (width - filled) + Color.RESET
    return f"[{bar}] {done_count:2d}/{total_count:2d} Experiments ({pct}%)"

def _get_subject_counts():
    """Returns (git_done, dsa_done, java_done)."""
    exps = set(_SESSION.get("experiments_done", []))
    git_done = len([e for e in exps if str(e).startswith("GIT-")])
    dsa_done = len([e for e in exps if str(e).startswith("DSA-")])
    java_done = len([e for e in exps if str(e).startswith("JAVA-")])
    return git_done, dsa_done, java_done

def _completion_bar(width=40):
    """Returns overall completion progress across all subjects."""
    git_done, dsa_done, java_done = _get_subject_counts()
    total_done = git_done + dsa_done + java_done
    total_target = 34  # 12 Git + 12 DSA + 10 Java
    pct = int((total_done / total_target) * 100) if total_target > 0 else 0
    pct = min(100, pct)
    filled = int(pct / 100 * width)
    bar = Color.GREEN + "█" * filled + Color.DIM + "░" * (width - filled) + Color.RESET
    return f"Completion [{bar}] {pct}/100 %"

def _xp_bar(xp=None, width=40):
    """Progress bar string."""
    return f"  {_completion_bar(width)}"

def _get_rank(xp=0):
    """Clean title showing syllabus progress instead of gaming levels."""
    exps = set(_SESSION.get("experiments_done", []))
    total = len(exps)
    if total >= 30:
        return "💎 Lab Exam Ready"
    elif total >= 15:
        return "🌟 Steady Practitioner"
    elif total >= 5:
        return "🌱 Lab Explorer"
    else:
        return "🐣 Curious Beginner"

def _show_session_header(show_welcome=True, subject=None):
    """Print clean learning progress and local DB status header."""
    if show_welcome:
        print_dialogue(subject or "general")

    git_done, dsa_done, java_done = _get_subject_counts()

    if subject == "git":
        bar = _make_progress_bar(git_done, 12, width=40)
        print(f"  {Color.BOLD}Git Lab (1BCSL307A):{Color.RESET}   {bar}")
    elif subject == "dsa":
        bar = _make_progress_bar(dsa_done, 12, width=40)
        print(f"  {Color.BOLD}DSA Lab (1BCSL306):{Color.RESET}    {bar}")
    elif subject == "java":
        bar = _make_progress_bar(java_done, 10, width=40)
        print(f"  {Color.BOLD}Java Lab (1BCS302):{Color.RESET}    {bar}")
    else:
        bar_git = _make_progress_bar(git_done, 12, width=40)
        bar_dsa = _make_progress_bar(dsa_done, 12, width=40)
        bar_java = _make_progress_bar(java_done, 10, width=40)
        print(f"  {Color.BOLD}Git Lab (1BCSL307A):{Color.RESET}   {bar_git}")
        print(f"  {Color.BOLD}DSA Lab (1BCSL306):{Color.RESET}    {bar_dsa}")
        print(f"  {Color.BOLD}Java Lab (1BCS302):{Color.RESET}    {bar_java}")

    print(f"  {Color.DIM}💾 Local DB: Active (Saved on your device){Color.RESET}\n")

def _mark_experiment_done(exp_id):
    """Marks an experiment as completed, evaluates milestones, and saves to DB."""
    if "experiments_done" not in _SESSION:
        _SESSION["experiments_done"] = []
    if exp_id not in _SESSION["experiments_done"]:
        _SESSION["experiments_done"].append(exp_id)
    _check_milestone_badges()
    _save_to_local_db()

def _record_visualizer_explored(vis_id):
    """Marks a visualizer as explored and checks milestones."""
    if "visualizers_explored" not in _SESSION:
        _SESSION["visualizers_explored"] = []
    if vis_id not in _SESSION["visualizers_explored"]:
        _SESSION["visualizers_explored"].append(vis_id)
        _check_milestone_badges()
        _save_to_local_db()

def _end_of_session_summary():
    """Full end-of-session learning summary — asks before saving progress."""
    clear_screen()
    elapsed = int(time.time() - _SESSION.get("start_time", time.time()))
    mins = elapsed // 60
    secs = elapsed % 60
    
    exps = set(_SESSION.get("experiments_done", []))
    git_done = len([e for e in exps if str(e).startswith("GIT-")])
    dsa_done = len([e for e in exps if str(e).startswith("DSA-")])
    java_done = len([e for e in exps if str(e).startswith("JAVA-")])
    total_exps = git_done + dsa_done + java_done
    
    vis_done = len(_SESSION.get("visualizers_explored", []))
    viva_done = _SESSION.get("viva_practiced", 0)
    trophies_unlocked = len(_SESSION.get("trophies", []) or _SESSION.get("badges", []))

    print(f"\n{Color.CYAN}{Color.BOLD}{'═'*74}{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}  🎓 LEARNING SESSION SUMMARY — OILS-3 LAB COMPANION{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}{'═'*74}{Color.RESET}\n")

    print_dialogue("general")
    typewrite(f"  ⏱️  Time Spent Learning : {mins}m {secs}s", 0.012, Color.CYAN)
    typewrite(f"  🧪 Lab Experiments Done : {total_exps}/34 (Git: {git_done}/12 · DSA: {dsa_done}/12 · Java: {java_done}/10)", 0.012, Color.GREEN)
    typewrite(f"  🎬 Visualizers Explored : {vis_done}/{len(_VISUALIZERS)} Core Memory & Architecture Concepts", 0.012, Color.BLUE)
    typewrite(f"  🎯 Viva Q&A Practiced   : {viva_done} Questions Explored", 0.012, Color.YELLOW)
    typewrite(f"  🏆 Milestones Achieved  : {trophies_unlocked}/{len(_TROPHIES)} Educational Milestones Unlocked", 0.012, Color.MAGENTA)
    print()

    active_trophies = _SESSION.get("trophies", []) or _SESSION.get("badges", [])
    if active_trophies:
        names = ", ".join(_TROPHIES[tid]["name"] for tid in active_trophies if tid in _TROPHIES)
        print(f"     ↳ {Color.GREEN}{names}{Color.RESET}")
    print()

    typewrite("  🌟 FANTASTIC SESSION! Every concept you practice gets you closer to cracking your labs! 💎", 0.015, Color.GREEN)

    print(f"\n{Color.CYAN}{'─'*74}{Color.RESET}")
    print(f"  {Color.BOLD}💾 LOCAL DEVICE DATABASE SAVE:{Color.RESET}")
    print("  Do you want to save what you've learned until now on this device,")
    print("  or would you like to start fresh when you open the terminal again?\n")
    print(f"    {Color.GREEN}[Enter / Y]{Color.RESET}  Save my progress to this device (Resume next time)")
    print(f"    {Color.YELLOW}[N / F]{Color.RESET}      Don't save — start completely fresh next time\n")
    save_choice = prompt_input(f"  {Color.BOLD}Save progress to device? [Y/n]: {Color.RESET}").strip().upper()

    if save_choice in ("", "Y", "YES", "S", "SAVE"):
        _save_to_local_db()
        print(f"\n  {Color.GREEN}✔ Progress saved locally on your device! See you next time buddy! ❤️{Color.RESET}\n")
    else:
        _clear_local_db()
        print(f"\n  {Color.YELLOW}🔄 Local save cleared! You will start fresh next time! ❤️{Color.RESET}\n")

    print(f"{Color.CYAN}{Color.BOLD}{'═'*74}{Color.RESET}\n")
    prompt_input("  Press Enter to exit... ❤️  ")

def _show_trophy_case():
    """Displays the educational milestone cabinet."""
    clear_screen()
    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*78}{Color.RESET}")
    print("  🏆 OILS-3 EDUCATIONAL MILESTONES & SYLLABUS MASTERY")
    print(f"{Color.MAGENTA}{Color.BOLD}{'═'*78}{Color.RESET}")
    _show_session_header()

    active_trophies = _SESSION.get("trophies", []) or _SESSION.get("badges", [])
    unlocked_count = len(active_trophies)
    total_count = len(_TROPHIES)
    print(f"  {Color.BOLD}Your Academic Milestones: {Color.YELLOW}{unlocked_count}/{total_count} Achieved{Color.RESET}\n")

    for tid, t in _TROPHIES.items():
        if tid in active_trophies:
            status = f"{Color.GREEN}{Color.BOLD}[🏆 ACHIEVED]{Color.RESET}"
            title = f"{Color.GREEN}{Color.BOLD}{t['name']}{Color.RESET}"
        else:
            status = f"{Color.DIM}[🔒 PENDING ]{Color.RESET} "
            title = f"{Color.DIM}{t['name']}{Color.RESET}"
        print(f"  {status} {title:<36} {Color.DIM}— {t['desc']}{Color.RESET}")

    print(f"\n{Color.DIM}{'─'*78}{Color.RESET}")
    prompt_input("\n  Press Enter to return to Main Menu... ")

BANNER_ART = r"""
   ____  ___ _     ____       _____
  / __ \|_ _| |   / ___|     |___ /
 | |  | || || |   \___ \ _____  |_ \
 | |__| || || |___ ___) |_____|___) |
  \____/|___|_____|____/      |____/
"""

BANNER = f"""{Color.CYAN}{Color.BOLD}{BANNER_ART}{Color.RESET}
{Color.YELLOW}{Color.BOLD}        🚀 Oops, I Learnt Something! — 3rd Sem Engineering, An Interactive Game to Crack Your Labs (VTU 2025 Scheme)
{Color.DIM}        Git (1BCSL307A) · DSA Lab (1BCSL306) · Java OOP Lab (1BCS302){Color.RESET}
"""



# Inject real funny praise and roast lists into arcade.core
_core_mod._FUNNY_PRAISES = _FUNNY_PRAISES
_core_mod._FUNNY_ROASTS = _FUNNY_ROASTS
