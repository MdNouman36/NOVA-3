# pyright: reportMissingImports=false
"""
arcade.viva_bank — Comprehensive Viva Question Bank for VTU 2025 Scheme.
Contains 6 full practice sets (2 sets per lab, 15 questions each):
  - Git Lab (1BCSL307A): Set 1 & Set 2
  - DSA Lab (1BCSL306): Set 1 & Set 2
  - Java OOP Lab (1BCS302): Set 1 & Set 2
Includes Socratic Guided Hinting runner with warm mentor feedback.
"""
try:
    from arcade.core import Color, clear_screen, prompt_input, spinner, anim_correct, anim_wrong, shuffle_mcq_options  # type: ignore
    from arcade.session import _record_concept_mastered, _unlock_badge  # type: ignore
    from arcade.dialogues import print_dialogue  # type: ignore
except (ImportError, ValueError):
    from .core import Color, clear_screen, prompt_input, spinner, anim_correct, anim_wrong, shuffle_mcq_options  # type: ignore
    from .session import _record_concept_mastered, _unlock_badge  # type: ignore
    from .dialogues import print_dialogue  # type: ignore

# ════════════════════════════════════════════════════════════════════════════════
# 1. GIT LAB (1BCSL307A) — 30 VIVA QUESTIONS (SET 1 & SET 2)
# ════════════════════════════════════════════════════════════════════════════════

GIT_VIVA_SET_1 = [
    {
        "q": "What is the primary difference between 'git init' and 'git clone'?",
        "options": [
            "A) git init creates a brand new local repository from scratch; git clone copies an existing remote repository.",
            "B) git init connects to GitHub; git clone only works offline.",
            "C) git init deletes the history; git clone preserves the history.",
            "D) They are exact synonyms for the same operation."
        ],
        "ans": "A",
        "tip": "Think about where the files originate: one starts in an empty folder locally, while the other downloads an existing project from a URL.",
        "praise": "Spot on buddy! git init starts fresh locally, while git clone downloads an existing remote repo.",
        "explanation": "git init creates a .git subdirectory in an empty or existing local directory. git clone fetches all commits, branches, and files from a remote URL."
    },
    {
        "q": "What are the three main areas/stages of a Git project?",
        "options": [
            "A) Working Directory, Staging Area (Index), and Repository (.git)",
            "B) RAM, Hard Disk, and Cloud Storage",
            "C) Source code, Compiler, and Output binary",
            "D) Main branch, Master branch, and Origin branch"
        ],
        "ans": "A",
        "tip": "Recall Git's file lifecycle: untracked/modified files are in your directory, staged with 'git add', and committed into .git.",
        "praise": "Brilliant! Working Directory -> Staging Area -> Repository is the heartbeat of Git.",
        "explanation": "Working Directory holds your active files; Staging Area (Index) formats what will go into the next commit; Repository (.git) permanently stores committed snapshots."
    },
    {
        "q": "What does the command 'git diff --staged' (or --cached) show?",
        "options": [
            "A) Differences between staged changes and the last commit in HEAD.",
            "B) Differences between the working directory and the staging area.",
            "C) Differences between local main and remote main.",
            "D) A list of all deleted files since yesterday."
        ],
        "ans": "A",
        "tip": "Standard 'git diff' checks unstaged changes in your working tree. Adding '--staged' compares what has already been added to the staging area with HEAD.",
        "praise": "Exact right answer! 'git diff --staged' shows what is about to be recorded in your next commit.",
        "explanation": "'git diff' shows changes not yet staged. 'git diff --staged' (or '--cached') shows changes you staged with 'git add' against the last commit."
    },
    {
        "q": "What happens when you run 'git commit -am \"message\"'?",
        "options": [
            "A) Automatically stages and commits modified tracked files, but does NOT stage new untracked files.",
            "B) Stages every file in the directory including new untracked files.",
            "C) Deletes untracked files and commits the rest.",
            "D) Amends the previous commit with a new message."
        ],
        "ans": "A",
        "tip": "The '-a' flag only catches files Git already knows about. Brand-new files created with touch or your IDE need an explicit 'git add'.",
        "praise": "Great catch! '-a' only stages modified tracked files; brand new untracked files still require 'git add'.",
        "explanation": "Examiners often set this trap: 'git commit -a' only works on files already tracked by Git. Newly created files remain untracked."
    },
    {
        "q": "In Git, what exactly is 'HEAD'?",
        "options": [
            "A) A pointer/reference to the currently checked-out commit or branch tip.",
            "B) The very first commit ever made in the repository.",
            "C) The remote server URL on GitHub.",
            "D) The master administrator account for the project."
        ],
        "ans": "A",
        "tip": "HEAD tells Git 'You are here'. Look inside the .git/HEAD file — it usually points to 'ref: refs/heads/main'.",
        "praise": "Spot on buddy! HEAD is simply a symbolic pointer indicating your current position in the commit history.",
        "explanation": "HEAD points to the branch or commit currently active in your working directory. Moving branches updates where HEAD points."
    },
    {
        "q": "What does 'Detached HEAD' state mean?",
        "options": [
            "A) You have checked out a specific commit directly, rather than a named branch.",
            "B) Your Git installation is corrupted and cannot commit.",
            "C) Your local repo has been disconnected from the internet.",
            "D) You pushed code without author credentials."
        ],
        "ans": "A",
        "tip": "When you do 'git checkout <commit-hash>', HEAD points directly to a commit SHA rather than a branch name like 'main'.",
        "praise": "Excellent! In detached HEAD, new commits are not attached to any branch until you name one.",
        "explanation": "In detached HEAD state, HEAD points directly to a commit SHA. To save commits made here, simply create a branch with 'git branch <new-branch>'."
    },
    {
        "q": "What is the difference between a Fast-Forward merge and a 3-Way merge?",
        "options": [
            "A) Fast-Forward simply moves the branch pointer forward when no divergent commits exist; 3-Way merge creates a new merge commit.",
            "B) Fast-Forward only works on GitHub; 3-Way merge only works locally.",
            "C) Fast-Forward resolves merge conflicts automatically; 3-Way fails on conflict.",
            "D) 3-Way merge is only used when deleting a branch."
        ],
        "ans": "A",
        "tip": "If the target branch hasn't received new commits since you branched off, Git doesn't need a merge commit — it just moves the branch label forward.",
        "praise": "Awesome answer! Fast-Forward has zero diverged history, so Git simply slides the pointer forward.",
        "explanation": "Fast-Forward occurs when the target branch has no independent commits. A 3-Way merge (base + branch A + branch B) creates a new merge commit with two parents."
    },
    {
        "q": "During a merge conflict, what do the markers '<<<<<<< HEAD' and '>>>>>>> branch' signify?",
        "options": [
            "A) '<<<<<<< HEAD' shows your current branch changes; '>>>>>>> branch' shows incoming changes from the branch being merged.",
            "B) Syntax errors generated by the C or Java compiler.",
            "C) Corrupted sectors on the local drive.",
            "D) Deleted code that Git failed to purge."
        ],
        "ans": "A",
        "tip": "The section between <<<<<<< HEAD and ======= is what you have right now. The section between ======= and >>>>>>> is what the other branch wants to bring in.",
        "praise": "Perfect buddy! You know how to read conflict markers like an experienced engineer.",
        "explanation": "Git inserts conflict markers to highlight conflicting lines: HEAD is your current branch, and the other label is the incoming branch. You choose the right lines and delete the markers."
    },
    {
        "q": "What does 'git stash' do?",
        "options": [
            "A) Temporarily shelves (saves) uncommitted working changes so you get a clean working directory.",
            "B) Permanently discards all uncommitted changes.",
            "C) Pushes uncommitted changes directly to GitHub without committing.",
            "D) Encrypts your source code with a password."
        ],
        "ans": "A",
        "tip": "Think of stashing like a temporary clipboard for your working files when an urgent bug on another branch needs your immediate attention.",
        "praise": "Spot on! 'git stash' lets you switch branches cleanly without losing uncommitted progress.",
        "explanation": "'git stash' saves your modified tracked files on a stack, resetting your working tree to match HEAD. 'git stash pop' restores them."
    },
    {
        "q": "What is the difference between 'git stash apply' and 'git stash pop'?",
        "options": [
            "A) 'git stash pop' applies changes and removes them from the stash stack; 'apply' keeps them in the stash stack.",
            "B) 'git stash apply' deletes the changes; 'pop' keeps them.",
            "C) 'git stash pop' works only on the main branch.",
            "D) They do the exact same thing."
        ],
        "ans": "A",
        "tip": "'pop' takes it off the stack (like stack popping). 'apply' leaves the saved stash in place so you could apply it again elsewhere.",
        "praise": "Great precision! 'pop' = apply + drop in one smooth move.",
        "explanation": "'git stash pop' applies the top stash and drops it from storage. 'git stash apply' restores the changes while leaving the stash in the stack."
    },
    {
        "q": "What is the difference between 'git fetch' and 'git pull'?",
        "options": [
            "A) git fetch downloads remote commits without merging; git pull downloads AND merges them into your current branch.",
            "B) git fetch only works on branches; git pull works on tags.",
            "C) git fetch is destructive; git pull is read-only.",
            "D) They are completely identical commands."
        ],
        "ans": "A",
        "tip": "Remember the formula: git pull = git fetch + git merge. Fetch is always safe because your working files remain untouched.",
        "praise": "Spot on buddy! 'git fetch' is safe inspection; 'git pull' brings remote changes into your active branch.",
        "explanation": "git fetch updates your remote-tracking branches (like origin/main) without altering your local files. git pull executes git fetch followed by git merge."
    },
    {
        "q": "What is an Annotated Tag in Git, and how is it created?",
        "options": [
            "A) Created with 'git tag -a', stores tagger name, email, date, message, and has its own checksum object.",
            "B) A tag that can only be created on GitHub.",
            "C) A temporary branch that deletes itself after 24 hours.",
            "D) A tag that requires an internet connection to create."
        ],
        "ans": "A",
        "tip": "Lightweight tags are just bookmarks (commit pointers). Annotated tags are full Git objects with author details and release notes.",
        "praise": "Excellent! Annotated tags are recommended for official releases because they preserve who tagged it and why.",
        "explanation": "Annotated tags ('git tag -a v1.0 -m \"Release\"') are stored as full objects in Git's database with tagger information, date, and verification."
    },
    {
        "q": "What is the function of the '.gitignore' file?",
        "options": [
            "A) Specifies intentionally untracked files (build artifacts, .class, .o, secrets) that Git should ignore.",
            "B) Hides sensitive branches from public view.",
            "C) Blocks unauthorized teammates from pushing to main.",
            "D) Disables Git features on slow networks."
        ],
        "ans": "A",
        "tip": "Think about compiled files like a.out, .class, or IDE folders (.vscode). We don't want them polluting our repository history.",
        "praise": "Spot on! .gitignore keeps compiled binaries and secret keys out of your Git history.",
        "explanation": ".gitignore patterns match untracked files and folders to prevent them from showing up in 'git status' or being accidentally staged."
    },
    {
        "q": "How can you view a concise, one-line-per-commit history with graphical branch lines?",
        "options": [
            "A) git log --oneline --graph --all",
            "B) git status --concise",
            "C) git show --compact",
            "D) git branch --verbose"
        ],
        "ans": "A",
        "tip": "Look for the flags: '--oneline' condenses each commit, '--graph' draws ASCII branch lines, and '--all' shows all branches.",
        "praise": "Awesome buddy! 'git log --oneline --graph --all' is every senior engineer's favorite command for quick visual history.",
        "explanation": "'git log --oneline --graph --all' renders an ASCII branch graph along with abbreviated SHA hashes and commit titles."
    },
    {
        "q": "What is the command to create a new branch named 'feature' and switch to it immediately?",
        "options": [
            "A) git checkout -b feature  (or  git switch -c feature)",
            "B) git branch -make feature",
            "C) git jump feature",
            "D) git new branch feature"
        ],
        "ans": "A",
        "tip": "The '-b' flag with checkout (or '-c' with modern 'git switch') combines branch creation and branch checkout in one step.",
        "praise": "Clean and correct! 'git checkout -b <name>' or 'git switch -c <name>' does it instantly.",
        "explanation": "'git checkout -b feature' creates the branch pointer at HEAD and switches your working directory to it."
    }
]

