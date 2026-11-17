# pyright: reportMissingImports=false
"""
arcade.git.story — Git for Humans story mode, Viva Gauntlet, Disaster Recovery,
Command Arena, and Git Arcade menu.
"""
import time
import random

try:
    from arcade.core import (  # type: ignore
        Color, clear_screen, prompt_input, spinner, progress_bar,
        print_slow, anim_correct, anim_wrong,
    )
    from arcade.session import (  # type: ignore
        _record_concept_mastered, _unlock_badge,
        _show_session_header, BANNER, _SESSION, _save_to_local_db,
        _mark_experiment_done,
    )
    from arcade.git.questions import _run_step_checkpoint  # type: ignore
    from arcade.git.sandbox import mode_git_command_sandbox  # type: ignore
    from arcade.dialogues import print_dialogue  # type: ignore
except (ImportError, ValueError):
    from ..core import (  # type: ignore
        Color, clear_screen, prompt_input, spinner, progress_bar,
        print_slow, anim_correct, anim_wrong,
    )
    from ..session import (  # type: ignore
        _record_concept_mastered, _unlock_badge,
        _show_session_header, BANNER, _SESSION, _save_to_local_db,
        _mark_experiment_done,
    )
    from .questions import _run_step_checkpoint  # type: ignore
    from .sandbox import mode_git_command_sandbox  # type: ignore
    from ..dialogues import print_dialogue  # type: ignore

VIVA_QUESTIONS = [
    {
        "q": "What is the difference between 'git fetch' and 'git pull'?",
        "options": [
            "A) They are identical commands with different names.",
            "B) git fetch downloads remote changes but does NOT merge; git pull downloads AND merges.",
            "C) git fetch only works on GitHub; git pull works everywhere.",
            "D) git fetch merges automatically; git pull asks for confirmation first."
        ],
        "ans": "B",
        "tip": "git fetch is safe — it updates your remote tracking branches without touching your local files. git pull = fetch + merge in one step.",
        "praise": "Correct! Knowing this distinction helps you avoid surprise merges on important branches.",
        "roast": "Not quite. git fetch downloads changes but leaves your local branch untouched. git pull goes further and merges them in."
    },
    {
        "q": "You pushed a buggy commit directly to 'main' and teammates have already pulled it. What is the safest way to undo it?",
        "options": [
            "A) git reset --hard HEAD~1  then force push",
            "B) git revert <commit-id>",
            "C) Delete the repository and start fresh",
            "D) Manually edit the files and commit again without documenting it"
        ],
        "ans": "B",
        "tip": "git revert creates a new commit that undoes the changes — it does NOT rewrite history, so it is safe for shared branches.",
        "praise": "Exactly right. git revert is the go-to for undoing shared commits because it preserves the full history everyone else already has.",
        "roast": "git reset --hard + force push would rewrite history that your teammates already have — that breaks their repositories."
    },
    {
        "q": "You are halfway through a feature when an urgent bug is reported on 'main'. You cannot commit unfinished code. What do you do?",
        "options": [
            "A) git stash  — to save your current work temporarily",
            "B) git commit -m 'WIP do not review'  and push to main",
            "C) Copy all files to a backup folder manually",
            "D) git checkout main -f  which discards all your in-progress changes"
        ],
        "ans": "A",
        "tip": "git stash shelves your uncommitted changes and gives you a clean working tree so you can safely switch branches.",
        "praise": "Perfect. git stash is exactly the tool for this — your work is saved, your workspace is clean, and you can fix the bug.",
        "roast": "git stash is the right answer. It saves your in-progress work without committing it, so you can switch branches cleanly."
    },
    {
        "q": "How do you cherry-pick commits from commit A through commit B inclusive?",
        "options": [
            "A) git cherry-pick A..B",
            "B) git cherry-pick A^..B",
            "C) git cherry-pick --range A B",
            "D) git cherry-pick A B  (listing both SHA IDs separated by a space)"
        ],
        "ans": "B",
        "tip": "In Git range syntax, A..B excludes A itself. Using A^..B (caret before A) includes commit A in the range.",
        "praise": "Correct! The caret ^ is the key detail here. Without it you'd miss the first commit in the range.",
        "roast": "Close! A..B actually excludes commit A. You need A^..B so the range starts from A and goes through B inclusive."
    },
    {
        "q": "What does this command output? → git log --author=\"Alice\" --since=\"2024-01-01\"",
        "options": [
            "A) All commits across the entire repository regardless of author or date",
            "B) Deletes all of Alice's commits made after Jan 1, 2024",
            "C) Shows only commits made by Alice since January 1, 2024",
            "D) Changes the author of recent commits to Alice"
        ],
        "ans": "C",
        "tip": "git log supports powerful filters: --author filters by contributor, --since filters by date. Very useful for auditing or reviewing.",
        "praise": "Correct. This is a commonly used combination for reviewing a team member's recent contributions.",
        "roast": "git log only reads and displays history — it never modifies commits. --author and --since are filters that narrow down what is shown."
    },
    {
        "q": "What is the difference between a lightweight tag and an annotated tag?",
        "options": [
            "A) There is no functional difference — it is just a naming preference.",
            "B) Lightweight tags are simple commit pointers; annotated tags store author, date, and a message.",
            "C) Annotated tags can only be pushed to private repositories.",
            "D) Lightweight tags expire after 30 days."
        ],
        "ans": "B",
        "tip": "Use lightweight tags for temporary bookmarks. Use annotated tags (git tag -a) for official releases — they carry full metadata.",
        "praise": "Exactly right. For software releases, annotated tags are the standard because they include context about who tagged and why.",
        "roast": "Lightweight tags are essentially just named pointers to a commit. Annotated tags (-a flag) store a full object with author, date, and message."
    },
    {
        "q": "You are on branch 'feature'. Running 'git merge main' does what?",
        "options": [
            "A) Pushes your feature branch commits to main",
            "B) Deletes your feature branch",
            "C) Brings the latest commits from main into your current feature branch",
            "D) Resets your feature branch to match main exactly"
        ],
        "ans": "C",
        "tip": "Merge direction matters: you're ON feature, merging FROM main. So main's changes come INTO feature — keeping feature up to date.",
        "praise": "Correct. This is a common workflow — keeping your feature branch updated with what others have merged into main.",
        "roast": "The merge target is always your CURRENT branch. Since you're on feature, main's commits flow INTO feature, not the other way around."
    },
    {
        "q": "What is the primary role of the Git staging area (also known as the 'index')?",
        "options": [
            "A) It is a temporary cache that gets wiped when you restart your terminal.",
            "B) An intermediate holding area where you prepare and curate exactly what changes go into the next commit.",
            "C) A cloud backup hosted on GitHub servers.",
            "D) A folder where Git stores deleted files."
        ],
        "ans": "B",
        "tip": "The staging area lets you split your working changes into clean, focused commits rather than saving everything at once.",
        "praise": "Exactly right! The staging area gives you surgical control over what goes into each snapshot.",
        "roast": "The staging area (index) is where Git holds changes that are queued up for the next commit (via git add)."
    },
    {
        "q": "What does 'HEAD' represent in a Git repository?",
        "options": [
            "A) The very first commit ever made when the repo was created.",
            "B) The server address of the remote repository on GitHub.",
            "C) A pointer to the current active branch or commit you are currently looking at.",
            "D) The user account currently logged into Git."
        ],
        "ans": "C",
        "tip": "HEAD is your current location marker in Git. When you switch branches or check out a commit, HEAD moves with you.",
        "praise": "Spot on! HEAD is essentially Git's 'You are here' bookmark.",
        "roast": "HEAD points to your current checkout location — usually the tip of your active branch."
    },
    {
        "q": "What does it mean when Git says you are in a 'detached HEAD' state?",
        "options": [
            "A) You have checked out a specific commit or tag directly, rather than a named branch.",
            "B) Your Git configuration file has been deleted.",
            "C) The remote repository has lost internet connection.",
            "D) Your computer does not have permission to commit."
        ],
        "ans": "A",
        "tip": "In detached HEAD, commits you make aren't attached to any branch. To keep them, create a branch: git switch -c new-branch.",
        "praise": "Correct! Detached HEAD happens when you checkout a specific commit SHA or tag. Create a branch to save new work.",
        "roast": "Detached HEAD just means HEAD points directly to a commit SHA rather than to a branch name."
    },
    {
        "q": "What is the key difference between 'git merge' and 'git rebase'?",
        "options": [
            "A) merge only works on Windows; rebase only works on Linux.",
            "B) merge preserves original history with a merge commit; rebase rewrites commits linearly on top of the target branch.",
            "C) merge deletes the source branch; rebase keeps both branches untouched.",
            "D) There is no difference; they are exact synonyms."
        ],
        "ans": "B",
        "tip": "Rebase produces a clean linear commit graph, but rewrites commit SHAs. Never rebase public shared branches!",
        "praise": "Clean, accurate explanation! Rebase creates a linear history by re-applying commits atop the target branch.",
        "roast": "Merge ties branches together with a merge commit; rebase re-plays your branch's commits on top of the other branch."
    },
    {
        "q": "What do the markers '<<<<<<<', '=======', and '>>>>>>>' inside a file indicate?",
        "options": [
            "A) Syntax errors generated by the Python interpreter.",
            "B) Merge conflict markers inserted by Git showing conflicting changes from two branches.",
            "C) Markdown formatting for block quotes and tables.",
            "D) Git security certificates for encrypted commits."
        ],
        "ans": "B",
        "tip": "When a merge conflict occurs, Git inserts these markers so you can manually inspect both versions and choose the right code.",
        "praise": "Correct! These are Git's conflict markers. Edit the code, remove the markers, stage, and commit to resolve.",
        "roast": "Those are merge conflict markers! Code between <<<<<<< and ======= is yours; code between ======= and >>>>>>> is theirs."
    },
    {
        "q": "What does running 'git commit --amend' allow you to do?",
        "options": [
            "A) Delete the entire commit history and restart.",
            "B) Combine all branches into one single branch.",
            "C) Update the most recent commit by adding staged changes or editing the commit message.",
            "D) Push commits directly to production without code review."
        ],
        "ans": "C",
        "tip": "Amend is great for fixing typos or adding a forgotten file to your latest local commit before pushing.",
        "praise": "Perfect. git commit --amend replaces the tip of your branch with a revised commit containing your updates.",
        "roast": "git commit --amend modifies your most recent commit — perfect for catching a forgotten file or fixing a typo."
    },
    {
        "q": "What is 'git bisect' primarily used for?",
        "options": [
            "A) Using binary search across commit history to quickly find the exact commit that introduced a bug.",
            "B) Splitting a single large commit into two equal halves.",
            "C) Converting a Git repository into a Subversion (SVN) repository.",
            "D) Compressing git files to save disk space."
        ],
        "ans": "A",
        "tip": "git bisect cuts debugging time from hours to minutes by automating binary search between a known good and bad commit.",
        "praise": "Senior-level Git knowledge! git bisect is one of Git's most potent debugging superpowers.",
        "roast": "git bisect uses binary search through history to isolate which commit caused a bug."
    },
    {
        "q": "Why is running 'git push --force' dangerous on shared branches like 'main'?",
        "options": [
            "A) It permanently disables GitHub Actions CI/CD pipelines.",
            "B) It costs money per forced gigabyte on cloud hosts.",
            "C) It overwrites remote history, potentially erasing teammates' pushed commits and corrupting their local trees.",
            "D) It converts all LF line endings to CRLF automatically."
        ],
        "ans": "C",
        "tip": "Force pushing replaces remote history with your local history. If teammates pushed work in between, their work is wiped out.",
        "praise": "Exactly right. Use --force-with-lease if you ever must force-push, and never do it on shared branches!",
        "roast": "Force push overwrites remote history. If teammates pulled or pushed in between, you risk deleting their work."
    },
    {
        "q": "What is the primary difference between 'git pull' and 'git pull --rebase'?",
        "options": [
            "A) git pull --rebase downloads faster by compressing history.",
            "B) git pull merges upstream commits with a merge commit; git pull --rebase replays your local unpushed commits on top of upstream for a linear history.",
            "C) git pull --rebase deletes local unpushed commits.",
            "D) git pull --rebase only works when connected over SSH."
        ],
        "ans": "B",
        "tip": "Many professional teams prefer 'git pull --rebase' because it prevents noisy 'Merge branch main into feature' clutter commits.",
        "praise": "Outstanding! Rebasing during pull keeps your Git log perfectly linear and clean.",
        "roast": "git pull --rebase avoids creating merge commits by replaying your local commits atop the updated remote tracking branch."
    },
    {
        "q": "What does 'git merge --squash feature' do when run on the main branch?",
        "options": [
            "A) Compresses the Git database into a single zip file.",
            "B) Deletes the feature branch and aborts all work.",
            "C) Combines all commits from the feature branch into a single staged change without automatically committing.",
            "D) Automatically force-pushes all feature commits directly to production."
        ],
        "ans": "C",
        "tip": "Squash merge is popular for feature branches with lots of messy WIP commits — it condenses them into one clean commit on main.",
        "praise": "Exactly right. Squash merges all branch modifications into the staging area, letting you write a clean single commit message.",
        "roast": "--squash condenses all the changes of a branch into your staging area so you can make one single cohesive commit."
    },
    {
        "q": "What problem does 'git worktree' solve for developers?",
        "options": [
            "A) It automatically designs UI wireframes from markdown.",
            "B) It allows you to check out and work on multiple branches simultaneously in separate directories without switching or stashing.",
            "C) It replaces GitHub by hosting repositories on peer-to-peer torrent networks.",
            "D) It converts Git repositories into Subversion repositories."
        ],
        "ans": "B",
        "tip": "With git worktree, you never have to stash dirty code just to review a PR or do a hotfix — you open a second folder on that branch instantly.",
        "praise": "Pro-tier knowledge! Worktrees eliminate the need to duplicate clone repos or constantly stash work to switch branches.",
        "roast": "git worktree allows you to link multiple working trees to the same repository database, letting you check out multiple branches at once."
    },
    {
        "q": "In Git 2.23+, what is the difference between 'git restore <file>' and 'git restore --staged <file>'?",
        "options": [
            "A) git restore <file> discards unstaged working tree changes; --staged unstages a file while keeping disk modifications intact.",
            "B) --staged deletes the file from disk permanently.",
            "C) They do the exact same thing.",
            "D) git restore only works on files under 1MB."
        ],
        "ans": "A",
        "tip": "Git 2.23 introduced 'git restore' to replace the confusingly overloaded 'git checkout -- <file>'.",
        "praise": "Clean and precise! Modern Git separates branch switching ('git switch') from file restoration ('git restore').",
        "roast": "git restore <file> resets your working copy. Adding --staged targets the staging area (index) without altering the file on disk."
    },
    {
        "q": "What does running 'git clean -fd' do?",
        "options": [
            "A) Formats all Python code using the Black formatter.",
            "B) Forcefully deletes all untracked files and directories from your working tree.",
            "C) Deletes all merged remote branches on GitHub.",
            "D) Fixes corrupted git commit objects."
        ],
        "ans": "B",
        "tip": "Always run 'git clean -nd' (dry-run) first to preview what would be deleted before running the destructive -f flag!",
        "praise": "Correct! -f forces deletion and -d includes untracked directories.",
        "roast": "git clean removes untracked files. -f is force, and -d includes untracked directories. Use with caution!"
    },
    {
        "q": "How can you see which developer last changed each line of 'server.py' between lines 50 and 80?",
        "options": [
            "A) git log -n 1 server.py",
            "B) git diff server.py",
            "C) git blame -L 50,80 server.py",
            "D) git show server.py:50-80"
        ],
        "ans": "C",
        "tip": "git blame annotates each line in a file with the commit hash, author name, and date it was last modified.",
        "praise": "Spot on! git blame with -L line ranges is essential for code archaeology and finding context behind changes.",
        "roast": "git blame with -L <start>,<end> shows line-by-line author and commit info for that specific range."
    },
    {
        "q": "In an interactive rebase ('git rebase -i'), what is the difference between 'squash' and 'fixup'?",
        "options": [
            "A) squash deletes the commit; fixup renames it.",
            "B) squash combines the commit and prompts to merge both messages; fixup combines the commit but discards this commit's message.",
            "C) fixup only works on test files; squash works on code files.",
            "D) There is no functional difference."
        ],
        "ans": "B",
        "tip": "Use 'fixup' when fixing a typo or small lint issue — you don't need 'fix typo' preserved in the final commit message.",
        "praise": "Expert answer! fixup is the cleanest way to absorb minor bugfix patches into previous commits silently.",
        "roast": "Both combine into the prior commit, but fixup automatically discards the commit message, keeping history cleaner."
    },
    {
        "q": "Where do client-side Git hooks reside in a repository, and how are they executed?",
        "options": [
            "A) In the cloud on GitHub Actions servers.",
            "B) Inside the .git/hooks/ directory as executable scripts triggered by events like pre-commit or pre-push.",
            "C) In package.json under scripts.",
            "D) In a global system folder managed by the operating system kernel."
        ],
        "ans": "B",
        "tip": "Git hooks are client-side scripts (bash, python, node) that run locally before actions like committing or pushing.",
        "praise": "Correct! .git/hooks holds local hook scripts that automate linting, tests, and commit message validation.",
        "roast": "Git hooks live in .git/hooks/. They are local scripts triggered before or after git operations."
    },
    {
        "q": "What is a shallow clone ('git clone --depth 1 <url>') and why is it heavily used in CI/CD pipelines?",
        "options": [
            "A) It only clones README files to save memory.",
            "B) It downloads only the latest single commit snapshot without full history, saving bandwidth and build time.",
            "C) It encrypts the repository with SSL certificates.",
            "D) It only clones branches created in the last 24 hours."
        ],
        "ans": "B",
        "tip": "CI/CD runners only need to build and test the latest code — downloading 10 years of commit history wastes time and bandwidth.",
        "praise": "Exact understanding! Shallow clones drastically accelerate automated build and test pipelines.",
        "roast": "--depth 1 truncates history to just the latest commit, minimizing transfer size for automated build environments."
    },
    {
        "q": "How does Git verify data integrity and uniquely identify every blob, tree, and commit object?",
        "options": [
            "A) By assigning an auto-incrementing integer ID (1, 2, 3...).",
            "B) By recording the file's Windows creation timestamp.",
            "C) By computing a cryptographic hash (SHA-1 or SHA-256) of the object's type, size, and content.",
            "D) By asking the GitHub server to assign an ID over HTTP."
        ],
        "ans": "C",
        "tip": "This is why Git is called 'content-addressable storage' — if a single byte in a file changes, its hash changes completely.",
        "praise": "Master-level computer science comprehension! Git's object model guarantees that history cannot be silently tampered with.",
        "roast": "Git uses cryptographic hashing (SHA) of object headers and content. Any modification produces a completely different hash."
    }
]

