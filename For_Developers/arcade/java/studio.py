# pyright: reportMissingImports=false
"""
arcade.java.studio — Java OOP Lab Studio (1BCS302 — 10 Experiments, VTU 2025 Scheme).
Interactive architecture & runtime sandboxes, fast & fun block logic breakdowns & viva.
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
    from arcade.java.experiments_data import JAVA_EXPERIMENTS  # type: ignore
    from arcade.java.disasters import JAVA_DISASTER_SCENARIOS  # type: ignore
    from arcade.java.vivas import JAVA_VIVA_GAUNTLET  # type: ignore
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
    from .experiments_data import JAVA_EXPERIMENTS  # type: ignore
    from .disasters import JAVA_DISASTER_SCENARIOS  # type: ignore
    from .vivas import JAVA_VIVA_GAUNTLET  # type: ignore


# ==============================================================================
# INTERACTIVE OOP & RUNTIME SANDBOXES (Commit 237ae62 Style)
# ==============================================================================

def visualizer_polymorphism():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🎭 RUNTIME POLYMORPHISM & VIRTUAL METHOD TABLE (Lab 04: Shape Hierarchy)   ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("  Concept: Superclass reference pointing to different objects on the JVM Heap:\n")
    print(f"    {Color.YELLOW}Shape s;{Color.RESET} (Reference variable allocated on Call Stack)")
    prompt_input(f"    {Color.DIM}Press Enter for Step 1 (Instantiating Circle)...{Color.RESET}")

    print(f"\n  [Step 1] s = {Color.GREEN}new Circle(){Color.RESET};  --> Heap allocates Circle object with its own vtable")
    print(f"           s.draw();           --> JVM invokes {Color.GREEN}Circle.draw() ⭕{Color.RESET}")
    prompt_input(f"    {Color.DIM}Press Enter for Step 2 (Reassigning to Triangle)...{Color.RESET}")

    print(f"\n  [Step 2] s = {Color.BLUE}new Triangle(){Color.RESET}; --> Heap allocates Triangle object")
    print(f"           s.draw();             --> Dynamic dispatch invokes {Color.BLUE}Triangle.draw() 🔺{Color.RESET}")
    prompt_input(f"    {Color.DIM}Press Enter for Step 3 (Reassigning to Square)...{Color.RESET}")

    print(f"\n  [Step 3] s = {Color.MAGENTA}new Square(){Color.RESET};   --> Heap allocates Square object")
    print(f"           s.draw();           --> Dynamic dispatch invokes {Color.MAGENTA}Square.draw() ⬛{Color.RESET}")

    print(f"\n{Color.CYAN}────────────────────────────────────────────────────────────────────────{Color.RESET}")
    print("  💡 Examiner Key Takeaways:")
    print("  1. Method call `s.draw()` resolves at RUNTIME based on the ACTUAL OBJECT type, not reference type.")
    print("  2. This is the definition of Dynamic Method Dispatch (Runtime Polymorphism).")
    print(f"{Color.CYAN}────────────────────────────────────────────────────────────────────────{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def visualizer_threads():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🧵 THREAD LIFE-CYCLE STATE MACHINE & CONCURRENCY (Lab 08: Threads)         ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("""
       [NEW] ──(start())──> [RUNNABLE] <───> [TIMED_WAITING] (sleep / wait)
                                 │
                                 └──(run() ends)──> [TERMINATED]
    """)
    print("  Step-by-step thread execution trace:\n")
    print("    [Step 1] Thread t = new ChildThread(); --> State: [NEW] (Object created, no thread spawned yet)")
    prompt_input(f"    {Color.DIM}Press Enter for Step 2...{Color.RESET}")

    print("    [Step 2] t.start();                    --> State: [RUNNABLE] (JVM creates separate call stack!)")
    prompt_input(f"    {Color.DIM}Press Enter for Step 3 (Concurrent execution)...{Color.RESET}")

    print("\n    [Step 3] JVM context switching between Main & Child thread:")
    for i in range(1, 4):
        print(f"       {Color.BLUE}[Main Thread]  Executing iteration {i}{Color.RESET}")
        time.sleep(0.35)
        print(f"       {Color.GREEN}[Child Thread] Executing iteration {i}{Color.RESET}")
        time.sleep(0.35)

    prompt_input(f"\n    {Color.DIM}Press Enter for Step 4...{Color.RESET}")
    print("\n    [Step 4] run() method completes       --> State: [TERMINATED] (Thread terminates cleanly)")
    print(f"\n  {Color.GREEN}✔ Concurrent execution and life-cycle demonstrated cleanly!{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def visualizer_stack_java():
    """Interactive Stack OOP Encapsulation Sandbox."""
    stack = [15, 30]
    cap = 4
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   ☕ JAVA STACK OOP ENCAPSULATION SANDBOX (Lab 02: Stack Class)               ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("  Heap Object State:")
        print("    Instance: Stack@7a81197d  |  private int[] s = new int[4]")
        print("         +------------+")
        for i in range(cap - 1, -1, -1):
            if i < len(stack):
                tag = f" {Color.YELLOW}<-- private int top = {i}{Color.RESET}" if i == len(stack) - 1 else ""
                print(f"      [{i}] |  {Color.GREEN}{stack[i]:6d}{Color.RESET}    |{tag}")
            else:
                print(f"      [{i}] |  {Color.DIM}(empty){Color.RESET}   |")
        print("         +------------+\n")

        print(f"  Actions: {Color.YELLOW}[1] s.push(val){Color.RESET}  {Color.RED}[2] s.pop(){Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 2, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            if len(stack) >= cap:
                print(f"\n  {Color.RED}🚨 Stack Overflow! (top == capacity - 1){Color.RESET}")
                prompt_input("Press Enter to continue...")
            else:
                val = prompt_input("Enter integer value to push: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    int_val = int(val)
                    print(f"\n  {Color.YELLOW}Step 1:{Color.RESET} s[++top] = {int_val} (Pre-increment advances top to {len(stack)})")
                    stack.append(int_val)
                    time.sleep(0.4)
        elif cmd == "2":
            if not stack:
                print(f"\n  {Color.RED}🚨 Stack Underflow! (top == -1){Color.RESET}")
                prompt_input("Press Enter to continue...")
            else:
                removed = stack.pop()
                print(f"\n  {Color.YELLOW}Step 1:{Color.RESET} return s[top--] (Captured {Color.GREEN}{removed}{Color.RESET}, top now {len(stack)-1})")
                time.sleep(0.4)
        elif cmd in ("0", "b", "exit", "back"):
            break


def visualizer_exceptions_java():
    """Call Stack Unwinding Sandbox for Java Exceptions."""
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   ⚠️  JAVA EXCEPTION CALL STACK UNWINDING (Lab 07: Custom Exception)          ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("  Execution Call Stack Trace for: divide(10, 0)\n")
    print("    [Frame 3] divide(int a, int b)   ──> Detected b == 0!")
    print("              throw new DivisionByZeroException(\"Cannot divide by zero\");")
    prompt_input(f"\n    {Color.DIM}Press Enter for Step 1: Throwing Exception...{Color.RESET}")

    print(f"\n  {Color.RED}💥 EXCEPTION INSTANTIATED on Heap: DivisionByZeroException{Color.RESET}")
    print("     JVM begins Call Stack Unwinding looking for matching 'catch' block...")
    prompt_input(f"\n    {Color.DIM}Press Enter for Step 2: Unwinding Call Stack...{Color.RESET}")

    print("\n    [Frame 3] Popped from stack (no try-catch inside divide)")
    print("    [Frame 2] main(String[] args)  ──> Has try block!")
    print(f"              {Color.GREEN}catch (DivisionByZeroException e){Color.RESET} MATCHES exception type!")
    prompt_input(f"\n    {Color.DIM}Press Enter for Step 3: Catch & Finally Execution...{Color.RESET}")

    print(f"\n  {Color.GREEN}✔ Catch block handles error:{Color.RESET} e.getMessage() -> 'Cannot divide by zero'")
    print(f"  {Color.YELLOW}✔ Finally block executes:{Color.RESET} Scanner.close(); (Cleanup guaranteed!)")
    print(f"  {Color.CYAN}✔ Program resumes execution normally without JVM crash.{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def mode_java_visualizers_menu():
    """Menu for all interactive Java OOP sandboxes."""
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   ☕ INTERACTIVE JAVA OOP & ARCHITECTURE VISUALIZERS                         ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 🎭  Runtime Polymorphism & VTable Dispatch (Lab 04: Shape)")
        print(f"  {Color.YELLOW}[2]{Color.RESET} 🧵  Thread Life-Cycle & Interleaved Concurrency (Lab 08: Threads)")
        print(f"  {Color.YELLOW}[3]{Color.RESET} 📦  Stack Class Encapsulation Sandbox (Lab 02: Stack)")
        print(f"  {Color.YELLOW}[4]{Color.RESET} ⚠️   Custom Exception Call Stack Unwinding (Lab 07: Exception)")
        print(f"\n  {Color.DIM}[0]   ⬅️  Back to Java Lab Studio{Color.RESET}\n")

        ch = prompt_input(f"{Color.BOLD}Choose Visualizer [1 - 4, 0=Back]: {Color.RESET}").strip()
        if ch in ("0", "B", "BACK", "EXIT"):
            return
        elif ch == "1":
            visualizer_polymorphism()
        elif ch == "2":
            visualizer_threads()
        elif ch == "3":
            visualizer_stack_java()
        elif ch == "4":
            visualizer_exceptions_java()


# Map Java experiments to interactive sandboxes
JAVA_EXP_SANDBOX_MAP = {
    2: ("📦 Stack Encapsulation Sandbox", visualizer_stack_java),
    4: ("🎭 Runtime Polymorphism Sandbox", visualizer_polymorphism),
    7: ("⚠️ Exception Call Stack Sandbox", visualizer_exceptions_java),
    8: ("🧵 Thread Concurrency Sandbox", visualizer_threads),
}


# ==============================================================================
# DISASTER RECOVERY & EXPERIMENT RUNNER
# ==============================================================================

def mode_java_disaster():
    clear_screen()
    print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║       🚨 MODE: JAVA OOP DISASTER RECOVERY (8 REAL EMERGENCIES)     ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_slow("These are real-world runtime exceptions and JVM traps students hit in exams.", 0.012, Color.CYAN)
    print_slow("Diagnose the bug before the JVM throws a fatal exception!\n", 0.012)

    score = 0
    scenarios = list(JAVA_DISASTER_SCENARIOS)
    random.shuffle(scenarios)
    for i, s in enumerate(scenarios, 1):
        clear_screen()
        print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║     🚨 JAVA EMERGENCY {i}/{len(scenarios)}: RUNTIME DISASTER IN PROGRESS       ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print(f"{Color.BOLD}{Color.WHITE}{s['title']}{Color.RESET}\n")
        print_slow(s['story'], 0.010, Color.WHITE)
        print(f"\n{Color.CYAN}{Color.BOLD}Diagnostic Question:{Color.RESET}\n  {s['prompt']}\n")

        # Dynamically shuffle choices so correct answer lands randomly!
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

        spinner("Inspecting JVM stack trace & classloader registers", duration=0.6, color=Color.RED)

        if pick == target_idx:
            anim_correct()
            _record_concept_mastered("java disaster averted")
            _unlock_badge("java_oop_core")
            score += 150
            print(f"\n{Color.GREEN}{Color.BOLD}✅ DISASTER AVERTED! Exception resolved.{Color.RESET}")
            print(f"{Color.GREEN}{s['reaction']}{Color.RESET}\n")
        else:
            anim_wrong()
            print(f"\n{Color.RED}{Color.BOLD}❌ WRONG DIAGNOSIS! Correct answer was [{target_idx}]:{Color.RESET}")
            print(f"   {Color.WHITE}{shuffled_choices[target_idx - 1]}{Color.RESET}")
            print(f"\n{Color.DIM}{s['reaction']}{Color.RESET}\n")
        prompt_input(f"{Color.DIM}Press Enter for next scenario...{Color.RESET}")

    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*51}")
    print(f"  Java Disaster Recovery Complete! Score: {score}/{len(scenarios)*150}")
    print(f"{'═'*51}{Color.RESET}\n")
    prompt_input("Press Enter to return...")


def run_java_experiment_lab(exp):
    base_dir = PROJECT_ROOT
    source_path = os.path.join(base_dir, exp["file"])

    # Stage 1: The Big Picture Story
    clear_screen()
    print()
    _show_session_header(subject="java")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  ☕ JAVA EXPERIMENT {exp['num']:02d}: {exp['title']:<54} ║")
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
    sb_tuple = JAVA_EXP_SANDBOX_MAP.get(exp["num"])
    if sb_tuple:
        sb_name, _ = sb_tuple
        print(f"  {Color.YELLOW}[S]{Color.RESET} 🎬 {Color.BOLD}Launch {sb_name}{Color.RESET}")

    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the complete Java code first...{Color.RESET}")

    # Stage 2: Complete Source Code First
    clear_screen()
    print()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  📄 [Stage 2/4] COMPLETE VERIFIED JAVA SOURCE CODE                            ║")
    print(f"║  Source: {exp['file']:<68} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)
    print()

    funny_spinners = [
        "Invoking Java Virtual Machine bytecode interpreter",
        "Warming up HotSpot JIT compiler",
        "Loading class into JVM Method Area",
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

    # Stage 3: Fast & Fun 3-Bullet Block Breakdown
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
    _show_session_header(subject="java")

    print(f"{Color.BOLD}{Color.WHITE}{ch['prompt']}{Color.RESET}\n")

    if "opts" in ch:
        # Dynamically shuffle options so correct answer is truly random on the fly!
        shuffled_opts, target_opt = shuffle_mcq_options(ch["opts"], ch.get("correct_opt", "A"))
        for opt in shuffled_opts:
            print(f"  {Color.CYAN}{opt}{Color.RESET}")
        print()
        print("  " + Color.DIM + "(Tip: Type A, B, C, D or 'H' for a Hint)" + Color.RESET)
        print()

        while True:
            ans = prompt_input(f"{Color.BOLD}Your Answer [A/B/C/D] (or 'H' for Hint): {Color.RESET}").strip().upper()
            if ans == "H":
                print(f"\n  {Color.YELLOW}💡 HINT: {ch['hint']}{Color.RESET}\n")
                continue
            if ans in ("A", "B", "C", "D"):
                break
            print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

        spinner("Evaluating JVM bytecode validity", duration=0.4, color=Color.CYAN)

        if ans == target_opt:
            anim_correct()
            _record_concept_mastered("Java MCQ correct")
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 {ch['praise']}{Color.RESET}\n")
        else:
            anim_wrong()
            print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
            print(f"   {Color.YELLOW}✅ Expected Answer was ({target_opt}): {ch['hint']}{Color.RESET}\n")

    # Mark experiment as done
    exp_id = f"JAVA-{exp['num']}"
    _mark_experiment_done(exp_id)

    print(f"{Color.DIM}File location: {exp['file']}{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Java Lab Studio...{Color.RESET}")


def mode_java_viva():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}  🎓 JAVA OOP LAB VIVA PREP & CONCEPT MASTERY (1BCS302) 🎓{Color.RESET}")
    print(f"{Color.YELLOW}{Color.BOLD}=================================================================={Color.RESET}")
    print("  Stress-free practice with Socratic hints and examiner expectations.\n")

    score = 0
    questions = list(JAVA_VIVA_GAUNTLET)
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
                _record_concept_mastered("java viva correct")
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


def mode_java_studio():
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  ☕ JAVA OOP LAB STUDIO: 1BCS302 (VTU 2025 Scheme — 10 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="java")
        print(f"  {Color.YELLOW}[VS]{Color.RESET} 🎬 {Color.BOLD}Interactive Java Visualizer Suite{Color.RESET} (4 OOP & Runtime Sandboxes)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨 Java Lab Emergency Recovery (8 Real Exam Problem Scenarios)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓 Java Lab Viva Prep & Examiner Expectations")
        print(f"{Color.CYAN}{'─'*78}{Color.RESET}")

        print(f"  {Color.BOLD}CORE VTU LAB EXPERIMENTS:{Color.RESET}")
        for i in range(10):
            exp = JAVA_EXPERIMENTS[i]
            done = "✅" if f"JAVA-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 10, VS, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice in ("VS", "V", "VIS"):
            mode_java_visualizers_menu()
        elif choice == "DR":
            mode_java_disaster()
        elif choice == "VG":
            mode_java_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 10:
                run_java_experiment_lab(JAVA_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)