GIT_VIVA_SET_2 = [
    {
        "q": "What is the key difference between 'git reset --soft', '--mixed', and '--hard'?",
        "options": [
            "A) --soft moves HEAD only (changes stay staged); --mixed moves HEAD and unstages changes; --hard wipes HEAD, staging, and working files.",
            "B) --soft deletes files; --hard keeps files in cloud.",
            "C) --mixed works only on merge commits; --soft works on linear commits.",
            "D) All three reset flags behave identically."
        ],
        "ans": "A",
        "tip": "Remember: --soft touches only HEAD; --mixed touches HEAD + Index; --hard touches HEAD + Index + Working Directory.",
        "praise": "Masterful answer! This is the single most tested Git concept in engineering viva exams.",
        "explanation": "--soft leaves your changes staged. --mixed (default) leaves changes in your working tree unstaged. --hard completely discards all uncommitted modifications."
    },
    {
        "q": "Why is 'git revert' preferred over 'git reset' on public/shared branches?",
        "options": [
            "A) git revert creates a NEW commit that inverts the changes without rewriting history; git reset rewrites history and breaks teammates' repos.",
            "B) git revert deletes the remote repo while git reset keeps it.",
            "C) git revert requires root permissions.",
            "D) git reset cannot be used on local branches."
        ],
        "ans": "A",
        "tip": "If teammates have already pulled a commit, rewriting history with reset will cause chaos. Revert creates an inverse commit that rolls forward cleanly.",
        "praise": "Spot on buddy! 'git revert' is safe for shared history because it moves forward by adding an undo commit.",
        "explanation": "git revert <commit-id> produces a new commit that cancels the target changes. Because no past commits are deleted or altered, history remains unbroken for collaborators."
    },
    {
        "q": "What is the Golden Rule of Git Rebase?",
        "options": [
            "A) Never rebase commits that exist outside your local repository and have been shared with others.",
            "B) Always rebase on the main branch before going to sleep.",
            "C) Never use rebase if you have more than 5 commits.",
            "D) Rebase should only be run by project owners."
        ],
        "ans": "A",
        "tip": "Rebase rewrites commit SHA hashes. If you rebase commits already pushed to a public remote, teammates will be working on top of obsolete history.",
        "praise": "Brilliant! Rewriting public shared history breaks everyone else's tracking.",
        "explanation": "Rebase creates new commit objects with new hashes. Rebasing a shared public branch forces other developers into messy reconciliation."
    },
    {
        "q": "What does 'git cherry-pick <commit-hash>' do?",
        "options": [
            "A) Applies the changes from a specific commit on another branch directly onto your current branch as a new commit.",
            "B) Deletes an unwanted commit from history.",
            "C) Picks the fastest remote mirror for cloning.",
            "D) Merges an entire branch and deletes it."
        ],
        "ans": "A",
        "tip": "Imagine you need just one specific bug fix from a colleague's experimental branch without merging all their other unfinished code.",
        "praise": "Spot on buddy! Cherry-pick selectively copies a single commit without merging whole branches.",
        "explanation": "git cherry-pick grabs the exact diff introduced by a commit and applies it to HEAD, creating a new commit with the same changes."
    },
    {
        "q": "If you accidentally delete a branch or make a bad 'git reset --hard', how can you recover lost commits?",
        "options": [
            "A) Use 'git reflog' to find the commit SHA of the deleted head, then create a branch there.",
            "B) Reinstall Git and reboot your machine.",
            "C) Check the Windows Recycle Bin.",
            "D) It is impossible; once deleted with reset --hard it is gone instantly."
        ],
        "ans": "A",
        "tip": "Git records every change of HEAD locally in a reference log. Look for the tool named 'reflog'.",
        "praise": "Legendary knowledge! 'git reflog' is the emergency parachute for every Git disaster.",
        "explanation": "Git keeps a log of every HEAD change in .git/logs. Even after branch deletion or hard reset, commits remain in reflog until garbage-collected."
    },
    {
        "q": "What are the four primary internal object types in Git's object database (.git/objects)?",
        "options": [
            "A) Blob, Tree, Commit, and Annotated Tag",
            "B) Text, Binary, Code, and Config",
            "C) Branch, Merge, Push, and Pull",
            "D) Header, Footer, Body, and Index"
        ],
        "ans": "A",
        "tip": "Blobs store file data, Trees store directory structures and file names, Commits tie trees to metadata, and Tags annotate commits.",
        "praise": "Incredible! Understanding Blobs, Trees, Commits, and Tags means you truly understand Git internals.",
        "explanation": "Git is a content-addressable storage system: Blobs store file contents, Trees store folder hierarchies, Commits link trees with author/parent info, and Tags mark releases."
    },
    {
        "q": "If a file was already tracked by Git and you subsequently add it to '.gitignore', why does Git keep tracking it?",
        "options": [
            "A) .gitignore only ignores untracked files; tracked files must first be removed from index via 'git rm --cached'.",
            "B) .gitignore has a bug on Windows.",
            "C) .gitignore requires an explicit Git restart.",
            "D) Git ignores the .gitignore file unless you push it first."
        ],
        "ans": "A",
        "tip": "If Git already indexed the file in a prior commit, adding the name to .gitignore does not untrack it. You must unstage it from the index.",
        "praise": "Spot on buddy! 'git rm --cached <file>' removes it from Git tracking while preserving it in your workspace.",
        "explanation": "Files already in the index must be removed from the staging tree using 'git rm --cached <file>' so Git stops tracking subsequent changes."
    },
    {
        "q": "What does 'git commit --amend' do?",
        "options": [
            "A) Modifies the most recent commit (combining newly staged changes or updating the commit message) without creating a separate commit.",
            "B) Deletes the last commit permanently.",
            "C) Amends all commits across the entire branch history.",
            "D) Sends an amendment notice to all repository contributors."
        ],
        "ans": "A",
        "tip": "Forgot to stage one little file or noticed a typo in your commit message? '--amend' rewrites the topmost commit.",
        "praise": "Spot on! '--amend' keeps your commit history tidy before pushing to remote.",
        "explanation": "'git commit --amend' replaces the tip of the current branch with a new commit containing your staged changes and updated message."
    },
    {
        "q": "What does 'git clean -fd' do in a Git repository?",
        "options": [
            "A) Forcefully deletes all untracked files (-f) and untracked directories (-d) from the working tree.",
            "B) Cleans compiled .git objects to compress storage.",
            "C) Formats all C and Java files according to code standards.",
            "D) Deletes all tracked files."
        ],
        "ans": "A",
        "tip": "The flags: -f stands for 'force' (required by safety settings) and -d stands for 'directories'.",
        "praise": "Clean and accurate! 'git clean -fd' sweeps away all temporary untracked clutter.",
        "explanation": "'git clean -fd' purges untracked files and directories. Running 'git clean -nd' first allows you to dry-run and preview what will be removed."
    },
    {
        "q": "During an interactive rebase conflict, which command should you run after manually resolving conflicting files?",
        "options": [
            "A) Stage with 'git add <file>', then run 'git rebase --continue'.",
            "B) Run 'git commit -m \"resolved\"' directly.",
            "C) Run 'git merge --complete'.",
            "D) Delete the .git directory."
        ],
        "ans": "A",
        "tip": "Never run 'git commit' during a rebase conflict! Stage the fixed files with 'git add' and tell rebase to proceed.",
        "praise": "Spot on buddy! Never commit during rebase — stage the fixes and run 'git rebase --continue'.",
        "explanation": "During rebase, Git is replaying individual commits. Once you resolve conflicts in a step, stage them with 'git add' and tell the rebase engine to continue."
    },
    {
        "q": "What is the difference between 'Forking' and 'Cloning' in open-source development?",
        "options": [
            "A) Forking creates a server-side copy of the repository under your own account (e.g. GitHub); Cloning downloads a copy onto your local machine.",
            "B) Forking is for Python; Cloning is for Java.",
            "C) Forking requires Git CLI; Cloning only works in the browser.",
            "D) They are different terms for the exact same local operation."
        ],
        "ans": "A",
        "tip": "Fork lives on the hosting platform (GitHub/GitLab) under your username. Clone brings repository files to your laptop's disk.",
        "praise": "Excellent! Fork = server-side duplicate; Clone = local disk working copy.",
        "explanation": "Forking gives you your own remote repository on GitHub where you have write access. You clone your fork locally to write code and open Pull Requests."
    },
    {
        "q": "What is a Pull Request (PR) or Merge Request (MR)?",
        "options": [
            "A) A platform mechanism to propose, review, discuss, and merge code changes from one branch/fork into a target branch.",
            "B) A command run in the terminal to download remote changes.",
            "C) An error thrown when the server disk is full.",
            "D) A request to increase repository size quota."
        ],
        "ans": "A",
        "tip": "PRs are where team code review happens: reviewers examine diffs, run automated tests (CI), and approve before merging into main.",
        "praise": "Spot on! Pull Requests are the foundation of collaborative code review in modern industry.",
        "explanation": "Pull Requests (GitHub) or Merge Requests (GitLab) provide an interface to review code diffs, run CI builds, and discuss changes before merging."
    },
    {
        "q": "What command helps identify which commit and author introduced a specific line of code in a file?",
        "options": [
            "A) git blame <filename>",
            "B) git who <filename>",
            "C) git find <filename>",
            "D) git history --line <filename>"
        ],
        "ans": "A",
        "tip": "The command sounds accusatory, but it simply displays the commit hash, author, and timestamp for every single line of a file.",
        "praise": "Spot on buddy! 'git blame' shows exactly who touched each line and in which commit.",
        "explanation": "'git blame' annotates each line of a given file with the author, timestamp, and commit SHA that last modified it."
    },
    {
        "q": "What does 'git bisect' do, and what algorithm does it use?",
        "options": [
            "A) Uses Binary Search across commit history to quickly pinpoint the exact commit that introduced a bug.",
            "B) Divides a large repository into two smaller repositories.",
            "C) Splits a branch into two parallel sub-branches.",
            "D) Automatically deletes half of the old commits."
        ],
        "ans": "A",
        "tip": "Bisect = Binary search. You tell it a 'good' commit and a 'bad' commit, and it checks out middle commits until the bug is isolated.",
        "praise": "Brilliant! 'git bisect' turns finding a regression across 1000 commits into just 10 quick checks.",
        "explanation": "git bisect uses binary search over commit ranges. By marking commits as good or bad, you find the regression in O(log n) steps."
    },
    {
        "q": "What is stored in '.git/config' versus global '~/.gitconfig'?",
        "options": [
            "A) .git/config holds repository-specific settings (like origin remote); ~/.gitconfig holds user-wide settings (like your global name and email).",
            "B) .git/config stores passwords; ~/.gitconfig stores code.",
            "C) .git/config is read-only; ~/.gitconfig is writable.",
            "D) Both files are identical mirrors."
        ],
        "ans": "A",
        "tip": "Global settings apply to every project on your laptop, while repository-local config overrides global settings for that specific repo.",
        "praise": "Spot on! Local settings in .git/config override global defaults in ~/.gitconfig.",
        "explanation": "Local configuration in .git/config takes precedence over the user's global ~/.gitconfig and system-level /etc/gitconfig."
    }
]

