"""
OILS-3: GIT LAB DATA (VTU 2025 Scheme - 1BCSL307A)
Comprehensive End-to-End Program Explanations:
1. Two-Tier Overview (High-level Story in plain English)
2. Complete Step-by-Step Functional Blocks covering every command from first line to last line
   - 🎯 What we are doing (1-2 sentences)
   - 🔍 How it works (2-3 quick bullets on flags, parameters, mechanics)
   - 💡 Exam trap / Real-world intuition
3. Randomly dynamic viva challenges with shuffle_mcq_options
"""

GIT_EXPERIMENTS = [
    {
        "num": 1,
        "part": "A",
        "title": "Repository Setup, Config & Basic Commits",
        "story": "Imagine a magical time-machine camera for your code: running 'git init' builds the camera (the hidden .git folder), setting your name/email writes who is taking the pictures, 'git add' puts your files on stage in front of the lens (Staging Area), and 'git commit' snaps an immutable historical photo (Commit snapshot) that you can always travel back to!",
        "problem": "Initialize a new repository using 'git init', configure user identity (name, email), create a sample file, stage it via 'git add', and commit it using 'git commit -m'. Verify the commit with 'git log'.",
        "concept": "Git is a content-addressable distributed version control system. Every commit represents an immutable snapshot of the entire project timeline stored in the hidden .git directory.",
        "commands": """# 1. Initialize local repository
git init

# 2. Configure user identity (Author details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Create content & verify working directory
echo "VTU Git Lab 1BCSL307A" > readme.txt
git status

# 4. Stage changes to Index
git add readme.txt

# 5. Commit snapshot to history
git commit -m "docs: initialize repository with readme"

# 6. Verify commit history
git log --oneline""",
        "blocks": [
            {
                "title": "Part 1: Initializing the Repo (.git Database)",
                "code": "git init",
                "doing": "Transforms any standard folder into a tracked Git repository by creating the hidden `.git/` database directory.",
                "how": [
                    "Creates `.git/` with internal folders: `objects/`, `refs/`, `HEAD`, and `config`.",
                    "All version control history, commit snapshots, and branch pointers live here."
                ],
                "watchout": "The .git folder IS your entire repository! If you delete it, all history vanishes and only plain files remain."
            },
            {
                "title": "Part 2: Configuring Author Identity",
                "code": "git config --global user.name \"Student Name\"\ngit config --global user.email \"student@college.edu\"",
                "doing": "Binds your name and email to every snapshot you create for author attribution.",
                "how": [
                    "`--global`: Writes to `~/.gitconfig` for all repositories on this machine.",
                    "Without `--global`, configurations are stored locally in `.git/config` for this project only."
                ],
                "watchout": "Git requires identity to commit — without it, commit attempts halt with an author identity error."
            },
            {
                "title": "Part 3: Staging Changes (The Index)",
                "code": "echo \"VTU Git Lab 1BCSL307A\" > readme.txt\ngit status\ngit add readme.txt",
                "doing": "Creates project content, inspects file states, and stages specific files for the next snapshot.",
                "how": [
                    "`git status`: Displays which files are modified, untracked, or staged.",
                    "`git add readme.txt`: Compresses file content into a Blob in `.git/objects/` and updates `.git/index`."
                ],
                "watchout": "Files don't commit directly from your folder! You must stage them with `git add` to prepare the snapshot."
            },
            {
                "title": "Part 4: Committing Snapshots & Log Verification",
                "code": "git commit -m \"docs: initialize repository with readme\"\ngit log --oneline",
                "doing": "Freezes the staged staging area into a permanent historical commit and prints a verification summary.",
                "how": [
                    "`git commit -m`: Writes a commit object with author, date, tree hash, and parent pointer, then advances HEAD.",
                    "`git log --oneline`: Shows the 7-character commit SHA hash and message summary."
                ],
                "watchout": "Always write clear, meaningful commit messages — cryptic messages like 'fix' make debugging past bugs painful."
            }
        ],
        "challenge": {
            "prompt": "What does 'git add <filename>' do under the hood in the Git object store?",
            "opts": [
                "A) It immediately uploads the file to GitHub cloud servers.",
                "B) It creates an immutable compressed Blob object of the file's contents inside .git/objects and updates the index file.",
                "C) It renames the file to .bak.",
                "D) It compiles the source code into binary."
            ],
            "correct_opt": "B",
            "hint": "Git creates Blob objects in .git/objects during 'git add', even before you commit!",
            "praise": "Examiner masterclass! git add creates Blob objects in the database immediately.",
            "roast": "git add creates a Blob object in `.git/objects` and stages its reference in `.git/index`!"
        }
    },
    {
        "num": 2,
        "part": "A",
        "title": "Creating, Switching & Merging Branches",
        "story": "Want to experiment with a crazy new idea without breaking working code? Create a Branch! In Git, a branch isn't a bulky copy of your files — it is literally a tiny 41-byte text file containing a commit hash pointer. You can create a branch, test features in total isolation, and smoothly merge them back into main in 0.01 seconds!",
        "problem": "Create a new branch named 'feature-branch', switch to it, make and commit changes in isolation, switch back to 'main' / 'master', and merge 'feature-branch' using fast-forward merge.",
        "commands": """# 1. Create and switch to new branch
git checkout -b feature-branch
# (Alternative modern syntax: git switch -c feature-branch)

# 2. Modify files on branch
echo "New feature logic" >> feature.txt
git add feature.txt
git commit -m "feat: implement initial feature logic"

# 3. Switch back to main branch
git checkout main
# (Alternative: git switch main)

# 4. Merge feature branch into main
git merge feature-branch

# 5. Clean up merged branch
git branch -d feature-branch""",
        "blocks": [
            {
                "title": "Part 1: Branch Creation & HEAD Switching",
                "code": "git checkout -b feature-branch\n# Modern syntax:\ngit switch -c feature-branch",
                "doing": "Creates a new branch pointer and points HEAD to it so all future commits happen on the branch.",
                "how": [
                    "`-b` / `-c`: Creates a pointer file `.git/refs/heads/feature-branch` pointing to current commit.",
                    "`HEAD`: Now points to `refs/heads/feature-branch`."
                ],
                "watchout": "Git 2.23 introduced `git switch` specifically for branches so you don't confuse `checkout` (which also restores files)."
            },
            {
                "title": "Part 2: Isolated Commits on Branch",
                "code": "echo \"New feature logic\" >> feature.txt\ngit add feature.txt\ngit commit -m \"feat: implement initial feature logic\"",
                "doing": "Adds new work specifically to `feature-branch` while keeping `main` completely untouched and stable.",
                "how": [
                    "New commit object is created with parent pointing to previous commit.",
                    "`feature-branch` pointer advances forward; `main` stays locked at its original position."
                ],
                "watchout": "If you don't commit before switching branches, uncommitted changes might block the switch or spill over!"
            },
            {
                "title": "Part 3: Fast-Forward Merge into Main",
                "code": "git checkout main\ngit merge feature-branch",
                "doing": "Switches back to main and brings the branch changes in by sliding the main pointer forward.",
                "how": [
                    "Because `main` did not create any new commits, Git performs a Fast-Forward (FF) merge.",
                    "`main` simply moves its pointer to the tip of `feature-branch` without creating a merge commit."
                ],
                "watchout": "Fast-Forward creates NO new commit! It is an instantaneous O(1) pointer advance."
            },
            {
                "title": "Part 4: Safe Branch Deletion",
                "code": "git branch -d feature-branch",
                "doing": "Removes the branch label now that its commits have been incorporated into main.",
                "how": [
                    "`-d` (lowercase): Safe deletion. Git checks that the branch has been merged before deleting.",
                    "If unmerged commits exist, Git refuses to delete unless you force with `-D` (uppercase)."
                ],
                "watchout": "Deleting a branch only deletes the 41-byte pointer; the commits remain safe inside main!"
            }
        ],
        "challenge": {
            "prompt": "How much disk storage does a newly created branch consume inside the .git directory?",
            "opts": [
                "A) The full size of all files in the project.",
                "B) Exactly 41 bytes (a tiny text file containing the 40-char SHA hash of the commit tip plus a newline).",
                "C) 1 Gigabyte.",
                "D) Nothing, branches live only in RAM."
            ],
            "correct_opt": "B",
            "hint": "Git branches are just lightweight pointer files in .git/refs/heads/.",
            "praise": "Spot on! Git branches are just 41-byte text pointers, making branching instantaneous.",
            "roast": "Git branches are NOT file copies — they are just 41-byte text pointers to commit hashes!"
        }
    },
    {
        "num": 3,
        "part": "A",
        "title": "Stashing Work in Progress",
        "story": "You're halfway through writing messy, untested code when your professor calls you over to fix an urgent bug on main. You can't commit broken code, but you don't want to delete your progress! Enter 'git stash': like sweeping your messy desk into a drawer (`git stash`), switching branches to fix the bug, and later dumping your work back onto the desk (`git stash pop`)!",
        "problem": "Modify tracked files while working on a feature, save unfinished work to the stash stack using 'git stash push -m', verify working tree is clean, inspect stash with 'git stash list', and restore changes using 'git stash pop'.",
        "commands": """# 1. Modify working files
echo "Incomplete draft" >> draft.txt

# 2. Stash unfinished work with a clear label
git stash push -m "WIP: draft calculations"

# 3. Verify clean working directory
git status

# 4. Inspect stash stack
git stash list

# 5. Restore work and drop from stash stack
git stash pop""",
        "blocks": [
            {
                "title": "Part 1: The Dilemma & Stashing Unfinished Work",
                "code": "echo \"halfway done\" >> draft.txt\ngit stash push -m \"WIP: draft calculations\"\ngit status",
                "doing": "Temporarily sweeps uncommitted modifications off your working desk into Git's hidden shelf and restores clean HEAD state.",
                "how": [
                    "`git stash push -m`: Takes tracked unstaged and staged diffs and creates special commit objects at `refs/stash`.",
                    "`git status` returns to clean, allowing you to switch branches or pull updates without conflicts."
                ],
                "watchout": "By default, `git stash` only stashes TRACKED files! Untracked files require `git stash -u` (include untracked)."
            },
            {
                "title": "Part 2: Inspecting the Stash Stack (list & show)",
                "code": "git stash list\ngit stash show -p stash@{0}",
                "doing": "Views all stashed work saved across time and previews specific code changes inside a stash.",
                "how": [
                    "`git stash list`: Shows the stack (`stash@{0}`, `stash@{1}`), with the newest at index 0.",
                    "`-p`: Shows the full unified diff of what was stashed inside."
                ],
                "watchout": "Remember stack ordering (LIFO): `stash@{0}` is always the most recently stashed item!"
            },
            {
                "title": "Part 3: Restoring Changes (pop vs apply)",
                "code": "git stash pop\n# Alternative if you want to keep the backup on stack:\n# git stash apply",
                "doing": "Brings your unfinished work right back onto your files so you can resume coding.",
                "how": [
                    "`git stash pop`: Applies `stash@{0}` AND removes it from the stack.",
                    "`git stash apply`: Replays modifications onto files but retains the backup in the stash stack."
                ],
                "watchout": "Use `apply` if you want to apply the same stash across multiple branches; use `pop` when done with it."
            }
        ],
        "challenge": {
            "prompt": "What command restores stashed changes WITHOUT removing them from the stash stack?",
            "opts": [
                "A) git stash drop",
                "B) git stash clear",
                "C) git stash apply",
                "D) git stash pop"
            ],
            "correct_opt": "C",
            "hint": "Pop removes the stash from the stack; Apply keeps it there for safety.",
            "praise": "Correct! 'git stash apply' restores changes while keeping the stash intact on the stack.",
            "roast": "Pop deletes the stash from the stack; 'git stash apply' restores and keeps it!"
        }
    },
    {
        "num": 4,
        "part": "A",
        "title": "Cloning Remote Repositories & Tracking",
        "story": "How do you download open-source projects like the Linux kernel or VS Code? You clone! When you run 'git clone', Git doesn't just download files: it downloads the ENTIRE project history, every commit ever made, all tags, and sets up read-only tracking bookmarks under 'origin/' so you can work completely offline!",
        "problem": "Clone an existing remote repository from GitHub/GitLab using 'git clone', inspect configured remotes with 'git remote -v', and check tracking branches with 'git branch -a'.",
        "commands": """# 1. Clone remote repository
git clone https://github.com/torvalds/subsurface-for-dirk.git my-repo

# 2. Enter cloned repository
cd my-repo

# 3. Inspect remote connections
git remote -v

# 4. View all local and remote-tracking branches
git branch -a

# 5. Inspect remote tracking details
git remote show origin""",
        "blocks": [
            {
                "title": "Part 1: git clone — Full Database Mirroring",
                "code": "git clone https://github.com/torvalds/subsurface-for-dirk.git my-repo\ncd my-repo",
                "doing": "Downloads the entire commit database and automatically configures remote tracking branches.",
                "how": [
                    "`git clone`: Automatically performs 4 actions: `git init`, `git remote add origin`, `git fetch`, and `git checkout main`.",
                    "You get 100% of the project history locally on your machine."
                ],
                "watchout": "Because you have the entire database locally, you can view logs, diffs, and switch branches with zero internet connection!"
            },
            {
                "title": "Part 2: Inspecting Remote URLs (git remote -v)",
                "code": "git remote -v\ngit remote show origin",
                "doing": "Checks what remote server you are connected to and inspects URL endpoints and push/fetch configurations.",
                "how": [
                    "`git remote -v`: Shows fetch and push URLs mapped to the `origin` alias.",
                    "`git remote show origin`: Displays tracking status, showing which local branches are configured for `git pull`."
                ],
                "watchout": "`origin` is not a server type or special command — it is just a friendly nickname for the repository URL."
            },
            {
                "title": "Part 3: Local vs Remote-Tracking Branches (git branch -a)",
                "code": "git branch -a",
                "doing": "Displays both your local editable branches and the read-only remote mirrors.",
                "how": [
                    "Green branches: Local branches you can commit to.",
                    "Red branches (`remotes/origin/*`): Read-only bookmarks recording where branches were when last fetched."
                ],
                "watchout": "You cannot commit directly onto `origin/main`! You commit on local `main` and then push."
            }
        ],
        "challenge": {
            "prompt": "What does 'origin' represent in a cloned Git repository?",
            "opts": [
                "A) The root folder on your C: drive.",
                "B) A shorthand alias name pointing to the remote repository URL.",
                "C) The first commit ever made in the project.",
                "D) The master password of the Git repository."
            ],
            "correct_opt": "B",
            "hint": "origin is simply the default nickname Git gives to the URL you cloned from.",
            "praise": "Spot on! 'origin' is just a convenient alias for the remote repository URL.",
            "roast": "'origin' is simply a nickname pointing to the remote repository URL!"
        }
    },
    {
        "num": 5,
        "part": "A",
        "title": "Fetch & Rebase vs Merge",
        "story": "Two teammates work on different features: one uses Merge, one uses Rebase. Merge creates a diamond 'merge bubble' commit that ties histories together. Rebase is like picking up your commits, lifting them into the air, and placing them neatly on top of the newest commit on main, creating a perfectly straight, linear timeline!",
        "problem": "Fetch the latest changes from origin using 'git fetch origin', switch to your feature branch, rebase your commits onto 'origin/main' with 'git rebase origin/main', and understand linear history.",
        "commands": """# 1. Download remote commits without merging
git fetch origin

# 2. Switch to working branch
git checkout feature-branch

# 3. Re-apply feature commits on top of origin/main
git rebase origin/main

# 4. View resulting linear history
git log --oneline --graph""",
        "blocks": [
            {
                "title": "Part 1: git fetch — The Safe Download",
                "code": "git fetch origin",
                "doing": "Downloads new commits and objects from the remote repository without altering your active work.",
                "how": [
                    "`git fetch`: Updates `origin/main` pointer and pulls down objects into `.git/objects/`.",
                    "Your working files and active branch pointers remain 100% untouched."
                ],
                "watchout": "fetch is safe; pull is risky! Pull immediately tries to merge downloaded code into your active files."
            },
            {
                "title": "Part 2: Inspecting Divergence (HEAD..origin/main)",
                "code": "git log HEAD..origin/main --oneline\ngit log origin/main..HEAD --oneline",
                "doing": "Compares your local branch against the server to see what commits they have that you don't, and vice versa.",
                "how": [
                    "`HEAD..origin/main`: Shows commits on remote that you haven't merged yet.",
                    "`origin/main..HEAD`: Shows your local unpushed commits."
                ],
                "watchout": "Always inspect divergence before rebasing or merging to avoid unexpected surprises."
            },
            {
                "title": "Part 3: git rebase — Replaying Commits for Linear History",
                "code": "git checkout feature-branch\ngit rebase origin/main\ngit log --graph --oneline",
                "doing": "Lifts your feature commits off their old base and replays them cleanly onto the tip of origin/main.",
                "how": [
                    "Saves feature commits as temporary patch files.",
                    "Resets branch tip to `origin/main`.",
                    "Applies patches one by one, giving each a brand new commit SHA."
                ],
                "watchout": "Golden Rule of Rebase: NEVER rebase commits that have already been pushed to public shared branches!"
            }
        ],
        "challenge": {
            "prompt": "Why is 'git pull' different from 'git fetch'?",
            "opts": [
                "A) 'git pull' downloads and immediately merges into your current branch; 'git fetch' only downloads without merging.",
                "B) 'git fetch' requires root permissions; 'git pull' does not.",
                "C) 'git fetch' deletes local branches.",
                "D) They are exact synonyms."
            ],
            "correct_opt": "A",
            "hint": "git pull = git fetch + git merge in one command.",
            "praise": "Universal Git truth! git pull = fetch + merge.",
            "roast": "git fetch downloads objects safely; git pull downloads AND merges them immediately!"
        }
    },
    {
        "num": 6,
        "part": "A",
        "title": "Merge with Custom Commit Message & No-Fast-Forward",
        "story": "Fast-Forward merges are neat, but they erase the evidence that a feature branch ever existed! Using `--no-ff` (No Fast-Forward), you force Git to create an explicit 3-Way Merge Commit with TWO parents, forever recording that this feature was developed as an isolated module and integrated on this date.",
        "problem": "Create divergent histories on 'main' and a feature branch, merge the feature branch using 'git merge --no-ff -m \"Merge feature module\"', and verify the 2-parent merge commit.",
        "commands": """# 1. Switch to main
git checkout main

# 2. Perform 3-way merge forcing a merge commit
git merge --no-ff feature-branch -m "merge: integrate user authentication module"

# 3. Verify two parent hashes in log
git log -n 1
git log --graph --oneline""",
        "blocks": [
            {
                "title": "Part 1: The Fast-Forward Problem",
                "code": "git checkout main\n# Normal merge would fast-forward and hide branch history:\n# git merge feature-branch",
                "doing": "Recognizes that default fast-forward merges erase historical branch boundaries by simply sliding the pointer forward.",
                "how": [
                    "When main has no new commits, Git defaults to fast-forwarding.",
                    "In production history, this makes it look like commits were developed directly on main."
                ],
                "watchout": "When you want to document a distinct feature integration milestone in enterprise audits, you must avoid default fast-forward."
            },
            {
                "title": "Part 2: The Explicit --no-ff Merge",
                "code": "git merge --no-ff feature-branch -m \"merge: integrate user authentication module\"",
                "doing": "Forces Git to create a genuine 2-parent merge commit even if a simple pointer advance was possible.",
                "how": [
                    "`--no-ff`: Disables fast-forward pointer movement.",
                    "`-m`: Custom log message for the integration milestone.",
                    "The resulting commit has two parents: Parent 1 (old main tip) and Parent 2 (feature branch tip)."
                ],
                "watchout": "Production teams love `--no-ff` because it keeps feature boundaries clearly visible in `git log --graph`."
            },
            {
                "title": "Part 3: Verifying the Dual-Parent Graph",
                "code": "git log -n 1\ngit log --graph --oneline",
                "doing": "Inspects the newly created commit to confirm the existence of two parent hashes and the merge bubble shape.",
                "how": [
                    "`git log -n 1`: Prints `Merge: <hash1> <hash2>`, proving two branch parents exist.",
                    "`git log --graph`: Draws the ASCII loop `*   merge commit` uniting two separate lines."
                ],
                "watchout": "If you ever need to revert a merge commit, you must specify which parent to follow using `-m 1` or `-m 2`!"
            }
        ],
        "challenge": {
            "prompt": "What does a merge commit created with '--no-ff' have that a fast-forward merge lacks?",
            "opts": [
                "A) A password protection hash.",
                "B) A compressed zip archive of the project.",
                "C) Exactly two parent commit hashes recording the integration of both branches.",
                "D) Automatic deployment to AWS."
            ],
            "correct_opt": "C",
            "hint": "A 3-way merge commit unites two branch histories, so it points back to both parent tips.",
            "praise": "Spot on! Merge commits connect two histories and have 2 parents.",
            "roast": "A 3-way merge commit has 2 parent pointers; fast-forward creates no commit at all!"
        }
    },
    {
        "num": 7,
        "part": "B",
        "title": "Git Tags & Releases",
        "story": "Branches move every time you make a commit. But what if you want to freeze a version forever, like 'Version 1.0 Release'? You use a Tag! A Tag is a permanent milestone pin attached to a specific commit hash that NEVER moves. Annotated tags even store release notes, creator name, and release dates!",
        "problem": "Create a lightweight tag using 'git tag v1.0', create an annotated tag with release notes using 'git tag -a v1.1 -m \"Release 1.1\"', inspect tag details with 'git show', and list all tags.",
        "commands": """# 1. Create lightweight tag
git tag v1.0

# 2. Create annotated tag with cryptographic metadata & message
git tag -a v1.1 -m "Release v1.1: Production verified build"

# 3. List all tags
git tag -l

# 4. Inspect annotated tag object
git show v1.1""",
        "blocks": [
            {
                "title": "Part 1: Lightweight Tags (Pointer Pins)",
                "code": "git tag v1.0\ngit tag -l",
                "doing": "Creates a simple bookmark pointing to the current commit without any additional metadata.",
                "how": [
                    "Creates a 41-byte text file in `.git/refs/tags/v1.0` containing the target commit SHA.",
                    "`git tag -l`: Lists all existing tags alphabetically."
                ],
                "watchout": "Lightweight tags contain no author name or date — use them only for quick personal bookmarks."
            },
            {
                "title": "Part 2: Annotated Tags (Full Release Objects)",
                "code": "git tag -a v1.1 -m \"Release v1.1: Production verified build\"",
                "doing": "Creates an official release tag with author signature, timestamp, and release notes.",
                "how": [
                    "`-a`: Tells Git to create a full Tag Object in `.git/objects/`.",
                    "`-m`: Attaches release notes or changelog message.",
                    "Can even be cryptographically signed with GPG keys using `-s`."
                ],
                "watchout": "Production software releases should ALWAYS use annotated tags (`-a`) for provenance and traceability."
            },
            {
                "title": "Part 3: Inspecting & Sharing Tags (git show & git push --tags)",
                "code": "git show v1.1\n# Sharing tags to GitHub:\n# git push origin v1.1\n# git push origin --tags",
                "doing": "Inspects tag metadata and explains how tags are published to remote repositories.",
                "how": [
                    "`git show v1.1`: Dumps the tagger identity, date, message, and the associated commit diff.",
                    "Normal `git push` does NOT push tags! You must explicitly push tags using `--tags`."
                ],
                "watchout": "Remember this viva favorite: `git push` does NOT transfer tags by default — you must use `git push --tags`."
            }
        ],
        "challenge": {
            "prompt": "When you make new commits on a branch, what happens to tags created earlier on that branch?",
            "opts": [
                "A) They advance automatically with the branch.",
                "B) They are erased.",
                "C) They stay permanently pinned to the specific commit they were created on.",
                "D) They are converted into branches."
            ],
            "correct_opt": "C",
            "hint": "Branches are moving pointers; tags are static milestone pins that never move.",
            "praise": "Exactly right! Tags are immutable pins in history.",
            "roast": "Tags never move! They stay permanently attached to their original target commit."
        }
    },
    {
        "num": 8,
        "part": "B",
        "title": "Cherry-Picking Specific Commits",
        "story": "Imagine a teammate is developing a big messy feature on a dev branch with 50 commits, but commit #12 contains an urgent security bugfix that you desperately need on production main right now. You don't want the 49 unfinished commits! With 'git cherry-pick', you surgically pluck that ONE single commit and apply it cleanly to main!",
        "problem": "Identify a critical bugfix commit on 'dev-branch', switch to 'main', and cherry-pick that isolated commit onto main using 'git cherry-pick <commit-sha>'.",
        "commands": """# 1. Locate bugfix commit on another branch
git log dev-branch --oneline -n 3

# 2. Switch to main
git checkout main

# 3. Apply isolated commit to main
git cherry-pick a1b2c3d""",
        "blocks": [
            {
                "title": "Part 1: Locating the Specific Commit SHA",
                "code": "git log dev-branch --oneline -n 5\ngit checkout main",
                "doing": "Finds the exact hash of the isolated commit on another branch and switches back to the target branch.",
                "how": [
                    "`git log dev-branch`: Inspects another branch's timeline without switching to it.",
                    "Copy the 7-character abbreviated commit SHA of the desired change."
                ],
                "watchout": "Make sure your current working directory on main is clean before cherry-picking to avoid conflicts."
            },
            {
                "title": "Part 2: git cherry-pick — Surgical Patch Application",
                "code": "git cherry-pick a1b2c3d",
                "doing": "Calculates the exact diff introduced by that past commit and commits it directly onto your current branch.",
                "how": [
                    "Git computes the diff between `a1b2c3d` and its parent commit.",
                    "Applies that diff patch to the current HEAD of `main`.",
                    "Generates a brand new commit on `main` with the same changes and message, but a new SHA."
                ],
                "watchout": "Cherry-pick generates a NEW commit hash because the parent commit on main is different."
            },
            {
                "title": "Part 3: Conflict Resolution & Aborting",
                "code": "# In case of conflicts during cherry-pick:\n# git status\n# Edit files to resolve conflicts, then:\n# git add resolved_file.txt\n# git cherry-pick --continue\n# OR cancel the entire cherry-pick:\n# git cherry-pick --abort",
                "doing": "Handles code conflicts gracefully if the cherry-picked changes collide with lines on main.",
                "how": [
                    "`--continue`: Resumes the cherry-pick after conflict markers are fixed and staged.",
                    "`--abort`: Safely rolls back everything to the state before cherry-picking was attempted."
                ],
                "watchout": "`--abort` is your best friend when a cherry-pick turns unexpectedly messy!"
            }
        ],
        "challenge": {
            "prompt": "When should you use 'git cherry-pick' instead of 'git merge'?",
            "opts": [
                "A) When you want to combine every single commit from a branch.",
                "B) When you need to surgically extract ONE specific bugfix commit from an unfinished branch without bringing along unfinished features.",
                "C) To delete a repository.",
                "D) To reset the author's password."
            ],
            "correct_opt": "B",
            "hint": "Cherry-pick is surgical extraction of an isolated commit.",
            "praise": "Spot on! Cherry-picking is used for surgical extraction of isolated hotfixes.",
            "roast": "Cherry-pick is for surgical extraction of individual commits, not entire branches!"
        }
    },
    {
        "num": 9,
        "part": "B",
        "title": "Deep Commit Inspection (Show & Cat-File)",
        "story": "Want to see what an engineer actually changed at 2:00 AM three months ago? 'git show' reveals the author, timestamp, commit message, and exact color-coded line-by-line diff. And if you want to look at Git's raw plumbing database, 'git cat-file -p' lets you peek inside any raw Blob, Tree, or Commit object!",
        "problem": "Inspect the most recent commit metadata and diff with 'git show HEAD', inspect file content at a past commit with 'git show <sha>:filename', and examine object types with 'git cat-file -t'.",
        "commands": """# 1. Inspect latest commit details and diff
git show HEAD

# 2. View file content at a past commit without checking it out
git show a1b2c3d:readme.txt

# 3. Plumbing: check object type and raw content
git cat-file -t a1b2c3d
git cat-file -p a1b2c3d""",
        "blocks": [
            {
                "title": "Part 1: git show HEAD — High-Level Commit & Diff Inspection",
                "code": "git show HEAD",
                "doing": "Prints full metadata (author, email, date, commit message) along with unified patch diff for the latest commit.",
                "how": [
                    "Shows the exact additions (green `+`) and deletions (red `-`).",
                    "Can be used with any commit SHA or relative reference like `HEAD~3`."
                ],
                "watchout": "`git show` defaults to HEAD if no argument is passed."
            },
            {
                "title": "Part 2: Historical File Peeking Without Checkout",
                "code": "git show a1b2c3d:readme.txt",
                "doing": "Reads and prints file contents from an arbitrary historical commit without switching branches or altering local files.",
                "how": [
                    "Uses the syntax `<commit-hash>:<relative-path>`.",
                    "Streams the content directly from the object database to the console output."
                ],
                "watchout": "Never checkout an old commit just to read a single file — use `git show <sha>:<file>` instead!"
            },
            {
                "title": "Part 3: Low-Level Plumbing Inspection (git cat-file)",
                "code": "git cat-file -t a1b2c3d   # Shows object type: blob, tree, commit, or tag\ngit cat-file -p a1b2c3d   # Pretty-prints raw decompressed contents",
                "doing": "Peeks directly into the Git object store (`.git/objects/`) to inspect internal database structures.",
                "how": [
                    "`-t`: Reveals the internal object type: `blob` (data), `tree` (directory), `commit` (snapshot), `tag` (annotated pin).",
                    "`-p`: Pretty-prints the internal content (e.g. tree entries with SHA pointers)."
                ],
                "watchout": "Porcelain commands (`commit`, `add`) are high-level; plumbing commands (`cat-file`, `hash-object`) are low-level engine tools."
            }
        ],
        "challenge": {
            "prompt": "What plumbing command pretty-prints the raw contents of ANY object in the .git database?",
            "opts": [
                "A) git cat-file -p <sha>",
                "B) git dump-object <sha>",
                "C) git show-raw <sha>",
                "D) git unpack <sha>"
            ],
            "correct_opt": "A",
            "hint": "-p stands for pretty-print in git cat-file.",
            "praise": "Correct! 'git cat-file -p' is the master plumbing inspection tool.",
            "roast": "The standard low-level inspection tool is 'git cat-file -p <sha>'!"
        }
    },
    {
        "num": 10,
        "part": "B",
        "title": "Filtering Commit History by Author, Date & Path",
        "story": "In a big company with 50,000 commits, finding that one change made by Sarah last Tuesday is impossible with plain 'git log'. Git's search filters let you slice through history like a laser: filter by `--author`, filter by date window (`--since` / `--until`), or filter only commits that touched a specific file path!",
        "problem": "Filter project commit log by author name using '--author', specify a calendar range using '--since' and '--until', and filter by file path using '-- <path>'.",
        "commands": """# 1. Filter by author name or email
git log --author="Prajwal" --oneline

# 2. Filter by date window
git log --since="2026-01-01" --until="2026-11-14" --oneline

# 3. Filter commits that touched a specific file
git log --oneline -- dsa-lab/programs/lab03_stack_operations.c""",
        "blocks": [
            {
                "title": "Part 1: Filtering by Author Name & Email",
                "code": "git log --author=\"Prajwal\" --oneline",
                "doing": "Filters commit history to show only changes authored by a specific team member.",
                "how": [
                    "`--author`: Performs regex pattern matching on the author name and email fields.",
                    "Case-insensitive matching can be enabled with `-i`."
                ],
                "watchout": "Author is who wrote the code; Committer is who committed it (they can be different in open-source patches!)."
            },
            {
                "title": "Part 2: Time Window Filtering (--since and --until)",
                "code": "git log --since=\"2026-01-01\" --until=\"2026-11-14\" --oneline\ngit log --since=\"2 weeks ago\" --until=\"yesterday\"",
                "doing": "Slices commit history to display only commits authored within a specific calendar range.",
                "how": [
                    "Supports ISO dates (`2026-01-01`) or natural language expressions like `'3 days ago'` or `'last month'`.",
                    "`--after` and `--before` are exact aliases for `--since` and `--until`."
                ],
                "watchout": "Great for generating sprint summaries or weekly progress reports."
            },
            {
                "title": "Part 3: Path and Message Filtering (-- <path> and --grep)",
                "code": "git log --oneline -- dsa-lab/programs/lab03_stack_operations.c\ngit log --grep=\"fix\" --oneline",
                "doing": "Tracks commits that touched a specific file path or whose commit message matches a search term.",
                "how": [
                    "`-- <path>`: The `--` separator disambiguates filenames from branch names.",
                    "`--grep`: Searches inside the commit messages for keywords like bug numbers or feature names."
                ],
                "watchout": "Always place `--` before file paths so Git never confuses a filename with a branch name!"
            }
        ],
        "challenge": {
            "prompt": "Which flag filters Git commit history to display only commits by a specific person?",
            "opts": [
                "A) --user",
                "B) --committer-only",
                "C) --author=\"Name\"",
                "D) --by"
            ],
            "correct_opt": "C",
            "hint": "The flag is --author='Name'.",
            "praise": "Spot on! '--author' filters commits by the author string.",
            "roast": "The flag is '--author=\"Name\"'!"
        }
    },
    {
        "num": 11,
        "part": "B",
        "title": "Commit History Formatting & Formats",
        "story": "Standard 'git log' fills up your entire screen with just 3 commits. By using compact formatting flags, you can compress commits into clean 1-liners and draw colorful ASCII tree diagrams (`--graph`) showing where every branch split and merged!",
        "problem": "Display the last 5 commits using 'git log -n 5 --oneline', and inspect branch tips with 'git log --graph --oneline --decorate --all'.",
        "commands": """# 1. Display last 5 commits in compact one-line format
git log -n 5 --oneline

# 2. Display all branches with decoration tags and ASCII graph
git log --graph --oneline --decorate --all""",
        "blocks": [
            {
                "title": "Part 1: Compressing History with -n and --oneline",
                "code": "git log -n 5 --oneline",
                "doing": "Limits history output to the 5 most recent commits and condenses each commit to a single line.",
                "how": [
                    "`-n 5`: Restricts output length so your terminal isn't overwhelmed.",
                    "`--oneline`: Prints the 7-character abbreviated SHA hash and the subject line."
                ],
                "watchout": "Without `-n`, Git opens a pager (`less`); press `q` to exit the pager!"
            },
            {
                "title": "Part 2: Visual Branch Topology (--graph, --decorate, --all)",
                "code": "git log --graph --oneline --decorate --all",
                "doing": "Draws an ASCII visualization of all branching, merging, and release milestones across the entire project.",
                "how": [
                    "`--graph`: Renders ASCII branch lines (`* | / \\`).",
                    "`--decorate`: Displays badges for branch tips (`HEAD -> main`), remotes, and tags.",
                    "`--all`: Shows all branches in the repository, not just your currently active branch."
                ],
                "watchout": "This is the most powerful visualization command in Git — it shows the entire repo topology without needing GUI tools!"
            },
            {
                "title": "Part 3: Custom Formats and Git Aliases",
                "code": "git log --format=\"%h - %an (%cr) : %s\"\ngit config --global alias.lg \"log --graph --oneline --decorate --all\"",
                "doing": "Customizes commit print formatting and binds long commands to short shell aliases.",
                "how": [
                    "`--format`: Allows placeholders: `%h` (hash), `%an` (author), `%cr` (relative date), `%s` (subject).",
                    "`alias.lg`: Lets you type `git lg` instead of typing the whole long flag sequence."
                ],
                "watchout": "Aliases are saved in `~/.gitconfig` and work in every Git repository on your computer."
            }
        ],
        "challenge": {
            "prompt": "What does the '--oneline' flag do in 'git log'?",
            "opts": [
                "A) Displays the full 40-character SHA and full commit body text.",
                "B) Compresses each commit to a 7-character abbreviated hash and the subject line.",
                "C) Shows only commits made online via GitHub.",
                "D) Limits the output to 1 total commit."
            ],
            "correct_opt": "B",
            "hint": "oneline = 7-char SHA prefix + commit summary.",
            "praise": "Correct! It compresses commits to 7-char SHA + subject line.",
            "roast": "The '--oneline' flag outputs the 7-character abbreviated hash and the commit subject line!"
        }
    },
    {
        "num": 12,
        "part": "B",
        "title": "Undoing Changes Safely (Revert vs Reset)",
        "story": "Everyone makes mistakes: maybe you pushed buggy code, or committed files you didn't mean to. Git gives you two undo buttons: 'git reset' is like a local eraser (rewrites history by moving the branch pointer back), while 'git revert' is a polite public undo (creates a NEW commit that cancels the old changes without breaking team history)!",
        "problem": "Safely undo a published commit using 'git revert <commit-sha>', and understand the difference between 'reset --soft', 'reset --mixed', and 'reset --hard'.",
        "commands": """# 1. Safely undo a published commit (creates new inverse commit)
git revert <commit-sha> --no-edit

# 2. Local undo: keep changes in Staging Area
git reset --soft HEAD~1

# 3. Local undo: keep changes in Working Directory (Default)
git reset --mixed HEAD~1

# 4. Local undo: DISCARD all changes (Dangerous!)
git reset --hard HEAD~1""",
        "blocks": [
            {
                "title": "Part 1: Safe Public Undo with git revert",
                "code": "git revert <commit-sha> --no-edit",
                "doing": "Undoes a past commit safely by recording a brand new commit with inverted changes, safe for shared GitHub branches.",
                "how": [
                    "Calculates the opposite diff (pluses become minuses, minuses become pluses).",
                    "Commits the inversion as a forward-moving commit: 'Revert \"original message\"'.",
                    "Does NOT rewrite past history, preventing merge conflicts for teammates."
                ],
                "watchout": "If you already pushed to GitHub, ALWAYS use `revert`! Never use `reset` on shared branches."
            },
            {
                "title": "Part 2: The 3 Modes of git reset (Local Only)",
                "code": "git reset --soft HEAD~1   # Moves HEAD back; files stay staged in Index\ngit reset --mixed HEAD~1  # Moves HEAD back; files stay in Working Directory (Default)\ngit reset --hard HEAD~1   # OVERWRITES EVERYTHING! Discards all uncommitted changes",
                "doing": "Moves the branch pointer backwards for local cleanups, with 3 levels of aggression.",
                "how": [
                    "`--soft`: Gentle. Keeps all your code staged in the Index.",
                    "`--mixed`: Default. Unstages code but leaves files in your working directory.",
                    "`--hard`: Nuclear! Overwrites your files to match the old commit. Uncommitted work is permanently gone!"
                ],
                "watchout": "Be extremely cautious with `git reset --hard`! If you haven't committed your work, it is destroyed."
            },
            {
                "title": "Part 3: git reflog — The Safety Net",
                "code": "git reflog\n# Recover a seemingly 'lost' commit after an accidental reset --hard:\n# git reset --hard <reflog-sha>",
                "doing": "Provides the ultimate safety net by recording every single movement of HEAD, even discarded commits.",
                "how": [
                    "`git reflog`: Shows all recent HEAD locations (`HEAD@{0}`, `HEAD@{1}`).",
                    "Even if you ran `reset --hard`, the old commit is still in `.git/objects/` for at least 30 days!",
                    "You can restore your repo to that exact commit using the reflog SHA."
                ],
                "watchout": "Remember the Git rule: In Git, committed data is almost never truly lost — check `git reflog`!"
            }
        ],
        "challenge": {
            "prompt": "You already pushed a commit to the remote GitHub team repo. Which command MUST you use to undo it safely without breaking your teammates' copies?",
            "opts": [
                "A) git reset --hard HEAD~1 && git push --force",
                "B) git revert <commit-sha>",
                "C) git clean -fd",
                "D) Delete the .git directory"
            ],
            "correct_opt": "B",
            "hint": "Revert creates a new forward-moving undo commit without rewriting shared history.",
            "praise": "Golden rule of Git! Never force-push history rewrites on shared branches; always use revert.",
            "roast": "On shared branches, always use 'git revert' to avoid breaking everyone else's repository!"
        }
    }
]

