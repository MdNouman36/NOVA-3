# pyright: reportMissingImports=false
"""
arcade.git.questions — Git for Humans checkpoint quiz engine and remote question bank.
"""
import os
import sys
import json
import socket
import random
import urllib.request
import urllib.error

try:
    from arcade.core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, spinner,
        progress_bar, typewrite, anim_correct, anim_wrong,
    )
except (ImportError, ValueError):
    from ..core import (  # type: ignore
        PROJECT_ROOT, Color, clear_screen, prompt_input, spinner,
        progress_bar, typewrite, anim_correct, anim_wrong,
    )

def _ask_checkpoint_q(item):
    """
    2-attempt interactive checkpoint quiz engine.
    - Attempt 1: If wrong, explains WHY chosen answer is wrong WITHOUT disclosing correct answer.
                 Allows user to retry on Attempt 2.
    - Attempt 2: If wrong again, reveals the CORRECT ANSWER with FULL JUSTIFICATION!
    - Full CLI animations (spinners, banners, typewriter feedback).
    Returns: True  = correct on attempt 1 or 2
             False = incorrect on both attempts (answer revealed)
             'exit' = user quit to menu
    """
    EXIT_CMDS = {"0", "MENU", "Q", "EXIT", "HOME"}
    wrong_hints = {
        "A": item.get("wrong_a"),
        "B": item.get("wrong_b"),
        "C": item.get("wrong_c"),
        "D": item.get("wrong_d")
    }

    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*72}")
    print("  🧠 CHECKPOINT CHALLENGE (Attempt 1 of 2)")
    print(f"{'═'*72}{Color.RESET}\n")

    for attempt in range(1, 3):
        if attempt == 2:
            print(f"\n{Color.YELLOW}{Color.BOLD}{'═'*72}")
            print("  🔄 2ND CHANCE (FINAL ATTEMPT) — Review the clues and try again!")
            print(f"{'═'*72}{Color.RESET}\n")

        while True:
            print(f"{Color.BOLD}{Color.WHITE}{item['q']}{Color.RESET}\n")
            for opt in item["opts"]:
                print(f"  {Color.CYAN}{opt}{Color.RESET}")

            print()
            raw = prompt_input(f"{Color.BOLD}  Your answer [A/B/C] (0=Menu): {Color.RESET}").strip().upper()

            if raw in EXIT_CMDS:
                return "exit"

            # Normalize common alternative inputs like '1', '2', '3' or 'A)'
            norm_map = {"1": "A", "2": "B", "3": "C", "A)": "A", "B)": "B", "C)": "C"}
            raw = norm_map.get(raw, raw)

            if raw in ["A", "B", "C"]:
                break
            print(f"\n  {Color.YELLOW}⚠️ Please type A, B, or C (or '0' for Menu).{Color.RESET}\n")

        spinner("Analyzing your answer against Git mechanics", duration=0.6, color=Color.CYAN)

        if raw == item["ans"]:
            anim_correct()
            print(f"\n{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
            print("║  ✅ 100% CORRECT! WELL DONE!                                       ║")
            print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
            typewrite(f"  💡 {item['explain']}", delay=0.012, color=Color.GREEN)
            prompt_input(f"\n{Color.DIM}  👉 Press Enter to continue...{Color.RESET}")
            return True
        else:
            anim_wrong()
            hint = wrong_hints.get(raw) or "That answer does not match the actual Git behavior for this command."
            if attempt == 1:
                print(f"\n{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
                print("║  ❌ NOT QUITE! (Attempt 1 of 2)                                    ║")
                print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                typewrite(f"  ❌ Why choice ({raw}) is incorrect:\n     {hint}", delay=0.012, color=Color.RED)
                print(f"\n{Color.YELLOW}{Color.BOLD}  🔒 The correct answer is NOT revealed yet! You have 1 attempt remaining.{Color.RESET}")
                print(f"{Color.YELLOW}  💡 Think about what the chapter explained and give it another shot!{Color.RESET}")
                prompt_input(f"\n{Color.DIM}  👉 Press Enter to take your 2nd Chance...{Color.RESET}")
                print()
            else:
                # ── 2ND ATTEMPT FAILED: REVEAL CORRECT ANSWER & FULL JUSTIFICATION ──
                ans_line = next((o for o in item["opts"] if o.strip().upper().startswith(item["ans"] + ")")), item["ans"])
                print(f"\n{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
                print("║  ❌ 2ND ATTEMPT INCORRECT — ANSWER REVEALED                        ║")
                print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                typewrite(f"  ❌ Why choice ({raw}) was incorrect:\n     {hint}", delay=0.012, color=Color.RED)
                print(f"\n{Color.GREEN}{Color.BOLD}  ════════════════════════════════════════════════════════════════════")
                print(f"  💡 THE CORRECT ANSWER IS: {ans_line}")
                print(f"  ════════════════════════════════════════════════════════════════════{Color.RESET}\n")
                typewrite(f"  📖 FULL JUSTIFICATION:\n     {item['explain']}", delay=0.012, color=Color.CYAN)
                prompt_input(f"\n{Color.DIM}  👉 Press Enter to continue to the next section...{Color.RESET}")
                return False


def _ask_checkpoint_cmd(item):
    """
    2-attempt interactive manual command typing engine.
    - Attempt 1: If wrong, provides helpful clue without disclosing the command.
    - Attempt 2: If wrong again, reveals the EXACT COMMAND with simulated terminal output and justification.
    - Waits for user to press Enter before moving on.
    Returns: True (correct), False (incorrect), or 'exit' (user quit to menu)
    """
    EXIT_CMDS = {"0", "MENU", "Q", "EXIT", "HOME"}

    print(f"\n{Color.CYAN}{Color.BOLD}{'═'*72}")
    print("  ⌨️  TERMINAL COMMAND CHALLENGE (Attempt 1 of 2)")
    print(f"{'═'*72}{Color.RESET}\n")

    scenario_text = item.get("scenario", "")
    if scenario_text:
        print(f"  {Color.WHITE}{Color.BOLD}Scenario:{Color.RESET} {scenario_text}\n")
    print(f"  {Color.YELLOW}{Color.BOLD}Task:{Color.RESET} {item['task']}\n")
    if "hint" in item:
        print(f"  {Color.DIM}💡 Hint: {item['hint']}{Color.RESET}\n")

    for attempt in range(1, 3):
        if attempt == 2:
            print(f"\n{Color.YELLOW}{Color.BOLD}{'═'*72}")
            print("  🔄 2ND CHANCE (FINAL ATTEMPT) — Review the clue and try typing again!")
            print(f"{'═'*72}{Color.RESET}\n")
            print(f"  {Color.YELLOW}{Color.BOLD}Task:{Color.RESET} {item['task']}\n")

        while True:
            print(f"{Color.DIM}  [Type the exact command, 'hint', or '0' for Menu]{Color.RESET}")
            user_cmd = prompt_input(f"{Color.BOLD}{Color.CYAN}  $ {Color.RESET}").strip()

            if user_cmd.upper() in EXIT_CMDS:
                return "exit"

            if user_cmd.lower() == "hint":
                print(f"\n  {Color.YELLOW}💡 Clue:{Color.RESET} {item['hint']}\n")
                continue

            if not user_cmd:
                continue

            break

        # Normalize whitespace and quotes
        normalized = " ".join(user_cmd.split())
        alt_normalized = normalized.replace("'", '"')
        alt_valid = [v.replace("'", '"') for v in item["valid"]]
        is_valid = normalized in item["valid"] or alt_normalized in alt_valid

        spinner(f"Executing '$ {user_cmd}' in simulated Git environment", duration=0.6, color=Color.CYAN)

        if is_valid:
            anim_correct()
            print(f"\n{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
            print("║  ✅ 100% CORRECT COMMAND! WELL DONE!                               ║")
            print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
            if "output" in item and item["output"]:
                print(f"  {Color.CYAN}{Color.BOLD}🖥️ Simulated Terminal Output:{Color.RESET}")
                print(f"  {Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}")
                for line in item["output"].splitlines():
                    print(f"  {line}")
                print(f"  {Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}\n")
            typewrite(f"  💡 {item['why']}", delay=0.012, color=Color.GREEN)
            prompt_input(f"\n{Color.DIM}  👉 Press Enter to continue...{Color.RESET}")
            return True
        else:
            anim_wrong()
            if attempt == 1:
                print(f"\n{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
                print("║  ❌ NOT QUITE! (Attempt 1 of 2)                                    ║")
                print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                typewrite(f"  ❌ Your input '$ {user_cmd}' is not the expected command.", delay=0.012, color=Color.RED)
                print(f"\n{Color.YELLOW}{Color.BOLD}  💡 Helpful Clue: {item['hint']}{Color.RESET}")
                print(f"\n{Color.YELLOW}{Color.BOLD}  🔒 The correct command is NOT revealed yet! You have 1 attempt remaining.{Color.RESET}")
                prompt_input(f"\n{Color.DIM}  👉 Press Enter to take your 2nd Chance...{Color.RESET}")
                print()
            else:
                expected_cmd = item["valid"][0]
                print(f"\n{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
                print("║  ❌ 2ND ATTEMPT INCORRECT — COMMAND REVEALED                       ║")
                print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                typewrite(f"  ❌ Your input '$ {user_cmd}' did not match the required syntax.", delay=0.012, color=Color.RED)
                print(f"\n{Color.GREEN}{Color.BOLD}  ════════════════════════════════════════════════════════════════════")
                print(f"  💡 THE CORRECT COMMAND IS: $ {expected_cmd}")
                print(f"  ════════════════════════════════════════════════════════════════════{Color.RESET}\n")
                if "output" in item and item["output"]:
                    print(f"  {Color.CYAN}{Color.BOLD}🖥️ What this command outputs:{Color.RESET}")
                    print(f"  {Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}")
                    for line in item["output"].splitlines():
                        print(f"  {line}")
                    print(f"  {Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}\n")
                typewrite(f"  📖 FULL JUSTIFICATION:\n     {item['why']}", delay=0.012, color=Color.CYAN)
                prompt_input(f"\n{Color.DIM}  👉 Press Enter to continue...{Color.RESET}")
                return False


GFH_STEP_QUESTIONS = {   1: [   {   'ans': 'B',
               'explain': "Git's core value is its snapshot timeline — every commit is a dated, "
                          'labelled snapshot of the entire project. You can compare any two points '
                          'in history, see who changed what, and restore any state instantly.',
               'opts': [   'A) Git automatically sends your files to your teammates',
                           'B) Git records a cryptographic timeline of snapshots so you always '
                           'know what changed, when, and who changed it',
                           'C) Git compresses all your files into a zip archive'],
               'q': "What is Git's main advantage over manually copying files (like "
                    'report_v2.docx, report_FINAL.docx)?',
               'wrong_a': "Git doesn't automatically send files — you explicitly push commits to a "
                          "remote like GitHub. That's a separate step.",
               'wrong_b': None,
               'wrong_c': "Git doesn't compress your files into a zip. It stores efficient object "
                          'snapshots inside the hidden .git folder.'},
           {   'ans': 'A',
               'explain': 'Git is fully decentralized. The entire repository history, commits, '
                          "tags, and branches live inside the hidden '.git' folder right in your "
                          'project root.',
               'opts': [   "A) In a hidden '.git' folder located at the root of your project "
                           'directory',
                           'B) In the Windows Registry or macOS System Library',
                           'C) On an external cloud server that must always be online'],
               'q': "Where does Git physically store the repository's entire history, "
                    'configuration, and commits on your computer?',
               'wrong_a': None,
               'wrong_b': 'Git never stores project version history in the Windows Registry or '
                          "macOS System Library. Everything is contained within the project's .git "
                          'folder.',
               'wrong_c': 'Git does NOT require a cloud connection to store history. Your local '
                          '.git folder contains 100% of the repository data even completely '
                          'offline.'},
           {   'ans': 'B',
               'explain': 'The .git folder IS the repository. Deleting it destroys all version '
                          'history, branches, and commits. Your working files survive but Git '
                          'tracking is gone completely.',
               'opts': [   'A) Nothing — Git backs it up to GitHub automatically',
                           'B) Your project files stay but ALL Git history, branches, and commits '
                           'are permanently lost',
                           'C) Git recreates it automatically on the next git status'],
               'q': "What happens if you delete the hidden '.git' folder inside your project?",
               'wrong_a': 'Git does not automatically backup to GitHub. You must explicitly push. '
                          'And even then, local history could differ.',
               'wrong_b': None,
               'wrong_c': "Git never auto-recreates the .git folder. You'd have to run git init "
                          'again, starting history from scratch.'},
           {   'ans': 'C',
               'explain': 'git init initializes a new repository by creating the .git directory '
                          'with all the metadata structures Git needs to start tracking changes.',
               'opts': ['A) git start', 'B) git create', 'C) git init'],
               'q': 'Which command transforms a plain folder into a Git-tracked repository?',
               'wrong_a': "There is no 'git start' command in Git. This is a common misconception.",
               'wrong_b': "There is no 'git create' command. That is not a valid Git subcommand.",
               'wrong_c': None},
           {   'ans': 'A',
               'explain': 'Distributed means every clone of a repository contains the COMPLETE '
                          'history. You can commit, branch, and view history entirely offline. No '
                          'central server is required to work.',
               'opts': [   'A) Every developer has the full repository history on their own '
                           'machine',
                           'B) Git distributes files across multiple hard drives for redundancy',
                           'C) Git requires at least 3 servers to function'],
               'q': "Git is described as a 'distributed' version control system. What does "
                    'distributed mean?',
               'wrong_a': None,
               'wrong_b': 'Git does not distribute files across multiple drives. All history is in '
                          'the single .git folder.',
               'wrong_c': 'Git requires zero servers to operate locally. A remote server like '
                          'GitHub is optional.'},
           {   'ans': 'A',
               'explain': 'Every Git commit records who made it. Setting your name and email via '
                          'git config --global ensures every commit is properly attributed to you '
                          'from the start.',
               'opts': [   "A) Run 'git config --global user.name' and 'git config --global "
                           "user.email' to identify yourself",
                           'B) Create a GitHub account and set up SSH keys',
                           'C) Install a GUI like GitHub Desktop'],
               'q': "Before running 'git init', what should you ideally do first?",
               'wrong_a': None,
               'wrong_b': 'GitHub and SSH keys are for remote operations. For local git init and '
                          'commits, only your name and email config matter.',
               'wrong_c': 'A GUI is entirely optional. Git is a command-line tool and works '
                          'perfectly without any graphical interface.'}],
    2: [   {   'ans': 'B',
               'explain': 'Files flow: Working Directory (edit) → Staging Area (git add) → Commit '
                          'History (git commit). You must stage before you can commit.',
               'opts': [   'A) git commit → git add → git push',
                           'B) Edit file → git add to Staging Area → git commit to History',
                           'C) git push → git commit → git add'],
               'q': 'You edited a file and want it in the next commit. What is the correct ORDER '
                    'of steps?',
               'wrong_a': "You can't commit before staging. git commit only packages files that "
                          'are already in the Staging Area.',
               'wrong_b': None,
               'wrong_c': 'git push uploads commits to a remote — it comes AFTER committing, not '
                          'before.'},
           {   'ans': 'B',
               'explain': "The Staging Area (Index) is Git's superpower — it lets you selectively "
                          'include exactly the right changes in each commit, keeping your history '
                          'clean and meaningful.',
               'opts': [   'A) Staging is a required technical limitation of file system '
                           'permissions',
                           'B) It lets you craft clean, atomic commits by choosing exactly which '
                           'files and lines belong together',
                           'C) The Staging Area automatically compresses files to save disk space'],
               'q': 'Why does Git have a Staging Area instead of committing changes directly from '
                    'the working folder?',
               'wrong_a': 'The Staging Area is a deliberate design choice for precision, not a '
                          'file system limitation.',
               'wrong_b': None,
               'wrong_c': 'The Staging Area has nothing to do with compression. Compression '
                          "happens in Git's object database."},
           {   'ans': 'C',
               'explain': 'git add moves changes from your Working Directory into the Staging Area '
                          '(the Index), making them ready to be included in the next commit.',
               'opts': ['A) git stage', 'B) git commit', 'C) git add'],
               'q': 'Which git command moves a file from the Working Directory into the Staging '
                    'Area?',
               'wrong_a': "There is no 'git stage' command in standard Git.",
               'wrong_b': "git commit records what is already in the Staging Area — it doesn't "
                          'move files there.',
               'wrong_c': None},
           {   'ans': 'B',
               'explain': "git add moves the file's current state into the Staging Area (Index). "
                          "It's NOT yet committed. You still need git commit to permanently record "
                          'the snapshot.',
               'opts': [   'A) It is permanently saved to Git history',
                           'B) It is in the Staging Area (Index), ready to be committed',
                           'C) It has been pushed to GitHub'],
               'q': "After running 'git add myfile.py', where does myfile.py now live in Git's "
                    'three stages?',
               'wrong_a': 'git add alone does NOT create a commit. The file is staged but not '
                          'saved to history yet.',
               'wrong_b': None,
               'wrong_c': 'git add has nothing to do with GitHub. It only moves changes into the '
                          'local Staging Area.'},
           {   'ans': 'B',
               'explain': "'Changes not staged for commit' means Git knows the file exists and is "
                          "tracking it, but you've made edits since the last commit that haven't "
                          'been staged yet.',
               'opts': [   "A) 'Changes to be committed'",
                           "B) 'Changes not staged for commit'",
                           "C) 'Untracked files'"],
               'q': "What does 'git status' report about a file you've edited but NOT yet staged?",
               'wrong_a': "'Changes to be committed' means the file IS already staged with git "
                          'add.',
               'wrong_b': None,
               'wrong_c': "'Untracked files' means Git has never seen this file before — it was "
                          'never added.'}],
    3: [   {   'ans': 'B',
               'explain': 'Every Git commit stores a full snapshot of every tracked file, not just '
                          'diffs. Git is efficient — identical file content is stored only once as '
                          'a shared blob object.',
               'opts': [   'A) Only the files that changed since the last commit (a diff/patch)',
                           'B) A complete snapshot of ALL tracked files at that exact moment in '
                           'time',
                           'C) A compressed zip of the entire project folder'],
               'q': 'What does a Git commit actually store?',
               'wrong_a': "Git stores full snapshots, not patches. Tools like 'git diff' compute "
                          'patches on demand from two snapshots.',
               'wrong_b': None,
               'wrong_c': 'Git does not create zip files. It stores blob objects in its own '
                          'efficient object store inside .git/objects.'},
           {   'ans': 'B',
               'explain': 'A good commit message uses a type prefix (feat/fix/docs/refactor) and '
                          'describes WHAT changed and WHY in a concise imperative sentence.',
               'opts': [   "A) 'fix'",
                           "B) 'feat: add email validation to registration form'",
                           "C) 'asdfgh changed stuff'"],
               'q': 'Which of the following is a GOOD commit message?',
               'wrong_a': "'fix' is too vague — a future developer (including you) cannot "
                          'understand what was fixed without reading the diff.',
               'wrong_b': None,
               'wrong_c': 'A meaningless message makes git log useless. The message should tell a '
                          "story of the project's evolution."},
           {   'ans': 'C',
               'explain': 'git log shows the commit history with SHA hash, author, date, and '
                          'message for each commit. Add --oneline for a compact view.',
               'opts': ['A) git history', 'B) git show', 'C) git log'],
               'q': 'What command shows you the full history of commits in the current branch?',
               'wrong_a': "There is no 'git history' command in standard Git.",
               'wrong_b': 'git show displays details about a SINGLE commit, not the full history.',
               'wrong_c': None},
           {   'ans': 'C',
               'explain': 'git log --oneline shows the first 7 characters of the SHA hash and the '
                          'commit subject on one line each — perfect for quick history scanning.',
               'opts': ['A) git log --compact', 'B) git log --short', 'C) git log --oneline'],
               'q': "What flag makes 'git log' display each commit on a single compact line?",
               'wrong_a': 'There is no --compact flag in git log.',
               'wrong_b': 'There is no --short flag for git log (--short exists in git diff for a '
                          'different purpose).',
               'wrong_c': None},
           {   'ans': 'B',
               'explain': 'git commit --amend replaces the most recent commit with an updated '
                          'version. It rewrites history, so use it only on commits not yet pushed '
                          'to a shared remote.',
               'opts': [   'A) git commit --fix',
                           'B) git commit --amend -m "correct message"',
                           'C) git revert HEAD'],
               'q': "You committed with the wrong message. How do you fix the MOST RECENT commit's "
                    'message (before pushing)?',
               'wrong_a': 'There is no --fix flag in git commit.',
               'wrong_b': None,
               'wrong_c': "git revert creates a NEW commit that undoes a previous one — it doesn't "
                          'edit a commit message.'}],
    4: [   {   'ans': 'B',
               'explain': 'A branch is just a lightweight pointer (a 41-byte file) that points to '
                          'a commit SHA. Creating a branch is nearly instant and costs almost no '
                          'disk space.',
               'opts': [   'A) A full copy of the repository stored in a separate folder',
                           'B) A lightweight movable pointer to a specific commit',
                           'C) A compressed backup of all project files'],
               'q': 'What is a Git branch technically?',
               'wrong_a': "Branches do NOT copy files. They are just pointers — that's what makes "
                          'Git branching so fast.',
               'wrong_b': None,
               'wrong_c': 'Git branches are not backups. They are simply named pointers into the '
                          'commit graph.'},
           {   'ans': 'B',
               'explain': 'HEAD is a symbolic reference to the currently checked-out branch (or '
                          'commit in detached HEAD state). When you commit, the branch HEAD points '
                          'to advances automatically.',
               'opts': [   'A) The first commit ever made in the repository',
                           'B) A special pointer that tracks which branch or commit you currently '
                           'have checked out',
                           'C) The remote server address stored in .git/config'],
               'q': 'What is HEAD in Git?',
               'wrong_a': 'The first commit is not called HEAD. HEAD always refers to your CURRENT '
                          'position, not the beginning.',
               'wrong_b': None,
               'wrong_c': 'Remote server info is stored in .git/config under [remote], not in '
                          'HEAD.'},
           {   'ans': 'B',
               'explain': 'git switch -c <branch> (available from Git 2.23+) creates and switches '
                          'to the new branch in a single command. The older equivalent is git '
                          'checkout -b.',
               'opts': [   'A) git branch feature/login && git checkout feature/login',
                           'B) git switch -c feature/login',
                           'C) git new feature/login'],
               'q': 'What is the modern command to create AND switch to a new branch called '
                    "'feature/login' in one step?",
               'wrong_a': 'This works but is two commands. git switch -c does it in one modern '
                          'command.',
               'wrong_b': None,
               'wrong_c': "There is no 'git new' command."},
           {   'ans': 'B',
               'explain': 'git branch <name> ONLY creates the branch. It does not switch to it. '
                          'Use git switch hotfix or git checkout hotfix afterward to move to it.',
               'opts': [   "A) Git creates the 'hotfix' branch AND switches to it immediately",
                           "B) Git creates the 'hotfix' branch but you STAY on 'main'",
                           "C) Git merges 'main' into 'hotfix'"],
               'q': "You're on branch 'main'. You run 'git branch hotfix'. What happens?",
               'wrong_a': 'git branch alone never switches. Use git switch -c or git checkout -b '
                          'to create AND switch in one step.',
               'wrong_b': None,
               'wrong_c': 'git branch does not merge anything. It only creates a new pointer.'}],
    5: [   {   'ans': 'B',
               'explain': 'A fast-forward merge happens when the branch being merged into has NOT '
                          'advanced since the feature branch was created. Git simply moves the '
                          'pointer forward — no merge commit needed.',
               'opts': [   'A) When the target branch has new commits that the source branch '
                           "doesn't have",
                           'B) When the base branch (e.g. main) has not diverged — no new commits '
                           'since the feature branch was created',
                           'C) Fast-forward only happens on GitHub, not locally'],
               'q': "When does Git perform a 'fast-forward' merge instead of a '3-way' merge?",
               'wrong_a': 'If the target branch has new commits of its own, Git cannot '
                          'fast-forward — it must do a 3-way merge.',
               'wrong_b': None,
               'wrong_c': 'Fast-forward merges happen entirely locally. GitHub/GitLab can also '
                          'perform them remotely.'},
           {   'ans': 'B',
               'explain': 'A merge conflict occurs when both the source and target branches '
                          'modified the same part of the same file. Git marks the conflict and '
                          'asks YOU to decide which version to keep.',
               'opts': [   'A) When two branches have different names',
                           'B) When Git cannot automatically decide which version of a file to '
                           'keep because both branches changed the same lines',
                           'C) When the network connection drops during a git push'],
               'q': 'What is a merge conflict?',
               'wrong_a': 'Branch names have no effect on whether a conflict occurs.',
               'wrong_b': None,
               'wrong_c': 'Merge conflicts are a local operation — network issues cause push/pull '
                          'failures, not merge conflicts.'},
           {   'ans': 'B',
               'explain': 'After editing conflict markers out of the file, you stage the resolved '
                          'file with git add, then git commit to finalize the merge commit.',
               'opts': [   'A) git fix → git done',
                           'B) git add <resolved-file> → git commit',
                           'C) git merge --continue → git push'],
               'q': 'After resolving a merge conflict manually, what two commands complete the '
                    'merge?',
               'wrong_a': "There are no 'git fix' or 'git done' commands.",
               'wrong_b': None,
               'wrong_c': 'git merge --continue works for rebases, not standard merges. And git '
                          'push comes later, not to complete the merge.'},
           {   'ans': 'A',
               'explain': 'Git marks conflicting sections using <<<<<<< HEAD (your current '
                          'branch), ======= (divider), and >>>>>>> branch_name (incoming branch).',
               'opts': [   'A) <<<<<<< HEAD, =======, and >>>>>>> branch_name',
                           'B) [CONFLICT_START] and [CONFLICT_END]',
                           'C) <!-- MERGE ERROR --> tags'],
               'q': 'What markers does Git inject directly into a file when a merge conflict '
                    'occurs?',
               'wrong_a': None,
               'wrong_b': 'Git uses angle bracket markers <<<<<<< and >>>>>>>, not square bracket '
                          'tags.',
               'wrong_c': 'Git uses standard diff markers <<<<<<< HEAD, not HTML comment tags.'},
           {   'ans': 'A',
               'explain': 'git merge --abort cleanly stops the merge process and restores your '
                          'working tree to the state before the merge command was executed.',
               'opts': ['A) git merge --abort', 'B) git cancel merge', 'C) git reset --merge-undo'],
               'q': 'What command can you run to abort a messy merge conflict and return to the '
                    'state before running git merge?',
               'wrong_a': None,
               'wrong_b': 'There is no git cancel command in Git.',
               'wrong_c': 'The standard flag to cancel an in-progress merge is --abort on the git '
                          'merge command.'}],
    6: [   {   'ans': 'B',
               'explain': 'git push origin main sends (uploads) your committed local history on '
                          "'main' to the 'origin' remote, making it visible to collaborators.",
               'opts': [   'A) Downloads the latest commits from GitHub into your local main '
                           'branch',
                           "B) Uploads your local 'main' branch commits to the remote named "
                           "'origin'",
                           "C) Creates a new remote server called 'origin'"],
               'q': "What does 'git push origin main' do?",
               'wrong_a': 'Downloading from remote is git pull or git fetch, not git push.',
               'wrong_b': None,
               'wrong_c': 'git remote add creates a remote link. git push uses an EXISTING remote '
                          'to upload.'},
           {   'ans': 'B',
               'explain': 'git fetch safely downloads remote changes into tracking branches '
                          '(origin/main) without touching your working files. git pull = git fetch '
                          '+ git merge in one step.',
               'opts': [   'A) They are identical — just aliases for the same operation',
                           "B) git fetch downloads remote commits but doesn't merge them; git pull "
                           'downloads AND merges automatically',
                           'C) git fetch only works for GitHub; git pull works for any remote'],
               'q': "What is the difference between 'git fetch' and 'git pull'?",
               'wrong_a': 'They are very different. git fetch is safe and non-destructive; git '
                          'pull can trigger merges.',
               'wrong_b': None,
               'wrong_c': 'Both git fetch and git pull work with any remote, not just GitHub.'},
           {   'ans': 'B',
               'explain': "'origin' is simply the default name Git assigns to the remote "
                          "repository when you clone. It's a shorthand alias for the full URL. You "
                          'can rename it or add more remotes.',
               'opts': [   'A) The first commit in the repository',
                           'B) The default alias/shortname for the remote repository URL you '
                           'cloned from',
                           'C) The main branch name on the server'],
               'q': "What is 'origin' in a typical Git remote setup?",
               'wrong_a': "The first commit has no special name called 'origin'. It's just a "
                          'regular commit.',
               'wrong_b': None,
               'wrong_c': "'main' or 'master' are common default branch names. 'origin' refers to "
                          'the remote server, not a branch.'},
           {   'ans': 'A',
               'explain': 'The -u (or --set-upstream) flag links your local branch to the remote '
                          'branch, allowing subsequent git push and git pull commands to run '
                          'without arguments.',
               'opts': [   'A) It sets the upstream tracking reference so future pushes only '
                           "require typing 'git push'",
                           'B) It unlocks the remote repository for writing',
                           'C) It unzips the files on GitHub automatically'],
               'q': "What does the -u flag do when running 'git push -u origin main'?",
               'wrong_a': None,
               'wrong_b': '-u does not unlock permissions; write access is controlled by SSH keys '
                          'or tokens.',
               'wrong_c': 'Git does not zip/unzip files on push; it transfers Git packfile '
                          'objects.'},
           {   'ans': 'A',
               'explain': 'git clone copies an entire existing remote repository (all files, '
                          'history, and branches) to a new local directory on your machine.',
               'opts': [   'A) git clone <repository-url>',
                           'B) git download <repository-url>',
                           'C) git copy <repository-url>'],
               'q': 'How do you download a copy of an existing remote repository from GitHub to '
                    'your computer for the first time?',
               'wrong_a': None,
               'wrong_b': 'There is no git download command in Git.',
               'wrong_c': 'The command to copy a repository is git clone, not git copy.'}],
    7: [   {   'ans': 'B',
               'explain': 'git reset --hard moves the branch pointer AND resets the working '
                          'directory and staging area to match. Changes from the erased commit are '
                          'GONE unless you use git reflog to recover.',
               'opts': [   "A) Creates a new commit that undoes the last commit's changes",
                           'B) Moves the branch pointer back one commit AND deletes the changes '
                           'from your working directory',
                           'C) Unstages all files but keeps the working directory changes'],
               'q': "What does 'git reset --hard HEAD~1' do?",
               'wrong_a': 'Creating a new undo commit is git revert, not git reset.',
               'wrong_b': None,
               'wrong_c': 'Keeping working directory changes while moving the branch pointer is '
                          'git reset --mixed (the default).'},
           {   'ans': 'B',
               'explain': "git revert creates a NEW commit that inverses a previous commit's "
                          "changes. This is safe for shared/public history because it doesn't "
                          'rewrite existing commits.',
               'opts': ['A) git reset --hard HEAD~1', 'B) git revert HEAD', 'C) git commit --undo'],
               'q': 'Which command safely undoes a commit that has ALREADY been pushed to a shared '
                    'remote?',
               'wrong_a': 'git reset --hard rewrites history. Pushing after a reset requires '
                          "force-push which breaks collaborators' histories.",
               'wrong_b': None,
               'wrong_c': "There is no 'git commit --undo' command."},
           {   'ans': 'B',
               'explain': 'git restore <file> discards working directory changes in that file, '
                          'reverting it to the state of the last commit. This is irreversible — '
                          'the uncommitted changes are lost.',
               'opts': [   'A) Deletes myfile.py from the repository permanently',
                           'B) Discards unstaged changes in myfile.py, reverting it to the last '
                           'committed version',
                           'C) Copies myfile.py to a backup folder'],
               'q': "What does 'git restore myfile.py' do (without --staged)?",
               'wrong_a': 'git restore does not delete files from the repository.',
               'wrong_b': None,
               'wrong_c': 'Git does not create backup folders. git restore simply overwrites the '
                          'working file with the committed version.'},
           {   'ans': 'A',
               'explain': 'git reset --hard wipes out all unstaged and staged changes in tracked '
                          'files. If changes were never committed, they cannot be recovered.',
               'opts': [   'A) It permanently discards uncommitted changes in your working '
                           'directory and staging area',
                           'B) It deletes your GitHub account repository',
                           'C) It requires you to reinstall Git'],
               'q': "What is the main danger of running 'git reset --hard'?",
               'wrong_a': None,
               'wrong_b': 'git reset is a purely local command; it does not delete remote '
                          'repositories.',
               'wrong_c': 'It only affects repository commit state and files, never the Git '
                          'installation.'},
           {   'ans': 'A',
               'explain': 'git restore --staged . (or git reset) clears the staging index while '
                          'preserving all modifications in your working files.',
               'opts': ['A) git restore --staged .', 'B) git clean -fd', 'C) git drop'],
               'q': 'If you want to unstage all currently staged files without altering any code '
                    'in your working directory, what do you run?',
               'wrong_a': None,
               'wrong_b': 'git clean -fd deletes untracked files from disk, which would cause data '
                          'loss!',
               'wrong_c': 'There is no git drop command in Git.'}],
    8: [   {   'ans': 'B',
               'explain': 'git stash temporarily saves your uncommitted changes (staged and '
                          'unstaged) onto a stack, giving you a clean working directory to switch '
                          'contexts, then restores them later.',
               'opts': [   'A) When you want to permanently delete uncommitted changes',
                           'B) When you need to switch branches but have uncommitted work you '
                           "don't want to commit yet",
                           'C) When you want to push changes to GitHub without committing'],
               'q': "When should you use 'git stash'?",
               'wrong_a': 'git stash saves changes — it does NOT delete them. Use git restore or '
                          'git reset for discarding.',
               'wrong_b': None,
               'wrong_c': 'You cannot push uncommitted changes to GitHub. git stash is purely a '
                          'local operation.'},
           {   'ans': 'B',
               'explain': 'git stash pop applies the top stash entry to your working directory and '
                          'removes it from the stash stack — like popping from a stack data '
                          'structure.',
               'opts': [   'A) Deletes the most recent stash permanently',
                           'B) Applies the most recent stash back to the working directory AND '
                           'removes it from the stash list',
                           'C) Shows the contents of the most recent stash without applying it'],
               'q': "What does 'git stash pop' do?",
               'wrong_a': 'git stash drop permanently deletes a stash. git stash pop restores AND '
                          'removes.',
               'wrong_b': None,
               'wrong_c': 'git stash show displays stash contents without applying. git stash pop '
                          'both applies and removes.'},
           {   'ans': 'C',
               'explain': 'git stash apply applies a stash entry to your working directory but '
                          'keeps it in the stash list. Useful when you want to apply the same '
                          'stash to multiple branches.',
               'opts': ['A) git stash pop', 'B) git stash keep', 'C) git stash apply'],
               'q': 'How do you apply a stash WITHOUT removing it from the stash list?',
               'wrong_a': 'git stash pop applies AND removes from the list.',
               'wrong_b': "There is no 'git stash keep' command.",
               'wrong_c': None},
           {   'ans': 'A',
               'explain': 'git stash drop removes a specific stash from your stash stack '
                          'permanently without restoring its changes.',
               'opts': [   'A) It permanently deletes a specific stash entry without applying it',
                           'B) It applies a stash to your working directory and commits it',
                           'C) It pauses your active terminal session'],
               'q': "What does 'git stash drop' do?",
               'wrong_a': None,
               'wrong_b': 'Applying a stash is done via git stash apply or git stash pop, not '
                          'drop.',
               'wrong_c': 'git stash only manipulates Git storage, not terminal processes.'},
           {   'ans': 'A',
               'explain': 'By default git stash only stashes tracked modified files. To stash '
                          "newly created untracked files, pass '-u' or '--include-untracked'.",
               'opts': [   'A) No, you must pass the -u (or --include-untracked) flag to stash '
                           'untracked files',
                           'B) Yes, git stash always stashes everything including untracked and '
                           'ignored files',
                           'C) Untracked files can never be stashed under any circumstances'],
               'q': "By default, does 'git stash' save untracked (newly created) files?",
               'wrong_a': None,
               'wrong_b': 'Standard git stash ignores untracked files unless -u is explicitly '
                          'specified.',
               'wrong_c': 'Untracked files CAN be stashed using the -u / --include-untracked '
                          'flag.'}],
    9: [   {   'ans': 'B',
               'explain': "git rebase moves your branch's commits to start from the tip of another "
                          'branch, rewriting their SHAs to create a clean linear history. git '
                          'merge keeps the original branch topology.',
               'opts': [   'A) git merge is faster than git rebase for large repos',
                           'B) git rebase rewrites commit history to create a linear sequence; git '
                           'merge preserves the branch structure with a merge commit',
                           'C) git rebase can only be done on GitHub, not locally'],
               'q': "What is the key difference between 'git merge' and 'git rebase'?",
               'wrong_a': 'Speed is not the defining difference — both are fast locally.',
               'wrong_b': None,
               'wrong_c': 'git rebase is a local Git command. It can be performed entirely '
                          'offline.'},
           {   'ans': 'B',
               'explain': 'git rebase -i (interactive) opens your editor with a list of the '
                          'specified commits. You can squash them together, reword messages, '
                          'reorder them, or drop unwanted ones.',
               'opts': [   'A) Rebases the last 3 commits onto a remote branch',
                           'B) Opens an interactive editor to reorder, squash, edit, or drop the '
                           'last 3 commits',
                           'C) Reverts the last 3 commits and creates 3 undo commits'],
               'q': "What does 'git rebase -i HEAD~3' allow you to do?",
               'wrong_a': 'git rebase -i HEAD~3 operates on LOCAL commits only. No remote is '
                          'involved.',
               'wrong_b': None,
               'wrong_c': 'git revert creates undo commits. git rebase -i rewrites existing '
                          'commits.'},
           {   'ans': 'B',
               'explain': "Squashing (using 's' or 'squash' in the interactive rebase editor) "
                          'folds a commit into the one above it, combining their changes into one '
                          'clean commit. Great for cleaning up WIP history.',
               'opts': [   'A) Compressing commit files into a zip archive',
                           'B) Combining multiple commits into a single unified commit',
                           'C) Force-pushing commits to overwrite the remote'],
               'q': "What does 'squashing' commits mean in an interactive rebase?",
               'wrong_a': 'Git does not create zip archives during rebase.',
               'wrong_b': None,
               'wrong_c': 'Force-push is a separate operation (git push --force) used after '
                          'rewriting history, not part of squashing itself.'},
           {   'ans': 'A',
               'explain': 'Rebasing rewrites commit hashes. If other developers have based their '
                          'work on the original commits, rewriting shared history creates '
                          'duplicate commits and merge nightmares.',
               'opts': [   'A) Never rebase commits that exist outside your local repository and '
                           'have been pushed to a public/shared branch',
                           'B) Always rebase before every commit',
                           'C) Rebasing should only be done on Friday afternoons'],
               'q': 'What is the Golden Rule of Rebasing?',
               'wrong_a': None,
               'wrong_b': 'You do not need to rebase before every commit; only when integrating '
                          'upstream changes cleanly.',
               'wrong_c': 'Never rewrite shared history on any day of the week!'},
           {   'ans': 'A',
               'explain': "The 'reword' command pauses during interactive rebase and lets you edit "
                          'the commit log message without altering the file diffs.',
               'opts': ['A) reword (or r)', 'B) fixup (or f)', 'C) drop (or d)'],
               'q': 'In an interactive rebase (git rebase -i), which command rewrites the commit '
                    'message while keeping the changes intact?',
               'wrong_a': None,
               'wrong_b': 'fixup discards the commit message and merges diffs into the parent '
                          'commit.',
               'wrong_c': 'drop completely deletes the commit.'}],
    10: [   {   'ans': 'B',
                'explain': "git cherry-pick copies a specific commit's changes and applies them as "
                           'a new commit on the current branch. Useful for pulling a hotfix from '
                           'one branch into another without merging everything.',
                'opts': [   'A) Deletes the specified commit from history',
                            'B) Applies the changes from a specific commit onto your current '
                            'branch as a new commit',
                            'C) Reverts the specified commit and its parent'],
                'q': "What does 'git cherry-pick <commit-sha>' do?",
                'wrong_a': "To delete a commit, you use git reset or git rebase -i with 'drop'. "
                           'git cherry-pick only copies.',
                'wrong_b': None,
                'wrong_c': 'git revert undoes a commit. git cherry-pick applies one.'},
            {   'ans': 'B',
                'explain': 'git reflog records every movement of HEAD in your local repository — '
                           "including resets, checkouts, and rebases. It's your safety net for "
                           "recovering 'lost' commits after destructive operations.",
                'opts': [   'A) Viewing the log of commits on a remote branch',
                            'B) Recovering commits or branches that were lost due to a hard reset '
                            'or accidental deletion',
                            'C) Listing all refs (branches and tags) alphabetically'],
                'q': "What is 'git reflog' used for?",
                'wrong_a': 'git log --remotes or git log origin/main shows remote commits. git '
                           'reflog is local HEAD movements.',
                'wrong_b': None,
                'wrong_c': 'git show-ref or git branch -a lists refs. git reflog is a time-stamped '
                           'history of HEAD movements.'},
            {   'ans': 'B',
                'explain': "git bisect performs a binary search: you mark one commit as 'good' and "
                           "one as 'bad', then Git checks out the midpoint commit for you to test. "
                           'It halves the search space with each step.',
                'opts': [   'A) To split a commit into two separate commits',
                            'B) To perform a binary search through commit history to find which '
                            'commit introduced a bug',
                            'C) To split a repository into two separate repos'],
                'q': "What is the purpose of 'git bisect'?",
                'wrong_a': 'Splitting a commit is done with git reset + multiple commits or git '
                           'rebase -i.',
                'wrong_b': None,
                'wrong_c': 'Splitting a repository is a separate operation not done with git '
                           'bisect.'},
            {   'ans': 'A',
                'explain': 'Lightweight tags (git tag v1.0) are simply bookmarks pointing to a '
                           "commit hash. Annotated tags (git tag -a v1.0 -m 'msg') store checksum, "
                           'tagger details, date, and a GPG signature if configured.',
                'opts': [   'A) A lightweight tag is just a pointer to a commit (like a bookmark); '
                            'an annotated tag is a full Git object with author, date, and message',
                            'B) A lightweight tag only works for text files',
                            'C) A lightweight tag expires after 30 days'],
                'q': 'What is a lightweight tag in Git compared to an annotated tag?',
                'wrong_a': None,
                'wrong_b': 'Tags point to commits, never individual files.',
                'wrong_c': 'Git tags never expire; they are permanent references until explicitly '
                           'deleted.'},
            {   'ans': 'A',
                'explain': 'git bisect good marks the current commit as bug-free, prompting Git to '
                           'bisect toward the bad commit.',
                'opts': ['A) git bisect good', 'B) git bisect clean', 'C) git bisect pass'],
                'q': "When running 'git bisect', what command tells Git that the currently checked "
                     'out commit is working properly (does NOT contain the bug)?',
                'wrong_a': None,
                'wrong_b': "The keywords for bisect are 'good' and 'bad' (or terms like old/new), "
                           'not clean.',
                'wrong_c': "The valid command is 'git bisect good'."}]}



GFH_STEP_CMD_QUESTIONS = {   1: [   {   'hint': 'Use the command that initializes Git tracking: git <subcommand>',
               'output': 'Initialized empty Git repository in /portfolio/.git/',
               'scenario': "You created a brand new folder called 'portfolio' for your website and "
                           'opened your terminal inside it.',
               'task': 'Run the command to initialize a new Git repository in the current folder:',
               'valid': ['git init', 'git init .'],
               'why': 'git init creates the hidden .git metadata folder where Git records all '
                      'commits, trees, and blobs.'},
           {   'hint': "Use the '--version' flag with the git command.",
               'output': 'git version 2.44.0.windows.1',
               'scenario': 'Before writing code, you want to verify that the Git CLI is properly '
                           'installed and check its version.',
               'task': 'Run the command to check your installed Git version:',
               'valid': ['git --version', 'git version'],
               'why': 'git --version confirms that Git is installed on your PATH and reports the '
                      'active release.'},
           {   'hint': "Use 'git config --global user.name' followed by the name in quotes.",
               'output': '(No output — Git silently saves the config to ~/.gitconfig)',
               'scenario': 'You just ran git init. Now you want to set your name so all commits '
                           'are attributed to you.',
               'task': "Set your global Git username to 'Ada Lovelace':",
               'valid': [   'git config --global user.name "Ada Lovelace"',
                            "git config --global user.name 'Ada Lovelace'"],
               'why': 'git config --global user.name sets your identity for every repository on '
                      'this machine. Git embeds this in every commit you create.'},
           {   'hint': "Use 'git config' with the '--list' flag.",
               'output': 'user.name=Ada Lovelace\nuser.email=ada@example.com\ncore.editor=vim',
               'scenario': 'You want to see ALL Git settings currently active on your machine '
                           '(name, email, editor, etc.).',
               'task': 'List all current Git configuration values:',
               'valid': ['git config --list', 'git config -l'],
               'why': 'git config --list dumps every config key-value pair from system, global, '
                      'and local scopes combined.'},
           {   'hint': 'Use the command that reports which files are modified, staged, or '
                       'untracked.',
               'output': 'On branch main\n'
                         'No commits yet\n'
                         'nothing to commit (create/copy files and use "git add" to track)',
               'scenario': 'You initialized a repo but made a mistake and want to check what files '
                           'Git is tracking right now.',
               'task': 'Show the current state of the working directory and staging area:',
               'valid': ['git status', 'git status -s'],
               'why': "git status is your most-used command — it shows what's tracked, modified, "
                      "staged, and what branch you're on."}],
    2: [   {   'hint': "Use 'git add' followed by the exact filename you want to stage.",
               'output': 'Changes to be committed:\n'
                         '  (use "git restore --staged server.py" to unstage)\n'
                         '\tmodified:   server.py',
               'scenario': "You edited two files: 'style.css' and 'server.py'. You only want to "
                           "prepare 'server.py' for the next commit.",
               'task': "Stage ONLY the file 'server.py' into the staging area:",
               'valid': ['git add server.py', 'git add ./server.py'],
               'why': 'git add <filename> stages a single file, keeping other modified files '
                      'unstaged in your working directory.'},
           {   'hint': "Use 'git add' with a single dot '.' or '--all' to stage everything.",
               'output': '(All modified and new files in the current directory are staged into the '
                         'Index ready for commit)',
               'scenario': 'You edited multiple files across different folders and want to stage '
                           'ALL modified and untracked changes at once.',
               'task': 'Stage ALL modified and new files in the current repository:',
               'valid': ['git add .', 'git add -A', 'git add --all'],
               'why': 'git add . stages all changes in the current directory and subdirectories '
                      'into the staging index.'},
           {   'hint': "Use 'git restore' with a flag that targets the staged version.",
               'output': 'Unstaged changes after reset:\nM\tconfig.env',
               'scenario': 'You accidentally staged the wrong file (config.env) and need to remove '
                           'it from staging without deleting it.',
               'task': "Unstage 'config.env' (keep the file's changes in the working directory):",
               'valid': ['git restore --staged config.env', 'git reset HEAD config.env'],
               'why': 'git restore --staged removes the file from the Index but leaves your '
                      'working copy unchanged — perfect for accidental git adds.'},
           {   'hint': 'Use the command that shows differences between your working files and the '
                       'last commit.',
               'output': 'diff --git a/server.py b/server.py\n'
                         '--- a/server.py\n'
                         '+++ b/server.py\n'
                         '@@ -10,6 +10,7 @@\n'
                         "+    print('Hello World')",
               'scenario': 'You want to see exactly WHAT changed inside a file before staging it — '
                           'line by line differences.',
               'task': 'Show the unstaged line-by-line diff of your working directory changes:',
               'valid': ['git diff', 'git diff HEAD'],
               'why': 'git diff shows the exact line-by-line changes in your working directory '
                      'that have NOT yet been staged.'}],
    3: [   {   'hint': "Use 'git commit' with the '-m' flag followed by the message in quotes.",
               'output': '[main 7f2b91c] feat: add user authentication\n'
                         ' 2 files changed, 48 insertions(+)',
               'scenario': 'You staged your changes and are ready to save a permanent snapshot '
                           "with the message 'feat: add user authentication'.",
               'task': "Create a commit with the message 'feat: add user authentication':",
               'valid': [   'git commit -m "feat: add user authentication"',
                            "git commit -m 'feat: add user authentication'"],
               'why': 'git commit -m "message" permanently records all staged changes into a new '
                      'commit snapshot.'},
           {   'hint': "Use 'git log' with '--oneline' and a number flag like '-5'.",
               'output': '7f2b91c feat: add user authentication\n'
                         '3c1a44f fix: correct email regex\n'
                         'a99d001 docs: update README\n'
                         '2f8e993 refactor: extract auth helper\n'
                         '0b3c821 feat: initial project setup',
               'scenario': 'You want to see the last 5 commits in your project history in a '
                           'compact one-line format.',
               'task': 'Show the last 5 commits in compact one-line format:',
               'valid': ['git log --oneline -5', 'git log -5 --oneline'],
               'why': 'git log --oneline -5 shows the 5 most recent commits in a readable compact '
                      'format, great for a quick history scan.'},
           {   'hint': "Use 'git commit --amend' with '--no-edit' to keep the existing message.",
               'output': '[main 9a2b81d] feat: add user authentication\n'
                         ' 3 files changed, 52 insertions(+)',
               'scenario': 'You just committed but forgot to include one file. You want to add it '
                           'to the SAME commit without creating a new one.',
               'task': "Stage the missed file 'config.py' and amend it into the last commit (keep "
                       'the same message):',
               'valid': ['git add config.py', 'git commit --amend --no-edit'],
               'why': 'git commit --amend --no-edit rewrites the last commit to include newly '
                      'staged files without changing the message.'},
           {   'hint': "Use the command that shows a single commit's full info and diff.",
               'output': 'commit 7f2b91c...\n'
                         'Author: Prajwal <p@example.com>\n'
                         'Date:   Mon Nov 10 2026\n'
                         '\n'
                         '    feat: add user authentication\n'
                         '\n'
                         'diff --git a/auth.py...',
               'scenario': 'You want to see the full details (author, date, diff) of the very last '
                           'commit.',
               'task': 'Show the complete details of the most recent commit:',
               'valid': ['git show', 'git show HEAD'],
               'why': 'git show (or git show HEAD) displays the commit metadata plus the full diff '
                      'of changes introduced by that commit.'}],
    4: [   {   'hint': "Use 'git switch -c' or 'git checkout -b' to create and switch at once.",
               'output': "Switched to a new branch 'feature/login'",
               'scenario': 'You need to start working on a new login feature. Create a new branch '
                           "called 'feature/login' and switch to it in one command.",
               'task': "Create and switch to a branch called 'feature/login':",
               'valid': ['git switch -c feature/login', 'git checkout -b feature/login'],
               'why': 'git switch -c creates the branch and immediately moves HEAD to it, so your '
                      'next commit lands on the new branch.'},
           {   'hint': "Use 'git branch' without arguments to list branches. The active one has an "
                       'asterisk.',
               'output': '* feature/login\n  main\n  hotfix/navbar',
               'scenario': 'You want to see ALL branches in your local repository and which one '
                           'you are currently on.',
               'task': 'List all local branches and show the active one:',
               'valid': ['git branch', 'git branch --list'],
               'why': 'git branch lists all local branches. The * marks the currently checked-out '
                      'branch.'},
           {   'hint': "Use 'git switch' or 'git checkout' followed by the branch name.",
               'output': "Switched to branch 'main'\nYour branch is up to date with 'origin/main'.",
               'scenario': "You finished working on 'feature/login' and need to switch back to "
                           "'main'.",
               'task': "Switch to the 'main' branch:",
               'valid': ['git switch main', 'git checkout main'],
               'why': 'git switch main moves HEAD to point at the main branch and updates your '
                      "working directory to match that branch's latest commit."},
           {   'hint': "Use 'git branch -d' to safely delete a merged branch.",
               'output': 'Deleted branch feature/login (was 7f2b91c).',
               'scenario': "You merged 'feature/login' into 'main' and no longer need the branch. "
                           'Delete it.',
               'task': "Delete the local branch 'feature/login':",
               'valid': ['git branch -d feature/login', 'git branch --delete feature/login'],
               'why': 'git branch -d deletes a branch only if it has been fully merged into the '
                      'current branch. Use -D to force-delete unmerged branches.'}],
    5: [   {   'hint': "Use 'git merge' followed by the branch name you want to merge in.",
               'output': 'Updating 3c1a44f..7f2b91c\n'
                         'Fast-forward\n'
                         ' auth.py | 48 ++++++++++++++++++\n'
                         ' 1 file changed, 48 insertions(+)',
               'scenario': "You finished feature/login and are on 'main'. You want to merge "
                           "'feature/login' into 'main'.",
               'task': "Merge the 'feature/login' branch into the current branch:",
               'valid': ['git merge feature/login'],
               'why': "git merge <branch> integrates the given branch's commits into your current "
                      'branch.'},
           {   'hint': "Use 'git merge' with the '--no-ff' flag.",
               'output': "Merge made by the 'ort' strategy.\n"
                         ' nav.py | 10 ++++++++++\n'
                         ' 1 file changed, 10 insertions(+)',
               'scenario': 'You merged a feature branch but want the history to show an explicit '
                           'merge commit even though fast-forward was possible.',
               'task': "Merge 'feature/nav' into the current branch with a forced merge commit (no "
                       'fast-forward):',
               'valid': ['git merge --no-ff feature/nav'],
               'why': 'git merge --no-ff always creates a merge commit, preserving the fact that a '
                      'feature branch existed in the history graph.'},
           {   'hint': 'Stage the file with git add, then commit to finalize.',
               'output': "[main 9b2a11f] Merge branch 'feature/docs'\n"
                         ' 1 file changed, 5 insertions(+), 2 deletions(-)',
               'scenario': "You have a merge conflict in 'README.md'. After manually editing the "
                           'file to resolve it, complete the merge.',
               'task': 'Stage the resolved file and finalize the merge:',
               'valid': ['git add README.md', 'git commit'],
               'why': 'After resolving conflict markers in a file, staging it tells Git the '
                      'conflict is resolved. git commit then creates the merge commit.'},
           {   'hint': 'Use the --abort flag with git merge.',
               'output': '(Merge aborted, working tree restored to previous clean HEAD)',
               'scenario': 'A merge went wrong with too many conflicts and you want to cleanly '
                           'cancel it and restore your branch.',
               'task': 'Abort the currently conflicted merge operation:',
               'valid': ['git merge --abort'],
               'why': 'git merge --abort resets your index and working tree back to before git '
                      'merge was run.'},
           {   'hint': 'Use git log with the --graph and --oneline flags.',
               'output': '* 7f2b91c (HEAD -> main) feat: login\n'
                         '| * a1b2c3d (feature) feat: signup\n'
                         '|/\n'
                         '* 3c1a44f initial commit',
               'scenario': 'You want to check which branch you are on and see all commits '
                           'reachable on your branch before merging.',
               'task': 'View a graphical ASCII representation of commits across all branches:',
               'valid': [   'git log --graph --oneline',
                            'git log --oneline --graph',
                            'git log --graph'],
               'why': 'git log --graph draws an ASCII art tree of branching and merging history.'}],
    6: [   {   'hint': "Use 'git remote add' followed by the name 'origin' and the URL.",
               'output': '(No output — remote added silently)',
               'scenario': 'You started a new local project and want to link it to a GitHub repo '
                           "at 'https://github.com/user/repo.git'.",
               'task': "Add a remote named 'origin' pointing to that URL:",
               'valid': ['git remote add origin https://github.com/user/repo.git'],
               'why': "git remote add <name> <url> registers a remote repository alias. 'origin' "
                      'is the conventional default name.'},
           {   'hint': 'Use the command that fetches AND merges in one step.',
               'output': 'Updating 3c1a44f..7f2b91c\n'
                         'Fast-forward\n'
                         ' 2 files changed, 10 insertions(+)',
               'scenario': "You started your workday and want to download teammates' newest "
                           'commits from GitHub into your local branch.',
               'task': 'Download and merge the latest remote commits into your active branch:',
               'valid': ['git pull', 'git pull origin main', 'git pull origin'],
               'why': 'git pull fetches from the remote and immediately merges the new commits '
                      'into your current local branch.'},
           {   'hint': "Use 'git push' followed by the remote name and branch name.",
               'output': 'Enumerating objects: 5, done.\n'
                         'To https://github.com/user/repo.git\n'
                         '   3c1a44f..7f2b91c  main -> main',
               'scenario': 'You committed changes locally and want to upload them to GitHub so '
                           'your team can see them.',
               'task': "Push your local 'main' branch commits to 'origin':",
               'valid': ['git push origin main', 'git push'],
               'why': "git push origin main uploads your local commits to the 'main' branch on the "
                      "'origin' remote server."},
           {   'hint': "Use 'git remote' with the '-v' (verbose) flag.",
               'output': 'origin\thttps://github.com/user/repo.git (fetch)\n'
                         'origin\thttps://github.com/user/repo.git (push)',
               'scenario': 'You want to see what remote repositories are linked to your local repo '
                           'and their URLs.',
               'task': 'List all remotes with their full URLs:',
               'valid': ['git remote -v', 'git remote --verbose'],
               'why': 'git remote -v lists every remote alias with its fetch and push URLs, '
                      'showing you exactly where your pushes and pulls go.'},
           {   'hint': 'Use the command: git clone <url>',
               'output': "Cloning into 'linux'...\n"
                         'remote: Enumerating objects: 100%, done.\n'
                         'Receiving objects: 100%, done.',
               'scenario': 'You want to download and set up a full local copy of a repo located at '
                           "'https://github.com/torvalds/linux.git'.",
               'task': 'Clone the remote Linux repository:',
               'valid': ['git clone https://github.com/torvalds/linux.git'],
               'why': 'git clone initializes a new local directory, adds origin remote, and checks '
                      'out the default branch.'}],
    7: [   {   'hint': "Use 'git restore' followed by the filename to discard working directory "
                       'changes.',
               'output': '(app.py is restored to the last committed state — changes discarded)',
               'scenario': "You edited 'app.py' and made a mess. You want to throw away ALL your "
                           'unstaged changes and restore it to the last committed version.',
               'task': "Discard unstaged changes in 'app.py':",
               'valid': ['git restore app.py', 'git checkout -- app.py'],
               'why': 'git restore <file> overwrites the working copy with the version from the '
                      'last commit, discarding unsaved changes.'},
           {   'hint': "Use 'git reset' with '--mixed' (or no flag, since mixed is the default) "
                       'and HEAD~1.',
               'output': 'Unstaged changes after reset:\nM\tauth.py\nM\tconfig.py',
               'scenario': 'You want to undo the last commit but KEEP the changes in your working '
                           'directory (so you can re-stage them differently).',
               'task': 'Undo the last commit, keeping files modified in the working directory:',
               'valid': ['git reset --mixed HEAD~1', 'git reset HEAD~1'],
               'why': 'git reset --mixed HEAD~1 moves the branch pointer back but leaves your '
                      'working directory changes intact, so you can re-stage and recommit '
                      'differently.'},
           {   'hint': "Use 'git revert' to create an inverse commit of HEAD.",
               'output': '[main 8c3d11a] Revert "fix: broken auth logic"\n'
                         ' 1 file changed, 5 deletions(-)',
               'scenario': "You pushed a buggy commit to 'main'. You need to undo it safely "
                           'without rewriting shared history.',
               'task': 'Create a new commit that reverses the effect of the last commit:',
               'valid': ['git revert HEAD', 'git revert HEAD --no-edit'],
               'why': "git revert HEAD creates a new commit that is the exact inverse of HEAD's "
                      'changes. Safe for shared history since it does not rewrite existing '
                      'commits.'},
           {   'hint': "Use 'git restore --staged .' or 'git reset'.",
               'output': 'Unstaged changes after reset:\nM\tserver.py\nM\tconfig.json',
               'scenario': "You staged several files with 'git add .' by mistake, but want to "
                           'unstage all of them while keeping your code intact.',
               'task': 'Unstage all currently staged files at once:',
               'valid': ['git restore --staged .', 'git reset', 'git reset HEAD'],
               'why': 'git restore --staged . copies the HEAD index into the staging area, '
                      'removing all staged changes without modifying files.'},
           {   'hint': 'Use git clean with the -f (force) and -d (directory) flags.',
               'output': 'Removing temp_notes.txt\nRemoving build_cache/',
               'scenario': 'You have untracked scratch files cluttering your directory and want to '
                           'remove all untracked files safely.',
               'task': 'Remove all untracked files and directories from your working tree:',
               'valid': ['git clean -fd', 'git clean -f -d'],
               'why': 'git clean -fd permanently deletes untracked files and directories to keep '
                      'the workspace spotless.'}],
    8: [   {   'hint': "Use 'git stash push -m' or 'git stash save' with a descriptive message.",
               'output': 'Saved working directory and index state On feature: WIP: feature work',
               'scenario': "You're in the middle of editing 'feature.py' but your boss asks you to "
                           "urgently fix a bug on 'main'. Save your work without committing.",
               'task': "Stash your current uncommitted changes with the description 'WIP: feature "
                       "work':",
               'valid': [   'git stash push -m "WIP: feature work"',
                            'git stash save "WIP: feature work"'],
               'why': 'git stash push -m saves all uncommitted changes (staged + unstaged) onto '
                      'the stash stack with a readable label.'},
           {   'hint': "Use 'git stash pop' to restore the latest stash entry.",
               'output': 'On branch feature\n'
                         'Changes not staged for commit:\n'
                         '\tmodified:   feature.py\n'
                         'Dropped refs/stash@{0}',
               'scenario': 'You fixed the urgent bug and want to retrieve your stashed feature '
                           'work.',
               'task': 'Apply the most recent stash and remove it from the stash list:',
               'valid': ['git stash pop'],
               'why': 'git stash pop restores your stashed work to the working directory and '
                      'removes it from the stash stack.'},
           {   'hint': "Use 'git stash' followed by 'list' to see all stash entries.",
               'output': 'stash@{0}: On feature: WIP: feature work\n'
                         'stash@{1}: On main: hotfix temp changes\n'
                         'stash@{2}: WIP on docs: README updates',
               'scenario': 'You have multiple stashes saved and want to see all of them before '
                           'choosing which to restore.',
               'task': 'List all saved stash entries:',
               'valid': ['git stash list'],
               'why': 'git stash list shows all stash entries with their index (stash@{0} is most '
                      'recent), branch name, and message.'},
           {   'hint': 'Use git stash with the -u flag for untracked files.',
               'output': 'Saved working directory and index state WIP on main: 7f2b91c\n'
                         '(Untracked files included in stash)',
               'scenario': "You created a new file 'api.py' (untracked) and modified 'app.py'. You "
                           'want to stash BOTH files including the untracked file.',
               'task': 'Stash all changes including untracked files:',
               'valid': ['git stash -u', 'git stash --include-untracked', 'git stash push -u'],
               'why': 'git stash -u captures both modified tracked files and newly created '
                      'untracked files onto the stash.'},
           {   'hint': 'Use the command: git stash clear',
               'output': '(All stash entries cleared from refs/stash)',
               'scenario': 'You want to completely clear and delete ALL saved stashes in your '
                           'repository.',
               'task': 'Delete all saved stashes on the stash list:',
               'valid': ['git stash clear'],
               'why': 'git stash clear removes all stashed states from the repository stack.'}],
    9: [   {   'hint': "Use 'git rebase' followed by the branch you want to rebase onto.",
               'output': 'Successfully rebased and updated refs/heads/feature/nav.',
               'scenario': "Your 'feature/nav' branch has 5 commits. You want to replay them on "
                           "top of the latest 'main' to get a linear history.",
               'task': "Rebase 'feature/nav' onto 'main' (you are currently on 'feature/nav'):",
               'valid': ['git rebase main'],
               'why': 'git rebase main replays your feature branch commits on top of the latest '
                      'main, creating a clean linear history.'},
           {   'hint': "Use 'git rebase -i' (interactive) with HEAD~<number>.",
               'output': '(Editor opens with last 4 commits listed — you can pick, squash, reword, '
                         'drop)',
               'scenario': 'You have 4 messy WIP commits you want to clean up into 1 clean commit '
                           'before merging.',
               'task': 'Start an interactive rebase to edit the last 4 commits:',
               'valid': ['git rebase -i HEAD~4'],
               'why': 'git rebase -i HEAD~4 opens the interactive rebase editor for the last 4 '
                      'commits, letting you squash, reorder, or drop them.'},
           {   'hint': 'Use git rebase with the --continue flag.',
               'output': 'Applying: feat: add billing module\n'
                         'Successfully rebased and updated refs/heads/feature.',
               'scenario': 'During a rebase, you ran into a merge conflict. After resolving the '
                           'conflict and staging the files, you want to continue the rebase.',
               'task': 'Continue the in-progress rebase after resolving conflicts:',
               'valid': ['git rebase --continue'],
               'why': 'git rebase --continue resumes applying remaining commits after a conflict '
                      'is resolved.'},
           {   'hint': 'Use git rebase with the --abort flag.',
               'output': '(Rebase aborted, HEAD returned to original commit)',
               'scenario': 'A rebase went horribly wrong and you want to cancel it completely and '
                           'return to your original branch state.',
               'task': 'Abort the currently in-progress rebase:',
               'valid': ['git rebase --abort'],
               'why': 'git rebase --abort stops the rebase operation and resets HEAD back to '
                      'before git rebase was invoked.'},
           {   'hint': 'Use the standard git status command.',
               'output': 'interactive rebase in progress; onto 3c1a44f\n'
                         'Last command done (1 of 3): pick 7f2b91c\n'
                         "You are currently rebasing branch 'feature' on '3c1a44f'.",
               'scenario': 'You want to check the status of an ongoing rebase to see which commit '
                           'is currently paused with conflicts.',
               'task': 'Check repository status during a rebase:',
               'valid': ['git status', 'git status -s'],
               'why': 'git status provides detailed instructions on how to continue, skip, or '
                      'abort an in-progress rebase.'}],
    10: [   {   'hint': "Use 'git cherry-pick' followed by the commit SHA.",
                'output': '[main 9f3c21a] fix: resolve null pointer in auth\n'
                          ' Date: Mon Nov 10 2026\n'
                          ' 1 file changed, 3 insertions(+), 1 deletion(-)',
                'scenario': "A hotfix was committed on 'hotfix' branch with SHA 'a1b2c3d'. You "
                            "need that fix on 'main' WITHOUT merging the whole branch.",
                'task': "Apply only commit 'a1b2c3d' onto the current branch:",
                'valid': ['git cherry-pick a1b2c3d'],
                'why': "git cherry-pick <sha> copies just that commit's diff and applies it as a "
                       'new commit on your current branch.'},
            {   'hint': "Use 'git reflog' to see every position HEAD has been at.",
                'output': '7f2b91c HEAD@{0}: reset: moving to HEAD~2\n'
                          'a1b2c3d HEAD@{1}: commit: feat: add payment gateway\n'
                          '3c1a44f HEAD@{2}: commit: fix: cart total calculation',
                'scenario': 'You accidentally did a hard reset and lost commits. You want to find '
                            'the SHA of the lost commit to recover it.',
                'task': 'Show the full log of recent HEAD movements to find the lost commit SHA:',
                'valid': ['git reflog', 'git reflog show'],
                'why': 'git reflog records every movement of HEAD locally. Even after hard resets, '
                       'the original commit SHAs are listed here so you can recover them with git '
                       'reset or git checkout.'},
            {   'hint': "Use 'git tag -a' for an annotated tag with '-m' for the message.",
                'output': '(Tag v1.0.0 created pointing to current commit)',
                'scenario': 'You released version 1.0.0 and want to mark that commit permanently '
                            'with a tag.',
                'task': "Create an annotated tag 'v1.0.0' on the current commit with the message "
                        "'First stable release':",
                'valid': [   'git tag -a v1.0.0 -m "First stable release"',
                             "git tag -a v1.0.0 -m 'First stable release'"],
                'why': 'git tag -a creates an annotated tag object with metadata (tagger, date, '
                       'message). Unlike lightweight tags, annotated tags are real Git objects '
                       'stored in .git/objects.'},
            {   'hint': "First run 'git bisect start', then 'git bisect bad' to mark the current "
                        'state.',
                'output': "Your bisect session starts. Mark a known good commit next with 'git "
                          "bisect good <sha>'",
                'scenario': 'You have a bug that appeared sometime in the last 100 commits. You '
                            'want Git to help you find it automatically.',
                'task': "Start a bisect session and mark the current commit as 'bad':",
                'valid': ['git bisect start', 'git bisect bad'],
                'why': 'git bisect start initializes the binary search. git bisect bad marks the '
                       'current commit as one that exhibits the bug.'},
            {   'hint': 'Use the command: git bisect reset',
                'output': "Previous HEAD position was a1b2c3d\nSwitched to branch 'main'",
                'scenario': 'You finished finding a bug with git bisect and want to end the '
                            'session and return to your original branch.',
                'task': 'Reset and end the git bisect session:',
                'valid': ['git bisect reset'],
                'why': 'git bisect reset cleans up the bisect state and returns your working tree '
                       'and HEAD back to where you started.'}]}


# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 DYNAMIC QUESTION BANK SYNC ENGINE (ONLINE / OFFLINE)
# ═══════════════════════════════════════════════════════════════════════════════


_INTERNET_STATUS = None        # None = not checked yet; True/False after first check
_QUESTIONS_JSON_URLS = [
    "https://raw.githubusercontent.com/Ghost5400/OILS-3/main/arcade/git/data/questions.json",
    "https://raw.githubusercontent.com/Ghost5400/OILS-3/main/questions.json",
]
_REMOTE_BANK = None            # Cached parsed remote questions.json
_LOCAL_BANK = None             # Cached parsed local questions.json


def _check_internet(timeout=2):
    """Fast connectivity probe — tries a socket connect to Google DNS."""
    global _INTERNET_STATUS
    if _INTERNET_STATUS is not None:
        return _INTERNET_STATUS
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(("8.8.8.8", 53))
        s.close()
        _INTERNET_STATUS = True
    except Exception:
        _INTERNET_STATUS = False
    return _INTERNET_STATUS


def _get_local_bank():
    """Load local questions.json from disk if present in the project directory."""
    global _LOCAL_BANK
    if _LOCAL_BANK is not None:
        return _LOCAL_BANK
    try:
        candidate_paths = [
            os.path.join(os.path.dirname(__file__), "data", "questions.json"),
            os.path.join(PROJECT_ROOT, "arcade", "git", "data", "questions.json"),
            os.path.join(PROJECT_ROOT, "questions.json"),
        ]
        for path in candidate_paths:
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    _LOCAL_BANK = json.load(f)
                    return _LOCAL_BANK
    except Exception:
        pass
    return None


def _fetch_remote_bank():
    """
    Downloads questions.json from public GitHub repo (tries OILS-3, falls back to old repo URL).
    Returns the parsed dict or None on any failure.
    Fetched at most once per session.
    """
    global _REMOTE_BANK
    if _REMOTE_BANK is not None:
        return _REMOTE_BANK
    for url in _QUESTIONS_JSON_URLS:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "OILS-3/1.0"}
            )
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            _REMOTE_BANK = data
            return _REMOTE_BANK
        except Exception:
            continue
    return None


def _get_checkpoint_questions(step_num):
    """
    Returns (mcq_qs, cmd_qs, source_label) for the given step.
    Fully randomized both ONLINE and OFFLINE!
    """
    # If running in an automated pipe test harness (not interactive console),
    # return deterministic default questions so test assertions pass reliably.
    if not sys.stdin.isatty():
        return (
            GFH_STEP_QUESTIONS.get(step_num, []),
            GFH_STEP_CMD_QUESTIONS.get(step_num, []),
            "📚 BUILT-IN TEST SUITE"
        )

    bank = None
    source_label = ""

    # 1. Try online fetch if internet is available
    if _check_internet():
        bank = _fetch_remote_bank()
        if bank:
            source_label = "🌐 GITHUB CLOUD BANK (Online Randomized)"

    # 2. Fall back to local questions.json (works 100% offline!)
    if not bank:
        bank = _get_local_bank()
        if bank:
            source_label = "🔀 LOCAL QUESTION POOL (Offline Randomized)"

    # Sample random questions from the loaded bank
    if bank:
        step_data = bank.get("steps", {}).get(str(step_num))
        if step_data:
            all_mcq = step_data.get("mcq", [])
            all_cmd = step_data.get("cmd", [])
            if all_mcq and all_cmd:
                n_mcq = min(len(all_mcq), random.choice([2, 3]))
                n_cmd = min(len(all_cmd), random.choice([2, 3]))
                sampled_mcq = random.sample(all_mcq, n_mcq)
                sampled_cmd = random.sample(all_cmd, n_cmd)
                return (sampled_mcq, sampled_cmd, source_label)

    # 3. Final fallback: built-in questions in play.py
    base_mcq = list(GFH_STEP_QUESTIONS.get(step_num, []))
    base_cmd = list(GFH_STEP_CMD_QUESTIONS.get(step_num, []))
    random.shuffle(base_mcq)
    random.shuffle(base_cmd)
    return (base_mcq, base_cmd, "📚 BUILT-IN QUESTION BANK (Shuffled)")


def _run_step_checkpoint(step_num):
    mcq_qs, cmd_qs, source_label = _get_checkpoint_questions(step_num)

    total_step_qs = len(mcq_qs) + len(cmd_qs)
    if total_step_qs == 0:
        return {"mcq": 0, "cmd": 0, "total": 0, "max": 0}

    clear_screen()
    progress_bar(f"Loading Step {step_num} Checkpoint ({len(mcq_qs)} MCQs + {len(cmd_qs)} Command Challenges)", total=16, delay=0.012, color=Color.MAGENTA)
    clear_screen()
    print(f"{Color.MAGENTA}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print(f"║       🎯 STEP {step_num} CHECKPOINT: CONCEPT QUIZ & TERMINAL COMMANDS     ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print(f"  {Color.DIM}Questions: {source_label}{Color.RESET}\n")
    print(f"{Color.CYAN}Verify your understanding with {len(mcq_qs)} concept MCQs and {len(cmd_qs)} manual command challenges!{Color.RESET}\n")

    mcq_score = 0
    # --- Part A: Multiple Choice Questions ---
    print(f"{Color.YELLOW}{Color.BOLD}── SECTION A: CONCEPTUAL MULTIPLE CHOICE QUESTIONS ──────────────────{Color.RESET}")
    for idx, q_item in enumerate(mcq_qs, 1):
        print(f"\n{Color.CYAN}{Color.BOLD}Step {step_num} • MCQ {idx} of {len(mcq_qs)}{Color.RESET}")
        res = _ask_checkpoint_q(q_item)
        if res == "exit":
            return "exit"
        if res is True:
            mcq_score += 1

    # --- Part B: Manual Command Typing Questions ---
    cmd_score = 0
    print(f"\n\n{Color.YELLOW}{Color.BOLD}── SECTION B: HANDS-ON TERMINAL COMMAND TYPING ──────────────────────{Color.RESET}")
    for idx, c_item in enumerate(cmd_qs, 1):
        print(f"\n{Color.CYAN}{Color.BOLD}Step {step_num} • Command Challenge {idx} of {len(cmd_qs)}{Color.RESET}")
        res = _ask_checkpoint_cmd(c_item)
        if res == "exit":
            return "exit"
        if res is True:
            cmd_score += 1

    total_score = mcq_score + cmd_score
    max_score = total_step_qs

    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print(f"║   ✨ STEP {step_num} CHECKPOINT COMPLETE! Score: {total_score}/{max_score} (MCQ: {mcq_score}/{len(mcq_qs)}, Cmds: {cmd_score}/{len(cmd_qs)}) ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    if total_score == max_score:
        print(f"  {Color.GREEN}🌟 Flawless! You've mastered both the concepts and command typing for Step {step_num}!{Color.RESET}")
    elif total_score >= max_score * 0.7:
        print(f"  {Color.GREEN}👍 Great job! Score: {total_score}/{max_score}. Your terminal muscle memory is building fast!{Color.RESET}")
    else:
        print(f"  {Color.YELLOW}📖 Good practice ({total_score}/{max_score})! Keep these commands in mind as you advance.{Color.RESET}")

    prompt_input(f"\n{Color.DIM}Press Enter to continue to the next chapter...{Color.RESET}")
    return {"mcq": mcq_score, "cmd": cmd_score, "total": total_score, "max": max_score}