# ════════════════════════════════════════════════════════════════════════════════
# 2. DSA LAB (1BCSL306) — 30 VIVA QUESTIONS (SET 1 & SET 2)
# ════════════════════════════════════════════════════════════════════════════════

DSA_VIVA_SET_1 = [
    {
        "q": "What is the difference between malloc() and calloc() in C dynamic memory allocation?",
        "options": [
            "A) malloc() allocates uninitialized memory; calloc() allocates and initializes all bytes to zero.",
            "B) malloc() initializes memory to zero; calloc() leaves garbage values.",
            "C) malloc() works on the Stack; calloc() works on the Heap.",
            "D) malloc() cannot fail; calloc() can fail."
        ],
        "ans": "A",
        "tip": "calloc(n, size) clears memory to zero. malloc(bytes) leaves whatever garbage bits were previously in RAM.",
        "praise": "Spot on! Examiners love asking this to test your understanding of heap initialization.",
        "explanation": "calloc takes (num_elements, size_of_element) and zeroes memory. malloc takes total bytes and leaves memory uninitialized (garbage values)."
    },
    {
        "q": "What is a 'Dangling Pointer' in C and how do you prevent undefined behavior from it?",
        "options": [
            "A) A pointer pointing to freed memory; prevented by immediately setting ptr = NULL after free(ptr).",
            "B) A pointer that was declared without a datatype.",
            "C) A pointer that points to another pointer on the stack.",
            "D) A pointer initialized to address 0x0."
        ],
        "ans": "A",
        "tip": "After free(ptr), the pointer still holds the old address. Accessing it is undefined behavior! Always do ptr = NULL after free.",
        "praise": "Excellent! Setting ptr = NULL after free() is the mark of a professional C programmer.",
        "explanation": "When memory is released with free(ptr), the pointer variable still stores the address. Setting ptr = NULL ensures subsequent accidental dereferences fail cleanly."
    },
    {
        "q": "What is a 'Memory Leak' in C and what causes it?",
        "options": [
            "A) Dynamically allocated memory on the heap that is never deallocated with free(), remaining inaccessible.",
            "B) Running out of hard drive space while writing code.",
            "C) A pointer that has its address overwritten by another variable.",
            "D) Printing a pointer address to stdout."
        ],
        "ans": "A",
        "tip": "Every malloc() or calloc() on the heap MUST have a corresponding free(). Otherwise, that RAM cannot be reclaimed by the OS during runtime.",
        "praise": "Spot on buddy! Memory leaks happen when heap allocations lose their pointers without calling free().",
        "explanation": "If a pointer pointing to heap memory is reassigned or goes out of scope without calling free(), that RAM chunk is leaked until the process terminates."
    },
    {
        "q": "Why do we use the 'Triplet Representation' (Row, Column, Value) for Sparse Matrices?",
        "options": [
            "A) It stores only non-zero elements, saving massive memory when most matrix entries are zero.",
            "B) It allows standard C matrices to exceed 4GB in size.",
            "C) It automatically transposes the matrix on every read.",
            "D) It converts integers to floating point numbers."
        ],
        "ans": "A",
        "tip": "In a sparse matrix of size 1000x1000 with only 10 non-zero elements, a 2D array wastes 1,000,000 entries. A triplet list stores only the 10 entries.",
        "praise": "Spot on! Triplet representation stores (row, col, value) for non-zero elements only.",
        "explanation": "Sparse matrices have predominantly zero values. Storing only non-zero entries in a 3-column table (row, column, non-zero value) drastically cuts memory usage."
    },
    {
        "q": "What is the LIFO principle, and which Data Structure implements it?",
        "options": [
            "A) Last-In, First-Out — implemented by Stack.",
            "B) Last-In, First-Out — implemented by Queue.",
            "C) Low-Index, Fast-Output — implemented by Array.",
            "D) Linear-Index, Fixed-Offset — implemented by Linked List."
        ],
        "ans": "A",
        "tip": "Think of a stack of plates: the last plate you place on top is the first one you pick up.",
        "praise": "Clean and spot on! Stack = LIFO (Last-In, First-Out).",
        "explanation": "A stack inserts (push) and deletes (pop) at the same end called 'top', satisfying the Last-In, First-Out principle."
    },
    {
        "q": "What are 'Stack Overflow' and 'Stack Underflow' conditions?",
        "options": [
            "A) Overflow: Attempting to push to a full stack (top == MAX-1); Underflow: Attempting to pop from an empty stack (top == -1).",
            "B) Overflow: Stack memory exceeding 1GB; Underflow: Stack running at 0Hz.",
            "C) Overflow: Pushing negative numbers; Underflow: Popping even numbers.",
            "D) Overflow occurs on linked lists; Underflow occurs on arrays."
        ],
        "ans": "A",
        "tip": "Check the bounds of the array: top starts at -1. If top reaches MAX-1, no more items fit. If top is -1, there is nothing to pop.",
        "praise": "Perfect answer! Checking boundary conditions before push and pop is essential in lab programs.",
        "explanation": "Stack Overflow occurs when pushing into a stack where top == MAX-1. Stack Underflow occurs when popping from a stack where top == -1."
    },
    {
        "q": "Why do computers convert Infix expressions (e.g. A + B * C) to Postfix (ABC*+) before evaluating?",
        "options": [
            "A) Postfix expressions require no parentheses and can be evaluated sequentially in a single pass using a stack.",
            "B) Postfix takes up half the memory in RAM.",
            "C) Compilers can only understand Polish mathematicians.",
            "D) Infix cannot support floating point numbers."
        ],
        "ans": "A",
        "tip": "Infix requires knowledge of operator precedence and parentheses. Postfix eliminates parentheses and operator ambiguities entirely.",
        "praise": "Spot on! Postfix removes parenthesis ambiguity and evaluates cleanly with a single stack pass.",
        "explanation": "In Postfix notation, operator precedence is embedded directly in the ordering of tokens, allowing linear O(n) evaluation using a stack."
    },
    {
        "q": "How does the algorithm for evaluating a Postfix expression using a stack work?",
        "options": [
            "A) Push operands onto the stack; when an operator is encountered, pop two operands, apply the operator, and push the result back.",
            "B) Push operators onto the stack; pop when an operand is seen.",
            "C) Reverse the string and sort it alphabetically.",
            "D) Evaluate from right to left using a circular queue."
        ],
        "ans": "A",
        "tip": "When you see a number, push it. When you see an operator (+, -, *, /), pop op2, then pop op1, calculate op1 <op> op2, and push result back.",
        "praise": "Spot on buddy! Remember: op2 is popped first, then op1, and evaluation is op1 - op2.",
        "explanation": "Tokens are scanned left to right. Operands go onto the stack. Operators pop the top two operands, evaluate, and push the result."
    },
    {
        "q": "What is the 'False Overflow' problem in a standard Linear Queue implemented with an array?",
        "options": [
            "A) rear reaches MAX-1 indicating the queue is full, even though front slots were freed by previous de-queue operations.",
            "B) An overflow error that only triggers on 64-bit systems.",
            "C) When elements are overwritten accidentally by the compiler.",
            "D) When front and rear pointers cross each other."
        ],
        "ans": "A",
        "tip": "In a linear queue, insertions only move rear forward. Once rear reaches the array end, you cannot insert more elements even if front has moved forward.",
        "praise": "Great insight! That's precisely why Circular Queues were invented.",
        "explanation": "In a linear array queue, rear increments with each insert and never resets until the queue is completely emptied, stranding usable slots at the front."
    },
    {
        "q": "In a Circular Queue of size MAX, what are the formulas to advance front and rear?",
        "options": [
            "A) rear = (rear + 1) % MAX   and   front = (front + 1) % MAX",
            "B) rear = rear + 1   and   front = front - 1",
            "C) rear = (rear * 2) / MAX",
            "D) rear = rear % 2   and   front = front % 2"
        ],
        "ans": "A",
        "tip": "The modulo operator (%) wraps the index back to 0 when it reaches MAX, forming a virtual circle.",
        "praise": "Spot on! Modulo arithmetic wraps rear and front around from index MAX-1 back to 0.",
        "explanation": "Using modulo arithmetic `(index + 1) % MAX` wraps index values seamlessly back to the beginning of the buffer."
    },
    {
        "q": "What is the primary advantage of a Singly Linked List over an Array?",
        "options": [
            "A) Dynamic size and efficient O(1) insertion/deletion at known node positions without shifting elements.",
            "B) Direct O(1) random access by index.",
            "C) Lower memory consumption than arrays.",
            "D) Automatic cache locality optimization."
        ],
        "ans": "A",
        "tip": "Arrays require shifting O(n) elements when inserting or deleting in the middle. Linked lists simply update pointer addresses.",
        "praise": "Spot on buddy! Linked lists insert and delete by rewiring pointers without shifting arrays.",
        "explanation": "Linked lists allocate nodes on demand on the heap, avoiding pre-allocated fixed memory and eliminating costly O(n) element shifts."
    },
    {
        "q": "What is the time complexity to access the k-th element in an array versus a singly linked list?",
        "options": [
            "A) Array: O(1)   |   Linked List: O(k) or O(n)",
            "B) Array: O(n)   |   Linked List: O(1)",
            "C) Both are O(1)",
            "D) Both are O(n)"
        ],
        "ans": "A",
        "tip": "Arrays have contiguous memory addresses calculated as base + index * size. Linked lists must be traversed node by node starting from head.",
        "praise": "Spot on! Arrays allow instant O(1) index calculation, while linked lists require sequential traversal.",
        "explanation": "Arrays support constant-time random access via address calculation `base + i * sizeof(type)`. Linked lists require traversing k pointers from head."
    },
    {
        "q": "In polynomial addition using linked lists, how is each term represented in a node?",
        "options": [
            "A) struct Node { int coeff; int exp; struct Node *next; };",
            "B) struct Node { char name[20]; struct Node *next; };",
            "C) struct Node { int data; int priority; };",
            "D) struct Node { float matrix[3][3]; };"
        ],
        "ans": "A",
        "tip": "A polynomial term like 4x^3 has two mathematical properties: a coefficient (4) and an exponent (3), plus a pointer to the next term.",
        "praise": "Spot on! (coeff, exp, next) is the standard node structure for polynomial addition.",
        "explanation": "Each node stores the term's coefficient and exponent. Terms with matching exponents are added together during traversal."
    },
    {
        "q": "What does a NULL pointer in the 'next' field of a node in a Singly Linked List signify?",
        "options": [
            "A) It marks the end of the linked list (tail node).",
            "B) It indicates a corrupted node that must be deleted.",
            "C) It means the list has infinite length.",
            "D) It tells the operating system to shut down."
        ],
        "ans": "A",
        "tip": "When traversing with `while (curr != NULL)`, the last node's next pointer points to NULL to terminate traversal.",
        "praise": "Spot on! The last node's next field is NULL, serving as the sentinel terminating condition.",
        "explanation": "In standard singly linked lists, the final node's next pointer points to NULL, indicating there are no subsequent elements."
    },
    {
        "q": "What is the difference between a Singly Linked List and a Doubly Linked List?",
        "options": [
            "A) Singly linked list nodes have only a 'next' pointer; Doubly linked list nodes have both 'next' and 'prev' pointers, enabling bidirectional traversal.",
            "B) Doubly linked lists can only store double floating-point numbers.",
            "C) Singly linked lists use twice as much memory.",
            "D) Doubly linked lists cannot be deleted."
        ],
        "ans": "A",
        "tip": "Look at the prefix: 'Doubly' means each node knows both its successor and its predecessor.",
        "praise": "Perfect answer! Doubly linked lists allow two-way traversal at the cost of an extra pointer per node.",
        "explanation": "Each node in a doubly linked list contains data, next pointer, and prev pointer. This allows forward and backward traversal and O(1) deletion given a node pointer."
    }
]

