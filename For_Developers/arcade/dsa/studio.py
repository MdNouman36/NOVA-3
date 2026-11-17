# pyright: reportMissingImports=false
"""
arcade.dsa.studio — DSA Lab Studio (1BCSL306 — 12 Experiments, VTU 2025 Scheme).
Interactive memory sandboxes, fast & fun block logic breakdowns, disaster recovery & viva.
"""
import os
import time
import random

try:
    from arcade.core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, spinner,
        print_slow, anim_correct, anim_wrong, shuffle_mcq_options,
    )
    from arcade.session import (  # type: ignore
        _SESSION, _record_concept_mastered, _unlock_badge,
        _save_to_local_db, _show_session_header, _mark_experiment_done,
    )
    from arcade.vault import _view_source_file  # type: ignore
    from arcade.dsa.experiments_data import DSA_EXPERIMENTS  # type: ignore
    from arcade.dsa.disasters import DSA_DISASTER_SCENARIOS  # type: ignore
    from arcade.dsa.vivas import DSA_VIVA_GAUNTLET  # type: ignore
    from arcade.dsa.visualizers_interactive import (  # type: ignore
        visualizer_stack,
        visualizer_linear_queue,
        visualizer_circular_queue,
        visualizer_singly_linked_list,
        visualizer_circular_linked_list,
        visualizer_bst,
        visualizer_hash_table,
        mode_dsa_visualizers_menu,
    )
except (ImportError, ValueError):
    from ..core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, spinner,
        print_slow, anim_correct, anim_wrong, shuffle_mcq_options,
    )
    from ..session import (  # type: ignore
        _SESSION, _record_concept_mastered, _unlock_badge,
        _save_to_local_db, _show_session_header, _mark_experiment_done,
    )
    from ..vault import _view_source_file  # type: ignore
    from .experiments_data import DSA_EXPERIMENTS  # type: ignore
    from .disasters import DSA_DISASTER_SCENARIOS  # type: ignore
    from .vivas import DSA_VIVA_GAUNTLET  # type: ignore
    from .visualizers_interactive import (  # type: ignore
        visualizer_stack,
        visualizer_linear_queue,
        visualizer_circular_queue,
        visualizer_singly_linked_list,
        visualizer_circular_linked_list,
        visualizer_bst,
        visualizer_hash_table,
        mode_dsa_visualizers_menu,
    )

# Map experiments to interactive sandboxes
EXP_SANDBOX_MAP = {
    3: ("📦 Interactive Stack Memory Sandbox", visualizer_stack),
    4: ("🔄 Interactive Linear & Circular Queue Sandbox", visualizer_circular_queue),
    5: ("⭕ Interactive Circular Linked List Sandbox", visualizer_circular_linked_list),
    8: ("🔗 Interactive Singly Linked List Sandbox", visualizer_singly_linked_list),
    9: ("🗄️ Interactive Hash Table Sandbox", visualizer_hash_table),
    10: ("🌳 Interactive Binary Search Tree Sandbox", visualizer_bst),
    11: ("🗄️ Interactive Hash Table Sandbox", visualizer_hash_table),
}


