# pyright: reportMissingImports=false
"""
arcade.git.studio — Git Lab Studio (1BCSL307A — 12 Experiments, VTU 2025 Scheme).
Strictly experiment-grounded engineering lab companion, command library & viva hub.
Features:
  - Two-Tier Overview (The Big Picture Story + Functional Sections)
  - Fast & Fun 3-Bullet Breakdown (Doing, How it Works, Watch Out)
  - Dynamic Runtime Shuffling across Challenges, Disasters, and Viva
"""
import os
import time
import random

try:
    from arcade.core import (  # type: ignore
        Color, clear_screen, prompt_input, spinner,
        print_slow, anim_correct, anim_wrong, shuffle_mcq_options,
    )
    from arcade.session import (  # type: ignore
        _SESSION, _record_concept_mastered, _unlock_badge,
        _save_to_local_db, _show_session_header, BANNER, _mark_experiment_done,
    )
    from arcade.git.sandbox import mode_git_command_sandbox  # type: ignore
    from arcade.git.experiments_data import GIT_EXPERIMENTS  # type: ignore
except (ImportError, ValueError):
    from ..core import (  # type: ignore
        Color, clear_screen, prompt_input, spinner,
        print_slow, anim_correct, anim_wrong, shuffle_mcq_options,
    )
    from ..session import (  # type: ignore
        _SESSION, _record_concept_mastered, _unlock_badge,
        _save_to_local_db, _show_session_header, BANNER, _mark_experiment_done,
    )
    from .sandbox import mode_git_command_sandbox  # type: ignore
    from .experiments_data import GIT_EXPERIMENTS  # type: ignore



# ==============================================================================
# CATEGORIZED GIT COMMAND LIBRARY
# ==============================================================================