DSA_VIVA_SET_2 = [
    {
        "q": "What is the definition and core property of a Binary Search Tree (BST)?",
        "options": [
            "A) For every node, all values in its left subtree are strictly smaller, and all values in its right subtree are strictly greater.",
            "B) Every node has exactly two children.",
            "C) The tree height is always guaranteed to be log(n).",
            "D) All leaf nodes are located on the same level."
        ],
        "ans": "A",
        "tip": "Remember: Left < Root < Right for every single subtree in the tree.",
        "praise": "Spot on buddy! Left < Root < Right is the universal invariant of a Binary Search Tree.",
        "explanation": "In a BST, keys in the left subtree are smaller than the node's key, and keys in the right subtree are greater. This enables binary search logic."
    },
    {
        "q": "What are the three standard Depth-First tree traversals and their node visit orders?",
        "options": [
            "A) Inorder: Left, Root, Right | Preorder: Root, Left, Right | Postorder: Left, Right, Root",
            "B) Inorder: Root, Left, Right | Preorder: Left, Root, Right | Postorder: Right, Left, Root",
            "C) Inorder: Right, Root, Left | Preorder: Root, Right, Left | Postorder: Left, Root, Right",
            "D) All three visit nodes in random sequence."
        ],
        "ans": "A",
        "tip": "Notice the position of 'Root': IN-order puts Root IN the middle. PRE-order puts Root BEFORE children. POST-order puts Root AFTER children.",
        "praise": "Awesome buddy! Inorder = LNR, Preorder = NLR, Postorder = LRN.",
        "explanation": "Traversals are named by when the Root (Node) is visited relative to Left and Right subtrees: Preorder visits root first, Inorder in the middle, Postorder last."
    },
    {
        "q": "Why is the Inorder Traversal of a Binary Search Tree (BST) special?",
        "options": [
            "A) It always visits and outputs the node values in sorted ascending order.",
            "B) It outputs values in reverse descending order.",
            "C) It finds the shortest path to all leaves.",
            "D) It deletes duplicate nodes automatically."
        ],
        "ans": "A",
        "tip": "Since BST property is Left < Root < Right, visiting Left first, then Root, then Right naturally produces sorted order.",
        "praise": "Spot on! Inorder traversal of any valid BST always yields strictly sorted values.",
        "explanation": "Because the BST invariant guarantees Left Subtree < Current Node < Right Subtree, recursive LNR traversal processes elements in monotonically increasing order."
    },
    {
        "q": "When deleting a node that has TWO children in a BST, how do you replace it?",
        "options": [
            "A) Replace its value with either its Inorder Successor (smallest in right subtree) or Inorder Predecessor (largest in left subtree), then delete that replacement node.",
            "B) Delete the entire tree rooted at that node.",
            "C) Swap the two children and set the parent to NULL.",
            "D) You cannot delete a node with two children in a BST."
        ],
        "ans": "A",
        "tip": "To preserve the BST property, the replacement value must be greater than all left descendants and smaller than all right descendants.",
        "praise": "Spot on buddy! Inorder Successor (min of right subtree) preserves the BST invariant perfectly.",
        "explanation": "The Inorder Successor is the smallest node in the right subtree. Copying its value and deleting that leaf/single-child node maintains BST ordering."
    },
    {
        "q": "What is the worst-case time complexity of searching in a BST, and when does it occur?",
        "options": [
            "A) O(n) — occurs when elements are inserted in already sorted order, causing the tree to degenerate into a skewed linked list.",
            "B) O(1) — occurs when the tree is very deep.",
            "C) O(log n) — guaranteed for all insertion orders.",
            "D) O(n^2) — occurs when deleting nodes."
        ],
        "ans": "A",
        "tip": "If you insert 1, 2, 3, 4, 5 in order, every node goes to the right child. The tree becomes a straight line (skewed tree).",
        "praise": "Spot on! Without balancing (like AVL or Red-Black), sorted inserts degenerate a BST into an O(n) line.",
        "explanation": "Inserting sorted inputs creates a right-skewed (or left-skewed) tree of height n, making search linear O(n). Balanced trees avoid this by keeping height O(log n)."
    },
    {
        "q": "What is 'Hashing' and what is the role of a 'Hash Function'?",
        "options": [
            "A) Hashing maps arbitrary keys to fixed table indices using a hash function, aiming for O(1) average time search.",
            "B) Hashing encrypts files so examiners cannot read them.",
            "C) Hashing is sorting an array using recursion.",
            "D) Hashing converts C code into assembly language."
        ],
        "ans": "A",
        "tip": "Think of a library catalog index: a mathematical formula takes a key (like employee ID) and tells you the exact array index where the record lives.",
        "praise": "Spot on buddy! Hashing achieves near constant time O(1) retrieval using direct index computation.",
        "explanation": "A hash function computes `index = h(key) % Table_Size` to store and locate items directly in an array in O(1) average time."
    },
    {
        "q": "What is a 'Hash Collision'?",
        "options": [
            "A) When a hash function maps two distinct keys to the exact same table index: h(k1) == h(k2).",
            "B) When the CPU overheats during hash computation.",
            "C) When an integer exceeds 32 bits in C.",
            "D) When two threads read the hash table simultaneously."
        ],
        "ans": "A",
        "tip": "Since the universe of possible keys is much larger than the hash table size, two different keys will eventually compute the same index.",
        "praise": "Spot on! By the Pigeonhole Principle, collisions are inevitable and must be resolved.",
        "explanation": "Because the key space is larger than table slots, multiple keys inevitably map to the same slot, requiring collision resolution techniques."
    },
    {
        "q": "What is 'Linear Probing' in Open Addressing collision resolution?",
        "options": [
            "A) When a collision occurs at index i, sequentially check slot (i + 1) % MAX, (i + 2) % MAX, ... until an empty slot is found.",
            "B) Allocate a new array with double size immediately.",
            "C) Discard the old element and overwrite it with the new key.",
            "D) Convert the array into a binary tree."
        ],
        "ans": "A",
        "tip": "If slot i is occupied, probe the very next slot (i+1), then (i+2), wrapping around with modulo until a free bucket appears.",
        "praise": "Spot on! Linear probing simply walks forward slot by slot until it finds an open cell.",
        "explanation": "Linear probing checks consecutive locations: `index = (h(key) + i) % Table_Size` for i = 0, 1, 2... until an unoccupied slot is located."
    },
    {
        "q": "What is 'Primary Clustering' in Linear Probing?",
        "options": [
            "A) Long continuous runs of occupied slots build up, increasing average search time for subsequent insertions.",
            "B) Storing data on physical hard drive clusters.",
            "C) Grouping students by their roll numbers.",
            "D) When all keys hash to index 0."
        ],
        "ans": "A",
        "tip": "As clusters of filled slots grow, any key hashing into the cluster has to probe past the entire block, making the cluster even larger.",
        "praise": "Spot on! Primary clustering makes occupied blocks grow bigger and slows down search times.",
        "explanation": "Occupied slots tend to clump together into contiguous blocks. Any collision in that region lengthens the block, degrading search time towards O(n)."
    },
    {
        "q": "How does 'Separate Chaining' resolve hash collisions?",
        "options": [
            "A) Each hash table slot acts as the head of an independent linked list storing all keys that hash to that slot.",
            "B) It chains multiple computers together in a network.",
            "C) It encrypts each element with the previous element's key.",
            "D) It creates separate array files on disk."
        ],
        "ans": "A",
        "tip": "Instead of storing one item directly in each slot, make each slot a pointer to a linked list. Multiple colliding keys are simply appended to the list.",
        "praise": "Awesome answer! Separate chaining uses a linked list for each bucket.",
        "explanation": "In separate chaining, every table entry is a linked list head. Collisions are handled by appending new nodes to the list at that index."
    },
    {
        "q": "What is the difference between an Adjacency Matrix and an Adjacency List for graph representation?",
        "options": [
            "A) Adjacency Matrix uses a V x V 2D array (O(V^2) space); Adjacency List uses an array of linked lists (O(V + E) space, ideal for sparse graphs).",
            "B) Adjacency Matrix is only for directed graphs; Adjacency List is only for undirected graphs.",
            "C) Adjacency Matrix cannot store edge weights.",
            "D) Adjacency List requires 3D arrays in C."
        ],
        "ans": "A",
        "tip": "A matrix always needs V*V memory even if there are very few edges. An adjacency list only allocates memory for edges that actually exist.",
        "praise": "Spot on buddy! Matrix is O(V^2) and great for dense graphs; List is O(V+E) and optimal for sparse graphs.",
        "explanation": "Adjacency Matrix requires V x V space regardless of edge count. Adjacency List allocates nodes only for existing edges, making it far more memory efficient for real-world sparse graphs."
    },
    {
        "q": "What data structure is used to implement Breadth First Search (BFS) on a graph?",
        "options": [
            "A) Queue (FIFO)",
            "B) Stack (LIFO)",
            "C) Binary Search Tree",
            "D) Hash Table"
        ],
        "ans": "A",
        "tip": "BFS explores neighbors level by level (breadth-wise). The first neighbor discovered must be the first one whose adjacent nodes are explored.",
        "praise": "Spot on! BFS = Queue (FIFO) level-order exploration.",
        "explanation": "BFS uses a Queue to explore vertices in increasing order of their distance from the source vertex."
    },
    {
        "q": "What data structure or mechanism is used to implement Depth First Search (DFS)?",
        "options": [
            "A) Stack (LIFO) or System Call Stack via Recursion",
            "B) Circular Queue",
            "C) Doubly Linked List",
            "D) Min-Heap"
        ],
        "ans": "A",
        "tip": "DFS plunges deep down a path until it hits a dead end, then backtracks. Backtracking naturally relies on LIFO stack behavior.",
        "praise": "Spot on buddy! DFS relies on a Stack (either explicit or via recursive call stack).",
        "explanation": "DFS explores as far as possible along each branch before backtracking. This depth-first path exploration is implemented recursively or with an explicit stack."
    },
    {
        "q": "In Graph Lab Experiment 12 (City Connectivity), how do you determine if the whole network is connected?",
        "options": [
            "A) Run BFS or DFS from node 0 and check if all vertices were visited (visited array all true).",
            "B) Check if the sum of edge weights is positive.",
            "C) Count if the number of edges equals vertices.",
            "D) Calculate the determinant of the adjacency matrix."
        ],
        "ans": "A",
        "tip": "If a graph is connected, starting a search from any one city must be able to reach every other city in the network.",
        "praise": "Spot on! If visited count == total vertices after a single BFS/DFS, the graph is connected.",
        "explanation": "Starting BFS/DFS from vertex 0 marks all reachable vertices. If all vertices are marked in the visited array, the graph is fully connected."
    },
    {
        "q": "What is a Minimum Spanning Tree (MST) of a connected, weighted graph?",
        "options": [
            "A) A subgraph that connects all V vertices with exactly (V - 1) edges while minimizing the total edge weight sum, with no cycles.",
            "B) A binary tree that contains the smallest numbers in the graph.",
            "C) A tree that has minimum height from root to leaf.",
            "D) The shortest path between two specific cities."
        ],
        "ans": "A",
        "tip": "Spanning = covers all vertices. Tree = connected and acyclic (V-1 edges). Minimum = lowest possible total sum of edge weights.",
        "praise": "Masterful! MST connects all V nodes using V-1 edges with minimum total cost (e.g. Kruskal's or Prim's algorithm).",
        "explanation": "An MST spans all vertices with exactly V-1 edges without cycles, minimizing overall cost. Essential in network routing and electrical grids."
    }
]