DISASTER_SCENARIOS = [
    {
        "title": "You committed directly to main instead of your feature branch",
        "story": "You were heads-down coding and forgot to switch branches. You just ran\n  'git commit -m \"add payment feature\"' — and the commit landed on main.\n  Your team has a rule: no direct commits to main.",
        "prompt": "You haven't pushed yet. What is the cleanest way to move that commit to your feature branch and undo it on main?",
        "choices": [
            "git checkout feature && git cherry-pick main && git checkout main && git reset --hard HEAD~1",
            "git reset --hard HEAD~1  (just delete the commit on main, losing your work)",
            "git push -f origin main  (force push and hope nobody notices)",
            "git revert HEAD  (create an undo commit on main, then manually copy code to feature)"
        ],
        "ans_idx": 1,
        "reaction": "Correct! Cherry-pick moves the commit to feature, then reset --hard removes it from main cleanly — since it hasn't been pushed, rewriting local history is safe here."
    },
    {
        "title": "You accidentally staged your .env file (it has real API keys)",
        "story": "You ran 'git add .' and then noticed '.env' is now staged.\n  It contains your database password and API tokens. It has NOT been committed yet.\n  You need to unstage it without losing the file.",
        "prompt": "Which command removes '.env' from the staging area but keeps the file on disk?",
        "choices": [
            "rm -f .env  (deletes the file entirely — worst option)",
            "git restore --staged .env",
            "git commit -m 'oops'  (commits it anyway)",
            "git push origin main  (uploads the secret to GitHub)"
        ],
        "ans_idx": 2,
        "reaction": "Correct! git restore --staged removes the file from staging without touching it on disk. Next step: add .env to your .gitignore file!"
    },
    {
        "title": "You ran 'git reset --hard' and your last 3 commits seem gone",
        "story": "You ran 'git reset --hard HEAD~3' trying to undo 3 commits.\n  But you actually needed those commits — they had a week of work.\n  'git log' doesn't show them anymore. Panic sets in.",
        "prompt": "Which Git tool records every movement of HEAD and can recover the lost commit SHA?",
        "choices": [
            "git log  (only shows the current reachable history — the commits are gone from here)",
            "git status  (shows working directory state, not lost commits)",
            "git reflog  (records all HEAD movements including resets — your commits are still here)",
            "git stash list  (shows stashed changes, not reset commits)"
        ],
        "ans_idx": 3,
        "reaction": "Correct! git reflog is your safety net. Run it, find the SHA of your lost commit, then run 'git reset --hard <that-SHA>' to recover everything."
    },
    {
        "title": "Merge conflict in server.py halts your work",
        "story": "You ran 'git merge feature' into 'main'. Git stopped with:\n  'CONFLICT (content): Merge conflict in server.py. Automatic merge failed.'\n  Git placed conflict markers inside server.py.",
        "prompt": "After opening server.py, choosing the right code, and removing the conflict markers, what do you run to finish?",
        "choices": [
            "git add server.py && git commit -m \"resolve merge conflict\"",
            "git reset --hard  (aborts the merge and discards all progress)",
            "git push origin main  (pushes the conflict markers to production)",
            "rm server.py  (deletes the conflicting file)"
        ],
        "ans_idx": 1,
        "reaction": "Correct! Once conflict markers are resolved manually, staging the resolved file with 'git add' and running 'git commit' concludes the merge cleanly."
    },
    {
        "title": "Accidentally committed a 500MB dataset zip file locally",
        "story": "You just ran 'git commit -m \"add data\"' and realized you accidentally included a 500MB 'archive.zip'!\n  GitHub rejects any push containing files over 100MB. You haven't pushed yet.",
        "prompt": "How do you remove archive.zip from the latest commit while keeping the file on your local disk?",
        "choices": [
            "git rm --cached archive.zip && git commit --amend --no-edit",
            "git push --force origin main  (attempt to force upload the 500MB file)",
            "git revert HEAD  (revert creates a new commit but keeps the 500MB file in Git history)",
            "Delete your entire repository folder from your laptop"
        ],
        "ans_idx": 1,
        "reaction": "Correct! 'git rm --cached' unstages the file without deleting it from disk, and '--amend' rewires the latest commit so the giant file is never saved in Git history."
    },
    {
        "title": "Git pull rejected: local uncommitted changes would be overwritten",
        "story": "You modified 'api.py' and have not committed it yet. You ran 'git pull'\n  to grab your teammate's new endpoints, but Git aborted with:\n  'error: Your local changes to the following files would be overwritten by merge: api.py'",
        "prompt": "How do you download your teammate's updates safely without losing your local in-progress code?",
        "choices": [
            "git stash && git pull && git stash pop",
            "git push --force origin main  (force push your uncommitted code)",
            "git reset --hard HEAD  (wipe all your uncommitted code to let the pull succeed)",
            "rm api.py && git pull  (delete the file and start your work over)"
        ],
        "ans_idx": 1,
        "reaction": "Correct! Stashing temporarily shelters your uncommitted modifications. The pull finishes cleanly, and 'git stash pop' puts your changes back on top!"
    },
    {
        "title": "Committed with the wrong author email on your laptop",
        "story": "You just made your first commit in the company repo, but realized your Git author config\n  was still set to your personal gaming email: 'gamer99@gmail.com'. You haven't pushed yet.",
        "prompt": "How do you correct the author name and email on your latest local commit before pushing?",
        "choices": [
            "git commit --amend --author=\"Jane Doe <jane@company.com>\" --no-edit",
            "git push --force origin main  (push it anyway and change it on GitHub web UI)",
            "Delete your GitHub account and create a new one",
            "git revert HEAD  (creates a second commit with the same wrong email)"
        ],
        "ans_idx": 1,
        "reaction": "Correct! 'git commit --amend --author=...' cleanly updates the authorship metadata of the tip commit without modifying its code or message."
    },
    {
        "title": "Hit a merge conflict midway through an interactive rebase",
        "story": "You ran 'git rebase -i main' to tidy up your feature branch. On commit 2 of 4,\n  Git stopped with a conflict in 'models.py'. You opened the file, removed the markers,\n  and verified the code is correct.",
        "prompt": "After staging the resolved 'models.py' with 'git add models.py', which command resumes the rebase?",
        "choices": [
            "git rebase --continue",
            "git commit -m \"fix conflict\"  (never run git commit during an active rebase!)",
            "git rebase --abort  (aborts the rebase and wipes all your rebase progress)",
            "git push origin feature"
        ],
        "ans_idx": 1,
        "reaction": "Correct! During a rebase, never run 'git commit'! Stage your resolved files with 'git add' and run 'git rebase --continue' to apply the remaining commits."
    }
]

LAB_EXPERIMENTS = [
    ("Step 01", "Setting Up and Basic Commands", "git init\necho 'Hello' > file.txt\ngit add file.txt\ngit commit -m 'Initial commit'"),
    ("Step 02", "Creating and Managing Branches", "git checkout -b feature-branch\n# make changes\ngit checkout master\ngit merge feature-branch"),
    ("Step 03", "Stashing Changes", "git stash save 'WIP'\ngit checkout master\n# do urgent work\ngit checkout feature-branch\ngit stash apply"),
    ("Step 04", "Cloning a Remote Repository", "git clone https://github.com/user/repo.git"),
    ("Step 05", "Fetch and Rebase", "git checkout main\ngit fetch origin\ngit rebase origin/main"),
    ("Step 06", "Merge with Custom Commit Message", "git checkout master\ngit merge feature-branch -m 'Custom merge message'"),
    ("Step 07", "Git Tags and Releases", "git tag v1.0\n# or annotated:\ngit tag -a v1.0 -m 'Release v1.0'"),
    ("Step 08", "Cherry-Picking a Range of Commits", "git cherry-pick start_commit^..end_commit"),
    ("Step 09", "Inspecting a Specific Commit", "git show <commit-id>\n# or summary only:\ngit log -n 1 <commit-id>"),
    ("Step 10", "Filtering by Author and Date Range", "git log --author='JohnDoe' --since='2023-01-01' --until='2023-12-31'"),
    ("Step 11", "Display Last 5 Commits", "git log -n 5 --oneline"),
    ("Step 12", "Undoing Changes via Revert", "git revert <commit-id> --no-edit")
]

# ----------------- GAME MODES -----------------