GIT_COMMAND_LIBRARY = {
    "basic": [
        {
            "cmd": "git init",
            "syntax": "git init [directory]",
            "summary": "Initializes a brand new, empty Git repository.",
            "explanation": "Creates the hidden `.git/` directory containing the internal object database, ref stores, and configuration files. Without this folder, version control does not exist.",
            "exam_tip": "Common viva question: What is inside .git? Answer: objects, refs (heads, tags), HEAD file, config, and index."
        },
        {
            "cmd": "git status",
            "syntax": "git status [-s]",
            "summary": "Displays the working tree status comparing Working Directory, Index, and HEAD.",
            "explanation": "Shows tracked, modified, and untracked files. Files in red are unstaged; files in green are staged in the Index ready to be committed.",
            "exam_tip": "Short status flag `-s` outputs `M` (modified), `A` (added), `??` (untracked) in compact columns."
        },
        {
            "cmd": "git add",
            "syntax": "git add <pathspec>  |  git add .",
            "summary": "Stages file modifications into the Index.",
            "explanation": "Hashes file contents into Blob objects inside `.git/objects/`, and records their paths and hashes in `.git/index`.",
            "exam_tip": "Does `git add` create Git objects immediately? YES! It creates Blob objects in the database even before you commit."
        },
        {
            "cmd": "git commit",
            "syntax": "git commit -m \"<message>\"",
            "summary": "Records a permanent, immutable snapshot of staged files.",
            "explanation": "Generates a Tree object for directory layout, creates a Commit object linking author, timestamp, parent commit, and tree, and advances the branch pointer.",
            "exam_tip": "Commits are immutable. You cannot edit a past commit — you can only create a new commit or rewrite history with new SHAs."
        },
        {
            "cmd": "git branch",
            "syntax": "git branch [-a] [-d <name>] [<new-branch>]",
            "summary": "Lists, creates, or deletes branch reference pointers.",
            "explanation": "A Git branch is simply a 41-byte text file inside `.git/refs/heads/` storing the 40-character commit SHA. Creating a branch takes O(1) time.",
            "exam_tip": "Viva question: Why is Git branching faster than SVN? In SVN, branching copies all files; in Git, branching just creates a 41-byte text pointer."
        },
        {
            "cmd": "git switch / checkout",
            "syntax": "git switch <branch>  |  git switch -c <new-branch>",
            "summary": "Switches branches or restores working tree files.",
            "explanation": "Updates the `HEAD` reference to point to the desired branch and updates files in the working directory to match the commit at the branch tip.",
            "exam_tip": "Git 2.23 introduced `git switch` (for branches) and `git restore` (for files) to separate the overloaded roles of `git checkout`."
        },
        {
            "cmd": "git log",
            "syntax": "git log [--oneline] [--graph] [--decorate]",
            "summary": "Displays the commit history starting backwards from HEAD.",
            "explanation": "Walks the Directed Acyclic Graph (DAG) backwards following parent commit pointers, outputting commit SHAs, authors, dates, and log messages.",
            "exam_tip": "Know the universal visualization command: `git log --oneline --graph --decorate --all`."
        },
        {
            "cmd": "git merge",
            "syntax": "git merge [--no-ff] <branch>",
            "summary": "Joins two or more development histories together.",
            "explanation": "Performs either a Fast-Forward (pointer advance) if history is linear, or a 3-way merge using common ancestor commit to create a merge commit with 2 parents.",
            "exam_tip": "If conflicting changes exist in the same line of a file, Git halts the merge and inserts conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)."
        }
    ],
    "advanced": [
        {
            "cmd": "git rebase",
            "syntax": "git rebase [-i] <upstream>",
            "summary": "Re-applies commits on top of another base tip for linear history.",
            "explanation": "Saves your branch commits as temporary patches, resets the branch pointer to the upstream target, and replays each patch sequentially with new parent SHAs.",
            "exam_tip": "Golden Rule of Rebase: NEVER rebase commits that have already been pushed to a public/shared repository."
        },
        {
            "cmd": "git cherry-pick",
            "syntax": "git cherry-pick <commit-sha>",
            "summary": "Applies changes introduced by specific commits onto current branch.",
            "explanation": "Extracts the exact diff of `<commit-sha>` compared to its parent, and commits that diff directly onto the current HEAD with a new SHA.",
            "exam_tip": "Ideal for backporting a single bugfix from a development branch into production without bringing along incomplete features."
        },
        {
            "cmd": "git stash",
            "syntax": "git stash [push -m \"msg\"]  |  git stash list  |  git stash pop",
            "summary": "Stashes changes in a dirty working directory onto a temporary stack.",
            "explanation": "Creates commit objects in `.git/refs/stash` capturing working tree and index diffs, and resets the working directory to HEAD.",
            "exam_tip": "`stash pop` applies the stash and removes it from the stack. `stash apply` applies the stash but keeps it in the stack."
        },
        {
            "cmd": "git reset",
            "syntax": "git reset [--soft | --mixed | --hard] <commit>",
            "summary": "Resets current HEAD to the specified state.",
            "explanation": "--soft moves HEAD pointer only; --mixed (default) moves HEAD and updates Index; --hard moves HEAD, updates Index, AND overwrites Working Directory.",
            "exam_tip": "Can git reset --hard delete uncommitted work permanently? YES. If changes were never committed or stashed, they cannot be recovered."
        },
        {
            "cmd": "git revert",
            "syntax": "git revert <commit-sha> [--no-edit]",
            "summary": "Records a new commit that reverses the effects of an earlier commit.",
            "explanation": "Computes the exact inverse diff of the target commit and records it as a new forward-moving commit, preserving history integrity for shared branches.",
            "exam_tip": "Always use `revert` instead of `reset` when undoing changes already pushed to GitHub."
        },
        {
            "cmd": "git reflog",
            "syntax": "git reflog [show] [<ref>]",
            "summary": "Records every position HEAD has ever occupied locally.",
            "explanation": "Git's safety net: even if you run `git reset --hard` or delete a branch, the lost commit SHAs remain recorded in `.git/logs/HEAD` for up to 90 days.",
            "exam_tip": "To rescue a lost commit after accidental hard reset: run `git reflog`, identify the SHA before the reset, and run `git reset --hard HEAD@{1}`."
        },
        {
            "cmd": "git cat-file",
            "syntax": "git cat-file (-t | -p | -s) <object-sha>",
            "summary": "Plumbing command to inspect object type (-t), content (-p), or size (-s).",
            "explanation": "Allows direct examination of raw compressed zlib objects inside `.git/objects/`. Confirms Git's 4 core types: blob, tree, commit, tag.",
            "exam_tip": "Plumbing vs Porcelain: Porcelain commands (add, commit) are user interfaces; Plumbing commands (cat-file, hash-object) are internal tools."
        }
    ]
}


# ==============================================================================
# BALANCED SOCRATIC VIVA HUB
# ==============================================================================