# ════════════════════════════════════════════════════════════════════════════════
# 3. JAVA OOP LAB (1BCS302) — 30 VIVA QUESTIONS (SET 1 & SET 2)
# ════════════════════════════════════════════════════════════════════════════════

JAVA_VIVA_SET_1 = [
    {
        "q": "What is the difference between JDK, JRE, and JVM?",
        "options": [
            "A) JDK is development kit (javac + tools); JRE is runtime environment (libraries); JVM is the virtual machine executing bytecode.",
            "B) JVM compiles code; JDK runs code; JRE is only for web browsers.",
            "C) JDK is for Windows; JRE is for Linux; JVM is for Mac.",
            "D) They are different brand names for the exact same Java executable."
        ],
        "ans": "A",
        "tip": "JDK contains JRE + development tools (compiler javac). JRE contains JVM + core runtime class libraries. JVM executes .class bytecode.",
        "praise": "Spot on! JDK > JRE > JVM is the foundational hierarchy of Java.",
        "explanation": "JDK (Java Development Kit) includes the compiler (javac) and tools. JRE provides libraries to run apps. JVM interprets/JIT-compiles bytecode into native machine instructions."
    },
    {
        "q": "Why is Java called 'Platform Independent'?",
        "options": [
            "A) The compiler produces platform-independent bytecode (.class), which can run on any OS that has a compatible JVM (WORA: Write Once, Run Anywhere).",
            "B) Java source code doesn't require a compiler.",
            "C) Java programs run directly on the motherboard without an OS.",
            "D) Java does not use memory."
        ],
        "ans": "A",
        "tip": "C compiles to native machine code specific to x86 or ARM. Java compiles to portable bytecode that any platform's JVM can execute.",
        "praise": "Spot on buddy! 'Write Once, Run Anywhere' thanks to standard bytecode and platform-specific JVMs.",
        "explanation": "Java source code (.java) compiles into bytecode (.class). Any device with a platform-specific JVM can execute this bytecode without recompilation."
    },
    {
        "q": "What is the difference between Method Overloading and Method Overriding?",
        "options": [
            "A) Overloading: Same method name with different parameters in the same class (Compile-time); Overriding: Same method signature in a subclass (Runtime).",
            "B) Overloading is in subclasses; Overriding is in the same class.",
            "C) Overloading requires the 'override' keyword; Overriding is automatic.",
            "D) Overloading only applies to static methods."
        ],
        "ans": "A",
        "tip": "Overloading = same name, different parameter lists (compile-time polymorphism). Overriding = child class redefines parent's method (runtime polymorphism).",
        "praise": "Spot on! Overloading is static/compile-time; Overriding is dynamic/runtime polymorphism.",
        "explanation": "Overloading occurs in the same class with different argument types/counts. Overriding occurs when a subclass provides its own implementation for an inherited parent method."
    },
    {
        "q": "What is Dynamic Method Dispatch in Java?",
        "options": [
            "A) The mechanism by which a call to an overridden method is resolved at runtime based on the actual object instance, not the reference type.",
            "B) Calling methods across multiple computers over the network.",
            "C) Compiling methods in parallel on multi-core CPUs.",
            "D) Dynamically changing method names while code runs."
        ],
        "ans": "A",
        "tip": "If `SuperClass ref = new SubClass(); ref.display();`, which display() runs? The SubClass version runs because the actual object is SubClass.",
        "praise": "Masterful! Dynamic Method Dispatch is the exact engine behind runtime polymorphism in Java.",
        "explanation": "When an overridden method is called through a superclass reference variable, Java determines which version to run at runtime based on the actual object type."
    },
    {
        "q": "What are the roles of 'this' and 'super' keywords in Java?",
        "options": [
            "A) 'this' refers to current class instance/constructor; 'super' refers to immediate parent class instance/constructor.",
            "B) 'this' is for static variables; 'super' is for private variables.",
            "C) 'this' calls methods on the thread; 'super' calls OS functions.",
            "D) Both keywords can only be used in interfaces."
        ],
        "ans": "A",
        "tip": "'this.x' resolves variable shadowing in the current object. 'super.display()' or 'super()' invokes parent class members and constructors.",
        "praise": "Spot on buddy! this = current object; super = parent object.",
        "explanation": "'this' refers to the current object instance (and this() calls an overloaded constructor). 'super' refers to the direct superclass members and constructor."
    },
    {
        "q": "Why does Java NOT support Multiple Inheritance with classes?",
        "options": [
            "A) To avoid ambiguity such as the 'Diamond Problem', keeping the language simple and robust.",
            "B) Because the JVM has a limitation of only one pointer.",
            "C) Because Sun Microsystems forgot to implement it.",
            "D) Multiple inheritance is illegal in object-oriented programming."
        ],
        "ans": "A",
        "tip": "If Class D inherits from Class B and Class C, and both B and C implement display() differently, which display() should D inherit? This is the Diamond Problem.",
        "praise": "Spot on! Multiple class inheritance creates the Diamond Problem; Java uses Interfaces instead to achieve multiple type implementation.",
        "explanation": "If two parent classes have a method with the same signature, a subclass wouldn't know which implementation to inherit. Interfaces solve this because they declare behavior without state."
    },
    {
        "q": "What is the key difference between an Abstract Class and an Interface (up to Java 7)?",
        "options": [
            "A) Abstract classes can have instance variables and concrete methods; Interfaces only have abstract methods and public static final constants.",
            "B) Abstract classes cannot have constructors; Interfaces have constructors.",
            "C) A class can inherit multiple abstract classes; but implement only one interface.",
            "D) Abstract classes are faster than interfaces."
        ],
        "ans": "A",
        "tip": "A class can extend only ONE abstract class (single inheritance), but can implement MULTIPLE interfaces.",
        "praise": "Spot on buddy! Abstract classes represent identity/state ('is-a'); interfaces represent contract/capability ('can-do').",
        "explanation": "Abstract classes support instance variables, constructors, and method bodies. Interfaces define pure behavioral contracts with multiple inheritance capability."
    },
    {
        "q": "What does the 'final' keyword mean when applied to a variable, method, and class?",
        "options": [
            "A) Final variable: constant value; Final method: cannot be overridden; Final class: cannot be inherited (subclassed).",
            "B) Final variable: global variable; Final method: runs last; Final class: deletes on exit.",
            "C) Final variable: destroyed by GC; Final method: private method; Final class: abstract class.",
            "D) It marks code that will be deleted in the next Java release."
        ],
        "ans": "A",
        "tip": "Final means 'cannot be changed': variable value cannot change, method logic cannot be overridden, class structure cannot be extended.",
        "praise": "Spot on! final variable = constant, final method = no override, final class = no subclassing.",
        "explanation": "`final` on a variable makes it an immutable constant; on a method it prevents subclass overriding; on a class (e.g. String) it prevents inheritance."
    },
    {
        "q": "What are the four access specifiers in Java and their visibility scopes?",
        "options": [
            "A) private (class only) < default (package only) < protected (package + subclasses) < public (everywhere)",
            "B) private < public < protected < default",
            "C) public (class only) < private (everywhere)",
            "D) protected (subclasses only) < default (world)"
        ],
        "ans": "A",
        "tip": "Private is locked inside the class. Default is visible to classmates in the same package. Protected adds access for children in other packages. Public is open to all.",
        "praise": "Clean and correct! private -> package-private -> protected -> public.",
        "explanation": "private is accessible only in the defining class. Default (package-private) is accessible within the same package. protected extends to subclasses in any package. public is universally accessible."
    },
    {
        "q": "Why is the String class in Java Immutable?",
        "options": [
            "A) For security, caching in the String Constant Pool, thread safety, and hashcode caching in HashMaps.",
            "B) Because the JVM cannot edit text once created.",
            "C) To save hard drive storage space.",
            "D) Strings are mutable in Java by default."
        ],
        "ans": "A",
        "tip": "If strings were mutable, changing a string shared in the String Constant Pool would silently corrupt other variables referencing the same literal.",
        "praise": "Spot on! Immutability guarantees security, thread-safety, and safe sharing in the String Pool.",
        "explanation": "String objects cannot be altered after creation. Operations like concat() return brand new String objects. This makes strings thread-safe and secure for network/DB connections."
    },
    {
        "q": "What is the difference between String, StringBuilder, and StringBuffer?",
        "options": [
            "A) String is immutable; StringBuilder is mutable and fast (non-thread-safe); StringBuffer is mutable and thread-safe (synchronized).",
            "B) String is mutable; StringBuilder is immutable.",
            "C) StringBuffer cannot append text.",
            "D) StringBuilder is only available on Android."
        ],
        "ans": "A",
        "tip": "Need frequent string modifications in a single thread? Use StringBuilder. Need thread-safe synchronization? Use StringBuffer. Static text? Use String.",
        "praise": "Spot on buddy! StringBuilder is fast single-threaded; StringBuffer is thread-safe synchronized.",
        "explanation": "String creates a new object on every edit. StringBuilder allows in-place modifications without thread locking (faster). StringBuffer synchronizes methods for thread safety."
    },
    {
        "q": "What does the 'static' keyword mean for variables and methods in Java?",
        "options": [
            "A) They belong to the Class itself rather than any individual object instance; shared by all instances and callable without creating an object.",
            "B) They can never be modified once initialized.",
            "C) They can only be accessed by one thread at a time.",
            "D) They are stored in read-only files on disk."
        ],
        "ans": "A",
        "tip": "That's why `main()` is static: `public static void main(String[] args)` — the JVM can invoke it before any object instance has been instantiated.",
        "praise": "Spot on! Static members belong to the class, not to object instances.",
        "explanation": "Static members are loaded once when the class is loaded. They share memory across all instances and can be invoked using `ClassName.methodName()`."
    },
    {
        "q": "What is the purpose of the 'package' keyword in Java?",
        "options": [
            "A) Groups related classes and interfaces, prevents naming conflicts, and controls access levels across namespaces.",
            "B) Compresses source files into ZIP archives.",
            "C) Encrypts code for commercial distribution.",
            "D) Automatically uploads code to Maven Central."
        ],
        "ans": "A",
        "tip": "Packages mirror folder directory structures (e.g. `package mypack.utils;` corresponds to `mypack/utils/`). They keep large projects organized without naming collisions.",
        "praise": "Spot on buddy! Packages provide modular namespaces and prevent class name collisions.",
        "explanation": "A package is a container that groups related classes and interfaces into a namespace matching the filesystem directory structure."
    },
    {
        "q": "What is Garbage Collection in Java and can a programmer force it?",
        "options": [
            "A) An automatic daemon thread that reclaims memory occupied by unreferenced objects; programmers can request it via System.gc(), but cannot force it.",
            "B) A manual free() command required for every object.",
            "C) A tool that removes unused Java files from disk.",
            "D) It can be strictly forced at any specific microsecond using delete."
        ],
        "ans": "A",
        "tip": "The JVM automatically cleans up unreachable heap objects. Calling `System.gc()` is merely an advisory suggestion to the JVM, not a mandatory command.",
        "praise": "Spot on! Garbage collection is automatic; System.gc() is only an advisory request.",
        "explanation": "The JVM's Garbage Collector identifies objects with zero active references and frees their heap space. System.gc() suggests collection, but the JVM chooses when to run."
    },
    {
        "q": "What is the difference between '==' and '.equals()' when comparing objects in Java?",
        "options": [
            "A) '==' compares memory reference addresses; '.equals()' compares the actual values/content of the objects.",
            "B) '==' compares values; '.equals()' compares references.",
            "C) They are exact synonyms and perform the same comparison.",
            "D) '.equals()' can only compare integers."
        ],
        "ans": "A",
        "tip": "Two different String objects `new String(\"hello\")` have different heap addresses (so `==` is false), but their contents match (so `.equals()` is true).",
        "praise": "Spot on! '==' tests reference identity; '.equals()' tests state/value equality.",
        "explanation": "`==` checks whether both references point to the exact same memory location. The `.equals()` method is overridden by classes like String to check logical value equality."
    }
]