def mode_viva_gauntlet():
    clear_screen()
    print(f"{Color.CYAN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║   🎓 MODE 3: GIT LAB VIVA PREP & CONCEPTUAL Q&A (1BCSL307A)       ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_dialogue("git")
    print_slow("Explore real examiner questions at your own pace with Socratic hints and clear takeaways.\n", 0.015, Color.CYAN)
    
    score = 0
    questions = list(VIVA_QUESTIONS)
    random.shuffle(questions)

    total_viva = min(10, len(questions))
    for i, item in enumerate(questions[:total_viva], 1):
        print(f"\n{Color.BOLD}{Color.WHITE}─── QUESTION {i}/{total_viva} | Concepts Mastered: {score} ───{Color.RESET}")
        print_slow(f"\n{Color.CYAN}{item['q']}{Color.RESET}", 0.015)
        print()
        for opt in item["options"]:
            print(f"  {Color.YELLOW}{opt}{Color.RESET}")
        
        attempt = 1
        solved = False
        while attempt <= 2 and not solved:
            prompt_str = f"\n{Color.BOLD}Your Answer [A / B / C / D] (or 'H' for Clue, 0 to Exit): {Color.RESET}" if attempt == 1 else f"\n{Color.BOLD}Second Try [A / B / C / D]: {Color.RESET}"
            choice = prompt_input(prompt_str).strip().upper()
            if choice in ["0", "MENU", "HOME", "Q", "EXIT"]:
                print(f"\n{Color.YELLOW}🏠 Returning to Main Menu...{Color.RESET}\n")
                time.sleep(0.5)
                return
            if choice == "H":
                print(f"  {Color.YELLOW}💡 Clue: {item['tip']}{Color.RESET}")
                continue
            if choice not in ["A", "B", "C", "D"]:
                print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")
                continue

            if choice == item["ans"]:
                solved = True
                anim_correct()
                _record_concept_mastered("git viva")
                score += 1
                if attempt == 1:
                    print(f"\n{Color.GREEN}{Color.BOLD}✔ CORRECT! {item['praise']}{Color.RESET}")
                else:
                    print(f"\n{Color.GREEN}{Color.BOLD}🎉 Excellent recovery buddy! You nailed it! ❤️{Color.RESET}")
            else:
                anim_wrong()
                if attempt == 1:
                    print(f"\n{Color.YELLOW}🌱 Not quite buddy! {item['roast']}{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {item['tip']}{Color.RESET}")
                    attempt += 1
                else:
                    print(f"\n{Color.MAGENTA}🤝 No worries buddy! The correct answer is [{item['ans']}].{Color.RESET}")
                    attempt += 1
        
        print(f"\n{Color.DIM}💡 Key Examiner Takeaway: {item['tip']}{Color.RESET}")
        prompt_input(f"\n{Color.DIM}Press Enter for next question...{Color.RESET}")

    print(f"\n{Color.BOLD}{Color.MAGENTA}═══════════════════════════════════════════════════")
    print(f"   🎉 Viva Practice Complete! Mastered: {score}/{total_viva} Concepts")
    print("   🏆 Great job! You navigated tricky situations and learned how Git thinks!")
    print(f"═══════════════════════════════════════════════════{Color.RESET}\n")
    prompt_input(f"{Color.DIM}Press Enter to return to main menu...{Color.RESET}")

def mode_disaster_recovery():
    clear_screen()
    print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║           🚨 MODE 4: REAL-WORLD GIT PROBLEM SOLVER                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print_slow("These are problems that actually happen to developers every day.", 0.015, Color.CYAN)
    print_slow("Read the situation carefully and pick the right Git command to fix it.\n", 0.015)

    score = 0
    scenarios = list(DISASTER_SCENARIOS)
    random.shuffle(scenarios)
    total_scenarios = len(scenarios)
    for i, scenario in enumerate(scenarios, 1):
        clear_screen()
        print(f"{Color.RED}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║           🚨 MODE 4: REAL-WORLD GIT PROBLEM SOLVER                 ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print(f"{Color.BOLD}{Color.YELLOW}── SCENARIO {i}/{total_scenarios} ──────────────────────────────────────────────────{Color.RESET}")
        print(f"\n{Color.BOLD}{Color.WHITE}{scenario['title']}{Color.RESET}\n")
        print_slow(scenario['story'], 0.013, Color.WHITE)
        print(f"\n{Color.CYAN}{Color.BOLD}What do you do?{Color.RESET}\n  {scenario['prompt']}\n")

        for idx, ch in enumerate(scenario["choices"], 1):
            print(f"  {Color.YELLOW}[{idx}]{Color.RESET} {ch}")

        while True:
            raw_pick = prompt_input(f"\n{Color.BOLD}Your answer [1 - {len(scenario['choices'])}] (or '0' for Menu): {Color.RESET}").strip().lower()
            if raw_pick in ["0", "menu", "home", "q", "exit"]:
                print(f"\n{Color.YELLOW}🏠 Returning to Main Menu...{Color.RESET}\n")
                time.sleep(0.5)
                return
            try:
                pick = int(raw_pick)
                if 1 <= pick <= len(scenario["choices"]):
                    break
            except ValueError:
                pass
            print(f"{Color.RED}Enter a number from 1 to {len(scenario['choices'])} (or '0' for Menu).{Color.RESET}")

        spinner("Simulating emergency command execution in production", duration=0.6, color=Color.RED)

        if pick == scenario["ans_idx"]:
            anim_correct()
            _record_concept_mastered("git disaster averted")
            _unlock_badge("git_recovery")
            score += 150
            print(f"\n{Color.GREEN}{Color.BOLD}✅ DISASTER AVERTED! Correct recovery strategy.{Color.RESET}")
            print(f"{Color.GREEN}{scenario['reaction']}{Color.RESET}\n")
        else:
            anim_wrong()
            correct_choice = scenario["choices"][scenario["ans_idx"] - 1]
            print(f"\n{Color.RED}{Color.BOLD}❌ Not quite. The right answer was [{scenario['ans_idx']}]:{Color.RESET}")
            print(f"   {Color.WHITE}{correct_choice}{Color.RESET}")
            print(f"\n{Color.DIM}{scenario['reaction']}{Color.RESET}\n")
        time.sleep(1.5)

    max_scenarios = total_scenarios * 150
    print(f"\n{Color.BOLD}{Color.MAGENTA}═══════════════════════════════════════════════════")
    print(f"   Problem Solver Complete! Score: {score}/{max_scenarios}")
    if score >= max_scenarios * 0.8:
        print("   ✅ Excellent! You handle real Git emergencies with confidence.")
    elif score >= max_scenarios * 0.5:
        print("   👍 Good job! Review the ones you missed to build confidence.")
    else:
        print("   📖 Check the GIT_COMMANDS.md cheatsheet to review these scenarios.")
    print(f"═══════════════════════════════════════════════════{Color.RESET}\n")
    prompt_input(f"{Color.DIM}Press Enter to return to main menu...{Color.RESET}")

def mode_vtu_cheatbook():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║          📚 MODE 5: 12-STEP PRACTICAL LAB & WORKFLOW CHEATBOOK      ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    print("Select any step to view the exact problem, commands & output:\n")

    for idx, (step_code, name, _) in enumerate(LAB_EXPERIMENTS, 1):
        print(f"  {Color.YELLOW}[{idx:2d}] {step_code}: {name}{Color.RESET}")

    print(f"\n  {Color.CYAN}[ 0] Return to Main Menu{Color.RESET}")

    while True:
        try:
            choice = int(prompt_input(f"\n{Color.BOLD}Enter Step [1 - 12] or 0 to exit: {Color.RESET}").strip())
            if choice == 0:
                return
            if 1 <= choice <= 12:
                step_code, name, code = LAB_EXPERIMENTS[choice - 1]
                exp_id = f"GIT-{choice}"
                _mark_experiment_done(exp_id)
                print(f"\n{Color.GREEN}{Color.BOLD}═════════════════════════════════════════════════════")
                print(f"📖 {step_code}: {name}  {Color.YELLOW}✔ [Progress Saved]{Color.RESET}")
                print(f"═════════════════════════════════════════════════════{Color.RESET}")
                print(f"{Color.WHITE}{code}{Color.RESET}")
                print(f"{Color.GREEN}═════════════════════════════════════════════════════{Color.RESET}")
        except ValueError:
            pass

def mode_git_internals():
    while True:
        clear_screen()
        print(f"{Color.MAGENTA}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║      🧬 MODE 6: GIT INTERNALS & ARCHITECTURE MASTERCLASS           ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print_slow("Want to truly understand Git like a core engineer? Look inside the .git engine.\n", 0.012, Color.CYAN)
        print(f"{Color.BOLD}EXPLORE THE GIT ENGINE:{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1] 📁 Anatomy of the .git Directory (What lives inside?){Color.RESET}")
        print(f"  {Color.GREEN}[2] 📦 The 4 Core Objects (Blobs, Trees, Commits, Tags){Color.RESET}")
        print(f"  {Color.CYAN}[3] 🌿 The Truth About Branches (Why they are only 41 bytes!){Color.RESET}")
        print(f"  {Color.RED}[4] 🕸️ Directed Acyclic Graph (DAG) & Content-Addressable Hashing{Color.RESET}")
        print(f"  {Color.BLUE}[5] 🛠️ Plumbing vs Porcelain Commands (git cat-file & hash-object){Color.RESET}")
        print(f"  {Color.MAGENTA}[6] 🎯 Quick Knowledge Check (3 Internals Questions){Color.RESET}")
        print(f"  {Color.WHITE}[0] 🏠 Return to Main Menu{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select a topic [1 - 6] or 0: {Color.RESET}").strip()
        if choice in ["0", "menu", "home", "exit", "q"]:
            return

        if choice == "1":
            clear_screen()
            print(f"{Color.YELLOW}{Color.BOLD}── 1. Anatomy of the hidden .git Directory ──────────────────────────{Color.RESET}\n")
            print("""When you run 'git init', Git creates a hidden '.git' folder. Here is what's inside:

  .git/
  ├── HEAD            -> Points to the current branch ref (e.g., ref: refs/heads/main)
  ├── config          -> Repository-specific configuration (remotes, user overrides)
  ├── description     -> Used mainly by GitWeb
  ├── hooks/          -> Client-side and server-side executable hook scripts
  ├── info/           -> Global excludes file (info/exclude acts like private .gitignore)
  ├── objects/        -> THE CONTENT DATABASE: all compressed blobs, trees, commits
  ├── refs/
  │   ├── heads/      -> Pointers to local branches (each file holds 1 commit hash!)
  │   ├── remotes/    -> Pointers to remote tracking branches (origin/main)
  │   └── tags/       -> Pointers to release tags
  └── index           -> The binary Staging Area (cache of what will go into next commit)

Every single branch, commit, and file in your repository lives inside this folder!""")
            prompt_input(f"\n{Color.DIM}Press Enter to return...{Color.RESET}")

        elif choice == "2":
            clear_screen()
            print(f"{Color.GREEN}{Color.BOLD}── 2. The 4 Core Object Types ────────────────────────────────────────{Color.RESET}\n")
            print("""Git stores all data using 4 fundamental object types inside .git/objects/:

  1. 📄 BLOB (Binary Large Object):
     - Stores only the raw file contents (compressed with zlib).
     - Does NOT store the filename, timestamp, or directory location.
     - Two identical files with different names share the EXACT SAME blob SHA!

  2. 🌳 TREE (Directory Listing):
     - Represents a folder.
     - Maps filenames and file permissions (100644 for regular, 100755 for executable)
       to their corresponding Blob or sub-Tree hashes.

  3. 📦 COMMIT (Snapshot & Metadata):
     - Points to a single root Tree (the entire project snapshot).
     - Points to parent Commit SHA(s) (forming history).
     - Records author name, email, timestamp, and commit message.

  4. 🏷️ ANNOTATED TAG:
     - A permanent pointer to a commit object containing tagger metadata, date,
       and optional cryptographic GPG signature.""")
            prompt_input(f"\n{Color.DIM}Press Enter to return...{Color.RESET}")

        elif choice == "3":
            clear_screen()
            print(f"{Color.CYAN}{Color.BOLD}── 3. The Truth About Branches ──────────────────────────────────────{Color.RESET}\n")
            print("""Most developers think creating a branch copies the entire project. IT DOES NOT!

In Git, a branch is literally just a 41-byte text file on your hard drive!
Take a look inside:

  $ cat .git/refs/heads/main
  4a8b1c9e8d2f10b7a6c5d4e3f2a1b0c9d8e7f6a5

That's it! 40 hexadecimal characters representing the commit hash, plus a newline character.
When you run 'git checkout -b new-feature':
  - Git creates a new 41-byte file '.git/refs/heads/new-feature' with that same SHA.
  - Git updates '.git/HEAD' to say: 'ref: refs/heads/new-feature'.
  - Time taken: less than 1 millisecond. Zero extra disk space used for files!""")
            prompt_input(f"\n{Color.DIM}Press Enter to return...{Color.RESET}")

        elif choice == "4":
            clear_screen()
            print(f"{Color.RED}{Color.BOLD}── 4. The Directed Acyclic Graph (DAG) ──────────────────────────────{Color.RESET}\n")
            print("""Git commits form a Directed Acyclic Graph (DAG):
  - Directed: Each commit points strictly in one direction: BACKWARDS to its parent!
  - Acyclic: History cannot loop back on itself.
  - Graph: Nodes (commits) connected by edges (parent references).

Visualizing the DAG:

  Commit C1 (Initial)  <--  Commit C2 (Feature A)  <--  Commit C3 (HEAD -> main)
      ▲
      │
      └───────────────────── Commit C4 (Feature B)  <--  Commit C5 (HEAD -> dev)

When you merge 'dev' into 'main', Git creates a Merge Commit (C6) with TWO parents:
  C6 points to both C3 AND C5!

Because every commit SHA is a SHA-1/SHA-256 hash of its content AND its parent SHA,
you cannot change past history without breaking every single subsequent commit hash!""")
            prompt_input(f"\n{Color.DIM}Press Enter to return...{Color.RESET}")

        elif choice == "5":
            clear_screen()
            print(f"{Color.BLUE}{Color.BOLD}── 5. Plumbing vs Porcelain Commands ─────────────────────────────────{Color.RESET}\n")
            print("""Git commands are divided into two categories:

  🎩 PORCELAIN (User-friendly high-level commands):
     git add, git commit, git status, git pull, git branch, git checkout.
     Designed for everyday developer productivity.

  🔧 PLUMBING (Low-level engine tools):
     Designed for internal Git scripts and deep inspection:

     • git hash-object -w <file>
       Hashes a file and writes a raw blob directly into .git/objects/

     • git cat-file -t <SHA>
       Prints the object type: 'blob', 'tree', 'commit', or 'tag'

     • git cat-file -p <SHA>
       Pretty-prints the exact contents of any Git object

     • git ls-tree <tree-SHA>
       Lists all files and subtrees in a directory object

Try running 'git cat-file -p HEAD' in any Git repo — you will see the exact tree hash,
parent hash, author, and commit message directly from the raw database!""")
            prompt_input(f"\n{Color.DIM}Press Enter to return...{Color.RESET}")

        elif choice == "6":
            clear_screen()
            print(f"{Color.MAGENTA}{Color.BOLD}── 6. Git Internals Knowledge Check ─────────────────────────────────{Color.RESET}\n")
            iqs = [
                {
                    "q": "What information does a Git 'blob' object store?",
                    "opts": ["A) The filename and permissions", "B) Only the raw compressed file content", "C) The commit author and date"],
                    "ans": "B",
                    "exp": "Blobs store ONLY the file content. Filenames and modes are stored in Trees."
                },
                {
                    "q": "What is physically stored inside a local branch file (e.g. .git/refs/heads/main)?",
                    "opts": ["A) A copy of all files", "B) A list of all commit messages", "C) A single 40-character commit hash"],
                    "ans": "C",
                    "exp": "A branch file is just 41 bytes containing the 40-char commit SHA of the branch tip."
                },
                {
                    "q": "Which plumbing command pretty-prints the raw contents of any Git object by its hash?",
                    "opts": ["A) git cat-file -p <hash>", "B) git print-object <hash>", "C) git log --raw <hash>"],
                    "ans": "A",
                    "exp": "git cat-file -p pretty-prints blobs, trees, commits, and tags."
                }
            ]
            shuffled_iqs = list(iqs)
            random.shuffle(shuffled_iqs)
            i_score = 0
            for i, item in enumerate(shuffled_iqs, 1):
                print(f"{Color.CYAN}{Color.BOLD}Q{i}: {item['q']}{Color.RESET}")
                for opt in item["opts"]:
                    print(f"  {opt}")
                ans = prompt_input(f"{Color.BOLD}Your answer [A/B/C]: {Color.RESET}").strip().upper()
                if ans == item["ans"]:
                    i_score += 1
                    print(f"{Color.GREEN}✅ Correct! {item['exp']}{Color.RESET}\n")
                else:
                    print(f"{Color.RED}❌ Wrong. {item['exp']}{Color.RESET}\n")
                time.sleep(0.8)
            print(f"{Color.YELLOW}{Color.BOLD}Internals Score: {i_score}/3{Color.RESET}\n")
            prompt_input(f"{Color.DIM}Press Enter to return...{Color.RESET}")

def _gfh_nav_bar(current_part, total_parts=10, completed=False):
    print(f"\n{Color.BOLD}{Color.WHITE}{'─'*72}{Color.RESET}")
    prev_str = f"{Color.YELLOW}[P]{Color.RESET} Prev ⏪" if current_part > 1 else f"{Color.DIM}[P] Prev{Color.RESET}"
    if not completed:
        next_str = f"{Color.GREEN}{Color.BOLD}[Enter/N]{Color.RESET} Step Checkpoint 🎯"
    else:
        if current_part < total_parts:
            next_str = f"{Color.YELLOW}[Enter/N]{Color.RESET} Next Chapter ⏩"
        else:
            next_str = f"{Color.GREEN}{Color.BOLD}[Enter/N]{Color.RESET} Finish & Graduate 🎓"

    sim_str = f"{Color.CYAN}[T]{Color.RESET} Mini-Sim 🎮"
    retake_str = f"{Color.MAGENTA}[Q]{Color.RESET} Retake Checkpoint 🧠" if completed else ""

    line1 = f"  {next_str}   {prev_str}   {sim_str}"
    if retake_str:
        line1 += f"   {retake_str}"

    line2 = f"  {Color.CYAN}[1-{total_parts}]{Color.RESET} Jump to Chapter   {Color.DIM}[0]{Color.RESET} Main Menu"

    print(line1)
    print(line2)
    print(f"{Color.BOLD}{Color.WHITE}{'─'*72}{Color.RESET}")
    choice = prompt_input(f"{Color.BOLD}Your choice: {Color.RESET}").strip().lower()
    return choice


def _gfh_sim_part1():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 1: Escape the Manual Backup Nightmare!                ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Your project folder is currently cluttered with duplicate copies:")
    print("  📁 my-project/")
    print(f"     ├── {Color.RED}report.docx{Color.RESET}")
    print(f"     ├── {Color.RED}report_v2.docx{Color.RESET}")
    print(f"     ├── {Color.RED}report_FINAL.docx{Color.RESET}")
    print(f"     └── {Color.RED}report_FINAL_actual_USE_THIS.docx{Color.RESET}\n")
    print(f"{Color.BOLD}The Concept & Command:{Color.RESET}")
    print("To replace manual confusion with Git, we initialize Git tracking using:")
    print(f"  👉 {Color.YELLOW}{Color.BOLD}git init{Color.RESET}")
    print("This creates a hidden '.git/' folder where all your project's snapshots live!\n")
    cmd = prompt_input(f"{Color.BOLD}Try typing it yourself — type 'git init': {Color.RESET}").strip()
    if cmd in ["git init", "git init ."]:
        spinner("Initializing empty Git repository in .git/", duration=0.8, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Initialized!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("Initialized empty Git repository in /my-project/.git/")
        print(f"\n{Color.YELLOW}✨ Look at your folder now:{Color.RESET}")
        print("  📁 my-project/")
        print(f"     ├── {Color.GREEN}report.docx{Color.RESET}   (ONE clean file!)")
        print(f"     └── {Color.MAGENTA}.git/{Color.RESET}         (Hidden engine recording all historical snapshots)")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git init{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 1...{Color.RESET}")

def _gfh_sim_part2():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 2: Moving Code Through the 3 Stages                   ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Stage 1: You just edited 'app.py' in your Working Directory.")
    print("Stage 2: Staging Area — we use 'git add app.py' to stage it into the buffer.")
    print("Stage 3: Commit History — we use 'git commit -m \"setup app\"' to seal it.\n")
    print(f"{Color.BOLD}Step 1: Staging a File{Color.RESET}")
    print(f"The command to stage 'app.py' is: {Color.YELLOW}{Color.BOLD}git add app.py{Color.RESET}\n")
    cmd1 = prompt_input(f"{Color.BOLD}Practice typing it — type 'git add app.py': {Color.RESET}").strip()
    if cmd1 in ["git add app.py", "git add .", "git add -A"]:
        spinner("Staging 'app.py' into index buffer", duration=0.7, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}✅ Staged! 'git status' now shows 'app.py' in green ready for commit.{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 Hint: 'git add app.py' stages the file.{Color.RESET}")

    print(f"\n{Color.BOLD}Step 2: Creating the Permanent Commit Snapshot{Color.RESET}")
    print(f"The command to commit with a message is: {Color.YELLOW}{Color.BOLD}git commit -m \"setup app\"{Color.RESET}\n")
    cmd2 = prompt_input(f"{Color.BOLD}Practice typing it — type 'git commit -m \"setup app\"': {Color.RESET}").strip()
    if cmd2 in ['git commit -m "setup app"', "git commit -m 'setup app'", 'git commit -m"setup app"', "git commit -m'setup app'"]:
        spinner("Writing commit object [hash, tree, author, message]", duration=0.9, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}🎉 Snapshot Sealed!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("[main (root-commit) 4a8b1c9] setup app\n 1 file changed, 18 insertions(+)")
        print(f"\n{Color.YELLOW}Commit 4a8b1c9 is now permanently recorded in .git!{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git commit -m \"setup app\"{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 2...{Color.RESET}")

def _gfh_sim_part3():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 3: The Daily 5 Workflow Drill                         ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("It's 9:00 AM. You sit at your desk to start work on a team project.")
    print("Rule #1 of engineering teams: Always download teammate commits BEFORE coding!")
    print(f"The command to download and merge teammate updates is: {Color.YELLOW}{Color.BOLD}git pull{Color.RESET}\n")
    cmd = prompt_input(f"{Color.BOLD}Practice downloading updates — type 'git pull': {Color.RESET}").strip()
    if cmd in ["git pull", "git pull origin main", "git pull origin"]:
        spinner("Connecting to remote origin -> fetching commits -> fast-forwarding", duration=1.0, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Perfect morning habit!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("Updating e2f7b10..4a8b1c9\nFast-forward\n server.py | 12 ++++++++++++\n 1 file changed, 12 insertions(+)")
        print(f"\n{Color.YELLOW}Your local files are now 100% up-to-date with your team. Zero surprise conflicts!{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git pull (always pull before you code!){Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 3...{Color.RESET}")

def _gfh_sim_part4():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 4: Read the Diff Like a Pro                           ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Here is a real line-by-line diff from 'git diff':\n")
    print(f"{Color.WHITE}diff --git a/auth.py b/auth.py{Color.RESET}")
    print(f"{Color.WHITE}--- a/auth.py{Color.RESET}")
    print(f"{Color.WHITE}+++ b/auth.py{Color.RESET}")
    print(f"{Color.CYAN}@@ -5,3 +5,4 @@{Color.RESET}")
    print(f"{Color.WHITE} def login(username, password):{Color.RESET}")
    print(f"{Color.RED}-    if password == \"1234\": return True{Color.RESET}")
    print(f"{Color.GREEN}+    if verify_hash(password): return True{Color.RESET}")
    print(f"{Color.GREEN}+    log_security_audit(username){Color.RESET}")
    print(f"{Color.WHITE}     return False{Color.RESET}\n")
    ans = prompt_input(f"{Color.BOLD}Question: How many lines were ADDED (+) in this diff? [Type a number]: {Color.RESET}").strip()
    if ans == "2":
        spinner("Diff engine scanning +/- line deltas", duration=0.7, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Correct! (2 lines added, 1 line deleted){Color.RESET}")
        print("Green lines with '+' are additions; red lines with '-' are deletions.")
        print("Always run 'git diff' before committing so you never save unintended edits!")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 Count the lines starting with '+': there are 2 lines added.{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 4...{Color.RESET}")

def _gfh_sim_part5():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 5: Creating an Isolated Universe (Branching)          ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Your production app is running smoothly on branch 'main'.")
    print("You want to build an experimental feature called 'ai-chat' in complete isolation.\n")
    print(f"{Color.BOLD}The Concept & Command:{Color.RESET}")
    print("To create and switch to a new branch in one command, Git provides:")
    print(f"  👉 {Color.YELLOW}{Color.BOLD}git switch -c ai-chat{Color.RESET}   (or: git checkout -b ai-chat)\n")
    cmd = prompt_input(f"{Color.BOLD}Try typing it yourself — type 'git switch -c ai-chat': {Color.RESET}").strip()
    if cmd in ["git checkout -b ai-chat", "git switch -c ai-chat"]:
        spinner("Creating branch pointer .git/refs/heads/ai-chat & updating HEAD", duration=0.8, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Parallel Universe Created!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("Switched to a new branch 'ai-chat'")
        print(f"\n{Color.YELLOW}Visualizing branch pointers:{Color.RESET}")
        print("  main:     4a8b1c9 (Production safe — untouched!)")
        print("  ai-chat:  4a8b1c9 (* HEAD is here! Code freely without fear)")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git switch -c ai-chat (or git checkout -b ai-chat){Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 5...{Color.RESET}")

def _gfh_sim_part6():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 6: Inspect Remote Changes Safely                      ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Your teammate Sarah says she pushed updates to GitHub.")
    print("You want to see her new commits WITHOUT modifying or merging anything into your local files yet.\n")
    print(f"{Color.BOLD}The Concept & Command:{Color.RESET}")
    print("The command to safely check remote updates without touching your local files is:")
    print(f"  👉 {Color.YELLOW}{Color.BOLD}git fetch{Color.RESET}  (or: git fetch origin)\n")
    cmd = prompt_input(f"{Color.BOLD}Try typing it yourself — type 'git fetch': {Color.RESET}").strip()
    if cmd in ["git fetch", "git fetch origin"]:
        spinner("Downloading remote tracking refs without touching working directory", duration=0.9, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Safe Inspection!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("From https://github.com/example/repo\n * [new branch]      sarah-feature -> origin/sarah-feature")
        print(f"\n{Color.YELLOW}Your working directory was NOT touched at all. git fetch is 100% safe!{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git fetch (downloads remote refs without merging){Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 6...{Color.RESET}")

def _gfh_sim_part7():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 7: Emergency Staging Rescue                           ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("🚨 EMERGENCY: You ran 'git add .' and accidentally staged '.env'!")
    print("'.env' contains your real production database password and Stripe API secret key.")
    print("You have NOT committed yet. You must unstage '.env' immediately without deleting the file!\n")
    print(f"{Color.BOLD}The Concept & Command:{Color.RESET}")
    print("To unstage a file without deleting it, Git provides:")
    print(f"  👉 {Color.YELLOW}{Color.BOLD}git restore --staged .env{Color.RESET}   (or: git reset HEAD .env)\n")
    cmd = prompt_input(f"{Color.BOLD}Practice typing it — type 'git restore --staged .env': {Color.RESET}").strip()
    if cmd in ["git restore --staged .env", "git reset HEAD .env", "git reset .env"]:
        spinner("Restoring staging index — removing .env from cache", duration=0.8, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}🛡️ SECRET SAVED!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("(Unstaged changes in '.env' — file kept safely on disk)")
        print(f"\n{Color.YELLOW}'.env' is out of the staging index! Next step: add '.env' to your .gitignore!{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git restore --staged .env (or git reset HEAD .env){Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 7...{Color.RESET}")

def _gfh_sim_part8():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 8: The Git Flight Recorder (Reflog)                   ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("A junior engineer ran 'git reset --hard HEAD~3' by mistake.")
    print("All 3 commits appear gone from 'git log'. Panic ensues!\n")
    print(f"{Color.BOLD}The Concept & Command:{Color.RESET}")
    print("Git never truly deletes anything right away. It logs every HEAD jump in:")
    print(f"  👉 {Color.YELLOW}{Color.BOLD}git reflog{Color.RESET}  (Git's internal black-box flight recorder!)\n")
    cmd = prompt_input(f"{Color.BOLD}Try typing it yourself — type 'git reflog': {Color.RESET}").strip()
    if cmd in ["git reflog", "git reflog show"]:
        spinner("Parsing .git/logs/HEAD flight recorder journal", duration=0.8, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✨ FLIGHT RECORDER OPENED!{Color.RESET}")
        print(f"{Color.CYAN}🖥️ Terminal Output:{Color.RESET}")
        print("4a8b1c9 HEAD@{0}: reset: moving to HEAD~3\n9b3d1f0 HEAD@{1}: commit: add user profile picture\n8c2a10d HEAD@{2}: commit: implement stripe checkout")
        print(f"\n{Color.YELLOW}The lost commit '9b3d1f0' is found! Running 'git reset --hard 9b3d1f0' restores it completely.{Color.RESET}")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The command was: git reflog (Git's black box recorder!){Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 8...{Color.RESET}")

def _gfh_sim_part9():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 9: The .gitignore Bouncer                             ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("You are configuring .gitignore for a new repository.")
    print("Which of these items MUST be added to .gitignore?\n")
    print("  [1] main.py (Your core application logic)")
    print("  [2] .env (Contains database passwords and API tokens)")
    print("  [3] node_modules/ or __pycache__/ (Giant auto-generated build dependencies)")
    print("  [4] README.md (Project documentation for teammates)\n")
    ans = prompt_input(f"{Color.BOLD}Type the numbers that belong in .gitignore (e.g. '2 3'): {Color.RESET}").strip().replace(",", " ")
    parts = set(ans.split())
    if parts == {"2", "3"} or ans in ["23", "32"]:
        spinner("Applying .gitignore rule matching patterns", duration=0.7, color=Color.GREEN)
        anim_correct()
        print(f"\n{Color.GREEN}{Color.BOLD}✅ 100% Correct!{Color.RESET}")
        print("Never commit secrets (.env) or generated dependencies (node_modules, __pycache__).")
        print("Tracked code (main.py) and documentation (README.md) should ALWAYS be committed.")
    else:
        anim_wrong()
        print(f"\n{Color.YELLOW}💡 The correct files were [2] and [3]! Secrets and generated folders never belong in Git.{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 9...{Color.RESET}")

def _gfh_sim_part10():
    clear_screen()
    print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print("║  🎮 MINI-SIM 10: The Full Production Deployment Cycle             ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("Scenario: You\'ve been assigned ticket #402: \'Add dark mode toggle\'.")
    print("Let\'s walk through the end-to-end command sequence.\n")

    print(f"{Color.CYAN}Task 1: First, make sure your local \'main\' branch has all latest team changes.{Color.RESET}")
    c1 = prompt_input(f"{Color.BOLD}Command to download latest commits from remote main: {Color.RESET}").strip()
    if c1 in ["git pull", "git pull origin main", "git pull origin"]:
        spinner("Contacting remote origin and pulling latest commits", duration=0.6, color=Color.GREEN)
        anim_correct()
        print(f"{Color.GREEN}✅ main is up to date!{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"{Color.YELLOW}💡 Recommended: git pull origin main{Color.RESET}\n")

    print(f"{Color.CYAN}Task 2: Create and switch to a new branch named \'feature/dark-mode\'.{Color.RESET}")
    c2 = prompt_input(f"{Color.BOLD}Command to create and switch branch: {Color.RESET}").strip()
    if c2 in ["git switch -c feature/dark-mode", "git checkout -b feature/dark-mode"]:
        spinner("Switched to new branch \'feature/dark-mode\'", duration=0.6, color=Color.GREEN)
        anim_correct()
        print(f"{Color.GREEN}✅ Switched to branch \'feature/dark-mode\'!{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"{Color.YELLOW}💡 Recommended: git switch -c feature/dark-mode (or git checkout -b feature/dark-mode){Color.RESET}\n")

    print(f"{Color.CYAN}Task 3: You wrote theme.js and staged it. Commit it with a message.{Color.RESET}")
    c3 = prompt_input(f"{Color.BOLD}Type commit command (e.g. git commit -m \"...\"): {Color.RESET}").strip()
    if c3.startswith("git commit -m") or c3.startswith("git commit --message"):
        spinner("Hashing blob, writing tree object, creating commit snapshot", duration=0.6, color=Color.GREEN)
        anim_correct()
        print(f"{Color.GREEN}✅ Commit created! [feature/dark-mode 4b89f2a]{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"{Color.YELLOW}💡 Format: git commit -m \"feat: add dark mode\"{Color.RESET}\n")

    print(f"{Color.CYAN}Task 4: Push your new branch to GitHub and set upstream tracking.{Color.RESET}")
    c4 = prompt_input(f"{Color.BOLD}Command to push and set upstream: {Color.RESET}").strip()
    if c4 in ["git push -u origin feature/dark-mode", "git push --set-upstream origin feature/dark-mode", "git push origin feature/dark-mode"]:
        spinner("Compressing objects, uploading to GitHub remote repository", duration=0.7, color=Color.GREEN)
        anim_correct()
        print(f"{Color.GREEN}✅ Branch pushed to GitHub! Pull request ready to open.{Color.RESET}")
        print(f"\n{Color.YELLOW}🚀 Teammates approved your PR, tests passed, and code merged into production!{Color.RESET}")
    else:
        anim_wrong()
        print(f"{Color.YELLOW}💡 Command: git push -u origin feature/dark-mode{Color.RESET}")
    prompt_input(f"\n{Color.DIM}Press Enter to return to Part 10...{Color.RESET}")

_GFH_SIMS = {
    1: _gfh_sim_part1,
    2: _gfh_sim_part2,
    3: _gfh_sim_part3,
    4: _gfh_sim_part4,
    5: _gfh_sim_part5,
    6: _gfh_sim_part6,
    7: _gfh_sim_part7,
    8: _gfh_sim_part8,
    9: _gfh_sim_part9,
    10: _gfh_sim_part10
}


def _gfh_show_graduation(scores, total_parts=10):
    total_score = sum(s.get("total", 0) if isinstance(s, dict) else s for s in scores.values())
    max_score = sum(s.get("max", 4) if isinstance(s, dict) else 4 for s in scores.values())
    if max_score == 0:
        max_score = 40
    clear_screen()
    spinner("Tallying responses & computing Git Mastery score", duration=0.8, color=Color.MAGENTA)
    clear_screen()
    print(f"{Color.BOLD}{Color.MAGENTA}╔════════════════════════════════════════════════════════════════════╗")
    print("║                 GIT FOR HUMANS — COMPLETE                          ║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print(f"  Total Score Across All Steps: {Color.BOLD}{total_score}/{max_score}{Color.RESET}\n")
    print(f"{Color.CYAN}  Step-by-step breakdown (MCQs + Manual Command Challenges):{Color.RESET}")
    for s in range(1, total_parts + 1):
        s_data = scores.get(s, {"mcq": 0, "cmd": 0, "total": 0, "max": 4})
        if isinstance(s_data, int):
            s_data = {"mcq": s_data, "cmd": 0, "total": s_data, "max": 4}
        tot = s_data.get("total", 0)
        mx = s_data.get("max", 4)
        m = s_data.get("mcq", 0)
        c = s_data.get("cmd", 0)
        icon = "✅" if tot == mx else ("🟡" if tot >= mx / 2 else "⚪")
        print(f"    {icon} Step {s:2d}: {tot:2d}/{mx:2d}  (MCQs: {m}, Commands: {c})")
    print()
    if total_score >= max_score * 0.9:
        print(f"  {Color.GREEN}🏆 Outstanding ({total_score}/{max_score})! You\'ve achieved complete Git fluency with sharp command muscle memory. Jump into the Practice Arena next!{Color.RESET}")
    elif total_score >= max_score * 0.7:
        print(f"  {Color.GREEN}👍 Strong result ({total_score}/{max_score}). Re-read any steps you missed, then try the Practice Arena.{Color.RESET}")
    elif total_score >= max_score * 0.5:
        print(f"  {Color.YELLOW}📖 Getting there ({total_score}/{max_score}). Go back through any steps you found tricky and retake their checkpoints.{Color.RESET}")
    else:
        print(f"  {Color.YELLOW}📖 Take your time — review earlier chapters and try the checkpoints again!{Color.RESET}")
    print(f"\n  {Color.YELLOW}[1-10] Jump to review any Step{Color.RESET}")
    print(f"  {Color.CYAN}[0] Return to Main Menu{Color.RESET}\n")
    post_choice = prompt_input(f"{Color.BOLD}Choose [1-10 or 0]: {Color.RESET}").strip()
    return post_choice

def _print_gfh_chapter(current_part):
    if current_part == 1:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 1 / 10 : Why Git Exists & First-Time Setup                ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Everyone has experienced this manual file nightmare:\n")
        print(f"  📄 {Color.RED}report.docx{Color.RESET}")
        print(f"  📄 {Color.RED}report_v2.docx{Color.RESET}")
        print(f"  📄 {Color.RED}report_FINAL.docx{Color.RESET}")
        print(f"  📄 {Color.RED}report_FINAL_actual_USE_THIS.docx{Color.RESET}\n")
        print(f"{Color.BOLD}Why manual copying fails:{Color.RESET}")
        print("  • Which file is actually the latest working code?")
        print("  • What changed between v2 and FINAL? Who changed it?")
        print("  • How do you undo one bad line from yesterday without losing today's work?")
        print("  • How can two people work together without overwriting each other?\n")
        print(f"{Color.GREEN}{Color.BOLD}Git's Solution:{Color.RESET}")
        print("  Your project lives in ONE clean folder. Git runs quietly inside a hidden")
        print("  '.git/' folder on your computer, recording a permanent timeline of snapshots called 'commits'.")
        print("  Git is 100% distributed — your laptop itself is your database, working completely offline!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  1. {Color.GREEN}{Color.BOLD}git --version{Color.RESET}")
        print("     Checks if Git is installed on your computer and shows the active release.\n")
        print(f"  2. {Color.GREEN}{Color.BOLD}git config --global user.name \"Your Name\"{Color.RESET}")
        print("     Tells Git your name! Git embeds this into every single commit you create.")
        print("     Example: git config --global user.name \"Ada Lovelace\"\n")
        print(f"  3. {Color.GREEN}{Color.BOLD}git config --global user.email \"your.email@example.com\"{Color.RESET}")
        print("     Tells Git your email (use the same email as your GitHub account).")
        print("     Example: git config --global user.email \"ada@example.com\"\n")
        print(f"  4. {Color.GREEN}{Color.BOLD}git config --list{Color.RESET} (or git config -l)")
        print("     Lists all active Git configuration settings on your computer.\n")
        print(f"  5. {Color.GREEN}{Color.BOLD}git init{Color.RESET}")
        print("     Turns your current folder into a tracked Git repository by creating the '.git/' folder.\n")
        print(f"  6. {Color.GREEN}{Color.BOLD}git status{Color.RESET}")
        print("     Inspects the repository: shows modified, staged, and untracked files.\n")

    elif current_part == 2:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 2 / 10 : The 3 Stages of Git & Reviewing Diffs            ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Most Git confusion vanishes once you understand your project has 3 distinct zones:\n")
        print("""  ┌─────────────────────────┐      git add       ┌─────────────────────────┐     git commit     ┌─────────────────────────┐
  │    Working Directory    │ ─────────────────► │   Staging Area (Index)  │ ─────────────────► │    Commit History       │
  │  (Files you edit here)  │                    │   (Curated checkpoint)  │                    │  (Permanent database)   │
  └─────────────────────────┘                    └─────────────────────────┘                    └─────────────────────────┘
""")
        print(f"  1. {Color.BOLD}Working Directory:{Color.RESET} The active files on your disk that you edit in VS Code.")
        print(f"  2. {Color.BOLD}Staging Area (Index):{Color.RESET} Think of this as a shopping cart! You pick which changed files belong together.")
        print(f"  3. {Color.BOLD}Commit History:{Color.RESET} Permanent snapshots stored in .git with author, date, and hash.\n")
        print(f"{Color.BOLD}Why have a Staging Area?{Color.RESET}")
        print("  If you edited 5 files for two different features, staging lets you commit 3 files for Feature A,")
        print("  and 2 files for Feature B in two clean, separate snapshots!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git add <filename>{Color.RESET}         — Stage ONE specific file (e.g. git add server.py)")
        print(f"  • {Color.GREEN}{Color.BOLD}git add .{Color.RESET}                  — Stage ALL modified & new files in the folder at once")
        print(f"  • {Color.GREEN}{Color.BOLD}git restore --staged <file>{Color.RESET} — Unstage a file back to working dir (your code stays safe on disk!)")
        print(f"  • {Color.GREEN}{Color.BOLD}git status{Color.RESET}                 — View red modified files vs green staged files")
        print(f"  • {Color.GREEN}{Color.BOLD}git diff{Color.RESET}                   — Show line-by-line unstaged changes (+ green additions, - red deletions)\n")

    elif current_part == 3:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 3 / 10 : Making Commits & Viewing History                 ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("A 'commit' is a permanent, sealed milestone in your project's timeline.\n")
        print("Each commit contains:")
        print("  • A complete snapshot of all files at that moment")
        print("  • Author name, email, and exact timestamp")
        print("  • A unique 40-character SHA hash (e.g. 9b8c7d6...)")
        print("  • A human message explaining WHAT changed and WHY\n")
        print(f"{Color.BOLD}Writing Great Commit Messages:{Color.RESET}")
        print(f"  {Color.GREEN}✔ GOOD:{Color.RESET} 'feat: add user authentication'  or  'fix: resolve crash on null input'")
        print(f"  {Color.RED}✘ BAD :{Color.RESET} 'update stuff', 'asdf', 'fixed bug finally omg'\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git commit -m \"descriptive message\"{Color.RESET} — Seal staged changes into history with a message")
        print(f"  • {Color.GREEN}{Color.BOLD}git commit --amend --no-edit{Color.RESET}        — Add forgotten staged changes into the last commit (keeps same message)")
        print(f"  • {Color.GREEN}{Color.BOLD}git commit --amend -m \"new msg\"{Color.RESET}    — Change the message of the most recent unpushed commit")
        print(f"  • {Color.GREEN}{Color.BOLD}git log{Color.RESET}                             — Show full commit history (press 'q' to exit pager)")
        print(f"  • {Color.GREEN}{Color.BOLD}git log --oneline{Color.RESET}                   — Compact one-line summary per commit (hash + message)")
        print(f"  • {Color.GREEN}{Color.BOLD}git log -n 5{Color.RESET}                        — Show only the last 5 commits")
        print(f"  • {Color.GREEN}{Color.BOLD}git show{Color.RESET} (or git show HEAD)         — Show the author, metadata, and full diff of the most recent commit\n")

    elif current_part == 4:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 4 / 10 : Branching — Working in Total Safety              ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Problem: Your code on 'main' works perfectly. You want to experiment with a new idea.")
        print("If you edit 'main' directly and make a mistake, your working app is broken!\n")
        print(f"{Color.GREEN}{Color.BOLD}Solution: Branches (Parallel Universes){Color.RESET}\n")
        print("  main branch:        ● ─────── ● ─────── ● ──────────── (Always clean & stable)")
        print("                                 \\")
        print("  feature branch:                 ● ─────── ● ────────── (Your safe experiment sandbox)\n")
        print("  • What is a branch? A lightweight, movable pointer to a commit snapshot.")
        print("  • What is HEAD? Git's pointer showing which branch/commit you are currently looking at.")
        print("  • On a branch, you can experiment, break things, and test freely without affecting main!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git branch{Color.RESET}                       — List all local branches (an asterisk '*' marks the active branch)")
        print(f"  • {Color.GREEN}{Color.BOLD}git switch -c <branch-name>{Color.RESET}     — Create AND switch to a new branch in one step (e.g. git switch -c feature/login)")
        print(f"  • {Color.GREEN}{Color.BOLD}git switch <branch-name>{Color.RESET}        — Switch to an existing branch (e.g. git switch main)")
        print(f"  • {Color.GREEN}{Color.BOLD}git switch -{Color.RESET}                    — Jump back to the previous branch you were just on")
        print(f"  • {Color.GREEN}{Color.BOLD}git branch -d <branch-name>{Color.RESET}     — Safely delete a branch after its changes are merged")
        print(f"  • {Color.GREEN}{Color.BOLD}git branch -D <branch-name>{Color.RESET}     — Force delete a branch (even if unmerged)\n")

    elif current_part == 5:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 5 / 10 : Merging Branches & Resolving Conflicts           ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Once your feature branch is tested and complete, you bring it home to 'main' via a merge.\n")
        print(f"{Color.BOLD}Types of Merges:{Color.RESET}")
        print("  • Fast-Forward: If main didn't move while you branched, Git simply points main forward in a straight line.")
        print("  • 3-Way Merge: If both main and your branch have new commits, Git combines them and creates a 'merge commit'.\n")
        print(f"{Color.RED}{Color.BOLD}What is a Merge Conflict?{Color.RESET}")
        print("  If you and a teammate modified the EXACT SAME lines in the same file, Git pauses and marks the conflict:")
        print(f"    {Color.CYAN}<<<<<<< HEAD{Color.RESET}        (your current branch code)")
        print("    port = 8080")
        print(f"    {Color.YELLOW}======={Color.RESET}             (conflict separator)")
        print("    port = 9000")
        print(f"    {Color.CYAN}>>>>>>> feature{Color.RESET}     (incoming branch code)\n")
        print(f"{Color.BOLD}How to Resolve Conflicts:{Color.RESET}")
        print("  1. Open file in VS Code, choose the right lines, and delete the conflict markers (<<<<, ===, >>>>).")
        print("  2. Stage the resolved file: git add <filename>")
        print("  3. Commit to finalize the merge: git commit -m \"Merge feature into main\"")
        print("  4. Panicking? Abort safely: git merge --abort (restores files to clean pre-merge state instantly!)\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git merge <branch-name>{Color.RESET}         — Merge specified branch into your current branch")
        print(f"  • {Color.GREEN}{Color.BOLD}git merge --no-ff <branch>{Color.RESET}      — Force create a dedicated merge commit (no fast-forward)")
        print(f"  • {Color.GREEN}{Color.BOLD}git merge --abort{Color.RESET}               — Cancel a conflicted merge and restore clean pre-merge state")
        print(f"  • {Color.GREEN}{Color.BOLD}git log --graph --oneline --all{Color.RESET} — Visualize the commit branch graph and merge points in ASCII\n")

    elif current_part == 6:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 6 / 10 : Going to the Cloud — Remotes & GitHub            ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"{Color.BOLD}Git vs GitHub:{Color.RESET}")
        print("  • Git = The local tool on your laptop that tracks versions in .git/")
        print("  • GitHub = The cloud website that hosts your Git repositories so teams can sync and collaborate!\n")
        print(f"{Color.BOLD}Key Cloud Concepts:{Color.RESET}")
        print("  • 'origin': The standard default nickname for your primary remote repository on GitHub.")
        print("  • 'git fetch' vs 'git pull':")
        print("      - git fetch: Safely downloads remote commits WITHOUT touching or modifying your working files.")
        print("      - git pull : Downloads remote commits AND immediately merges them into your active branch.\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git clone <url>{Color.RESET}                 — Download an entire repository with all history from GitHub")
        print(f"  • {Color.GREEN}{Color.BOLD}git remote add origin <url>{Color.RESET}     — Connect a local repository to a remote GitHub URL")
        print(f"  • {Color.GREEN}{Color.BOLD}git remote -v{Color.RESET}                   — List all registered remote nicknames and their URLs")
        print(f"  • {Color.GREEN}{Color.BOLD}git fetch origin{Color.RESET}                — Safely download remote commits to inspect before merging")
        print(f"  • {Color.GREEN}{Color.BOLD}git pull{Color.RESET} (or git pull origin main) — Download and merge latest remote commits into active branch")
        print(f"  • {Color.GREEN}{Color.BOLD}git push -u origin <branch>{Color.RESET}      — Upload local commits to GitHub and link upstream tracking\n")

    elif current_part == 7:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 7 / 10 : Undoing Mistakes Safely (Emergency Guide)       ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Mistakes happen to every developer! Git has safe undo tools for every level:\n")
        print("  1. Unstaged changes in working directory?  ──►  git restore <file>")
        print("  2. Accidentally staged a file (green)?    ──►  git restore --staged <file>")
        print("  3. Committed locally, want to undo?       ──►  git reset HEAD~1 (Mixed: code stays safe on disk!)")
        print("  4. Already pushed commit to shared branch? ──►  git revert <commit-hash> (Safe public undo!)\n")
        print(f"{Color.RED}{Color.BOLD}⚠️ DANGER ZONE:{Color.RESET}")
        print("  • 'git reset --hard' wipes uncommitted edits permanently!")
        print("  • 'git clean -fd' deletes untracked files with ZERO backup — always dry-run first with 'git clean -nd'!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git restore <filename>{Color.RESET}          — Discard uncommitted edits in working directory (restore from index)")
        print(f"  • {Color.GREEN}{Color.BOLD}git restore --staged <file>{Color.RESET}     — Unstage a file back to red without touching its contents on disk")
        print(f"  • {Color.GREEN}{Color.BOLD}git restore --staged .{Color.RESET}         — Unstage ALL staged files at once")
        print(f"  • {Color.GREEN}{Color.BOLD}git reset HEAD~1{Color.RESET}                — Undo the last commit; all modified files stay safe on your disk!")
        print(f"  • {Color.GREEN}{Color.BOLD}git revert <commit-hash>{Color.RESET}        — Safely undo a commit by creating a brand-new opposite commit")
        print(f"  • {Color.GREEN}{Color.BOLD}git clean -fd{Color.RESET}                   — Force delete untracked files (-f) and directories (-d)")
        print(f"  • {Color.GREEN}{Color.BOLD}git clean -nd{Color.RESET}                   — Dry-run preview: see what WOULD be deleted without touching disk\n")

    elif current_part == 8:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 8 / 10 : Stashing — The Developer's Secret Clipboard      ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Scenario: You are half-way through coding a big feature. Your code is broken and untested.")
        print("Suddenly, your team asks you to urgently fix a critical bug on 'main'.\n")
        print("You can't commit broken code, and Git won't let you switch branches with uncommitted conflicts!")
        print(f"{Color.GREEN}{Color.BOLD}Solution: git stash!{Color.RESET}")
        print("  Stashing shelves your uncommitted modifications onto a temporary clipboard stack,")
        print("  instantly returning your working tree to a 100% clean state.\n")
        print("The Professional Stash Loop:")
        print(f"  1. {Color.GREEN}git stash{Color.RESET}        → Working directory is clean!")
        print(f"  2. {Color.GREEN}git switch main{Color.RESET}  → Fix urgent bug, test, and commit.")
        print(f"  3. {Color.GREEN}git switch feature{Color.RESET} → Return to your feature branch.")
        print(f"  4. {Color.GREEN}git stash pop{Color.RESET}    → All your unfinished edits are restored right where you left them!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash{Color.RESET}                       — Shelve all modified & staged changes onto stash stack")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash push -m \"message\"{Color.RESET}    — Stash with a descriptive note (e.g. git stash -m 'WIP: auth')")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash pop{Color.RESET}                   — Restore the most recent stash and remove it from stash list")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash apply{Color.RESET}                 — Restore the stash but KEEP it in the stash list")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash list{Color.RESET}                  — View all saved stash entries (stash@{0}, stash@{1}...)")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash -u{Color.RESET}                    — Stash all changes INCLUDING newly created untracked files")
        print(f"  • {Color.GREEN}{Color.BOLD}git stash clear{Color.RESET}                 — Delete all stashes from the stash list\n")

    elif current_part == 9:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 9 / 10 : Rewriting History with Rebase & Squashing        ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"{Color.BOLD}Merge vs Rebase:{Color.RESET}")
        print("  • Merge: Preserves true historical timeline by creating a diamond merge commit.")
        print("  • Rebase: Replays your commits on top of another base, creating a clean linear timeline.\n")
        print(f"{Color.RED}{Color.BOLD}⭐ The Golden Rule of Rebasing:{Color.RESET}")
        print("  NEVER rebase commits that have already been pushed to a shared public branch!")
        print("  Only rebase your own local, private feature branch commits before opening a Pull Request.\n")
        print(f"{Color.BOLD}Interactive Rebase (git rebase -i):{Color.RESET}")
        print("  Allows you to tidy up your work before sharing it with your team:")
        print("  • 'pick'   : Keep commit as is")
        print("  • 'squash' : Combine commit into previous commit (combine 5 'wip' commits into 1!)")
        print("  • 'reword' : Edit the commit message")
        print("  • 'drop'   : Delete a commit completely\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git rebase <base-branch>{Color.RESET}        — Replay current branch commits on top of base (e.g. git rebase main)")
        print(f"  • {Color.GREEN}{Color.BOLD}git rebase -i HEAD~4{Color.RESET}            — Start interactive rebase to squash, edit, or drop last 4 commits")
        print(f"  • {Color.GREEN}{Color.BOLD}git rebase --continue{Color.RESET}           — Resume rebase after resolving a conflict")
        print(f"  • {Color.GREEN}{Color.BOLD}git rebase --abort{Color.RESET}              — Cancel rebase and restore original branch state immediately")
        print(f"  • {Color.GREEN}{Color.BOLD}git status{Color.RESET}                      — Check progress and current paused state during a rebase\n")

    elif current_part == 10:
        print(f"{Color.YELLOW}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║  🐣 PART 10 / 10 : Ninja Utilities — Cherry-Pick, Reflog & Bisect  ║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("Congratulations on reaching Chapter 10! Here are the senior engineer superpower tools:\n")
        print(f"  1. {Color.BOLD}Cherry-Pick:{Color.RESET} Need ONE specific bugfix commit from a teammate's branch without merging the whole thing?")
        print("     'git cherry-pick <hash>' copies that exact commit onto your current branch!\n")
        print(f"  2. {Color.BOLD}The Reflog (Git's Flight Recorder):{Color.RESET} Ran 'git reset --hard' or deleted a branch by accident?")
        print("     Git records EVERY movement of HEAD for 90 days. Run 'git reflog' to find the lost commit hash,")
        print("     then 'git reset --hard <hash>' to bring it back instantly!\n")
        print(f"  3. {Color.BOLD}Release Tags:{Color.RESET} Permanent milestone bookmarks for releases (e.g. 'v1.0.0').\n")
        print(f"  4. {Color.BOLD}Git Bisect:{Color.RESET} A bug appeared somewhere in the last 100 commits, but you don't know where?")
        print("     Bisect uses binary search O(log N) to isolate the exact breaking commit in ~7 steps!\n")
        print(f"{Color.CYAN}{Color.BOLD}── 🛠️ COMMANDS TAUGHT IN THIS CHAPTER (Tested in Checkpoint!) ──────────{Color.RESET}\n")
        print(f"  • {Color.GREEN}{Color.BOLD}git cherry-pick <commit-hash>{Color.RESET}   — Apply a specific commit onto current branch (e.g. git cherry-pick a1b2c3d)")
        print(f"  • {Color.GREEN}{Color.BOLD}git reflog{Color.RESET}                      — View Git's secret flight recorder to find lost commit hashes")
        print(f"  • {Color.GREEN}{Color.BOLD}git tag -a v1.0.0 -m \"Release\"{Color.RESET} — Create an annotated release milestone tag")
        print(f"  • {Color.GREEN}{Color.BOLD}git bisect start{Color.RESET}                — Begin binary search bug hunt")
        print(f"  • {Color.GREEN}{Color.BOLD}git bisect bad{Color.RESET}                  — Mark current commit as broken")
        print(f"  • {Color.GREEN}{Color.BOLD}git bisect good <commit-hash>{Color.RESET}  — Mark an older known-working commit")
        print(f"  • {Color.GREEN}{Color.BOLD}git bisect reset{Color.RESET}                — Exit bisect and return to your original branch\n")


def mode_git_for_humans():
    clear_screen()
    progress_bar("Entering Git for Humans (Interactive Handbook)", total=16, delay=0.015, color=Color.CYAN)
    current_part = 1
    total_parts = 10
    last_part = None
    completed_steps = set()
    step_scores = {}

    while True:
        clear_screen()
        if last_part is not None and last_part != current_part:
            progress_bar(f"Loading Chapter {current_part} / {total_parts}", total=14, delay=0.012, color=Color.YELLOW)
            clear_screen()
        last_part = current_part

        _print_gfh_chapter(current_part)

        is_completed = (current_part in completed_steps)
        choice = _gfh_nav_bar(current_part, total_parts=total_parts, completed=is_completed)

        if choice in ["0", "menu", "exit", "home"]:
            spinner("Returning to Main Menu", duration=0.4, color=Color.MAGENTA)
            return
        elif choice in ["t", "sim", "try"]:
            if current_part in _GFH_SIMS:
                spinner(f"Launching Chapter {current_part} Mini-Sim", duration=0.5, color=Color.CYAN)
                _GFH_SIMS[current_part]()
                spinner("Returning to Chapter Handbook", duration=0.4, color=Color.YELLOW)
            continue
        elif choice in ["p", "prev", "previous", "b", "back"]:
            if current_part > 1:
                spinner(f"Navigating back to Chapter {current_part - 1}", duration=0.4, color=Color.YELLOW)
                current_part -= 1
            else:
                print(f"{Color.YELLOW}You are already at Part 1!{Color.RESET}")
                time.sleep(0.6)
            continue
        elif choice in ["q", "quiz", "retake"] and is_completed:
            spinner(f"Loading Chapter {current_part} Checkpoint", duration=0.4, color=Color.MAGENTA)
            res = _run_step_checkpoint(current_part)
            if res == "exit":
                return
            step_scores[current_part] = res
            continue
        elif choice.isdigit() and 1 <= int(choice) <= total_parts:
            target_part = int(choice)
            spinner(f"Jumping to Chapter {target_part}", duration=0.4, color=Color.CYAN)
            current_part = target_part
            continue
        elif choice in ["n", "next", ""] or choice.startswith("n"):
            if current_part not in completed_steps:
                res = _run_step_checkpoint(current_part)
                if res == "exit":
                    return
                step_scores[current_part] = res
                completed_steps.add(current_part)

            if current_part < total_parts:
                spinner(f"Advancing to Chapter {current_part + 1}", duration=0.4, color=Color.GREEN)
                current_part += 1
            else:
                grad_choice = _gfh_show_graduation(step_scores, total_parts=total_parts)
                if grad_choice and grad_choice.isdigit() and 1 <= int(grad_choice) <= total_parts:
                    current_part = int(grad_choice)
                else:
                    return

# ----------------- COMMAND CHALLENGES BY DIFFICULTY (30 TOTAL) -----------------

CHALLENGES_LOW = [
    {
        "concept": "Starting fresh — initializing a repository",
        "situation": "You just created a new folder called 'my-project' for your work.\n  Right now it is a plain folder. Git doesn't know about it yet.\n  You need to tell Git to start tracking this folder.",
        "task": "Run the command that initializes Git in the current folder:",
        "valid": ["git init", "git init ."],
        "hint": "Think of the subcommand used to 'initialize' a repository: git <subcommand>",
        "output": "Initialized empty Git repository in C:/Users/user/my-project/.git/",
        "why": "This creates a hidden '.git' folder inside your project. That's where Git stores all your history."
    },
    {
        "concept": "Checking what has changed",
        "situation": "You edited a file called 'index.html'.\n  Before doing anything else, you want to see what files have changed,\n  which are staged, and which are untracked.",
        "task": "Run the command to see the current state of your working directory:",
        "valid": ["git status", "git st", "git status -s", "git status --short"],
        "hint": "Look for the subcommand that reports working tree 'status' (starts with 's')",
        "output": "On branch main\n\nNo commits yet\n\nChanges not staged for commit:\n  (use \"git add <file>...\" to update what will be committed)\n  (use \"git restore <file>...\" to discard changes in working directory)\n\tmodified:   index.html\n\nno changes added to commit (use \"git add\" and/or \"git commit -a\")",
        "why": "git status is the most used Git command. Run it constantly — it always tells you what's going on."
    },
    {
        "concept": "Staging all files before saving",
        "situation": "You edited two files today. You want to include all of them\n  in your next commit. Git doesn't save anything automatically —\n  you have to explicitly select what goes into the next snapshot.",
        "task": "Stage all changed files in the current directory:",
        "valid": ["git add .", "git add -A", "git add --all"],
        "hint": "Use the 'add' subcommand followed by a symbol meaning 'current directory / everything here'",
        "output": "(Changes in the current directory are staged into the index — 'git status' now shows them in green ready for commit)",
        "why": "The dot '.' means 'everything here'. git add picks what goes into your next commit."
    },
    {
        "concept": "Staging one specific file only",
        "situation": "You modified 'README.md' and 'app.py'. You only want to stage\n  'README.md' right now so your commit is focused on documentation.",
        "task": "Stage only the file 'README.md':",
        "valid": ["git add README.md"],
        "hint": "Use 'git add' followed by the exact filename you want to stage",
        "output": "(File 'README.md' is staged into the index; other modified files remain unstaged)",
        "why": "Naming a specific file stages only that file, leaving other modified files unstaged."
    },
    {
        "concept": "Saving a snapshot with a message",
        "situation": "You staged your changes. Now you want to permanently save\n  that snapshot with a note describing what you did.\n  The message should be: 'add homepage layout'",
        "task": "Commit your staged files with the message: 'add homepage layout'",
        "valid": [
            'git commit -m "add homepage layout"',
            "git commit -m 'add homepage layout'",
            'git commit -m"add homepage layout"',
            "git commit -m'add homepage layout'"
        ],
        "hint": "Use 'git commit' with the message flag (-m) followed by the message in quotes",
        "output": "[main (root-commit) 4a8b1c9] add homepage layout\n 2 files changed, 48 insertions(+)\n create mode 100644 index.html\n create mode 100644 style.css",
        "why": "Every commit needs a message (-m flag). It describes what changed so you (and your team) can understand the history."
    },
    {
        "concept": "Viewing the commit history",
        "situation": "You've made a few commits over the past few days.\n  You want to see all of them — who made them, when, and what the message said.",
        "task": "Show the full commit history of this repository:",
        "valid": ["git log", "git lg", "git log --oneline", "git log -n 5"],
        "hint": "A 3-letter word meaning record or history log: git <subcommand>",
        "output": "commit 4a8b1c9e8d2f10b7a6c5d4e3f2a1b0c9d8e7f6a5 (HEAD -> main)\nAuthor: Prajwal Chonnad <prajwal@example.com>\nDate:   Wed Nov 4 14:30:00 2026 +0530\n\n    add homepage layout\n\ncommit e2f7b10c9a4b8d7e6f5a3b2c1d0e9f8a7b6c5d4e\nAuthor: Prajwal Chonnad <prajwal@example.com>\nDate:   Wed Nov 4 10:15:22 2026 +0530\n\n    initial commit",
        "why": "git log lists every commit in reverse order (newest first). Each has a unique ID, author, date, and message."
    },
    {
        "concept": "Viewing compact one-line commit log",
        "situation": "You want to quickly scan past commits without reading multi-line blocks for each one.",
        "task": "Display the commit history with each commit on a single line:",
        "valid": ["git log --oneline", "git lg"],
        "hint": "Add a flag to 'git log' that condenses each commit to a single line: --one...",
        "output": "4a8b1c9 (HEAD -> main) add homepage layout\ne2f7b10 initial commit",
        "why": "'--oneline' condenses each commit to its 7-character SHA and commit subject message."
    },
    {
        "concept": "Inspecting line-by-line differences",
        "situation": "You edited 'style.css'. Before staging it, you want to see the exact lines added or removed.",
        "task": "Show the unstaged modifications in your working tree:",
        "valid": ["git diff", "git diff style.css"],
        "hint": "The subcommand name is short for 'differences' (4 letters)",
        "output": "diff --git a/style.css b/style.css\nindex 7a12b3c..9f4e2d1 100644\n--- a/style.css\n+++ b/style.css\n@@ -1,3 +1,5 @@\n body {\n+    background-color: #f4f4f4;\n+    font-family: sans-serif;\n }",
        "why": "'git diff' shows + (green) for added lines and - (red) for deleted lines in files that haven't been staged yet."
    },
    {
        "concept": "Listing local branches",
        "situation": "You want to check what branches exist in your local repository and see which one you are currently on.",
        "task": "List all local branches in the repository:",
        "valid": ["git branch", "git branch --list"],
        "hint": "Use the command named after tree limbs: git <subcommand>",
        "output": "* main",
        "why": "'git branch' lists all branches, marking the currently checked-out branch with an asterisk (*)."
    },
    {
        "concept": "Checking your installed Git version",
        "situation": "You opened a new terminal and want to quickly verify that Git is installed and see which version is running.",
        "task": "Check the installed Git version:",
        "valid": ["git --version", "git version", "git -v"],
        "hint": "Use the standard double-dash version flag with git: git --v...",
        "output": "git version 2.44.0.windows.1",
        "why": "Verifies that the Git binary is available on your system PATH."
    },
    {
        "concept": "Inspecting short compact status",
        "situation": "You want a fast, two-letter abbreviated overview of what files are modified and untracked without long explanations.",
        "task": "Run git status in compact short mode:",
        "valid": ["git status -s", "git status --short"],
        "hint": "Add the short flag (-s or --short) to the status command",
        "output": " M index.html\n?? notes.txt",
        "why": "'git status -s' shows a concise two-column format: column 1 is staging state, column 2 is working tree state."
    },
    {
        "concept": "Inspecting the latest commit in detail",
        "situation": "You want to inspect the author, timestamp, commit message, and full code diff of the latest commit (HEAD).",
        "task": "Display the latest commit's metadata and diff:",
        "valid": ["git show", "git show HEAD"],
        "hint": "Use the 4-letter subcommand that displays an object's contents: git <subcommand>",
        "output": "commit 4a8b1c9 (HEAD -> main)\nAuthor: Prajwal Chonnad <prajwal@example.com>\nDate:   Wed Nov 4 14:30:00 2026 +0530\n\n    add homepage layout\n\ndiff --git a/index.html b/index.html\n--- a/index.html\n+++ b/index.html\n@@ -1,3 +1,6 @@\n+<header>Welcome</header>",
        "why": "'git show' (or 'git show HEAD') presents the full details and diff of the most recent snapshot."
    }
]

CHALLENGES_MEDIUM = [
    {
        "concept": "Creating and switching to a new branch",
        "situation": "You're on 'main' and want to start building a new 'search' feature.\n  You don't want to work directly on main — you need a separate branch\n  so the working code stays safe while you build.",
        "task": "Create a new branch called 'search-feature' and switch to it in one command:",
        "valid": ["git checkout -b search-feature", "git switch -c search-feature"],
        "hint": "Use 'checkout' with the new-branch flag (-b) or 'switch' with (-c), followed by the branch name",
        "output": "Switched to a new branch 'search-feature'",
        "why": "The -b flag creates the branch AND switches to it. (Modern syntax: git switch -c search-feature)."
    },
    {
        "concept": "Switching back to an existing branch",
        "situation": "You're on 'search-feature'. Your team lead just told you to\n  review something on the 'main' branch. You need to switch without losing anything.",
        "task": "Switch to the already-existing branch called 'main':",
        "valid": ["git checkout main", "git switch main"],
        "hint": "Use 'git checkout <branch>' or 'git switch <branch>' (no -b or -c needed for existing branches)",
        "output": "Switched to branch 'main'\nYour branch is up to date with 'origin/main'.",
        "why": "No -b flag here — that would try to create a new branch. Without -b, git checkout just switches to main."
    },
    {
        "concept": "Uploading your commits to GitHub",
        "situation": "You've made 3 commits locally on the 'main' branch.\n  None of them are on GitHub yet. You want to upload them so\n  they're backed up and visible to your team.",
        "task": "Push your local 'main' branch to the remote called 'origin':",
        "valid": ["git push origin main", "git push", "git push -u origin main"],
        "hint": "Use 'push' followed by the remote name ('origin') and branch name ('main')",
        "output": "Enumerating objects: 5, done.\nCounting objects: 100% (5/5), done.\nDelta compression using up to 8 threads\nCompressing objects: 100% (3/3), done.\nWriting objects: 100% (3/3), 320 bytes | 320.00 KiB/s, done.\nTotal 3 (delta 1), reused 0 (delta 0), pack-reused 0\nTo https://github.com/example/my-project.git\n   e2f7b10..4a8b1c9  main -> main",
        "why": "'origin' is the default name for your GitHub remote. 'main' is the branch you're pushing."
    },
    {
        "concept": "Downloading your teammate's new commits",
        "situation": "Your teammate pushed a bug fix to GitHub an hour ago.\n  Your local copy doesn't have it. You need to download\n  AND apply their latest commits to your machine.",
        "task": "Download and merge the latest commits from the remote repository:",
        "valid": ["git pull", "git pull origin main"],
        "hint": "A 4-letter command that downloads AND merges remote changes into your active branch",
        "output": "Updating e2f7b10..4a8b1c9\nFast-forward\n index.html | 12 ++++++++++++\n 1 file changed, 12 insertions(+)",
        "why": "git pull = git fetch + git merge. It downloads remote changes and applies them to your current branch."
    },
    {
        "concept": "Downloading remote updates WITHOUT merging",
        "situation": "You want to see what your teammates pushed to 'origin' without touching or merging into your local files yet.",
        "task": "Fetch remote updates from 'origin' safely without modifying your local working files:",
        "valid": ["git fetch", "git fetch origin", "git fetch --all"],
        "hint": "A 5-letter command that downloads remote commits without touching your working directory",
        "output": "From https://github.com/example/my-project\n * [new branch]      main       -> origin/main\n * [new branch]      feature-x  -> origin/feature-x",
        "why": "'git fetch' downloads remote commits and updates remote branches (origin/main) without changing your local working directory."
    },
    {
        "concept": "Merging a feature branch into main",
        "situation": "You switched to 'main'. Your work on 'search-feature' is complete and tested.\n  Now you want to bring the commits from 'search-feature' into 'main'.",
        "task": "Merge 'search-feature' into the current branch:",
        "valid": ["git merge search-feature"],
        "hint": "Use the 'merge' command followed by the name of the branch you want to bring in",
        "output": "Updating 4a8b1c9..9b3d1f0\nFast-forward\n search.js | 45 +++++++++++++++++++++++++++++++++++++++++++++\n 1 file changed, 45 insertions(+)\n create mode 100644 search.js",
        "why": "'git merge <branch>' brings the target branch's commits into your current checked-out branch."
    },
    {
        "concept": "Deleting a completed feature branch",
        "situation": "You already merged 'search-feature' into 'main'. You want to clean up your local branch list.",
        "task": "Safely delete the local branch named 'search-feature':",
        "valid": ["git branch -d search-feature"],
        "hint": "Use 'git branch' with the safe delete flag (-d) and the branch name",
        "output": "Deleted branch search-feature (was 9b3d1f0).",
        "why": "The lowercase '-d' safely deletes the branch only if it has already been merged."
    },
    {
        "concept": "Cloning a repository from GitHub",
        "situation": "You joined a new project. You need to download the full repository from GitHub onto your computer.",
        "task": "Clone the repo at 'https://github.com/example/repo.git':",
        "valid": ["git clone https://github.com/example/repo.git"],
        "hint": "Use the command that creates a full copy of a remote repo: git <subcommand> <url>",
        "output": "Cloning into 'repo'...\nremote: Enumerating objects: 124, done.\nremote: Counting objects: 100% (124/124), done.\nremote: Compressing objects: 100% (68/68), done.\nremote: Total 124 (delta 45), reused 110 (delta 35), pack-reused 0\nReceiving objects: 100% (124/124), 54.20 KiB | 1.20 MiB/s, done.\nResolving deltas: 100% (45/45), done.",
        "why": "'git clone' copies the entire Git database, remote connections, and working files in one command."
    },
    {
        "concept": "Inspecting the last 5 commits concisely",
        "situation": "You want to inspect only the latest 5 commits in concise format.",
        "task": "Show exactly the last 5 commits on one line each:",
        "valid": ["git log -n 5 --oneline", "git log --oneline -n 5", "git log -5 --oneline"],
        "hint": "Combine 'git log' with a count limit flag (-n 5) and the single-line flag (--oneline)",
        "output": "9b3d1f0 (HEAD -> main) add search filtering\n4a8b1c9 add homepage layout\ne2f7b10 initial setup\n8c2a10d configure routes\n7b4e311 create package.json",
        "why": "'-n 5' limits the output count to 5, keeping your terminal uncluttered."
    },
    {
        "concept": "Filtering commit history by author",
        "situation": "You are doing code review and want to view only the commits made by contributor 'Alice'.",
        "task": "Filter git log to show commits by author 'Alice':",
        "valid": ['git log --author="Alice"', "git log --author='Alice'", "git log --author=Alice"],
        "hint": "Pass the author filter flag to git log: git log --author=\"...\"",
        "output": "commit 8c2a10d5e1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6\nAuthor: Alice <alice@example.com>\nDate:   Tue Nov 3 17:15:00 2026 +0530\n\n    configure routes",
        "why": "'--author' filters history by author name or email pattern."
    },
    {
        "concept": "Checking remote repository URLs",
        "situation": "You want to verify which GitHub repository URLs your project is connected to for fetching and pushing.",
        "task": "List all configured remote connections with their full URLs:",
        "valid": ["git remote -v", "git remote --verbose"],
        "hint": "Use 'git remote' with the verbose flag (-v or --verbose)",
        "output": "origin  https://github.com/example/my-project.git (fetch)\norigin  https://github.com/example/my-project.git (push)",
        "why": "'git remote -v' shows the exact fetch and push URLs mapped to the 'origin' remote alias."
    },
    {
        "concept": "Renaming a local branch cleanly",
        "situation": "You created a branch called 'search-ui' but your team's convention requires 'feature-search'. You want to rename it without losing commits.",
        "task": "Rename the current branch to 'feature-search':",
        "valid": ["git branch -m feature-search", "git branch -m search-ui feature-search"],
        "hint": "Use 'git branch' with the move/rename flag (-m) followed by the new branch name",
        "output": "(Renamed branch to 'feature-search' — HEAD and all commit history are preserved)",
        "why": "The '-m' flag renames/moves a branch safely while retaining all linked commit references."
    }
]

CHALLENGES_HIGH = [
    {
        "concept": "Safely undoing a pushed commit",
        "situation": "You pushed commit 'a3f9c12' to main and teammates already pulled it.\n  It has a bug. You cannot use git reset because that would rewrite\n  history that your teammates already have.",
        "task": "Create a new commit that undoes commit 'a3f9c12' without rewriting history:",
        "valid": ["git revert a3f9c12", "git revert a3f9c12 --no-edit", "git revert --no-edit a3f9c12"],
        "hint": "Use the command that creates an inverse commit to safely undo changes: git <subcommand> <commit-id>",
        "output": "[main d8e4a21] Revert \"introduce broken payment api\"\n 1 file changed, 2 insertions(+), 8 deletions(-)",
        "why": "git revert doesn't erase the bad commit — it creates a new one that undoes it. Safe for shared branches."
    },
    {
        "concept": "Saving unfinished work before switching branches",
        "situation": "You're halfway through writing new code on 'feature' branch.\n  An urgent bug was just reported on 'main'. You need to switch branches\n  but you can't commit unfinished code.",
        "task": "Temporarily save your uncommitted changes so the workspace is clean:",
        "valid": ["git stash", "git stash save", "git stash push"],
        "hint": "A 5-letter command that shelves your uncommitted changes into a temporary drawer",
        "output": "Saved working directory and index state WIP on feature: 4a8b1c9 work in progress",
        "why": "git stash shelves your in-progress changes. Your workspace is clean, you switch to main, fix the bug, then come back."
    },
    {
        "concept": "Restoring stashed work after fixing the bug",
        "situation": "You fixed the urgent bug on main. Now you're back on 'feature' branch.\n  Your unfinished code from before is still in the stash.\n  You want to get it back and remove it from the stash in one step.",
        "task": "Restore and remove the most recent stash entry:",
        "valid": ["git stash pop", "git stash apply"],
        "hint": "Use 'git stash' with the action that applies and drops the entry (like popping a stack)",
        "output": "On branch feature\nChanges not staged for commit:\n  (use \"git add <file>...\" to update what will be committed)\n  (use \"git restore <file>...\" to discard changes in working directory)\n\tmodified:   server.py\n\nDropped refs/stash@{0} (7c1a48d89f81a6c5d4e3f2a1b0c9d8e7f6a5b4c3)",
        "why": "git stash pop applies the stashed changes back to your working directory and removes the stash entry."
    },
    {
        "concept": "Marking a release version with a lightweight tag",
        "situation": "Your team just finished testing v2.0 of the app.\n  You want to mark the current commit as an official release\n  so the team can always refer back to exactly this version.",
        "task": "Create a lightweight tag named 'v2.0' on the current commit:",
        "valid": ["git tag v2.0", "git tag -a v2.0 -m 'v2.0'", 'git tag -a v2.0 -m "v2.0"'],
        "hint": "Use the tag command followed by the version name: git <subcommand> <tagname>",
        "output": "(Created lightweight tag 'v2.0' pointing to commit 4a8b1c9 — verifiable with 'git tag')",
        "why": "Tags are permanent named pointers to specific commits. Use them for version releases so you can always find them."
    },
    {
        "concept": "Creating an annotated tag with metadata and message",
        "situation": "For an official public production release, you want to attach author, date, and a release description message 'production launch'.",
        "task": "Create an annotated tag 'v1.0' with message 'production launch':",
        "valid": [
            'git tag -a v1.0 -m "production launch"',
            "git tag -a v1.0 -m 'production launch'",
            'git tag -a v1.0 -m"production launch"'
        ],
        "hint": "Use 'git tag' with the annotated flag (-a) and message flag (-m)",
        "output": "(Created annotated tag 'v1.0' with metadata and message \"production launch\")",
        "why": "Annotated tags (-a) store complete cryptographic object data including tagger info and message."
    },
    {
        "concept": "Unstaging a file without discarding local edits",
        "situation": "You accidentally ran 'git add config.json'. You do NOT want config.json in the upcoming commit,\n  but you want to keep all the changes you wrote in the file on disk.",
        "task": "Unstage 'config.json' while preserving its changes on disk:",
        "valid": [
            "git restore --staged config.json",
            "git reset HEAD config.json",
            "git reset config.json"
        ],
        "hint": "Use 'git restore' with the flag that targets staged files: --staged",
        "output": "(Unstaged changes in 'config.json' — file modifications are kept safely on disk in working directory)",
        "why": "'git restore --staged' pulls the file back out of the staging index without altering your file on disk."
    },
    {
        "concept": "Discarding unwanted modifications in working directory",
        "situation": "You made experimental edits in 'style.css' that didn't work out.\n  You haven't staged it yet, and you want to discard your changes and revert 'style.css' back to the last commit.",
        "task": "Discard all uncommitted changes in 'style.css':",
        "valid": ["git restore style.css", "git checkout -- style.css"],
        "hint": "Use the restore command followed by the filename (without --staged)",
        "output": "(Discarded uncommitted local changes in 'style.css' — file restored to clean state from HEAD)",
        "why": "'git restore <file>' discards uncommitted working tree modifications and resets the file to the last committed version."
    },
    {
        "concept": "Amending the latest commit without changing message",
        "situation": "You just made a commit, but realized you forgot to stage 'assets/logo.png'.\n  You staged it with 'git add assets/logo.png' and want to merge it into that latest commit without re-typing the message.",
        "task": "Amend the latest commit keeping its existing commit message:",
        "valid": ["git commit --amend --no-edit", "git commit --amend -C HEAD"],
        "hint": "Combine 'git commit' with the amend flag (--amend) and a flag to skip editing the message (--no-edit)",
        "output": "[main 4a8b1c9] add homepage layout\n Date: Wed Nov 4 14:30:00 2026 +0530\n 3 files changed, 52 insertions(+)",
        "why": "'--amend --no-edit' updates the last commit with new staged files while keeping the exact same commit message."
    },
    {
        "concept": "Cherry-picking a specific commit from another branch",
        "situation": "Branch 'experimental' has a bugfix in commit 'c4b1a8f' that you need on 'main' right now without merging the whole branch.",
        "task": "Apply commit 'c4b1a8f' onto your current branch:",
        "valid": ["git cherry-pick c4b1a8f"],
        "hint": "The command is named after picking fruit: git cherry-... followed by the commit SHA",
        "output": "[main 8f1e2d3] fix: resolve critical auth token leak\n Author: Alice <alice@example.com>\n Date: Tue Nov 3 19:40:12 2026 +0530\n 1 file changed, 3 insertions(+), 1 deletion(-)",
        "why": "'git cherry-pick' copies and applies a single specific commit SHA from any branch onto your current branch."
    },
    {
        "concept": "Recovering commits after an accidental reset",
        "situation": "A developer on your team ran 'git reset --hard HEAD~5' by mistake.\n  Five commits appear gone from git log. But Git almost never truly deletes\n  data — there's a hidden timeline you can check.",
        "task": "Show the full timeline of all HEAD movements including the 'lost' ones:",
        "valid": ["git reflog", "git reflog show"],
        "hint": "A 6-letter command short for 'reference log' — Git's flight recorder",
        "output": "4a8b1c9 (HEAD -> main) HEAD@{0}: commit: add homepage layout\ne2f7b10 HEAD@{1}: commit: initial setup\n9b3d1f0 HEAD@{2}: checkout: moving from search-feature to main\nc4b1a8f HEAD@{3}: commit: fix: resolve critical auth token leak",
        "why": "git reflog records every movement of HEAD, including resets. Find the commit SHA and run 'git reset --hard <SHA>' to recover."
    },
    {
        "concept": "Dry-run preview before deleting untracked files",
        "situation": "You have various temporary logs and test scripts scattered in your project. You want to see which untracked files 'git clean' would delete without actually deleting anything yet.",
        "task": "Perform a safe dry-run preview of git clean:",
        "valid": ["git clean -n", "git clean --dry-run", "git clean -nd", "git clean -dn"],
        "hint": "Combine 'git clean' with the dry-run flag (-n or --dry-run)",
        "output": "Would remove debug_test.log\nWould remove temp_cache/\nWould remove scratch.py",
        "why": "'git clean -n' lists untracked files that are candidates for deletion without modifying your filesystem."
    },
    {
        "concept": "Working on multiple branches simultaneously with worktree",
        "situation": "You are deep in a feature branch, but need to check out 'hotfix-branch' in a new folder '../hotfix' to fix a critical bug without stashing or switching.",
        "task": "Add a new linked worktree for 'hotfix-branch' at '../hotfix':",
        "valid": ["git worktree add ../hotfix hotfix-branch", "git worktree add ../hotfix"],
        "hint": "Use 'git worktree add' followed by the destination path ('../hotfix') and the branch name ('hotfix-branch')",
        "output": "Preparing worktree (checking out 'hotfix-branch')\nHEAD is now at 8f1e2d3 fix: resolve critical auth token leak",
        "why": "'git worktree add' links a second working directory to your repository, allowing you to build and test multiple branches at once."
    }
]

def run_arena_level(level_name, challenges, level_color):
    clear_screen()
    print(f"{level_color}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
    print(f"║   🎯 PRACTICE ARENA: {level_name:<45}║")
    print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print(f"{Color.DIM}  Type 'hint' if you need a clue. Type '0' or 'menu' anytime to return to Main Menu.{Color.RESET}\n")

    score = 0
    active_challenges = list(challenges)
    random.shuffle(active_challenges)
    total = len(active_challenges)

    for i, ch in enumerate(active_challenges, 1):
        clear_screen()
        print(f"{level_color}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"║   🎯 PRACTICE ARENA: {level_name:<45}║")
        print(f"╚════════════════════════════════════════════════════════════════════╝{Color.RESET}")
        print(f"\n{level_color}{Color.BOLD}── Challenge {i}/{total}: {ch['concept']} ──────────────{Color.RESET}")

        situation_text = ch.get("situation") or ch.get("human_story", "")
        print(f"\n{Color.BOLD}Situation:{Color.RESET}\n  {situation_text}")
        print(f"\n{Color.YELLOW}{Color.BOLD}Your task:{Color.RESET} {ch['task']}")

        attempts = 0
        max_attempts = 2
        while attempts < max_attempts:
            print(f"\n{Color.DIM}[Type your command, 'hint', or '0' for Menu]{Color.RESET}")
            user_cmd = prompt_input(f"{Color.BOLD}{Color.CYAN}$ {Color.RESET}").strip()

            if user_cmd.lower() in ["0", "menu", "home", "back", "exit", "q"]:
                print(f"\n{Color.YELLOW}🏠 Returning to Main Menu...{Color.RESET}\n")
                time.sleep(0.5)
                return False

            if user_cmd.lower() == "hint":
                print(f"  {Color.YELLOW}💡 Clue:{Color.RESET} {ch['hint']}")
                continue

            if not user_cmd:
                continue

            # Normalize whitespace and quote style
            normalized = " ".join(user_cmd.split())
            alt_normalized = normalized.replace("'", '"')
            alt_valid = [v.replace("'", '"') for v in ch["valid"]]
            is_valid = normalized in ch["valid"] or alt_normalized in alt_valid

            if is_valid:
                spinner(f"Simulating '$ {user_cmd}'", duration=0.6, color=Color.GREEN)
                anim_correct()
                points = 100 if attempts == 0 else 50
                _record_concept_mastered("git arena command")
                score += points
                print(f"\n{Color.GREEN}{Color.BOLD}✅ Correct command! Nicely done.{Color.RESET}\n")
                if "output" in ch:
                    print(f"{Color.CYAN}{Color.BOLD}🖥️ Simulated Terminal Output:{Color.RESET}")
                    print(f"{Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}")
                    print(f"{ch['output']}")
                    print(f"{Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}\n")
                print(f"  {Color.DIM}💡 Why this works: {ch['why']}{Color.RESET}\n")
                break
            else:
                attempts += 1
                anim_wrong()
                if attempts < max_attempts:
                    print(f"\n{Color.RED}❌ Not quite (Attempt 1 of 2).{Color.RESET}  💡 Clue: {ch['hint']}")
                else:
                    expected_answer = ch["valid"][0]
                    print(f"\n{Color.RED}{Color.BOLD}❌ Out of attempts (2/2 failed). The command was:{Color.RESET} {Color.GREEN}{Color.BOLD}{expected_answer}{Color.RESET}\n")
                    if "output" in ch:
                        print(f"{Color.CYAN}{Color.BOLD}🖥️ What this command outputs:{Color.RESET}")
                        print(f"{Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}")
                        print(f"{ch['output']}")
                        print(f"{Color.WHITE}─────────────────────────────────────────────────────────────{Color.RESET}\n")
                    print(f"  {Color.DIM}💡 Why this works: {ch['why']}{Color.RESET}\n")

        time.sleep(1.2)

    max_possible = total * 100
    print(f"\n{Color.BOLD}{Color.MAGENTA}═══════════════════════════════════════════════════")
    print(f"   {level_name} LEVEL FINISHED! Final Score: {score}/{max_possible}")
    if score >= max_possible * 0.8:
        print("   🏆 Rank: Champion! Your terminal muscle memory is exceptional!")
    elif score >= max_possible * 0.5:
        print("   ⭐ Rank: Solid Developer! Great progress, keep building the habit!")
    else:
        print("   🌱 Rank: Apprentice. Play again or check 'Git for Humans' to level up!")
    print(f"═══════════════════════════════════════════════════{Color.RESET}\n")
    
    print(f"  {Color.YELLOW}[1] 🔄 Play Another Difficulty Level{Color.RESET}")
    print(f"  {Color.CYAN}[0] 🏠 Return to Main Menu{Color.RESET}\n")
    nxt = prompt_input(f"{Color.BOLD}Choose [1 or 0]: {Color.RESET}").strip().lower()
    if nxt in ["1", "replay", "r"]:
        return True
    return False

def mode_command_arena():
    while True:
        clear_screen()
        print(f"{Color.GREEN}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print("║        🎯 MODE 2: 'TYPE THE COMMAND' HANDS-ON PRACTICE ARENA       ║")
        print("╚════════════════════════════════════════════════════════════════════╝\n")
        print_slow("Reading won't build muscle memory — typing real commands will!", 0.012, Color.CYAN)
        print_slow("No matter your background, you'll learn Git step-by-step through real scenarios.\n", 0.012, Color.WHITE)
        
        print(f"{Color.BOLD}CHOOSE YOUR DIFFICULTY LEVEL:{Color.RESET}\n")
        print(f"  {Color.GREEN}[1] 🌱 LOW / EASY (Zero Git Knowledge / Absolute Beginner){Color.RESET}")
        print("      • Friendly gaming & real-life analogies for someone who has never touched Git.")
        print("      • Helpful on-screen hints displayed upfront. High success rate & confidence boost!\n")
        
        print(f"  {Color.YELLOW}[2] ⚔️ MEDIUM (Apprentice Developer / Everyday Workflow){Color.RESET}")
        print("      • Branching, pushing to GitHub, pulling teammate changes, staging files.")
        print("      • Smart hints available on demand or after your first attempt.\n")
        
        print(f"  {Color.RED}[3] 🔥 HIGH (Git Ninja / Emergency Survival){Color.RESET}")
        print("      • Disaster recovery: git revert, stashing, reflog time-machine, release tags.")
        print("      • Strict test of real-world terminal muscle memory under pressure.\n")
        
        print(f"  {Color.CYAN}[0] 🏠 Return to Main Menu{Color.RESET}\n")
        
        diff_choice = prompt_input(f"{Color.BOLD}Select Difficulty [1 / 2 / 3] or 0 for Main Menu: {Color.RESET}").strip().lower()
        if diff_choice in ["0", "menu", "home", "back", "q", "exit"]:
            print(f"\n{Color.YELLOW}🏠 Returning to Main Menu...{Color.RESET}\n")
            time.sleep(0.5)
            return
        
        if diff_choice == "1":
            level_name = "LOW / EASY (BEGINNER)"
            challenges = CHALLENGES_LOW
            color = Color.GREEN
        elif diff_choice == "2":
            level_name = "MEDIUM (APPRENTICE)"
            challenges = CHALLENGES_MEDIUM
            color = Color.YELLOW
        elif diff_choice == "3":
            level_name = "HIGH (GIT NINJA)"
            challenges = CHALLENGES_HIGH
            color = Color.RED
        else:
            print(f"{Color.RED}Please choose 1, 2, 3 or 0!{Color.RESET}")
            time.sleep(1)
            continue
        
        should_continue = run_arena_level(level_name, challenges, color)
        if not should_continue:
            return



def mode_git_arcade():
    while True:
        clear_screen()
        print(BANNER)
        _show_session_header(subject="git")
        print(f"{Color.BOLD}  🐙 GIT LAB COMPANION: 1BCSL307A — Choose your learning mode:{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 🐣  'Git for Humans' (10-Chapter Visual Concepts)")
        print(f"  {Color.GREEN}[2]{Color.RESET} 🎯  Hands-on Command Practice (36 Challenges)")
        print(f"  {Color.CYAN}[3]{Color.RESET} 🎓  Viva Prep & Conceptual Q&A (25 High-Yield Questions)")
        print(f"  {Color.RED}[4]{Color.RESET} 🚨  Real-World Scenarios & Recovery Guide (8 Common Fixes)")
        print(f"  {Color.BLUE}[5]{Color.RESET} 📚  12-Step Practical Lab & Workflow Cheatbook")
        print(f"  {Color.MAGENTA}[6]{Color.RESET} 🧬  Git Internals & Architecture Masterclass")
        print(f"  {Color.WHITE}[7]{Color.RESET} ⚡  Show My Configured Git Aliases")
        print(f"  {Color.GREEN}[8]{Color.RESET} 🧪  Interactive Command Sandbox & Safety Checker")
        print(f"  {Color.DIM}[0]{Color.RESET} ⬅️   Back to Main Menu\n")

        choice = prompt_input(f"{Color.BOLD}Enter your choice [0 - 8]: {Color.RESET}").strip()

        if choice == "1":
            mode_git_for_humans()
        elif choice == "2":
            mode_command_arena()
        elif choice == "3":
            mode_viva_gauntlet()
        elif choice == "4":
            mode_disaster_recovery()
        elif choice == "5":
            mode_vtu_cheatbook()
        elif choice == "6":
            mode_git_internals()
        elif choice == "7":
            clear_screen()
            print(f"\n{Color.YELLOW}{Color.BOLD}⚡ YOUR SUPERCHARGED GIT ALIASES:{Color.RESET}\n")
            print(f"  {Color.CYAN}git st{Color.RESET}    -> Instant status check")
            print(f"  {Color.CYAN}git lg{Color.RESET}    -> Clean, one-line commit log")
            print(f"  {Color.CYAN}git files{Color.RESET} -> View commits with file names and stats")
            print(f"  {Color.CYAN}git last{Color.RESET}  -> Deep inspection of the latest commit\n")
            prompt_input(f"{Color.DIM}Press Enter to return...{Color.RESET}")
        elif choice == "8":
            mode_git_command_sandbox()
        elif choice in ("0", "b", "back", "exit"):
            break