GIT_VIVA_BANK = [
    {
        "q": "What is the fundamental architectural difference between Git and centralized VCS like SVN?",
        "options": [
            "A) SVN requires internet connection only on Fridays.",
            "B) Centralized VCS stores full history on a single central server; Git is distributed, meaning every cloned copy contains the COMPLETE project history and database locally.",
            "C) Git only works with Python programs.",
            "D) SVN uses SHA hashing while Git uses MD5."
        ],
        "ans": "B",
        "tip": "Think about what happens if your network goes down: with Git, you can still commit, branch, view logs, and diff offline.",
        "praise": "Precisely! Distributed means full autonomous offline capability with complete repository history on every developer machine.",
        "roast": "In Git (distributed), every clone is a full repository backup with complete history, unlike centralized VCS where history lives only on the central server."
    },
    {
        "q": "What exactly is stored inside a Git 'Blob' object?",
        "options": [
            "A) ONLY raw compressed file content — filenames and directory structures are stored in Tree objects, not in Blobs.",
            "B) Filename, directory permissions, and file content.",
            "C) Commit messages and author emails.",
            "D) Branch pointers."
        ],
        "ans": "A",
        "tip": "Blobs are content-addressable by their data alone. Two identical files with different names share the exact same Blob in Git!",
        "praise": "Examiner favorite! Blobs hold ONLY file bytes. File names and permissions belong to Trees.",
        "roast": "Blobs store ONLY file content. File names, modes, and folder structures are stored in Tree objects!"
    },
    {
        "q": "What is the meaning of a 'Detached HEAD' state in Git?",
        "options": [
            "A) The computer screen disconnected from the CPU.",
            "B) The .git folder was accidentally deleted.",
            "C) HEAD points directly to a specific commit SHA rather than to a named branch reference.",
            "D) You pushed code without commit privileges."
        ],
        "ans": "C",
        "tip": "Normally HEAD points to a branch ref (like refs/heads/main). In detached HEAD, HEAD points directly to a raw commit hash.",
        "praise": "Spot on! Detached HEAD is harmless for inspecting history, but new commits won't belong to any branch unless you create one.",
        "roast": "Detached HEAD simply means HEAD points directly to a commit hash instead of a branch pointer name."
    },
    {
        "q": "What is the difference between 'git fetch' and 'git pull'?",
        "options": [
            "A) They are identical synonyms.",
            "B) git fetch works on GitHub; git pull works only on GitLab.",
            "C) git pull never causes merge conflicts.",
            "D) 'git fetch' downloads remote objects and updates tracking branches without touching local files; 'git pull' executes 'git fetch' followed immediately by 'git merge'."
        ],
        "ans": "D",
        "tip": "git fetch is safe and non-intrusive. git pull modifies your active working files by merging downloaded commits.",
        "praise": "Mastered! Understanding fetch vs pull prevents unexpected merge conflicts during code pulls.",
        "roast": "Remember: `git pull = git fetch + git merge`. Fetch downloads; pull downloads AND merges."
    },
    {
        "q": "How does Git calculate the 40-character hexadecimal SHA identifier for a commit?",
        "options": [
            "A) It cryptographically hashes the commit header, tree SHA, parent commit SHA(s), author name/timestamp, committer name/timestamp, and commit message.",
            "B) It generates a random UUID.",
            "C) It hashes the file sizes added together.",
            "D) It takes the current Unix time multiplied by 100."
        ],
        "ans": "A",
        "tip": "Git is a Merkle DAG. Every single attribute of the commit, including its parent pointer, is part of the hash computation.",
        "praise": "Pure computer science elegance! This cryptographic linkage makes Git history immutable and tamper-evident.",
        "roast": "Git SHA hashes are generated by cryptographically hashing the commit tree, parent SHA, author, timestamp, and message."
    },
    {
        "q": "What is the purpose of the 'git reflog' command?",
        "options": [
            "A) To submit a bug report to the Git development team.",
            "B) To format Python code according to PEP 8.",
            "C) To view a local chronological log of every change to the HEAD pointer, allowing recovery of deleted commits and branches.",
            "D) To print network connection speeds."
        ],
        "ans": "C",
        "tip": "Reflog is your local safety net. Even if a commit is lost after a hard reset, its SHA remains in reflog.",
        "praise": "Exam lifesaver! Reflog allows you to recover from almost any catastrophic git command.",
        "roast": "Reflog is Git's ultimate undo mechanism, recording every movement of HEAD on your local machine."
    }
]


# ==============================================================================
# DISASTER RECOVERY SCENARIOS
# ==============================================================================