JAVA_VIVA_SET_2 = [
    {
        "q": "What is the root class of the Java Exception hierarchy?",
        "options": [
            "A) java.lang.Throwable",
            "B) java.lang.Exception",
            "C) java.lang.Error",
            "D) java.lang.Object"
        ],
        "ans": "A",
        "tip": "Both Exception (recoverable conditions) and Error (catastrophic JVM problems like OutOfMemoryError) inherit directly from Throwable.",
        "praise": "Spot on buddy! Throwable is the superclass of all errors and exceptions in Java.",
        "explanation": "Throwable has two main subclasses: Error (serious system failures an application should not catch) and Exception (conditions a reasonable app might want to catch)."
    },
    {
        "q": "What is the difference between Checked and Unchecked Exceptions in Java?",
        "options": [
            "A) Checked exceptions (e.g. IOException) are checked at compile-time and must be handled with try-catch or throws; Unchecked exceptions (RuntimeException) occur at runtime.",
            "B) Checked exceptions crash the JVM; Unchecked exceptions are ignored.",
            "C) Unchecked exceptions must be declared with throws; Checked exceptions do not.",
            "D) Checked exceptions only happen on 32-bit JVMs."
        ],
        "ans": "A",
        "tip": "Exceptions inheriting from RuntimeException (like NullPointerException or ArrayIndexOutOfBoundsException) are unchecked. All other Exception subclasses are checked.",
        "praise": "Spot on! Checked = compiler forces handling; Unchecked = RuntimeException caused by programming logic bugs.",
        "explanation": "Checked exceptions represent external recoverable conditions (file not found, network drop) and are enforced by the compiler. Unchecked exceptions extend RuntimeException."
    },
    {
        "q": "Does the 'finally' block execute if a 'return' statement is executed inside the 'try' block?",
        "options": [
            "A) Yes, the finally block ALWAYS executes before the method actually returns (unless System.exit() was called).",
            "B) No, the return statement terminates execution immediately, skipping finally.",
            "C) Only if an exception occurred.",
            "D) It results in a compilation error."
        ],
        "ans": "A",
        "tip": "The JVM guarantees that finally blocks run for resource cleanup (closing files, sockets) even when try or catch blocks encounter a return statement.",
        "praise": "Brilliant answer! Examiners ask this trap constantly: finally executes even after a return statement.",
        "explanation": "The finally block is guaranteed to execute regardless of how the try block exits (normal completion, exception, or return). The only exception is System.exit()."
    },
    {
        "q": "What is the difference between the 'throw' and 'throws' keywords in Java?",
        "options": [
            "A) 'throw' explicitly throws an exception instance inside a method; 'throws' declares that a method might throw an exception in its method signature.",
            "B) 'throws' is inside method bodies; 'throw' is in signatures.",
            "C) 'throw' catches errors; 'throws' ignores errors.",
            "D) They are different spellings for the same keyword."
        ],
        "ans": "A",
        "tip": "Singular 'throw' is an action verb (`throw new MyException(\"message\");`). Plural 'throws' is a signature warning (`void readFile() throws IOException`).",
        "praise": "Spot on! throw = trigger an exception; throws = declare an exception in the method header.",
        "explanation": "`throw` is used in code blocks to raise an exception object directly. `throws` is used in method signatures to warn callers about checked exceptions."
    },
    {
        "q": "How do you create a User-Defined (Custom) Exception in Java?",
        "options": [
            "A) Create a class that extends java.lang.Exception (or RuntimeException) and provide constructors.",
            "B) Implement the ThrowableInterface.",
            "C) Declare a variable with the 'exception' keyword.",
            "D) Overwrite the java.lang.Error class."
        ],
        "ans": "A",
        "tip": "A custom exception is simply a standard Java class that inherits from Exception: `class InvalidAgeException extends Exception { ... }`.",
        "praise": "Spot on buddy! Extending Exception or RuntimeException is all it takes to build domain-specific exceptions.",
        "explanation": "To create a custom checked exception, extend `Exception`. To create an unchecked exception, extend `RuntimeException`. Typically, pass a message string to `super(msg)`."
    },
    {
        "q": "What are the two primary ways to create a Thread in Java?",
        "options": [
            "A) 1. By extending the Thread class, or 2. By implementing the Runnable interface.",
            "B) 1. By calling JVM.spawn(), or 2. By using fork().",
            "C) 1. By extending the Object class, or 2. By implementing Serializable.",
            "D) Threads can only be created by the OS, not in Java code."
        ],
        "ans": "A",
        "tip": "Implementing Runnable is usually preferred in industry because Java only supports single class inheritance, leaving your class free to extend another parent.",
        "praise": "Spot on! Extending Thread vs implementing Runnable is the classic multithreading interview topic.",
        "explanation": "Extending `Thread` or implementing `Runnable` and passing it to `new Thread(runnable)` are the two foundational mechanisms to execute concurrent threads."
    },
    {
        "q": "What is the difference between calling 't.start()' and 't.run()' on a Thread object?",
        "options": [
            "A) 't.start()' creates a new OS thread and invokes run() on that new thread; 't.run()' merely executes run() synchronously on the current thread.",
            "B) 't.run()' starts a new thread; 't.start()' does nothing.",
            "C) 't.start()' can only be called once per program.",
            "D) They behave identically."
        ],
        "ans": "A",
        "tip": "Calling `t.run()` directly is just a standard method call on the main thread — no concurrency occurs! You must call `t.start()` to spawn a thread.",
        "praise": "Awesome buddy! Calling run() directly gives zero multithreading; start() registers a new thread with the JVM scheduler.",
        "explanation": "`t.start()` requests the OS/JVM to allocate a call stack and spawn an independent thread. `t.run()` executes the method sequentially within the calling thread."
    },
    {
        "q": "What is the purpose of the 'synchronized' keyword in Java?",
        "options": [
            "A) Prevents race conditions by ensuring that only one thread can execute a critical section / access a shared monitor lock at a time.",
            "B) Speeds up thread execution by 2x.",
            "C) Synchronizes local clocks with network time servers.",
            "D) Forces all threads to sleep simultaneously."
        ],
        "ans": "A",
        "tip": "When multiple threads write to the same shared variable simultaneously, data corruption occurs. Synchronization enforces mutual exclusion (mutex).",
        "praise": "Spot on buddy! 'synchronized' acquires an object monitor lock to protect critical sections from race conditions.",
        "explanation": "A synchronized method or block acquires the intrinsic lock (monitor) on the target object, ensuring mutual exclusion so only one thread executes that block at any time."
    },
    {
        "q": "Where are the wait(), notify(), and notifyAll() methods defined in Java, and why?",
        "options": [
            "A) In the java.lang.Object class, because locks are associated with individual objects, not threads.",
            "B) In java.lang.Thread class.",
            "C) In java.lang.Runnable interface.",
            "D) In java.util.concurrent package."
        ],
        "ans": "A",
        "tip": "Every single Java object has an intrinsic monitor lock. Since any object can be used as a synchronization lock, wait() and notify() belong on Object.",
        "praise": "Masterful! Because every object has a monitor, wait() and notify() are defined on Object, not Thread.",
        "explanation": "Inter-thread communication depends on object monitors. Since every Java object contains a monitor lock, wait(), notify(), and notifyAll() are members of Object."
    },
    {
        "q": "What is a 'Deadlock' in Java Multithreading?",
        "options": [
            "A) A situation where two or more threads are permanently blocked, each waiting for a lock held by the other.",
            "B) A thread that runs out of memory and stops.",
            "C) When a thread finishes execution normally.",
            "D) A hardware crash on the host machine."
        ],
        "ans": "A",
        "tip": "Thread 1 holds Lock A and wants Lock B. Thread 2 holds Lock B and wants Lock A. Neither releases until they get both — resulting in permanent standoff.",
        "praise": "Spot on! Circular lock dependencies create unresolvable deadlocks.",
        "explanation": "Deadlock occurs when four Coffman conditions are met (mutual exclusion, hold & wait, no preemption, circular wait). Enforcing consistent lock ordering prevents deadlocks."
    },
    {
        "q": "What are Generics in Java, and what is their primary benefit?",
        "options": [
            "A) Parameterized types (e.g. ArrayList<String>) that provide compile-time type safety and eliminate runtime ClassCastExceptions.",
            "B) Code that runs on any operating system without JVM.",
            "C) Methods that have no return type.",
            "D) Generating random numbers automatically."
        ],
        "ans": "A",
        "tip": "Before generics, ArrayList stored bare Objects, requiring explicit type casting like `(String) list.get(0)`. Generics ensure the compiler checks types at build time.",
        "praise": "Spot on! Generics give compile-time type checking and remove clumsy explicit casting.",
        "explanation": "Generics allow classes, interfaces, and methods to operate on specified type parameters, catching type mismatches at compile time rather than crashing at runtime."
    },
    {
        "q": "What is the difference between ArrayList and LinkedList in the Java Collections Framework?",
        "options": [
            "A) ArrayList is backed by a dynamic resizable array (O(1) random access); LinkedList is a doubly-linked list (O(1) insert/delete at known nodes).",
            "B) ArrayList cannot store objects; LinkedList can only store numbers.",
            "C) LinkedList has faster random index access than ArrayList.",
            "D) ArrayList is synchronized; LinkedList is not."
        ],
        "ans": "A",
        "tip": "Need frequent lookups by index? Choose ArrayList. Need frequent insertions/deletions at the beginning or middle? Choose LinkedList.",
        "praise": "Spot on buddy! ArrayList is contiguous array; LinkedList is node-pointer based.",
        "explanation": "ArrayList provides fast index lookups O(1) but slow middle insertions O(n). LinkedList provides O(1) insertions at head/tail but requires sequential O(n) traversal to reach index k."
    },
    {
        "q": "What is the difference between List, Set, and Map in the Java Collections Framework?",
        "options": [
            "A) List: ordered collection with duplicates allowed; Set: unordered collection with NO duplicates; Map: key-value pairs with unique keys.",
            "B) List stores numbers; Set stores text; Map stores files.",
            "C) Set allows duplicates; List forbids duplicates.",
            "D) They are different implementations of the same interface."
        ],
        "ans": "A",
        "tip": "List = sequence (0, 1, 2...). Set = unique math set (no duplicates). Map = dictionary (unique key -> value).",
        "praise": "Spot on! List (ordered, duplicates), Set (unique items), Map (key-value mapping).",
        "explanation": "List preserves insertion order and permits duplicates. Set guarantees unique elements. Map maps unique keys to values and is not a subtype of Collection."
    },
    {
        "q": "What is Autoboxing and Unboxing in Java?",
        "options": [
            "A) Automatic conversion between primitive types (e.g. int) and their corresponding wrapper object classes (e.g. Integer).",
            "B) Packing Java files into JAR files.",
            "C) Moving data between CPU registers and RAM.",
            "D) Converting Java code to HTML."
        ],
        "ans": "A",
        "tip": "Collections like ArrayList<Integer> cannot store raw primitive `int`. Java automatically converts `int` to `Integer` (autoboxing) and back (unboxing).",
        "praise": "Spot on! Autoboxing bridges the gap between primitive types and object wrapper classes.",
        "explanation": "Autoboxing is the compiler's automatic conversion of primitive types into wrapper objects (`Integer obj = 5;`). Unboxing is the reverse (`int val = obj;`)."
    },
    {
        "q": "What is the difference between Byte Streams and Character Streams in Java File I/O?",
        "options": [
            "A) Byte streams (InputStream/OutputStream) read/write 8-bit raw bytes; Character streams (Reader/Writer) read/write 16-bit Unicode characters.",
            "B) Byte streams are for text; Character streams are for images and audio.",
            "C) Character streams can only handle ASCII.",
            "D) Both streams operate on 64-bit integers."
        ],
        "ans": "A",
        "tip": "Use Byte streams (FileInputStream) for binary files like images, PDFs, and compiled code. Use Character streams (FileReader) for human-readable text files.",
        "praise": "Spot on buddy! Byte streams = 8-bit raw binary; Character streams = 16-bit Unicode text.",
        "explanation": "Byte streams handle raw binary data (8-bit bytes). Character streams are designed for text, automatically handling character encoding (Unicode/UTF-8) translation."
    }
]