def mode_dsa_disaster():
    clear_screen()
    print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║        🚨 MODE: DSA LAB DISASTER RECOVERY (8 REAL EMERGENCIES)     ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_slow("These are actual bugs and pointer disasters students encounter in lab exams.", 0.012, Color.CYAN)
    print_slow("Identify the root cause and save your program before the system crashes!\n", 0.012)

    score = 0
    scenarios = list(DSA_DISASTER_SCENARIOS)
    random.shuffle(scenarios)
    for i, s in enumerate(scenarios, 1):
        clear_screen()
        print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║     🚨 DSA EMERGENCY {i}/{len(scenarios)}: EXAM DISASTER IN PROGRESS          ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print(f"{Color.BOLD}{Color.WHITE}{s['title']}{Color.RESET}\n")
        print_slow(s['story'], 0.010, Color.WHITE)
        print(f"\n{Color.CYAN}{Color.BOLD}Diagnostic Question:{Color.RESET}\n  {s['prompt']}\n")

        # Dynamically shuffle disaster choices so option 1 isn't always correct!
        shuffled_choices, target_idx = shuffle_mcq_options(s["choices"], s["ans_idx"])
        for idx, ch in enumerate(shuffled_choices, 1):
            print(f"  {Color.YELLOW}[{idx}]{Color.RESET} {ch}")

        while True:
            pick = prompt_input(f"\n{Color.BOLD}Your decision [1 - {len(shuffled_choices)}] (0=Menu): {Color.RESET}").strip()
            if pick in ["0", "menu", "q", "exit"]:
                return
            if pick.isdigit() and 1 <= int(pick) <= len(shuffled_choices):
                pick = int(pick)
                break
            print(f"{Color.RED}Please enter 1, 2, 3, or 4!{Color.RESET}")

        spinner("Analyzing heap state & pointer registers", duration=0.6, color=Color.RED)

        if pick == target_idx:
            anim_correct()
            _record_concept_mastered("disaster averted")
            _unlock_badge("dsa_memory")
            score += 150
            print(f"\n{Color.GREEN}{Color.BOLD}✅ DISASTER AVERTED! Bug diagnosed and resolved.{Color.RESET}")
            print(f"{Color.GREEN}{s['reaction']}{Color.RESET}\n")
        else:
            anim_wrong()
            print(f"\n{Color.RED}{Color.BOLD}❌ WRONG DIAGNOSIS! Correct answer was [{target_idx}]:{Color.RESET}")
            print(f"   {Color.WHITE}{shuffled_choices[target_idx - 1]}{Color.RESET}")
            print(f"\n{Color.DIM}{s['reaction']}{Color.RESET}\n")
        prompt_input(f"{Color.DIM}Press Enter for next scenario...{Color.RESET}")

    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*51}")
    print(f"  DSA Disaster Recovery Complete! Score: {score}/{len(scenarios)*150}")
    print(f"{'═'*51}{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def run_dsa_experiment_lab(exp):
    base_dir = PROJECT_ROOT
    source_path = os.path.join(base_dir, exp["file"])

    # Stage 1: The Big Picture Story
    clear_screen()
    print()
    _show_session_header(subject="dsa")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  🌳 EXPERIMENT {exp['num']:02d} ({exp['part']}): {exp['title']:<52} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()
    print(f"{Color.YELLOW}{Color.BOLD}[Stage 1/4] 💡 THE BIG PICTURE STORY (How the whole program works):{Color.RESET}")
    print()
    story_text = exp.get("story", exp.get("concept", ""))
    print_slow(f"  {story_text}", 0.008, Color.WHITE)
    print()
    print(f"{Color.CYAN}{Color.BOLD}🎯 VTU Lab Requirement:{Color.RESET}")
    print(f"  {exp['problem']}")
    print()

    # Direct launch prompt if this experiment has an interactive sandbox
    sb_tuple = EXP_SANDBOX_MAP.get(exp["num"])
    if sb_tuple:
        sb_name, _ = sb_tuple
        print(f"  {Color.YELLOW}[S]{Color.RESET} 🎬 {Color.BOLD}Launch {sb_name}{Color.RESET}")

    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the complete C code first...{Color.RESET}")

    # Stage 2: Complete Source Code
    clear_screen()
    print()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  📄 [Stage 2/4] COMPLETE VERIFIED C PROGRAM CODE                              ║")
    print(f"║  Source: {exp['file']:<68} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    funny_spinners = [
        "Consulting Stack Overflow (just kidding, we have the code)",
        "malloc()-ing your brain cells for maximum absorption",
        "Compiling elegance into your neurons",
    ]
    spinner(random.choice(funny_spinners), duration=0.4, color=Color.GREEN)
    print()

    if os.path.isfile(source_path):
        with open(source_path, "r", encoding="utf-8", errors="replace") as sf:
            lines = sf.readlines()
        preview_limit = min(36, len(lines))
        for idx in range(preview_limit):
            print(f"{Color.DIM}{idx+1:3d} |{Color.RESET} {lines[idx]}", end="")
        if len(lines) > preview_limit:
            print(f"\n  {Color.YELLOW}... [{len(lines) - preview_limit} more lines in full file: {exp['file']}]{Color.RESET}")
    else:
        print(f"  {Color.RED}Source file available in {exp['file']}{Color.RESET}")

    print()
    print(Color.DIM + ("─" * 80) + Color.RESET)
    extra_prompt = f"   {Color.YELLOW}[S]{Color.RESET} Sandbox" if sb_tuple else ""
    print(f"  {Color.CYAN}Options:{Color.RESET}  {Color.YELLOW}[V]{Color.RESET} View Full Code in Vault{extra_prompt}   {Color.GREEN}[Enter]{Color.RESET} Continue to Logic Breakdown")
    sub_pick = prompt_input("  Your choice: ").strip().upper()
    if sub_pick == "V":
        _view_source_file(source_path, exp['title'])
    elif sub_pick == "S" and sb_tuple:
        sb_tuple[1]()

    # Stage 3: Fast & Fun 3-Bullet Block Logic Breakdown
    clear_screen()
    print()
    print(Color.MAGENTA + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🔍 [Stage 3/4] STEP-BY-STEP CODE EXPLANATION (From First Line to Last Line) ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    for idx, b in enumerate(exp["blocks"], 1):
        print(f"  {Color.YELLOW}{Color.BOLD}🧱 Block {idx}: {b['title']}{Color.RESET}")
        print("  " + Color.DIM + ("─" * 72) + Color.RESET)
        for l in b["code"].splitlines():
            print(f"    {Color.WHITE}{Color.BOLD}{l}{Color.RESET}")
        print("  " + Color.DIM + ("─" * 72) + Color.RESET)

        # 1. 🎯 What we are doing
        doing_text = b.get("doing", b.get("purpose", ""))
        print(f"  {Color.GREEN}{Color.BOLD}1. 🎯 What we are doing:{Color.RESET}")
        print(f"     {doing_text}\n")

        # 2. 🔍 How it works
        how_items = b.get("how", b.get("inside", []))
        if how_items:
            print(f"  {Color.CYAN}{Color.BOLD}2. 🔍 How it works:{Color.RESET}")
            for item in how_items:
                print(f"     • {item}")
            print()

        # 3. 💡 Real-world intuition / Watch out
        watchout_text = b.get("watchout", "")
        if watchout_text:
            print(f"  {Color.YELLOW}{Color.BOLD}3. 💡 Real-World Intuition / Exam Trap:{Color.RESET}")
            print(f"     {watchout_text}\n")

        if idx < len(exp["blocks"]):
            prompt_input(f"  {Color.DIM}Press Enter for Block {idx+1}...{Color.RESET}\n")

    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Ready? Press Enter to test your understanding with a quick challenge!{Color.RESET}")

    # Stage 4: Guided Code Challenge (MCQ with Dynamic Randomization)
    clear_screen()
    ch = exp["challenge"]
    print()
    print(Color.YELLOW + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🎮 [Stage 4/4] GUIDED CODE CHALLENGE — Check Your Understanding!             ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()
    _show_session_header(subject="dsa")

    print(f"{Color.BOLD}{Color.WHITE}{ch['prompt']}{Color.RESET}\n")

    if "opts" in ch:
        # Dynamically shuffle options so correct answer is truly random on the fly!
        shuffled_opts, target_opt = shuffle_mcq_options(ch["opts"], ch.get("correct_opt", "A"))
        for opt in shuffled_opts:
            print(f"  {Color.CYAN}{opt}{Color.RESET}")
        print()
        print("  " + Color.DIM + "(Tip: Type A, B, C, D or 'H' for a Hint  |  No shame in hints!)" + Color.RESET)
        print()

        while True:
            ans = prompt_input(f"{Color.BOLD}Your Answer [A/B/C/D] (or 'H' for Hint): {Color.RESET}").strip().upper()
            if ans == "H":
                print(f"\n  {Color.YELLOW}💡 HINT: {ch['hint']}{Color.RESET}\n")
                continue
            if ans in ("A", "B", "C", "D"):
                break
            print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

        spinner("Analyzing your answer", duration=0.4, color=Color.CYAN)

        if ans == target_opt:
            anim_correct()
            _record_concept_mastered("MCQ correct")
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 {ch['praise']}{Color.RESET}\n")
        else:
            anim_wrong()
            print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
            print(f"   {Color.YELLOW}✅ Expected Answer was ({target_opt}): {ch['hint']}{Color.RESET}\n")

    # Mark experiment as done
    exp_id = f"DSA-{exp['num']}"
    _mark_experiment_done(exp_id)

    print(f"{Color.DIM}File location: {exp['file']}{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to DSA Lab Studio...{Color.RESET}")


def mode_dsa_viva():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎓 DSA LAB VIVA PREP & CONCEPT MASTERY (1BCSL306) 🎓{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print("  Stress-free practice with Socratic hints and examiner expectations.\n")

    score = 0
    questions = list(DSA_VIVA_GAUNTLET)
    random.shuffle(questions)

    for idx, q in enumerate(questions, 1):
        # Dynamically shuffle options so answer is truly randomized!
        shuffled_opts, target_ans = shuffle_mcq_options(q["options"], q["ans"])
        print(f"\n{Color.CYAN}{Color.BOLD}[Question {idx}/{len(questions)}]{Color.RESET}")
        print(f"{Color.BOLD}{q['q']}{Color.RESET}\n")
        for opt in shuffled_opts:
            print(f"  {opt}")

        attempt = 1
        solved = False
        while attempt <= 2 and not solved:
            prompt_str = "\nYour Answer [A / B / C / D] (or 'H' for Clue, 0 to Exit): " if attempt == 1 else "\nSecond Try [A / B / C / D]: "
            ans = prompt_input(prompt_str).strip().upper()

            if ans in ("0", "EXIT", "Q"):
                return
            if ans == "H":
                print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                continue
            if ans not in ("A", "B", "C", "D"):
                print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")
                continue

            if ans == target_ans:
                solved = True
                anim_correct()
                _record_concept_mastered("viva correct")
                score += 1
                if attempt == 1:
                    print(f"  {Color.GREEN}{Color.BOLD}✔ {q['praise']}{Color.RESET}")
                else:
                    print(f"  {Color.GREEN}{Color.BOLD}🎉 Excellent recovery! You got it right!{Color.RESET}")
            else:
                anim_wrong()
                if attempt == 1:
                    print(f"  {Color.YELLOW}🌱 Not quite! {q['roast']}{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                    attempt += 1
                else:
                    print(f"  {Color.MAGENTA}No worries! The correct answer is [{target_ans}].{Color.RESET}")
                    attempt += 1

        print(f"\n  {Color.CYAN}💡 Examiner Expectation: {q['tip']}{Color.RESET}")
        prompt_input(f"\n{Color.DIM}Press Enter for next question...{Color.RESET}")

    print(f"\n{Color.CYAN}===================================================={Color.RESET}")
    print(f"  🎉 Viva Practice Complete! Mastered: {Color.BOLD}{score}/{len(questions)} Concepts{Color.RESET}")
    print(f"{Color.CYAN}===================================================={Color.RESET}\n")
    prompt_input("Press Enter to return...")


def mode_dsa_studio():
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  🌳 DSA LAB STUDIO: 1BCSL306 (VTU 2025 Scheme — 12 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="dsa")
        print(f"  {Color.YELLOW}[VS]{Color.RESET} 🎬 {Color.BOLD}Interactive Data Structure Visualizer Suite{Color.RESET} (7 Interactive Memory Sandboxes)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨 DSA Lab Emergency Recovery (8 Real Exam Problem Scenarios)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 DSA Lab Viva Prep & Examiner Expectations")
        print(f"{Color.CYAN}{'─'*78}{Color.RESET}")
        print(f"  {Color.BOLD}PART A: FIXED EXPERIMENTS{Color.RESET}")
        for i in range(6):
            exp = DSA_EXPERIMENTS[i]
            done = "✅" if f"DSA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.BOLD}PART B: OPEN-ENDED EXPERIMENTS{Color.RESET}")
        for i in range(6, 12):
            exp = DSA_EXPERIMENTS[i]
            done = "✅" if f"DSA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 12, VS, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice in ("VS", "V", "VIS"):
            mode_dsa_visualizers_menu()
        elif choice == "DR":
            mode_dsa_disaster()
        elif choice == "VG":
            mode_dsa_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 12:
                run_dsa_experiment_lab(DSA_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)