GIT_DISASTERS = [
    {
        "title": "🚨 DISASTER 1: The Accidental 'git reset --hard' Panic",
        "story": "You had 3 critical commits with your exam code. You accidentally ran 'git reset --hard HEAD~3'.\nAll your commits vanished from 'git log' and your files disappeared from the folder! The examiner walks over in 2 minutes.",
        "prompt": "How do you instantly restore the lost commits?",
        "choices": [
            "Run 'git reflog' to find the SHA before the reset, then run 'git reset --hard HEAD@{1}' (or the specific SHA)!",
            "Re-type the entire program from memory.",
            "Delete the repository and re-clone.",
            "Restart your laptop."
        ],
        "ans_idx": 1,
        "reaction": "REFLOG SAVES THE DAY! Git does not immediately garbage-collect commits. Reflog records the exact commit hash before the reset."
    },
    {
        "title": "🚨 DISASTER 2: The Merge Conflict Marker Crash",
        "story": "You ran 'git merge feature-branch' and Git reported:\n  CONFLICT (content): Merge conflict in main.c\nWithout thinking, you tried to run 'gcc main.c -o main', and GCC spat out 50 syntax errors on '<<<<<<< HEAD'!",
        "prompt": "What must you do to fix the file before compiling?",
        "choices": [
            "Run 'git kill --force'.",
            "Open main.c, locate conflict markers (<<<<<<<, =======, >>>>>>>), decide which code to keep, delete the marker lines, stage with 'git add main.c', and commit!",
            "Ignore the file and rename it to main.cpp.",
            "Comment out the whole file."
        ],
        "ans_idx": 2,
        "reaction": "EXACTLY! Conflict markers are inserted into your source code by Git. You must manually resolve the differences and remove the markers."
    },
    {
        "title": "🚨 DISASTER 3: The Secret API Key Committed to History",
        "story": "You committed a file containing your private cloud API key. You made another commit on top of it. Now you must push to public GitHub, but the secret is in history!",
        "prompt": "Why is simply editing the file and committing 'removed API key' insufficient?",
        "choices": [
            "GitHub automatically rotates passwords.",
            "Git deletes old commits automatically.",
            "The compiler warns about API keys.",
            "Because Git stores the full snapshot of past commits! Anyone can run 'git show' on the earlier commit and read the secret key."
        ],
        "ans_idx": 4,
        "reaction": "BINGO! Version control remembers every past version forever. To remove secrets, you must revoke the key and rewrite history (or use tools like git-filter-repo)."
    }
]


# ==============================================================================
# EXPERIMENT RUNNER & PRESENTATION LOGIC
# ==============================================================================