# ════════════════════════════════════════════════════════════════════════════════
# VIVA SET MAPPING & INTERACTIVE DRILL RUNNER
# ════════════════════════════════════════════════════════════════════════════════

VIVA_PRACTICE_SETS = {
    "git": {
        "title": "🐙 Git Lab (1BCSL307A)",
        "sets": {
            "1": {"name": "Set 1: Core Fundamentals & Workflow Mastery", "questions": GIT_VIVA_SET_1},
            "2": {"name": "Set 2: Advanced Scenarios, Disaster Recovery & Traps", "questions": GIT_VIVA_SET_2}
        }
    },
    "dsa": {
        "title": "🌳 DSA Lab (1BCSL306)",
        "sets": {
            "1": {"name": "Set 1: Memory, Pointers, Stacks, Queues & Lists", "questions": DSA_VIVA_SET_1},
            "2": {"name": "Set 2: Trees, BST, Hashing, Graph Algorithms", "questions": DSA_VIVA_SET_2}
        }
    },
    "java": {
        "title": "☕ Java OOP Lab (1BCS302)",
        "sets": {
            "1": {"name": "Set 1: OOP Principles, Classes, Inheritance & Dispatch", "questions": JAVA_VIVA_SET_1},
            "2": {"name": "Set 2: Exceptions, Multithreading, Generics & Collections", "questions": JAVA_VIVA_SET_2}
        }
    }
}

def run_viva_drill_session(subject_key, set_key):
    """
    Executes a 15-question interactive viva session with Socratic Guided Hinting.
    If the student makes a mistake, provides a mentor clue and second chance.
    """
    sub_data = VIVA_PRACTICE_SETS.get(subject_key)
    if not sub_data:
        return
    set_data = sub_data["sets"].get(set_key)
    if not set_data:
        return

    questions = set_data["questions"]
    total_q = len(questions)
    correct_first_try = 0
    correct_second_try = 0
    reviewed_together = 0

    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║  🎓 {sub_data['title']:<72} ║")
    print(f"║  📖 {set_data['name']:<72} ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print_dialogue(subject_key or "viva")
    print(f"  {Color.DIM}15 high-yield viva questions with Socratic hints. No stress, take your time!{Color.RESET}\n")
    prompt_input("  Press Enter to begin the practice drill... ")

    for idx, item in enumerate(questions, 1):
        # Dynamically shuffle options so the correct answer is randomized every session!
        shuffled_opts, target_ans = shuffle_mcq_options(item["options"], item["ans"])

        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║  Question {idx:02d} of {total_q:02d}  •  {sub_data['title']:<53} ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        print(f"  {Color.BOLD}{Color.WHITE}{item['q']}{Color.RESET}\n")
        for opt in shuffled_opts:
            print(f"    {Color.CYAN}{opt}{Color.RESET}")

        print(f"\n  {Color.DIM}(Tip: Type A, B, C, D  |  'H' for Mentor Clue  |  '0' to Exit){Color.RESET}\n")

        attempt = 1
        solved = False

        while attempt <= 2 and not solved:
            prompt_text = f"  {Color.BOLD}Your Answer [A / B / C / D]: {Color.RESET}" if attempt == 1 else f"  {Color.BOLD}Second Try [A / B / C / D]: {Color.RESET}"
            ans = prompt_input(prompt_text).strip().upper()

            if ans in ("0", "EXIT", "Q", "MENU"):
                return
            if ans == "H":
                print(f"\n  {Color.YELLOW}💡 Mentor Clue: {item['tip']}{Color.RESET}\n")
                continue
            if ans not in ("A", "B", "C", "D"):
                print(f"  {Color.RED}Please type A, B, C, or D buddy!{Color.RESET}")
                continue

            spinner("Reflecting on your answer", duration=0.35, color=Color.YELLOW)

            if ans == target_ans:
                solved = True
                anim_correct()
                if attempt == 1:
                    correct_first_try += 1
                    _record_concept_mastered("viva question correct")
                    print(f"\n  {Color.GREEN}{Color.BOLD}✔ {item['praise']}{Color.RESET}")
                else:
                    correct_second_try += 1
                    _record_concept_mastered("viva second attempt correct")
                    print(f"\n  {Color.GREEN}{Color.BOLD}🎉 Brilliant recovery buddy! You nailed it! ❤️{Color.RESET}")
            else:
                if attempt == 1:
                    anim_wrong()
                    print(f"\n  {Color.YELLOW}🌱 Not quite buddy, but you're thinking along the right lines!{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {item['tip']}{Color.RESET}")
                    print(f"  {Color.DIM}Take another look at the options and try once more:{Color.RESET}\n")
                    attempt += 1
                else:
                    anim_wrong()
                    reviewed_together += 1
                    print(f"\n  {Color.MAGENTA}🤝 No worries at all buddy! Learning is a process — we face it together.{Color.RESET}")
                    print(f"  {Color.YELLOW}The correct answer is [{target_ans}].{Color.RESET}")
                    attempt += 1

        print(f"\n  {Color.CYAN}{'─'*74}{Color.RESET}")
        print(f"  {Color.BOLD}📖 Key Takeaway for Lab Exam:{Color.RESET}")
        print(f"  {Color.WHITE}{item['explanation']}{Color.RESET}")
        print(f"  {Color.CYAN}{'─'*74}{Color.RESET}\n")
        prompt_input(f"  {Color.DIM}Press Enter for next question...{Color.RESET}")

    # Summary Screen
    clear_screen()
    print(f"\n{Color.GREEN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║  🎉 PRACTICE DRILL COMPLETE — {sub_data['title']:<43} ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

    print_dialogue("viva")
    print(f"  🎯 Questions Practiced       : {total_q}")
    print(f"  🌟 Mastered on First Try    : {Color.GREEN}{correct_first_try}{Color.RESET}")
    print(f"  💡 Mastered with Mentor Clue : {Color.YELLOW}{correct_second_try}{Color.RESET}")
    print(f"  🤝 Learned Concepts Together : {Color.CYAN}{reviewed_together}{Color.RESET}\n")

    score_total = correct_first_try + correct_second_try
    if score_total >= 13:
        _unlock_badge("quickfire_ace")
        print(f"  {Color.GREEN}{Color.BOLD}🏆 Outstanding mastery! You are 100% ready to ace the external viva! 🌟{Color.RESET}\n")
    elif score_total >= 9:
        print(f"  {Color.YELLOW}{Color.BOLD}👏 Great job buddy! Review the few tricky questions and you're golden! ✨{Color.RESET}\n")
    else:
        print(f"  {Color.CYAN}{Color.BOLD}🌱 Solid effort today! Keep this practice up and the concepts will be second nature! ☕{Color.RESET}\n")

    prompt_input("  Press Enter to return to Main Menu... ")