def run_git_experiment_lab(exp):
    clear_screen()
    _show_session_header(subject="git")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  🐙 GIT LAB EXPERIMENT {exp['num']:02d} ({exp['part']}): {exp['title']:<48} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)

    # Stage 1: Big Picture Story
    print(f"\n{Color.YELLOW}{Color.BOLD}[Stage 1/4] 💡 THE BIG PICTURE STORY (How this workflow works in real life):{Color.RESET}\n")
    story_text = exp.get("story", exp.get("concept", ""))
    print_slow(f"  {story_text}\n", 0.008, Color.WHITE)
    print(f"{Color.CYAN}{Color.BOLD}🎯 VTU Lab Syllabus Requirement:{Color.RESET}")
    print(f"  {exp['problem']}\n")
    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the exact Git commands...{Color.RESET}")

    # Stage 2: Verified Command Script
    clear_screen()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  📄 [Stage 2/4] VERIFIED COMMAND SCRIPT — EXPERIMENT {exp['num']:02d}                    ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")
    for line in exp["commands"].splitlines():
        if line.startswith("#"):
            print(f"  {Color.YELLOW}{line}{Color.RESET}")
        else:
            print(f"  {Color.GREEN}{Color.BOLD}$ {line}{Color.RESET}")
    print("\n" + Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the Code/Command Breakdown...{Color.RESET}")

    # Stage 3: Fast & Fun 3-Bullet Block Breakdown
    clear_screen()
    print(Color.MAGENTA + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🔍 [Stage 3/4] STEP-BY-STEP WORKFLOW EXPLANATION                             ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")

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
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter for the Quick Understanding Challenge...{Color.RESET}")

    # Stage 4: Understanding Challenge with Dynamic Option Shuffling
    clear_screen()
    ch = exp["challenge"]
    print(Color.YELLOW + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🎮 [Stage 4/4] GUIDED UNDERSTANDING CHALLENGE                               ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")
    print(f"{Color.BOLD}{Color.WHITE}{ch['prompt']}{Color.RESET}\n")

    shuffled_opts, target_opt = shuffle_mcq_options(ch["opts"], ch["correct_opt"])
    for opt in shuffled_opts:
        print(f"  {Color.CYAN}{opt}{Color.RESET}")
    print()

    while True:
        ans = prompt_input(f"{Color.BOLD}Your Answer [A/B/C/D] (or 'H' for Hint): {Color.RESET}").strip().upper()
        if ans == "H":
            print(f"\n  {Color.YELLOW}💡 HINT: {ch['hint']}{Color.RESET}\n")
            continue
        if ans in ("A", "B", "C", "D"):
            break
        print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

    if ans == target_opt:
        anim_correct()
        _record_concept_mastered("Git MCQ")
        print(f"\n{Color.GREEN}{Color.BOLD}✔ {ch['praise']}{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
        print(f"   {Color.YELLOW}Expected ({target_opt}): {ch['hint']}{Color.RESET}\n")

    exp_id = f"GIT-{exp['num']}"
    _mark_experiment_done(exp_id)

    prompt_input("Press Enter to return to Git Lab Studio...")


def mode_git_command_library():
    """Browse Basic vs Advanced Git commands with syntax, purpose, and exam tips."""
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   📚 GIT COMMAND LIBRARY — Categorized Command Reference & Syntax Guide       ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 📗  {Color.BOLD}Basic Everyday Commands{Color.RESET}   (init, status, add, commit, branch, checkout, log, merge)")
        print(f"  {Color.GREEN}[2]{Color.RESET} 🚀  {Color.BOLD}Advanced & Plumbing Tools{Color.RESET} (rebase, cherry-pick, stash, reset, revert, reflog, cat-file)")
        print(f"\n  {Color.DIM}[0]   ⬅️  Back to Git Lab Studio{Color.RESET}\n")

        ch = prompt_input(f"{Color.BOLD}Choose Category [1, 2, 0=Back]: {Color.RESET}").strip()
        if ch in ("0", "B", "BACK", "EXIT"):
            return
        elif ch in ("1", "2"):
            cat_key = "basic" if ch == "1" else "advanced"
            cat_name = "BASIC COMMANDS" if ch == "1" else "ADVANCED COMMANDS"
            cmd_list = GIT_COMMAND_LIBRARY[cat_key]

            while True:
                clear_screen()
                print(f"\n{Color.CYAN}{Color.BOLD}─── {cat_name} ({len(cmd_list)} Commands) ───{Color.RESET}\n")
                for i, item in enumerate(cmd_list, 1):
                    print(f"  {Color.YELLOW}[{i}]{Color.RESET} {Color.BOLD}{item['cmd']:<18}{Color.RESET} — {item['summary']}")
                print(f"\n  {Color.DIM}[0] ⬅️  Back to Categories{Color.RESET}\n")

                pick = prompt_input(f"{Color.BOLD}Select command [1 - {len(cmd_list)}, 0=Back]: {Color.RESET}").strip()
                if pick in ("0", "B", "BACK"):
                    break
                if pick.isdigit() and 1 <= int(pick) <= len(cmd_list):
                    cmd_obj = cmd_list[int(pick) - 1]
                    clear_screen()
                    print(f"\n{Color.GREEN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
                    print(f"║  📖 COMMAND: {cmd_obj['cmd']:<63} ║")
                    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                    print(f"  {Color.YELLOW}{Color.BOLD}Syntax:{Color.RESET}       {Color.WHITE}{cmd_obj['syntax']}{Color.RESET}\n")
                    print(f"  {Color.CYAN}{Color.BOLD}Purpose:{Color.RESET}      {cmd_obj['summary']}\n")
                    print(f"  {Color.MAGENTA}{Color.BOLD}Explanation:{Color.RESET}  {cmd_obj['explanation']}\n")
                    print(f"  {Color.YELLOW}{Color.BOLD}💡 Exam Tip:{Color.RESET}   {cmd_obj['exam_tip']}\n")
                    prompt_input("Press Enter to return to list...")


def mode_git_viva():
    """Socratic Viva Gauntlet for Git Lab 1BCSL307A with Dynamic Shuffling."""
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🎓 GIT LAB SOCRATIC VIVA GAUNTLET (1BCSL307A — VTU Exam Drills)            ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("  Practice examiner questions with Socratic hints and conceptual breakdowns.\n")

    score = 0
    questions = list(GIT_VIVA_BANK)
    random.shuffle(questions)

    for idx, q in enumerate(questions, 1):
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
                _record_concept_mastered("Git Viva")
                score += 1
                print(f"\n  {Color.GREEN}{Color.BOLD}✔ {q['praise']}{Color.RESET}")
            else:
                anim_wrong()
                if attempt == 1:
                    print(f"\n  {Color.YELLOW}🌱 {q['roast']}{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                    attempt += 1
                else:
                    print(f"\n  {Color.MAGENTA}The correct answer is [{target_ans}].{Color.RESET}")
                    attempt += 1

        print(f"\n  {Color.CYAN}💡 Examiner Expectation: {q['tip']}{Color.RESET}")
        prompt_input(f"\n{Color.DIM}Press Enter for next question...{Color.RESET}")

    print(f"\n{Color.CYAN}===================================================={Color.RESET}")
    print(f"  🎉 Git Viva Practice Complete! Mastered: {Color.BOLD}{score}/{len(questions)} Concepts{Color.RESET}")
    print(f"{Color.CYAN}===================================================={Color.RESET}\n")
    prompt_input("Press Enter to return...")


def mode_git_disaster():
    """Real-World Git Exam Emergency Scenarios with Dynamic Option Shuffling."""
    clear_screen()
    print(f"\n{Color.RED}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🚨 GIT LAB DISASTER RECOVERY (3 Real Exam Emergencies)                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

    for idx, sc in enumerate(GIT_DISASTERS, 1):
        shuffled_choices, target_idx = shuffle_mcq_options(sc["choices"], sc["ans_idx"])
        print(f"\n{Color.YELLOW}{Color.BOLD}{sc['title']}{Color.RESET}")
        print(f"{Color.WHITE}{sc['story']}{Color.RESET}\n")
        print(f"{Color.CYAN}{sc['prompt']}{Color.RESET}\n")
        for i, ch in enumerate(shuffled_choices, 1):
            print(f"  [{i}] {ch}")

        while True:
            ans = prompt_input(f"\nYour Choice [1-{len(shuffled_choices)}, 0=Exit]: ").strip()
            if ans == "0":
                return
            if ans.isdigit() and 1 <= int(ans) <= len(shuffled_choices):
                val = int(ans)
                if val == target_idx:
                    anim_correct()
                    print(f"\n{Color.GREEN}{Color.BOLD}✔ {sc['reaction']}{Color.RESET}\n")
                else:
                    anim_wrong()
                    print(f"\n{Color.RED}❌ That makes the disaster worse! Correct: Option [{target_idx}]{Color.RESET}\n")
                    print(f"   {Color.YELLOW}{sc['reaction']}{Color.RESET}\n")
                prompt_input("Press Enter for next emergency...")
                break


def mode_git_studio():
    """Master Git Lab Studio Menu (1BCSL307A)."""
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  🐙 GIT LAB STUDIO: 1BCSL307A (VTU 2025 Scheme — 12 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="git")

        print(f"  {Color.YELLOW}[CL]{Color.RESET} 📚  {Color.BOLD}Categorized Command Library{Color.RESET}  (Basic & Advanced Reference)")
        print(f"  {Color.GREEN}[SB]{Color.RESET} 🧪  {Color.BOLD}Interactive Command Sandbox{Color.RESET}  (Test Commands & Safety Check)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨  {Color.BOLD}Disaster Recovery Scenarios{Color.RESET}  (Reflog, Conflict Resolution)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓  {Color.BOLD}Socratic Viva Practice Hub{Color.RESET}   (Examiner Questions & Traps)")
        print(f"{Color.CYAN}{'─'*78}{Color.RESET}")

        print(f"  {Color.BOLD}PART A: CORE REPOSITORY & BRANCHING EXPERIMENTS{Color.RESET}")
        for i in range(6):
            exp = GIT_EXPERIMENTS[i]
            done = "✅" if f"GIT-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.BOLD}PART B: ADVANCED WORKFLOWS, TAGS & RECOVERY EXPERIMENTS{Color.RESET}")
        for i in range(6, 12):
            exp = GIT_EXPERIMENTS[i]
            done = "✅" if f"GIT-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 12, CL, SB, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "CL":
            mode_git_command_library()
        elif choice == "SB":
            mode_git_command_sandbox()
        elif choice == "DR":
            mode_git_disaster()
        elif choice == "VG":
            mode_git_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 12:
                run_git_experiment_lab(GIT_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)
