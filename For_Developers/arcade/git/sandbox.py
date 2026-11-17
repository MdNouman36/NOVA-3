# pyright: reportMissingImports=false
"""
arcade.git.sandbox — Universal Git Command Sandbox and Danger Radar.
"""
try:
    from arcade.core import Color, clear_screen, prompt_input  # type: ignore
    from arcade.session import _record_concept_mastered, _unlock_badge  # type: ignore
except (ImportError, ValueError):
    from ..core import Color, clear_screen, prompt_input  # type: ignore
    from ..session import _record_concept_mastered, _unlock_badge  # type: ignore

GIT_CORE_SUBCOMMANDS = {
    "add": ("Stages file changes from the working directory into the Staging Area (Index) for the next commit snapshot.", "CAUTION", 3.0),
    "am": ("Applies a series of patches from an email mailbox (mbox) into the current branch.", "CAUTION", 4.0),
    "annotate": ("Annotates file lines with commit information (historical alias for git blame).", "SAFE", 0.0),
    "apply": ("Applies a diff/patch file to files in the working directory or staging index without creating a commit.", "CAUTION", 4.0),
    "archive": ("Creates an archive (zip or tar) containing the files from a named repository tree/commit.", "SAFE", 0.5),
    "bisect": ("Uses binary search through commit history to find the exact commit that introduced a bug.", "SAFE", 1.0),
    "blame": ("Annotates each line in a file with the author, commit hash, and timestamp of who last modified it.", "SAFE", 0.0),
    "branch": ("Lists, creates, renames, or deletes branches.", "SAFE", 2.0),
    "bundle": ("Packages repository objects and references into a single portable archive file.", "SAFE", 1.0),
    "cat-file": ("Plumbing command: provides content, type, or size information for repository objects in .git/objects.", "SAFE", 0.0),
    "check-attr": ("Displays gitattributes information for specified file paths.", "SAFE", 0.0),
    "check-ignore": ("Debugs gitignore rules by showing which pattern caused a file to be ignored.", "SAFE", 0.0),
    "check-mailmap": ("Shows canonical names and email addresses of contacts according to .mailmap.", "SAFE", 0.0),
    "check-ref-format": ("Ensures that a reference name (branch or tag name) conforms to Git naming rules.", "SAFE", 0.0),
    "checkout": ("Switches branches or restores working tree files to match a commit snapshot.", "CAUTION", 4.0),
    "checkout-index": ("Copies files from the staging index to the working tree.", "CAUTION", 5.0),
    "cherry": ("Finds commits yet to be applied to upstream branch.", "SAFE", 0.0),
    "cherry-pick": ("Applies the changes introduced by an existing commit onto your current branch.", "CAUTION", 4.0),
    "clean": ("Deletes untracked files and directories from the working tree.", "DANGER", 9.0),
    "clone": ("Clones a repository into a newly created directory, checking out the default branch.", "SAFE", 0.5),
    "column": ("Displays data in formatted terminal columns.", "SAFE", 0.0),
    "commit": ("Records changes staged in the index as a permanent new snapshot in repository history.", "CAUTION", 3.5),
    "commit-graph": ("Writes and verifies Git commit-graph files to accelerate commit graph walks.", "SAFE", 1.0),
    "commit-tree": ("Plumbing command: creates a new commit object based on a tree object and parent commit SHAs.", "CAUTION", 4.0),
    "config": ("Gets, sets, or lists repository or global configuration options.", "SAFE", 1.0),
    "count-objects": ("Counts unpacked object files and reports disk consumption.", "SAFE", 0.0),
    "credential": ("Retrieves and stores user credentials for remote operations.", "SAFE", 1.0),
    "describe": ("Gives an object a human-readable name based on an available tag (e.g. v1.2-4-g1a2b3c).", "SAFE", 0.0),
    "diff": ("Shows line-by-line changes between commits, commit and working tree, or staged changes.", "SAFE", 0.0),
    "diff-files": ("Plumbing command: compares files in the working tree and the index.", "SAFE", 0.0),
    "diff-index": ("Plumbing command: compares a tree object to the index or working tree.", "SAFE", 0.0),
    "diff-tree": ("Plumbing command: compares the content and mode of blobs found via two tree objects.", "SAFE", 0.0),
    "difftool": ("Launches an external visual diff tool (e.g. VS Code, Meld, Beyond Compare) to show differences.", "SAFE", 0.0),
    "fast-export": ("Git data exporter: dumps repository history in a format suitable for piping into fast-import.", "SAFE", 0.5),
    "fast-import": ("Backend for fast Git data importers, streaming commits and trees into the repository.", "CAUTION", 6.0),
    "fetch": ("Downloads objects, commits, and tags from a remote repository without merging them into local branches.", "SAFE", 1.0),
    "filter-branch": ("Rewrites Git revision history across all or selected branches (e.g. removing sensitive files).", "DANGER", 9.5),
    "fmt-merge-msg": ("Produces a standard merge commit message from annotations.", "SAFE", 0.0),
    "for-each-ref": ("Plumbing command: iterates over all references and prints formatted metadata.", "SAFE", 0.0),
    "format-patch": ("Prepares each commit as an email-ready patch file formatted with mbox headers.", "SAFE", 0.5),
    "fsck": ("Verifies the connectivity and cryptographic validity of all objects in the Git database.", "SAFE", 0.0),
    "gc": ("Runs Garbage Collection: cleans up unnecessary files and optimizes the local repository database.", "SAFE", 2.0),
    "grep": ("Searches tracked files, staged index, or historical commits for text or regular expressions.", "SAFE", 0.0),
    "hash-object": ("Computes the object ID (SHA-1/SHA-256 hash) for a file and optionally writes it to .git/objects.", "SAFE", 0.5),
    "help": ("Displays manual and help documentation for Git commands.", "SAFE", 0.0),
    "hook": ("Runs or manages Git repository lifecycle automation hooks.", "SAFE", 1.0),
    "init": ("Initializes an empty Git repository or reinitializes an existing repository.", "SAFE", 1.0),
    "instaweb": ("Instantly starts a local lighttpd/apache web server and opens a web browser to browse GitWeb.", "SAFE", 0.5),
    "interpret-trailers": ("Parses or adds structured trailers (like Signed-off-by, Co-authored-by) to commit messages.", "SAFE", 0.5),
    "log": ("Shows commit logs, commit author information, commit dates, and branch topology graphs.", "SAFE", 0.0),
    "ls-files": ("Plumbing command: lists all tracked, untracked, ignored, or staged files in the index.", "SAFE", 0.0),
    "ls-remote": ("Lists references (branches, tags, PR refs) available in a remote repository without downloading them.", "SAFE", 0.0),
    "ls-tree": ("Plumbing command: lists the contents of a tree object (mode, type, SHA, filename).", "SAFE", 0.0),
    "maintenance": ("Registers and runs background repository maintenance tasks (prefetch, gc, commit-graph).", "SAFE", 1.0),
    "merge": ("Joins two or more development histories together into the current active branch.", "CAUTION", 4.5),
    "merge-base": ("Finds the best common ancestor commit between two branches for three-way merging.", "SAFE", 0.0),
    "merge-file": ("Runs a three-way file merge on three files.", "CAUTION", 3.0),
    "merge-tree": ("Plumbing command: performs a 3-way merge in memory without touching the index or working tree.", "SAFE", 0.0),
    "mergetool": ("Runs an external visual merge conflict resolution tool to resolve conflicted files.", "CAUTION", 3.0),
    "mktag": ("Creates a tag object with cryptographic validation.", "SAFE", 1.0),
    "mktree": ("Plumbing command: builds a tree object from ls-tree formatted text input.", "SAFE", 0.5),
    "mv": ("Moves or renames a tracked file, directory, or symlink and stages the change in the index.", "CAUTION", 2.5),
    "name-rev": ("Finds symbolic names (e.g. tags or branch tips) for given commit hashes.", "SAFE", 0.0),
    "notes": ("Adds, inspects, or removes commit notes/annotations without changing commit SHAs.", "SAFE", 1.5),
    "pack-objects": ("Creates a packed archive of repository objects to save disk space and network bandwidth.", "SAFE", 1.0),
    "pack-refs": ("Packs loose reference files into a single packed-refs file for faster lookups.", "SAFE", 1.0),
    "patch-id": ("Computes unique ID for a patch, allowing identification of cherry-picked commits.", "SAFE", 0.0),
    "prune": ("Prunes all unreachable objects from the object database.", "DANGER", 8.0),
    "pull": ("Fetches from and immediately integrates (merges or rebases) with another repository or branch.", "CAUTION", 4.0),
    "push": ("Updates remote refs along with associated objects to synchronize local commits to GitHub/remote.", "CAUTION", 4.5),
    "range-diff": ("Compares two commit ranges (e.g. two versions of a rebased patch series).", "SAFE", 0.0),
    "read-tree": ("Plumbing command: reads tree information into the index.", "CAUTION", 5.0),
    "rebase": ("Reapplies commits on top of another base tip, or interactively squashes/edits commit history.", "DANGER", 8.5),
    "reflog": ("Manages and displays the reference log — records every movement of HEAD and branch tips.", "SAFE", 0.0),
    "remote": ("Manages the set of tracked remote repositories (nicknames, fetch/push URLs, default branches).", "SAFE", 1.0),
    "repack": ("Packs unpacked objects in a repository into packfiles.", "SAFE", 1.0),
    "replace": ("Creates replacement refs for Git objects, allowing substituting objects without rewriting history.", "CAUTION", 6.0),
    "rerere": ("Reuse Recorded Resolution: remembers how you resolved a merge conflict and resolves it automatically.", "SAFE", 1.0),
    "reset": ("Resets current HEAD to the specified state, optionally modifying index and working tree.", "CAUTION", 5.0),
    "restore": ("Restores specified paths in the working tree or staging index from a chosen commit/index.", "CAUTION", 4.0),
    "revert": ("Reverts existing commits by creating new inverse commits that subtract the changes.", "SAFE", 2.0),
    "rev-list": ("Plumbing command: lists commit objects in reverse chronological order.", "SAFE", 0.0),
    "rev-parse": ("Plumbing command: parses parameters, outputs commit SHAs, and identifies repository paths.", "SAFE", 0.0),
    "rm": ("Removes files from the working tree and from the staging index.", "CAUTION", 4.0),
    "shortlog": ("Summarizes git log output grouped by commit author, showing commit counts and titles.", "SAFE", 0.0),
    "show": ("Shows various types of objects (commits with diff, tags, trees, blobs).", "SAFE", 0.0),
    "show-branch": ("Shows branches and their commit divergence in a visual column format.", "SAFE", 0.0),
    "show-ref": ("Plumbing command: lists references in a local repository.", "SAFE", 0.0),
    "sparse-checkout": ("Reduces working tree size by checking out only a subset of directories in large monorepos.", "CAUTION", 3.0),
    "stage": ("Synonym for git add.", "CAUTION", 3.0),
    "stash": ("Temporarily shelves (stashes) modified and staged tracking changes for a clean working directory.", "CAUTION", 2.0),
    "status": ("Shows the working tree status: staged, modified, and untracked files.", "SAFE", 0.0),
    "stripspace": ("Removes unnecessary whitespace from text or commit messages.", "SAFE", 0.0),
    "submodule": ("Initializes, updates, or inspects nested Git repositories inside the parent repository.", "CAUTION", 4.0),
    "switch": ("Switches to a specified branch or creates and switches to a new branch.", "SAFE", 1.5),
    "symbolic-ref": ("Plumbing command: reads, modifies, and deletes symbolic references like HEAD.", "CAUTION", 4.0),
    "tag": ("Creates, lists, deletes, or verifies a tag object signed with GPG or annotated.", "SAFE", 1.0),
    "update-index": ("Plumbing command: registers file changes directly into the staging index.", "CAUTION", 5.0),
    "update-ref": ("Plumbing command: updates the object name stored in a ref safely.", "CAUTION", 6.0),
    "var": ("Displays a Git logical variable (e.g. GIT_AUTHOR_IDENT, GIT_EDITOR, GIT_PAGER).", "SAFE", 0.0),
    "verify-commit": ("Checks the GPG cryptographic signature of commits.", "SAFE", 0.0),
    "verify-pack": ("Verifies packed Git archive files (.pack) for internal corruption.", "SAFE", 0.0),
    "verify-tag": ("Checks the GPG cryptographic signature of tags.", "SAFE", 0.0),
    "version": ("Displays the currently installed Git version.", "SAFE", 0.0),
    "whatchanged": ("Historical alias for git log --raw: shows what commits changed which files.", "SAFE", 0.0),
    "worktree": ("Manages multiple working trees attached to the same repository, allowing parallel branch checkouts.", "SAFE", 2.0),
    "write-tree": ("Plumbing command: creates a tree object from the current staging index.", "SAFE", 1.0)
}

GIT_COMMAND_RADAR_DB = [
    {"id":1,"cmd":"git reset --hard","aliases":["reset --hard","git reset --hard","reset --hard head~1","git reset --hard head~1","reset --hard head","git reset --hard origin/main"],"category":"DANGER","risk_score":10.0,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Can permanently obliterate uncommitted work & rewinds branch history!","summary":"Destructively resets the current branch to a specified commit, wiping all uncommitted modifications in tracked files and clearing the staging index.","detail":"Moves HEAD back to the specified commit AND resets staging index + working tree. Any uncommitted code in tracked files is DISCARDED with no native undo.","simulated_output":"$ git reset --hard HEAD~1\nHEAD is now at 8b4a2c1 fix(auth): simplify login validator","when_to_use":["When a full experiment failed and you want a 100% clean slate.","To sync your local branch with remote: git reset --hard origin/main.","WARNING: Never run this if you have uncommitted edits you want to keep!"],"mistake_rescue":["1. DO NOT PANIC! Git keeps a secret journal called the REFLOG.","2. Run:  git reflog\n   Find the commit right before the reset (e.g. HEAD@{1}: commit: My cool feature).","3. Recover everything:  git reset --hard HEAD@{1}","4. What about uncommitted edits? Check your IDE Local History:\n   - VS Code: Explorer -> Timeline (bottom left)\n   - PyCharm: Right-click file -> Local History -> Show History\n   - Editor undo buffer: Ctrl+Z (if file is still open in RAM)"]},
    {"id":2,"cmd":"git push --force","aliases":["push --force","git push --force","push -f","git push -f","force push","git push origin main --force","git push origin main -f","git push --force-with-lease"],"category":"DANGER","risk_score":9.5,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Overwrites remote branch history and can DESTROY teammates' commits!","summary":"Forces your local commit history onto the remote server, discarding any divergent commits that exist on remote.","detail":"By default Git rejects pushes if remote has commits you don't have. --force says 'Ignore conflicts; overwrite with mine' — extremely dangerous on shared branches.","simulated_output":"$ git push origin main --force\nTo https://github.com/organization/project.git\n + 9f8e7d6...a1b2c3d main -> main (forced update)","when_to_use":["Only on PERSONAL, PRIVATE feature branches after squashing/rebasing your own commits.","GOLDEN RULE: NEVER force-push to shared branches (main/develop) without team consensus!"],"mistake_rescue":["1. Alert your team on chat immediately!","2. Find the pre-force hash in your local reflog: git reflog","3. Reset to that hash: git reset --hard <original-sha>","4. Force push the correct history: git push --force origin main","5. PRO-TIP: Use 'git push --force-with-lease' — it auto-aborts if someone else pushed!"]},
    {"id":3,"cmd":"git clean -fd","aliases":["clean -fd","git clean -fd","clean -f","git clean -f","clean -xdf","git clean -xdf"],"category":"DANGER","risk_score":9.0,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Permanently deletes untracked files & folders with ZERO Git backup!","summary":"Recursively deletes all untracked files (-f) and directories (-d) from your project folder.","detail":"Untracked files = files never added to Git. Git has NO snapshot of them so they cannot be recovered via reflog once deleted.","simulated_output":"$ git clean -fd\nRemoving build/\nRemoving temp_test_results.log\nRemoving scratchpad.py","when_to_use":["When cleaning up compiled build artifacts and temp junk.","ALWAYS do a dry run first:  git clean -nd  (-n previews without deleting!)"],"mistake_rescue":["1. CRITICAL: git reflog CANNOT recover untracked files!","2. Check IDE Local History: VS Code Timeline or PyCharm Local History -> Revert.","3. Check your OS Recycle Bin / Trash immediately.","4. NEXT TIME: Run 'git clean -nd' first (dry run previews everything that WOULD be deleted)"]},
    {"id":4,"cmd":"git branch -D","aliases":["branch -D","git branch -D","branch -d","git branch -d","git branch --delete"],"category":"DANGER","risk_score":8.5,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Force-deletes a branch even if its commits are completely unmerged!","summary":"Forcefully deletes a branch reference, ignoring whether its changes were merged.","detail":"Lowercase -d refuses if unmerged. Uppercase -D (--delete --force) bypasses all safety checks.","simulated_output":"$ git branch -D experiment-ml\nDeleted branch experiment-ml (was e4b3a21).","when_to_use":["Only when you are 100% sure the branch work is permanently abandoned.","Use 'git branch -d' (lowercase) for safe everyday deletions."],"mistake_rescue":["1. RELAX! Commits still exist — only the branch LABEL was deleted.","2. Notice the output: 'was e4b3a21' — that commit hash is still in the repo!","3. Run git reflog to find the last commit on that branch.","4. Recreate it instantly:  git checkout -b experiment-ml e4b3a21","5. Your entire branch history is 100% restored!"]},
    {"id":5,"cmd":"git rebase -i","aliases":["rebase","git rebase","rebase -i","git rebase -i","git rebase -i head~3","rebase -i head~3","git rebase origin/main"],"category":"DANGER","risk_score":8.5,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Rewrites commit history by replaying, editing, squashing commits!","summary":"Interactive editor to reorder, squash, edit, or drop commits in your branch history.","detail":"Rebasing creates brand-new commit SHAs. Done on shared branches = all collaborators desynchronized. Done wrong = complex merge conflicts or dropped commits.","simulated_output":"$ git rebase -i HEAD~3\n[detached HEAD 7a8b9c0] feat: polished login flow\nSuccessfully rebased and updated refs/heads/feature-auth.","when_to_use":["To clean up messy WIP commits into logical ones before a Pull Request.","RULE: NEVER rebase commits already pushed to a shared/public branch!"],"mistake_rescue":["1. Mid-rebase confusion?  git rebase --abort  (restores branch to pre-rebase state instantly!)","2. Rebase already finished and scrambled history?\n   Run: git reflog\n   Find the entry right before 'rebase (start)'\n   Run: git reset --hard HEAD@{N}  to restore your pre-rebase history instantly!"]},
    {"id":6,"cmd":"git checkout .","aliases":["checkout .","git checkout .","restore .","git restore .","checkout -- .","git checkout -- ."],"category":"DANGER","risk_score":8.0,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Discards ALL unstaged modifications in tracked files with no Git undo!","summary":"Reverts all modified tracked files back to the last committed snapshot, wiping recent uncommitted edits.","detail":"Overwrites working tree files with the index copy. Edits that were never committed are unrecoverable through Git.","simulated_output":"$ git checkout .\nUpdated 3 paths from the index","when_to_use":["When a quick experiment failed completely and you want the clean committed version back."],"mistake_rescue":["1. Git reflog CANNOT recover unstaged edits.","2. Press Ctrl+Z in your code editor if the file is still open in RAM.","3. Check IDE Local History: VS Code Timeline or PyCharm Local History.","4. PRO-TIP: Shelter unsure code with 'git stash' instead — recoverable anytime with 'git stash pop'!"]},
    {"id":7,"cmd":"git stash drop","aliases":["stash drop","git stash drop","stash clear","git stash clear"],"category":"DANGER","risk_score":8.0,"risk_title":"🔴 DANGER ZONE / HIGH RISK","warning":"Permanently deletes a stashed work snapshot from your stash queue!","summary":"Removes a specific stash entry (or all stashes with 'git stash clear') from the stash stack.","detail":"A stash entry is a commit referenced by refs/stash. Dropping removes the reference; commit becomes dangling until GC runs.","simulated_output":"$ git stash drop stash@{0}\nDropped stash@{0} (7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b)","when_to_use":["When you are 100% certain you no longer need that stashed work."],"mistake_rescue":["1. Check your terminal! Git printed the stash hash: (7a8b9c0...)","2. If you caught it:  git stash apply 7a8b9c0","3. If you cleared your screen, find dangling commits:\n   git fsck --no-reflog\n   Inspect with 'git show <hash>', then:  git stash apply <hash>"]},
    {"id":8,"cmd":"git commit --amend","aliases":["commit --amend","git commit --amend","amend","--amend","git commit --amend --no-edit"],"category":"CAUTION","risk_score":5.5,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Rewrites the latest commit hash — only safe on unpushed commits!","summary":"Modifies the most recent commit by combining staged changes and/or updating the commit message.","detail":"Creates a brand-new commit replacing the old tip. If the old commit was already pushed, you'll need --force to push the amended version.","simulated_output":"$ git commit --amend -m \"feat(auth): add google oauth\"\n[main c7d8e9f] feat(auth): add google oauth\n 2 files changed, 45 insertions(+), 3 deletions(-)","when_to_use":["You just committed but forgot a file or made a typo in the message.","Only amend commits NOT yet pushed to GitHub!"],"mistake_rescue":["1. If you amended by mistake: run git reflog","2. Find the entry before the amend: HEAD@{1}","3. Run: git reset --soft HEAD@{1}  (restores original commit, keeps edits staged in green!)"]},
    {"id":9,"cmd":"git reset HEAD~1","aliases":["reset","git reset","reset head~1","git reset head~1","reset --mixed","git reset --mixed"],"category":"CAUTION","risk_score":5.0,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Undoes commits and unstages files, but your code stays safe on disk!","summary":"Moves branch pointer back by one commit and unstages changes — file contents remain untouched.","detail":"This is Git's default reset mode (--mixed). It rewinds HEAD and index but NEVER touches files on disk. Code is 100% safe.","simulated_output":"$ git reset HEAD~1\nUnstaged changes after reset:\nM\tsrc/auth.py\nM\tconfig/settings.json","when_to_use":["When you want to reorganize a commit, split it, or add more files before committing.","The gentlest and safest way to undo a local commit."],"mistake_rescue":["1. Zero code was lost! Files are sitting as modified in your workspace.","2. To restore the original commit:  git reflog -> git reset --hard HEAD@{1}"]},
    {"id":10,"cmd":"git merge","aliases":["merge","git merge","git merge feature","merge --no-ff","git merge --no-ff"],"category":"CAUTION","risk_score":4.5,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Combines branch histories; may produce merge conflicts!","summary":"Joins two branch histories together, creating a merge commit or fast-forwarding HEAD.","detail":"Three-way merge between branch tips and their common ancestor. If both branches edited the same lines, Git marks conflict blocks (<<<<<<) for manual resolution.","simulated_output":"$ git merge feature-billing\nAuto-merging src/app.py\nMerge made by the 'ort' strategy.\n 2 files changed, 97 insertions(+)","when_to_use":["When a feature branch is done and ready to integrate into main."],"mistake_rescue":["1. Stuck in a terrifying conflict you aren't ready for?\n   git merge --abort  (instantly restores files to pre-merge state!)","2. Merge completed but you want to undo it before pushing:\n   git reset --hard HEAD~1"]},
    {"id":11,"cmd":"git push","aliases":["push","git push","git push origin","git push origin main","push -u origin","git push -u origin main"],"category":"CAUTION","risk_score":4.5,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Publishes local commits to GitHub — visible to your entire team!","summary":"Uploads local branch commits to the remote repository and updates remote branch refs.","detail":"Pushes new commit objects, trees, and blobs to the remote server. Collaborators can then fetch and build on your commits.","simulated_output":"$ git push origin main\nWriting objects: 100% (4/4), 620 bytes\nTo https://github.com/developer/oils-project.git\n   1a2b3c4..5d6e7f8  main -> main","when_to_use":["When commits are tested and ready to share with your team or back up to GitHub."],"mistake_rescue":["1. If you pushed a bad commit to a SHARED branch:\n   DO NOT force push! Use safe undo:  git revert <bad-commit-hash>\n   Then:  git push origin main\n   This appends an undo commit without breaking your teammates' repos!"]},
    {"id":12,"cmd":"git pull","aliases":["pull","git pull","git pull origin","git pull origin main","pull --rebase","git pull --rebase"],"category":"CAUTION","risk_score":4.0,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Fetches AND immediately merges remote commits into your branch!","summary":"Runs git fetch to download remote commits, then immediately git merge them into your local branch.","detail":"Convenient shortcut for fetch + merge. If remote has changes conflicting with your local work, merge conflicts can occur.","simulated_output":"$ git pull origin main\nFast-forward\n README.md        | 4 ++--\n 2 files changed, 8 insertions(+), 4 deletions(-)","when_to_use":["At the START of every session to stay in sync with teammates.","Before pushing your branch or opening a Pull Request."],"mistake_rescue":["1. Unexpected conflicts?  git merge --abort","2. Want to fully undo the pull?  git reset --hard ORIG_HEAD\n   (Git auto-saves your pre-pull position in ORIG_HEAD!)"]},
    {"id":13,"cmd":"git cherry-pick","aliases":["cherry-pick","git cherry-pick","git cherry-pick 4a5b6c7"],"category":"CAUTION","risk_score":4.0,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Copies a specific commit from another branch and replays it here!","summary":"Selects one commit from any branch and applies its exact changes as a new commit on your current branch.","detail":"Calculates the patch of the target commit and applies it onto HEAD, creating a new commit SHA.","simulated_output":"$ git cherry-pick 4a5b6c7\n[main 9d8e7f6] hotfix(security): sanitize sql parameters\n 1 file changed, 5 insertions(+), 2 deletions(-)","when_to_use":["Committed to the wrong branch? Switch to the right one, cherry-pick the commit, then reset the wrong branch.","Need one specific bugfix from another branch without merging the whole thing."],"mistake_rescue":["1. Mid-cherry-pick conflict?  git cherry-pick --abort","2. Cherry-picked the wrong commit?  git reset --hard HEAD~1"]},
    {"id":14,"cmd":"git rm --cached","aliases":["rm --cached","git rm --cached","git rm --cached .env"],"category":"CAUTION","risk_score":3.5,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Un-tracks a file from Git while keeping the file on your disk!","summary":"Removes a file from Git's staging index so Git stops tracking it, without deleting the physical file.","detail":"Tells Git: Stop versioning this file, but don't delete it from my computer. Essential for accidentally tracked sensitive files.","simulated_output":"$ git rm --cached config/database.env\nrm 'config/database.env'","when_to_use":["You accidentally committed a .env file, API tokens, or build output and want Git to stop tracking it.","Always add the path to .gitignore RIGHT AFTER!"],"mistake_rescue":["1. Your file was NEVER deleted from disk — it's still there!","2. If you ran it by accident:  git add config/database.env"]},
    {"id":15,"cmd":"git commit","aliases":["commit","git commit","commit -m","git commit -m","git commit -am"],"category":"CAUTION","risk_score":3.5,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Creates a permanent history snapshot — make sure you are on the right branch!","summary":"Packages all currently staged changes into a permanent version-controlled snapshot with a descriptive message.","detail":"Writes a new commit object: tree pointer, author/committer metadata, timestamp, parent SHA, and your message.","simulated_output":"$ git commit -m \"feat(dsa): implement binary search tree insertion\"\n[main 4f5a6b7] feat(dsa): implement binary search tree insertion\n 2 files changed, 68 insertions(+)","when_to_use":["When you have finished and tested a logical unit of work. Commit often!"],"mistake_rescue":["1. Typo in message?  git commit --amend -m \"better message\"","2. Committed too soon?  git reset --soft HEAD~1  (undoes commit, files stay staged in green!)","3. Wrong branch? Cherry-pick to right branch, then reset HEAD~1 on the wrong branch."]},
    {"id":16,"cmd":"git add","aliases":["add","git add","add .","git add .","add -A","git add -A","git add -p"],"category":"CAUTION","risk_score":3.0,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Stages file changes into the Index ready for the next commit!","summary":"Copies file changes from your working tree into the Staging Area (Index), marking them for the next commit snapshot.","detail":"Creates blob objects for modified files and updates index entries. Untracked files become tracked.","simulated_output":"$ git add src/app.py README.md\n(Files turn green in git status)","when_to_use":["After editing code, stage only the files that belong together in the next logical commit."],"mistake_rescue":["1. Accidentally staged a sensitive file?  git restore --staged <file>\n   Or unstage everything:  git restore --staged .","2. Your code is completely untouched! Files simply go back to unstaged (red) status."]},
    {"id":17,"cmd":"git stash","aliases":["stash","git stash","stash pop","git stash pop","stash list","git stash list","git stash apply"],"category":"CAUTION","risk_score":2.0,"risk_title":"🟡 CAUTION / STATE CHANGE","warning":"Temporarily shelves uncommitted changes so working tree is clean!","summary":"Saves your uncommitted changes onto a temporary clipboard stack, reverting working tree to clean HEAD.","detail":"Creates temporary commit objects storing index + working directory states referenced by refs/stash. Allows safe branch switching.","simulated_output":"$ git stash\nSaved working directory and index state WIP on main: 3a2b1c0 initial work on login\n\n$ git stash pop\nDropped refs/stash@{0} (a1b2c3d...)","when_to_use":["Mid-feature and urgently need to fix a bug on main? Stash -> switch -> fix -> switch back -> stash pop!"],"mistake_rescue":["1. Forgot what you stashed?  git stash list  or  git stash show -p","2. Stash pop has a conflict? Resolve it manually, then run  git stash drop  once satisfied."]},
    {"id":18,"cmd":"git reset --soft","aliases":["reset --soft","git reset --soft","reset --soft head~1","git reset --soft head~1"],"category":"SAFE","risk_score":2.0,"risk_title":"🟢 SAFE & SMART UNDO","warning":"Undoes commits while keeping all edits staged in green — the safest reset!","summary":"Rewinds HEAD back to an earlier commit but leaves ALL changed files staged (green) ready to commit again.","detail":"Only updates the branch HEAD ref pointer. Does not touch staging index or working directory. Perfect for squashing or re-authoring commits.","simulated_output":"$ git reset --soft HEAD~1\n(Silent success - commit undone, changes remain staged in green)","when_to_use":["To combine multiple recent commits into one clean commit.","When you committed too early and want to add more files to the same snapshot."],"mistake_rescue":["1. If you ran it by accident:  git reflog -> git reset --hard HEAD@{1}"]},
    {"id":19,"cmd":"git revert","aliases":["revert","git revert","revert head","git revert head"],"category":"SAFE","risk_score":2.0,"risk_title":"🟢 SAFE PUBLIC UNDO","warning":"Safely undoes a commit by creating a brand-new OPPOSITE commit!","summary":"Applies the exact inverse of a previous commit as a new commit, undoing bugs without rewriting history.","detail":"Unlike reset, revert does NOT alter existing commit history. It appends a new commit subtracting the faulty code. Completely safe for shared branches.","simulated_output":"$ git revert 9f8e7d6\n[main d3e4f5a] Revert \"Add buggy auth middleware\"\n 1 file changed, 2 insertions(+), 18 deletions(-)","when_to_use":["THE SAFEST way to undo a bug already pushed to a shared/public GitHub branch!","Collaborators are unaffected — no history rewrite, no conflicts for them."],"mistake_rescue":["1. Reverted the wrong commit? Simply revert the revert:  git revert d3e4f5a"]},
    {"id":20,"cmd":"git switch","aliases":["switch","git switch","switch -c","git switch -c","checkout -b","git checkout -b"],"category":"SAFE","risk_score":2.0,"risk_title":"🟢 SAFE NAVIGATION","warning":"Switches active branch or creates a new branch!","summary":"Updates HEAD to point to a different branch and updates workspace files to match that branch's latest snapshot.","detail":"Modern Git introduced 'git switch' specifically for branches, separating it from 'git checkout' (which also modifies files).","simulated_output":"$ git switch -c feature-user-profiles\nSwitched to a new branch 'feature-user-profiles'","when_to_use":["Every time you start a new feature or experiment — create a branch to protect main!","Use 'git switch main' to return to your primary branch."],"mistake_rescue":["1. Want to jump back to your previous branch instantly?  git switch -"]},
    {"id":21,"cmd":"git restore --staged","aliases":["restore --staged","git restore --staged","restore --staged .","git restore --staged ."],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE & HELPFUL","warning":"Safely unstages files without touching a single line of code!","summary":"Removes files from the green staging area back to red working directory without touching file contents.","detail":"Restores staging index entry for the path to match HEAD, leaving working directory modifications completely untouched.","simulated_output":"$ git restore --staged src/app.py\n(Silent success - src/app.py is now unstaged)","when_to_use":["When you ran 'git add .' and accidentally included a file not ready to commit yet."],"mistake_rescue":["1. Zero risk! Your code is completely untouched. To re-stage:  git add src/app.py"]},
    {"id":22,"cmd":"git status","aliases":["status","git status","status -s","git status -s"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE & READ-ONLY","warning":"The friendliest Git command — your best friend, run it constantly!","summary":"Displays the state of the working directory and staging area: untracked, modified, and staged files.","detail":"Compares working tree against index and index against HEAD. Computes file hashes to detect modifications. NEVER modifies anything.","simulated_output":"$ git status\nOn branch main\nChanges to be committed:\n\tmodified:   src/app.py\n\nUntracked files:\n\tdata/test_results.csv","when_to_use":["Run this CONSTANTLY! Before add, before commit, before push, after switching branches.","It never modifies or deletes anything. 100% safe anytime."],"mistake_rescue":["1. No rescue needed! Pure read-only lens. Run it as many times as you want!"]},
    {"id":23,"cmd":"git log","aliases":["log","git log","log --oneline","git log --oneline","git log --graph","git log --oneline --graph --all"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE & READ-ONLY","warning":"History viewer — press q to exit the pager!","summary":"Displays chronological commit history with author, date, hash, and commit messages.","detail":"Traverses commit graph backwards from HEAD. Press q to exit the pager if Git opens one.","simulated_output":"$ git log --oneline --graph --all\n* 9b8c7d6 (HEAD -> main) feat(dsa): add AVL tree visualizer\n* 4a5b6c7 fix(java): resolve thread deadlock\n* 1e2f3a4 docs: update lab installation notes","when_to_use":["To review project activity, find commit hashes, or visualize branch topology."],"mistake_rescue":["1. Read-only. Press q to exit the log pager if it appears."]},
    {"id":24,"cmd":"git diff","aliases":["diff","git diff","diff --staged","git diff --staged","git diff head~1"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE & READ-ONLY","warning":"Line-by-line diff viewer; green = addition, red = deletion!","summary":"Displays exact line-by-line additions (+) and subtractions (-) between workspace, staging area, or commits.","detail":"Runs LCS diff algorithm comparing file contents. Completely read-only.","simulated_output":"$ git diff src/calculator.c\n--- a/src/calculator.c\n+++ b/src/calculator.c\n+    if (b == 0) return -1; // protect against division by zero\n     return a / b;","when_to_use":["Before 'git add' or 'git commit' to review every line you modified.","Use 'git diff --staged' to inspect what's already staged."],"mistake_rescue":["1. Read-only. Press q to exit."]},
    {"id":25,"cmd":"git reflog","aliases":["reflog","git reflog"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE — THE TIME MACHINE OF GIT","warning":"Git's black-box flight recorder — records every HEAD movement for 90 days!","summary":"Records every movement of the HEAD pointer (commits, resets, checkouts, merges) over the past 90 days.","detail":"Even 'deleted' branches and 'lost' commits after git reset --hard are logged here by their SHA. The supreme emergency rescue tool.","simulated_output":"$ git reflog\na1b2c3d (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1\ne5f6a7b HEAD@{1}: commit: Add experimental neural search\n9c8d7e6 HEAD@{2}: checkout: moving from feature to main","when_to_use":["When you think you lost code after a reset --hard, deleted branch, or failed rebase.","This is YOUR PRIMARY LIFESAVER for recovering anything!"],"mistake_rescue":["1. Use the printed hash with:  git checkout <hash>  or  git reset --hard <hash>  to bring back anything!"]},
    {"id":26,"cmd":"git blame","aliases":["blame","git blame"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE & READ-ONLY","warning":"The detective tool — annotates each line with its author and commit!","summary":"Annotates each line of a file with the author, timestamp, and commit SHA that last modified that exact line.","detail":"Inspects commit graph and file history to attribute line modifications. Completely harmless and read-only.","simulated_output":"$ git blame src/config.py\na1b2c3d4 (Alice 2026-10-12 14:32:01 +0530  15) MAX_CONNECTIONS = 50\ne5f6a7b8 (Bob   2026-11-01 09:15:20 +0530  16) RETRY_TIMEOUT_SEC = 10","when_to_use":["To understand why a line was written or who to ask about a complex algorithm."],"mistake_rescue":["1. Read-only. Press q to exit."]},
    {"id":27,"cmd":"git remote -v","aliases":["remote","git remote","remote -v","git remote -v"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE & READ-ONLY","warning":"Lists registered cloud repository URLs!","summary":"Lists all registered remote repository nicknames and their fetch/push URLs.","detail":"Reads configuration entries under [remote] in .git/config.","simulated_output":"$ git remote -v\norigin  https://github.com/developer/oils-project.git (fetch)\norigin  https://github.com/developer/oils-project.git (push)","when_to_use":["To verify where your local repo is pointing on GitHub."],"mistake_rescue":["1. Safe and read-only. To fix URL:  git remote set-url origin <new_url>"]},
    {"id":28,"cmd":"git tag","aliases":["tag","git tag","tag -a","git tag -a","git tag -l"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE","warning":"Creates a permanent release version milestone marker on a commit!","summary":"Creates a named, permanent pointer at a specific commit for version releases or lab submissions.","detail":"Annotated tags store tagger metadata, date, optional GPG signature, and message in .git/refs/tags.","simulated_output":"$ git tag -a v1.0.0 -m \"Release version 1.0.0 for lab submission\"\n(Silent success - release marker created)","when_to_use":["To mark software version releases (v1.0, v2.1) or lab submission checkpoints."],"mistake_rescue":["1. Wrong tag? Delete it:  git tag -d v1.0.0"]},
    {"id":29,"cmd":"git bisect","aliases":["bisect","git bisect","bisect start","git bisect start"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE — BINARY SEARCH FOR BUGS","warning":"Binary-searches commit history to find which commit broke the code!","summary":"Checks out midpoint commits and asks you good or bad until the exact breaking commit is isolated.","detail":"O(log N) binary search through your commits. Git checks out midpoints automatically.","simulated_output":"$ git bisect start\n$ git bisect bad\n$ git bisect good v1.0\nBisecting: 6 revisions left to test (roughly 3 steps)\n[3a4b5c6] refactor(cache): switch to redis cluster","when_to_use":["When something worked last week but is broken now across dozens of commits."],"mistake_rescue":["1. Want to abort and return to normal?  git bisect reset"]},
    {"id":30,"cmd":"git clone","aliases":["clone","git clone"],"category":"SAFE","risk_score":0.0,"risk_title":"🟢 100% SAFE","warning":"Downloads a complete copy of a repository to your computer!","summary":"Copies an entire remote Git repository onto your local machine, with full history, all branches, and config.","detail":"Initializes a directory, sets up remote origin tracking, fetches all packfiles, checks out default branch.","simulated_output":"$ git clone https://github.com/organization/oils-project.git\nCloning into 'oils-project'...\nReceiving objects: 100% (184/184), 512.40 KiB | 2.45 MiB/s, done.","when_to_use":["When onboarding to a new project or setting up a repo on a new machine."],"mistake_rescue":["1. Cloned into the wrong folder? Simply delete the newly cloned directory and re-clone."]},
    {"id":31,"cmd":"git init","aliases":["init","git init","git init .","git init -b main","git init --initial-branch=main"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE & REPO CREATION","warning":"Creates a hidden '.git/' administrative directory. Safe, but do NOT run in your user root (C:\\Users) or Desktop!","summary":"Initializes a brand-new, empty Git repository in the current folder, creating the hidden '.git' metadata and object directory.","detail":"Sets up the internal repository skeleton inside '.git/': including 'objects/' (the object store for all commits/blobs), 'refs/heads/' (branch pointers), HEAD pointer file (pointing to your active branch), hooks, and local repository config. It does NOT delete or alter any existing files in your folder.","simulated_output":"$ git init\nInitialized empty Git repository in C:/Users/Student/Documents/my-project/.git/","when_to_use":["When starting a brand-new project from scratch, or when putting an existing project folder under Git version control for the first time.","Run it ONCE at the top-level root folder of your project (never inside subfolders!).","NOTE: You do NOT need to run 'git init' if you cloned a repository using 'git clone' (cloning already initializes Git!)."],"mistake_rescue":["1. WHAT IF YOU RAN 'git init' IN THE WRONG FOLDER? (e.g. your Desktop, Downloads, or entire C:\\Users directory):","   DO NOT PANIC! Git only created a single hidden folder named '.git'. None of your real personal files were modified, moved, or deleted.","2. How to undo 'git init' completely and remove Git tracking from the folder:","   • In PowerShell / Windows Terminal:","     Remove-Item -Recurse -Force .git","   • In Windows Command Prompt (cmd.exe):","     rmdir /s /q .git","   • In Git Bash / Linux / macOS:","     rm -rf .git","3. Boom! The folder is instantly back to being a normal everyday directory with zero Git tracking!"]},
    {"id":32,"cmd":"git config","aliases":["config","git config","git config --list","git config --global user.name","git config --global user.email","git config --list --show-origin"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 SAFE & CONFIGURATION","warning":"Configures author identity, default branch, or custom shortcuts.","summary":"Gets, sets, or lists repository-level and global user configuration settings (author name, email, editor, line endings).","detail":"Reads or writes key-value pairs stored in '~/.gitconfig' (global), '.git/config' (local repo), or system-wide configuration files.","simulated_output":"$ git config --list\nuser.name=Prajwal Chonnad\nuser.email=prajwal@example.com\ninit.defaultbranch=main\ncore.editor=code --wait\ncore.autocrlf=true","when_to_use":["Run 'git config --global user.name' and 'user.email' when setting up Git for the first time on a new computer.","Run 'git config --list' to check all active resolved settings."],"mistake_rescue":["1. Made a typo in your name or email? Simply run the command again with the right value to overwrite it:","   git config --global user.name 'Your Name'","   git config --global user.email 'you@example.com'","2. To remove a configuration key:  git config --global --unset <key>"]},
    {"id":33,"cmd":"git fetch","aliases":["fetch","git fetch","git fetch origin","git fetch --all","git fetch --prune"],"category":"SAFE","risk_score":1.0,"risk_title":"🟢 100% SAFE REMOTE INSPECTION","warning":"100% SAFE. Downloads remote commits and branches without touching or modifying your local working files!","summary":"Downloads objects, commits, and branch refs from a remote repository (GitHub/GitLab) without merging them into your local branches.","detail":"Updates remote-tracking branches (like 'origin/main') in your local '.git' database. Does NOT alter your working directory files or staging area, making it far safer than 'git pull' for previewing remote work.","simulated_output":"$ git fetch origin\nFrom https://github.com/organization/project\n * [new branch]      feature-payment -> origin/feature-payment\n   1a2b3c4..5d6e7f8  main            -> origin/main","when_to_use":["When you want to see what teammates have pushed to GitHub WITHOUT immediately merging or creating conflicts in your local code.","Run before 'git diff main origin/main' to compare incoming changes before integrating."],"mistake_rescue":["1. 'git fetch' is completely safe and read-only for your working directory files.","2. It only updates your remote tracking branches (like origin/main). Nothing in your code was changed."]}

]


def _radar_find(user_query):
    q = user_query.strip().lower()
    if not q:
        return None
    if q.isdigit():
        num = int(q)
        for e in GIT_COMMAND_RADAR_DB:
            if e["id"] == num:
                return e
    norm = q[4:].strip() if q.startswith("git ") else q
    # 1. Exact alias match
    for e in GIT_COMMAND_RADAR_DB:
        for a in e["aliases"]:
            an = a.lower()
            an = an[4:].strip() if an.startswith("git ") else an
            if norm == an or q == a.lower():
                return e
    # 2. Longest prefix match (matches alias + space, sorted by longest alias first)
    matches = []
    for e in GIT_COMMAND_RADAR_DB:
        for a in e["aliases"]:
            an = a.lower()
            an = an[4:].strip() if an.startswith("git ") else an
            if norm == an or norm.startswith(an + " "):
                matches.append((len(an), e))
    if matches:
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[0][1]
    return None


def analyze_universal_git_command(user_query):
    raw = user_query.strip()
    if not raw:
        return None

    # First check pre-indexed catalog
    pre = _radar_find(raw)
    if pre:
        return {
            "raw_cmd": pre["cmd"],
            "subcmd": pre["cmd"].replace("git ", "").split()[0],
            "category": pre["category"],
            "risk_score": pre["risk_score"],
            "risk_title": pre["risk_title"],
            "warning": pre["warning"],
            "summary": pre["summary"],
            "detail": pre.get("detail", pre["summary"]),
            "simulated_output": pre["simulated_output"],
            "when_to_use": pre["when_to_use"],
            "mistake_rescue": pre["mistake_rescue"]
        }

    # Normalize command
    cmd_str = raw
    if cmd_str.lower().startswith("git "):
        cmd_str = cmd_str[4:].strip()

    tokens = cmd_str.split()
    if not tokens:
        return None

    subcmd = tokens[0].lower()
    args = tokens[1:]
    args_str = " ".join(args).lower()

    subcmd_info = GIT_CORE_SUBCOMMANDS.get(subcmd)
    if subcmd_info:
        base_desc, base_cat, base_score = subcmd_info
    else:
        base_desc = f"Executes the Git '{subcmd}' operation with the provided flags."
        base_cat = "CAUTION"
        base_score = 4.0

    cat = base_cat
    score = base_score
    warning = ""
    simulated_output = ""
    when_to_use = []
    mistake_rescue = []

    # Destructive pattern: --hard
    if "--hard" in args_str:
        cat = "DANGER"
        score = 10.0
        warning = "DESTRUCTIVE! Discards ALL uncommitted edits in tracked files & violently rewinds HEAD!"
        simulated_output = f"$ git {cmd_str}\nHEAD is now at 8b4a2c1 fix(auth): simplify login validator"
        when_to_use = [
            "When a local experiment failed completely and you want a 100% clean slate.",
            "NEVER run this if you have uncommitted changes in your editor that you want to keep!"
        ]
        mistake_rescue = [
            "1. DO NOT PANIC! Git records every commit in the secret REFLOG.",
            "2. Run:  git reflog\n   Find the commit hash right before your reset (e.g. HEAD@{1}: commit: My work).",
            "3. Bring it back:  git reset --hard HEAD@{1}",
            "4. For uncommitted edits never committed to Git: check IDE Local History (VS Code Timeline / JetBrains Local History) or Ctrl+Z."
        ]

    # Destructive pattern: force push
    elif subcmd == "push" and any(f in args_str for f in ["--force", "-f", "--force-with-lease"]):
        cat = "DANGER"
        score = 9.5 if "--force-with-lease" not in args_str else 7.5
        warning = "HIGH RISK! Overwrites remote branch history, potentially destroying teammate commits!"
        simulated_output = f"$ git {cmd_str}\nTo https://github.com/organization/project.git\n + 9f8e7d6...a1b2c3d main -> main (forced update)"
        when_to_use = [
            "Only on personal, private feature branches after rebasing/squashing.",
            "NEVER force-push to a shared branch ('main' or 'develop') without team consensus!"
        ]
        mistake_rescue = [
            "1. Alert teammates immediately on Slack/Discord before they pull the rewritten branch!",
            "2. Find the pre-force commit hash via:  git reflog",
            "3. Reset local branch to original commit:  git reset --hard <original-sha>",
            "4. Force push true history back:  git push --force origin <branch>",
            "5. Best practice: Use '--force-with-lease' which refuses if someone else pushed new commits."
        ]

    # Destructive pattern: clean
    elif subcmd == "clean":
        is_dry_run = "-n" in args_str or "--dry-run" in args_str
        if is_dry_run:
            cat = "SAFE"
            score = 0.5
            warning = "Dry-run preview: shows what untracked files WOULD be deleted without touching disk."
            simulated_output = f"$ git {cmd_str}\nWould remove build/\nWould remove temp_test_results.log\nWould remove scratchpad.py"
            when_to_use = ["Always run dry-run first before actual clean!"]
            mistake_rescue = ["No files were touched. Safe to run anytime."]
        else:
            cat = "DANGER"
            score = 9.0
            warning = "PERMANENT DELETION! Removes untracked files with ZERO Git backup!"
            simulated_output = f"$ git {cmd_str}\nRemoving build/\nRemoving temp_test_results.log\nRemoving scratchpad.py"
            when_to_use = ["When purging generated build artifacts or temporary logs not tracked by Git."]
            mistake_rescue = [
                "1. CRITICAL: Because Git never tracked these files, 'git reflog' CANNOT recover them!",
                "2. Check IDE Local History (VS Code Timeline / JetBrains Local History -> Revert).",
                "3. Check OS Recycle Bin / Trash.",
                "4. Always dry-run first with 'git clean -nd'!"
            ]

    # Destructive pattern: branch force delete
    elif subcmd == "branch" and any(f in args_str for f in ["-d", "-d", "--delete"]):
        is_force = "-d" in args or "-d" in tokens
        cat = "DANGER" if is_force else "CAUTION"
        score = 8.5 if is_force else 4.0
        warning = "Force-deletes a branch even if its commits are completely unmerged!" if is_force else "Deletes a merged branch."
        simulated_output = f"$ git {cmd_str}\nDeleted branch feature-experiment (was e4b3a21)."
        when_to_use = ["When abandoning a prototype branch that you'll never need again."]
        mistake_rescue = [
            "1. RELAX! Commits are NOT deleted immediately — only the branch reference label was removed.",
            "2. Look for the hash printed in output ('was e4b3a21') or run:  git reflog",
            "3. Recreate the branch at that exact commit:  git checkout -b feature-experiment e4b3a21",
            "4. Your branch is 100% restored!"
        ]

    # Destructive pattern: filter-branch
    elif subcmd == "filter-branch":
        cat = "DANGER"
        score = 9.8
        warning = "DANGER ZONE! Rewrites the entire Git commit graph across revisions!"
        simulated_output = f"$ git {cmd_str}\nRewrite 3a4b5c6d (1/15) (0 seconds passed)\nRewrite 8e9f0a1b (2/15)\nRef 'refs/heads/main' was rewritten"
        when_to_use = ["When scrubbing an exposed password, token, or large binary from all past Git commits."]
        mistake_rescue = [
            "1. Git keeps original refs backed up under 'refs/original/'.",
            "2. To restore:  git reset --hard refs/original/refs/heads/main",
            "3. Modern replacement: Use 'git-filter-repo' (faster and less prone to corruption)."
        ]

    # Destructive pattern: checkout . / restore .
    elif (subcmd in ("checkout", "restore") and ("." in args or "-- ." in args_str or "*" in args_str)):
        cat = "DANGER"
        score = 8.0
        warning = "Discards all local uncommitted edits in tracked files!"
        simulated_output = f"$ git {cmd_str}\nUpdated 4 paths from the index"
        when_to_use = ["When you made experimental modifications that you want to completely throw away."]
        mistake_rescue = [
            "1. Git never recorded uncommitted edits, so 'git reflog' cannot bring them back.",
            "2. Press 'Ctrl+Z' in your editor if the file buffer is still open in memory.",
            "3. Check IDE Local History (VS Code Timeline / JetBrains Local History).",
            "4. PRO-TIP: Run 'git stash' instead so you can recover anytime with 'git stash pop'!"
        ]

    # Destructive pattern: stash drop / clear
    elif subcmd == "stash" and any(w in args_str for w in ["drop", "clear"]):
        cat = "DANGER"
        score = 8.0
        warning = "Deletes stashed commit snapshots from your stash queue!"
        simulated_output = f"$ git {cmd_str}\nDropped stash@{{0}} (7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b)"
        when_to_use = ["When you are 100% certain you will never need that stashed work again."]
        mistake_rescue = [
            "1. If you just dropped a stash, note the hash in terminal output: '(7a8b9c0...)'.",
            "2. Apply it directly:  git stash apply 7a8b9c0",
            "3. If lost: run  git fsck --no-reflog  to find dangling commits, inspect with 'git show <hash>', and apply!"
        ]

    # Rebase
    elif subcmd == "rebase":
        if "--abort" in args_str:
            cat = "SAFE"
            score = 1.0
            warning = "Aborts conflicted rebase and returns to original branch state."
            simulated_output = f"$ git {cmd_str}\n(Rebase aborted cleanly. Returned to pre-rebase state.)"
            when_to_use = ["When a rebase has too many conflicts and you want to cancel it."]
            mistake_rescue = ["Safe abort. Returns your branch to before rebase began."]
        else:
            cat = "DANGER"
            score = 8.5
            warning = "Rewrites commit history by replaying commits onto a new base!"
            simulated_output = f"$ git {cmd_str}\nFirst, rewinding head to replay your work on top of it...\nApplying: feat(auth): add oauth\nSuccessfully rebased and updated refs/heads/feature."
            when_to_use = [
                "To clean up local commits or maintain a linear commit history before opening a Pull Request.",
                "NEVER rebase commits that have already been pushed to a shared/public branch!"
            ]
            mistake_rescue = [
                "1. If stuck in conflicts mid-rebase:  git rebase --abort",
                "2. If rebase finished and messed up your branch: run  git reflog\n   Find the commit before rebase started (e.g. HEAD@{4}), and run:  git reset --hard HEAD@{4}"
            ]

    # Merge
    elif subcmd == "merge":
        if "--abort" in args_str:
            cat = "SAFE"
            score = 1.0
            warning = "Aborts conflicted merge and restores pre-merge state."
            simulated_output = f"$ git {cmd_str}\n(Merge aborted. Files restored to pre-merge state.)"
            when_to_use = ["When merge conflicts are overwhelming and you want to back out safely."]
            mistake_rescue = ["Safe command. Clears conflict markers and restores files."]
        else:
            cat = "CAUTION"
            score = 4.5
            warning = "Combines branch histories; may produce merge conflicts if both branches edited the same lines."
            simulated_output = f"$ git {cmd_str}\nAuto-merging src/app.py\nMerge made by the 'ort' strategy.\n 2 files changed, 24 insertions(+)"
            when_to_use = ["When a feature branch is complete and ready to be integrated into main."]
            mistake_rescue = [
                "1. If conflicts occur: run  git merge --abort  to undo instantly.",
                "2. If merge already succeeded locally:  git reset --hard HEAD~1"
            ]

    # Check for init
    elif subcmd == "init":
        cat = "SAFE"
        score = 1.0
        warning = "Creates a hidden '.git/' administrative directory. Safe, but do NOT run in your user root (C:\\Users) or Desktop!"
        target_dir = args[0] if args and not args[0].startswith("-") else "my-project"
        simulated_output = f"$ git {cmd_str}\nInitialized empty Git repository in C:/Users/Student/Documents/{target_dir}/.git/"
        when_to_use = [
            "When starting a brand-new project from scratch, or when putting an existing project folder under Git version control for the first time.",
            "Run it ONCE at the top-level root folder of your project (never inside subfolders!).",
            "NOTE: You do NOT need to run 'git init' if you cloned a repository using 'git clone' (cloning already initializes Git!)."
        ]
        mistake_rescue = [
            "1. WHAT IF YOU RAN 'git init' IN THE WRONG FOLDER? (e.g. your Desktop, Downloads, or entire C:\\Users directory):",
            "   DO NOT PANIC! Git only created a single hidden folder named '.git'. None of your real personal files were modified, moved, or deleted.",
            "2. How to undo 'git init' completely and remove Git tracking from the folder:",
            "   • In PowerShell / Windows Terminal:",
            "     Remove-Item -Recurse -Force .git",
            "   • In Windows Command Prompt (cmd.exe):",
            "     rmdir /s /q .git",
            "   • In Git Bash / Linux / macOS:",
            "     rm -rf .git",
            "3. Boom! The folder is instantly back to being a normal everyday directory with zero Git tracking!"
        ]

    # Check for config
    elif subcmd == "config":
        cat = "SAFE"
        score = 1.0
        warning = "Configures author identity, default branch, or custom shortcuts."
        if "--list" in args_str:
            simulated_output = f"$ git {cmd_str}\nuser.name=Prajwal Chonnad\nuser.email=prajwal@example.com\ninit.defaultbranch=main\ncore.editor=code --wait\ncore.autocrlf=true"
        else:
            simulated_output = f"$ git {cmd_str}\n(Configuration updated in Git config file)"
        when_to_use = [
            "Run 'git config --global user.name' and 'user.email' when setting up Git for the first time on a new computer.",
            "Run 'git config --list' to check all active resolved settings."
        ]
        mistake_rescue = [
            "1. Made a typo in your name or email? Simply run the command again with the right value to overwrite it:",
            "   git config --global user.name 'Your Name'",
            "   git config --global user.email 'you@example.com'",
            "2. To remove a configuration key:  git config --global --unset <key>"
        ]

    # Check for fetch
    elif subcmd == "fetch":
        cat = "SAFE"
        score = 1.0
        warning = "100% SAFE. Downloads remote commits and branches without touching or modifying your local working files!"
        simulated_output = f"$ git {cmd_str}\nFrom https://github.com/organization/project\n * [new branch]      feature-payment -> origin/feature-payment\n   1a2b3c4..5d6e7f8  main            -> origin/main"
        when_to_use = [
            "When you want to see what teammates have pushed to GitHub WITHOUT immediately merging or creating conflicts in your local code.",
            "Run before 'git diff main origin/main' to compare incoming changes before integrating."
        ]
        mistake_rescue = [
            "1. 'git fetch' is completely safe and read-only for your working directory files.",
            "2. It only updates your remote tracking branches (like origin/main). Nothing in your code was changed."
        ]

    # === READ-ONLY DIAGNOSTIC COMMANDS ===
    elif subcmd == "status":
        cat = "SAFE"; score = 0.0
        warning = "THE FRIENDLIEST COMMAND! Absolutely 100% safe — shows state without touching anything."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "On branch main\n"
            "Your branch is up to date with 'origin/main'.\n\n"
            "Changes to be committed:\n"
            "  (use \"git restore --staged <file>...\" to unstage)\n"
            "\tmodified:   src/app.py\n\n"
            "Changes not staged for commit:\n"
            "  (use \"git add <file>...\" to update what will be committed)\n"
            "\tmodified:   README.md\n\n"
            "Untracked files:\n"
            "  (use \"git add <file>...\" to track)\n"
            "\tdata/results.csv"
        )
        when_to_use = [
            "Run this CONSTANTLY — before add, before commit, before push, after switching branches.",
            "Three zones: STAGED (green, ready to commit), MODIFIED (red, not staged), UNTRACKED (Git doesn't know about it).",
            "Never modifies or deletes anything. Zero risk, anytime."
        ]
        mistake_rescue = ["100% read-only. Press q if output opens in a pager. No rescue needed!"]

    elif subcmd == "log":
        cat = "SAFE"; score = 0.0
        warning = "Read-only history browser! Press 'q' to exit the pager if it appears."
        if "--oneline" in args_str and "--graph" in args_str:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "* 9b8c7d6 (HEAD -> main, origin/main) feat(dsa): add AVL tree visualizer\n"
                "| * 3a4b5c6 (feature-auth) feat(auth): add google oauth login\n"
                "|/\n"
                "* 4a5b6c7 fix(java): resolve thread deadlock\n"
                "* 1e2f3a4 docs: update lab installation notes"
            )
        elif "--oneline" in args_str:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "9b8c7d6 (HEAD -> main) feat(dsa): add AVL tree visualizer\n"
                "4a5b6c7 fix(java): resolve thread deadlock\n"
                "1e2f3a4 docs: update lab installation notes\n"
                "8b4a2c1 fix(auth): simplify login validator"
            )
        else:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "commit 9b8c7d6e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c (HEAD -> main)\n"
                "Author: Prajwal Chonnad <prajwal@example.com>\n"
                "Date:   Fri Nov 14 10:00:00 2026 +0530\n\n"
                "    feat(dsa): add AVL tree visualizer\n\n"
                "commit 4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b\n"
                "Author: Alice <alice@example.com>\n"
                "Date:   Thu Nov 13 15:30:00 2026 +0530\n\n"
                "    fix(java): resolve thread deadlock"
            )
        when_to_use = [
            "To review project activity, find commit hashes, or visualize branch topology.",
            "Tip: 'git log --oneline --graph --all' gives the best visual of all branches!",
            "Tip: 'git log --author=Name' filters commits by a specific person."
        ]
        mistake_rescue = ["Read-only. Press 'q' to exit the pager if it appears. No recovery needed."]

    elif subcmd == "diff":
        cat = "SAFE"; score = 0.0
        warning = "Line-by-line diff viewer! Green (+) = added lines, Red (-) = deleted lines."
        if "--staged" in args_str or "--cached" in args_str:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "diff --git a/src/app.py b/src/app.py\n"
                "index 4b825dc..a1b2c3d 100644\n"
                "--- a/src/app.py\n"
                "+++ b/src/app.py\n"
                "@@ -10,3 +10,5 @@ def run():\n"
                "+    print('System initialized')\n"
                "+    logger.info('App started')\n"
                "     return True"
            )
        else:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "diff --git a/src/calculator.c b/src/calculator.c\n"
                "--- a/src/calculator.c\n"
                "+++ b/src/calculator.c\n"
                "@@ -22,6 +22,7 @@ int divide(int a, int b) {\n"
                "+    if (b == 0) return -1; // protect against division by zero\n"
                "     return a / b;\n"
                " }"
            )
        when_to_use = [
            "Before 'git add' — check every change you're about to stage.",
            "Use 'git diff --staged' to review what's already staged and will go into the commit.",
            "Use 'git diff HEAD~1' to compare current state to the previous commit."
        ]
        mistake_rescue = ["Read-only. Press 'q' to exit. No recovery needed."]

    elif subcmd == "reflog":
        cat = "SAFE"; score = 0.0
        warning = "Git's Black-Box Flight Recorder — records EVERY HEAD movement for 90 days! This is your time machine!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "a1b2c3d (HEAD -> main) HEAD@{0}: commit: feat(dsa): add AVL tree visualizer\n"
            "e5f6a7b HEAD@{1}: reset: moving to HEAD~1\n"
            "9f8e7d6 HEAD@{2}: commit: Add experimental neural search algorithm\n"
            "3c4d5e6 HEAD@{3}: checkout: moving from feature-auth to main\n"
            "7a8b9c0 HEAD@{4}: commit (amend): feat(auth): improved google oauth"
        )
        when_to_use = [
            "YOUR EMERGENCY LIFESAVER after any reset --hard, deleted branch, or failed rebase.",
            "Find the commit SHA before the disaster, then: git reset --hard HEAD@{N}",
            "Even 'deleted' commits still exist in reflog for 90 days (default expiry)."
        ]
        mistake_rescue = ["Read-only. This command IS the rescue tool. No recovery needed!"]

    elif subcmd == "blame":
        cat = "SAFE"; score = 0.0
        warning = "The Detective Tool! Annotates every line with who wrote it and when."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "a1b2c3d4 (Alice    2026-10-12 14:32:01 +0530  12) def calculate_tax(income):\n"
            "e5f6a7b8 (Bob      2026-11-01 09:15:20 +0530  13)     rate = 0.30\n"
            "9c0d1e2f (Prajwal  2026-11-14 10:00:00 +0530  14)     if income > 1000000:\n"
            "9c0d1e2f (Prajwal  2026-11-14 10:00:00 +0530  15)         rate = 0.35  # updated bracket\n"
            "e5f6a7b8 (Bob      2026-11-01 09:15:20 +0530  16)     return income * rate"
        )
        when_to_use = [
            "To understand WHY a specific line of code was written — click the commit hash for full context.",
            "To find out who to ask about a confusing algorithm or business logic.",
            "Useful during code reviews and bug investigations."
        ]
        mistake_rescue = ["Read-only. Press 'q' to exit. No recovery needed."]

    elif subcmd == "show":
        cat = "SAFE"; score = 0.0
        warning = "Read-only object inspector — shows commit details with diff, tags, blobs."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "commit 9b8c7d6e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c (HEAD -> main)\n"
            "Author: Prajwal Chonnad <prajwal@example.com>\n"
            "Date:   Fri Nov 14 10:00:00 2026 +0530\n\n"
            "    feat(dsa): add AVL tree visualizer with rotation counter\n\n"
            "diff --git a/src/avl_tree.py b/src/avl_tree.py\n"
            "new file mode 100644\n"
            "+++ b/src/avl_tree.py\n"
            "+class AVLTree:\n"
            "+    def __init__(self): self.root = None"
        )
        when_to_use = [
            "'git show <hash>' to inspect any past commit's metadata and diff.",
            "'git show HEAD' to view the most recent commit you just made.",
            "'git show v1.0.0' to inspect an annotated tag's contents."
        ]
        mistake_rescue = ["Read-only. Press 'q' to exit. No recovery needed."]

    elif subcmd == "grep":
        cat = "SAFE"; score = 0.0
        warning = "Blazing-fast code search across all Git-tracked files in the repository."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "src/auth.py:15:    if validate_token(user_token):\n"
            "src/middleware.py:42:    token = request.headers.get('Authorization')\n"
            "tests/test_auth.py:8:    mock_token = 'Bearer eyJhbG...'"
        )
        when_to_use = [
            "Faster than grep for searching ONLY files tracked by Git.",
            "'git grep -n <pattern>' shows line numbers.",
            "'git grep <pattern> <commit>' searches a specific historical commit!"
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "cat-file":
        cat = "SAFE"; score = 0.0
        warning = "Low-level plumbing — inspects raw Git objects (commits, trees, blobs) stored in .git/objects."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904\n"
            "author Prajwal Chonnad <prajwal@example.com> 1763059200 +0530\n"
            "committer Prajwal Chonnad <prajwal@example.com> 1763059200 +0530\n\n"
            "feat(dsa): add AVL tree visualizer"
        )
        when_to_use = [
            "To inspect the raw contents of ANY Git object: commit, tree, blob, or tag.",
            "'git cat-file -t <hash>' shows the object type. 'git cat-file -p <hash>' pretty-prints it.",
            "Used internally by Git to build diffs and traverse history."
        ]
        mistake_rescue = ["Read-only plumbing. No recovery needed."]

    elif subcmd == "ls-tree":
        cat = "SAFE"; score = 0.0
        warning = "Plumbing: lists the directory tree structure stored inside a Git commit object."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "100644 blob a1b2c3d4e5f6a7b8  README.md\n"
            "100644 blob b2c3d4e5f6a7b8c9  play.py\n"
            "040000 tree c3d4e5f6a7b8c9d0  src/\n"
            "040000 tree d4e5f6a7b8c9d0e1  tests/"
        )
        when_to_use = [
            "To explore the file/directory tree at any historical commit.",
            "'git ls-tree HEAD' shows what's in your current commit snapshot.",
            "'git ls-tree --recursive HEAD' shows all nested files recursively."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "rev-parse":
        cat = "SAFE"; score = 0.0
        warning = "Plumbing: resolves symbolic refs (HEAD, branch names) to full SHA-1 commit hashes."
        simulated_output = f"$ git {cmd_str}\ne2cdd2e842918414197e42d768114f6b28c89b41"
        when_to_use = [
            "'git rev-parse HEAD' gives the full SHA-1 hash of the current commit.",
            "'git rev-parse --abbrev-ref HEAD' gives the current branch name.",
            "Used heavily in shell scripts to get commit hashes for automation."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "describe":
        cat = "SAFE"; score = 0.0
        warning = "Gives a human-readable name to a commit based on the nearest annotated tag."
        simulated_output = f"$ git {cmd_str}\nv1.2.0-4-g9b8c7d6"
        when_to_use = [
            "To generate a human-readable version string like 'v1.2.0-4-g9b8c7d6' for CI/CD builds.",
            "Tells you: 4 commits after tag v1.2.0, at commit hash 9b8c7d6."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "fsck":
        cat = "SAFE"; score = 0.5
        warning = "Verifies integrity of all objects in .git/objects — a Git health check."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Checking object directories: 100% (256/256), done.\n"
            "Checking connectivity: done.\n"
            "dangling commit a1b2c3d4e5f6a7b8c9d0  (from dropped stash)"
        )
        when_to_use = [
            "After a Git crash, disk error, or corruption suspicion.",
            "'git fsck --no-reflog' shows ALL dangling commits (useful for recovering dropped stashes!)",
            "Run periodically as a repository health check."
        ]
        mistake_rescue = ["Read-only health scan. Inspect dangling commits with 'git show <hash>'."]

    elif subcmd == "ls-files":
        cat = "SAFE"; score = 0.0
        warning = "Lists tracked, untracked, ignored, or staged files in the index — read-only!"
        if "--others" in args_str or "-o" in args:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "data/results.csv\n"
                "temp_debug.log\n"
                "build/output.bin"
            )
        elif "--ignored" in args_str or "-i" in args:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "__pycache__/\n"
                "*.pyc\n"
                ".env"
            )
        else:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "README.md\n"
                "play.py\n"
                "src/app.py\n"
                "src/utils.py"
            )
        when_to_use = [
            "'git ls-files' lists all files currently tracked by Git.",
            "'git ls-files --others --exclude-standard' shows untracked files.",
            "'git ls-files -s' shows file hashes and modes in the staging index."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "ls-remote":
        cat = "SAFE"; score = 0.0
        warning = "Lists references on a remote — requires network, but touches NOTHING locally!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "9b8c7d6e1f2a3b4c  HEAD\n"
            "9b8c7d6e1f2a3b4c  refs/heads/main\n"
            "3a4b5c6d7e8f9a0b  refs/heads/feature-auth\n"
            "a1b2c3d4e5f6a7b8  refs/tags/v1.0.0"
        )
        when_to_use = [
            "To check which branches and tags exist on a remote BEFORE fetching or cloning.",
            "'git ls-remote origin' shows what's on GitHub without downloading anything."
        ]
        mistake_rescue = ["Read-only network inspection. No local changes made."]

    elif subcmd == "shortlog":
        cat = "SAFE"; score = 0.0
        warning = "Summarizes git log by author — shows contributor stats!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Prajwal Chonnad (12):\n"
            "      feat(dsa): add AVL tree visualizer\n"
            "      fix(java): resolve thread deadlock\n"
            "Alice Kumar (5):\n"
            "      docs: update installation guide"
        )
        when_to_use = [
            "To generate contributor statistics for a project.",
            "'git shortlog -sn' shows just name + count, sorted by most commits."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "version":
        cat = "SAFE"; score = 0.0
        warning = "Prints the installed Git version — completely harmless!"
        simulated_output = "$ git version\ngit version 2.47.1.windows.1"
        when_to_use = [
            "To check which Git version is installed.",
            "First thing to check when debugging Git compatibility issues."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "help":
        cat = "SAFE"; score = 0.0
        warning = "Shows the Git manual or help for a specific command."
        if args:
            subcmd_help = GIT_CORE_SUBCOMMANDS.get(args[0], ("A Git command.", "SAFE", 0))[0]
            simulated_output = (
                f"$ git {cmd_str}\n"
                f"GIT-{args[0].upper()}(1)   Git Manual\n\n"
                f"NAME\n"
                f"       git-{args[0]} - {subcmd_help}"
            )
        else:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "usage: git [--version] [--help] <command> [<args>]\n\n"
                "The most commonly used git commands are:\n"
                "   add       Add file contents to the index\n"
                "   commit    Record changes to the repository\n"
                "   push      Update remote refs\n"
                "   pull      Fetch from and integrate with another repository\n"
                "   status    Show the working tree status"
            )
        when_to_use = ["'git help <command>' opens the full manual page for any command."]
        mistake_rescue = ["Read-only. No recovery needed."]

    # === WORKHORSE COMMANDS ===
    elif subcmd == "add":
        cat = "CAUTION"; score = 3.0
        warning = "Stages file changes into the Index. Your gateway before every commit!"
        if "." in args or "-A" in args or "--all" in args_str:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "(All modified and untracked files staged — now show green in git status)"
            )
        elif "-p" in args or "--patch" in args_str:
            simulated_output = (
                f"$ git {cmd_str}\n"
                "diff --git a/src/app.py b/src/app.py\n"
                "@@ -10,3 +10,4 @@ def run():\n"
                "+    print('System initialized')\n"
                "Stage this hunk [y,n,q,a,d,/,e,?]? "
            )
        else:
            simulated_output = f"$ git {cmd_str}\n(Files turn green in git status — staged and ready to commit!)"
        when_to_use = [
            "After editing code, 'git add <file>' to stage only what belongs in the next logical commit.",
            "'git add -p' (patch mode) lets you stage only specific hunks within a file — very powerful!",
            "Never 'git add .' blindly — always check with 'git status' first to see what you're staging."
        ]
        mistake_rescue = [
            "1. Accidentally staged a sensitive file (.env, secrets.json)?  git restore --staged <file>",
            "2. Unstage everything staged:  git restore --staged .",
            "3. Your code is NEVER modified — files simply move back to unstaged (red) status."
        ]

    elif subcmd == "rm":
        cat = "CAUTION"; score = 4.0
        is_cached = "--cached" in args_str
        if is_cached:
            warning = "Un-tracks a file from Git while keeping it safe on your disk!"
            simulated_output = (
                f"$ git {cmd_str}\n"
                "rm 'config/database.env'\n"
                "(File still exists on disk but Git will no longer version it)"
            )
            when_to_use = [
                "When you accidentally committed a .env, API key, or build artifact.",
                "Always add the file path to .gitignore RIGHT AFTER so it stays untracked!"
            ]
            mistake_rescue = [
                "1. File was NEVER deleted from your disk!",
                "2. To re-track it accidentally removed: git add <file>"
            ]
        else:
            warning = "Removes a file from BOTH Git tracking AND the actual disk filesystem!"
            simulated_output = f"$ git {cmd_str}\nrm 'src/old_module.py'"
            when_to_use = [
                "When you want to delete a file from your project AND tell Git to stop tracking it simultaneously.",
                "Use '--cached' if you only want to untrack without deleting from disk."
            ]
            mistake_rescue = [
                "1. If file was committed before: git checkout HEAD -- <file> to restore from last commit.",
                "2. If the file was only on disk and never committed, check IDE Local History."
            ]

    elif subcmd == "mv":
        cat = "CAUTION"; score = 2.5
        warning = "Renames or moves a tracked file — Git records this as a rename (preserves history!)."
        old_name = args[0] if args else "old_name.py"
        new_name = args[1] if len(args) > 1 else "new_name.py"
        simulated_output = f"$ git {cmd_str}\n(Renamed {old_name} -> {new_name} and staged the rename)"
        when_to_use = [
            "To rename or move files inside a Git project — always use 'git mv' instead of OS rename!",
            "Using 'git mv' preserves the file's full commit history through the rename.",
            "Using plain OS rename makes Git think you deleted one file and created a new one."
        ]
        mistake_rescue = [
            "1. If you renamed by mistake: git mv new_name.py old_name.py (rename it back)",
            "2. Or: git restore --staged . then manually rename back via OS."
        ]

    elif subcmd == "switch":
        cat = "SAFE"; score = 1.5
        is_new = "-c" in args or "--create" in args_str or "-C" in args
        branch_name = next((a for a in args if not a.startswith("-")), "feature-branch")
        if is_new:
            warning = "Creates AND switches to a brand-new branch — great for starting a feature!"
            simulated_output = f"$ git {cmd_str}\nSwitched to a new branch '{branch_name}'"
        else:
            warning = "Switches your working directory to an existing branch."
            simulated_output = (
                f"$ git {cmd_str}\n"
                f"Switched to branch '{branch_name}'\n"
                f"Your branch is up to date with 'origin/{branch_name}'."
            )
        when_to_use = [
            "Every time you start a new feature — ALWAYS create a branch first with 'git switch -c feature-name'!",
            "'git switch -' instantly jumps back to the previous branch you were on.",
            "Prefer 'git switch' over 'git checkout' for branch operations (cleaner, safer)."
        ]
        mistake_rescue = [
            "1. If you have uncommitted changes that conflict with the target branch, Git will refuse and warn you.",
            "2. Stash your changes first: git stash → git switch <branch> → git stash pop"
        ]

    elif subcmd == "restore":
        cat = "CAUTION"; score = 4.0
        is_staged = "--staged" in args_str
        if is_staged and "." not in args and "*" not in args_str:
            cat = "SAFE"; score = 1.0
            warning = "Safely unstages files without touching a single character of your code!"
            simulated_output = f"$ git {cmd_str}\n(Silent success — file moved from green staged back to red unstaged)"
            when_to_use = ["When you accidentally staged a file you didn't want in this commit."]
            mistake_rescue = ["Zero risk! Code completely untouched. Re-stage with: git add <file>"]
        elif "." in args or "*" in args_str:
            cat = "DANGER"; score = 8.0
            warning = "DANGER! Discards ALL uncommitted modifications in tracked files — cannot be undone via Git!"
            simulated_output = f"$ git {cmd_str}\nUpdated 5 paths from the index"
            when_to_use = ["When an experiment failed completely and you want clean state from last commit."]
            mistake_rescue = [
                "1. Git never recorded uncommitted edits — 'git reflog' cannot bring them back.",
                "2. Press Ctrl+Z in your editor if the buffer is still in memory.",
                "3. Check IDE Local History (VS Code Timeline / JetBrains Local History).",
                "4. PRO-TIP: Use 'git stash' next time — recoverable anytime!"
            ]
        else:
            warning = "Restores a specific file to its last committed version, discarding uncommitted edits."
            simulated_output = f"$ git {cmd_str}\n(File restored to last committed state)"
            when_to_use = ["When you want to discard edits in a specific file only."]
            mistake_rescue = [
                "1. Uncommitted edits in this file are gone from Git.",
                "2. Check editor Ctrl+Z or IDE Local History immediately."
            ]

    elif subcmd == "stash" and not any(w in args_str for w in ["drop", "clear"]):
        cat = "CAUTION"; score = 2.0
        sub = args[0].lower() if args else ""
        if sub == "pop":
            warning = "Applies the top stashed work and removes it from the stash queue."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "On branch main\nChanges not staged for commit:\n"
                "\tmodified:   src/feature.py\nDropped refs/stash@{0} (a1b2c3d...)"
            )
        elif sub == "list":
            warning = "Lists all saved stash entries — safe, read-only."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "stash@{0}: WIP on main: 9b8c7d6 feat(dsa): add AVL tree\n"
                "stash@{1}: WIP on feature-auth: 3a4b5c6 partial oauth work"
            )
        elif sub in ("apply", "show"):
            warning = "Applies (or previews) a stash without removing it from the queue."
            simulated_output = f"$ git {cmd_str}\n(Stash applied. Stash entry still remains in queue.)"
        else:
            warning = "Saves all uncommitted changes onto a clipboard stack and cleans your working directory."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Saved working directory and index state WIP on main: 9b8c7d6 feat(dsa): add AVL tree\n"
                "HEAD is now at 9b8c7d6 feat(dsa): add AVL tree"
            )
        when_to_use = [
            "Mid-feature and urgent bug reported on main? Stash → switch → fix → push → switch back → stash pop!",
            "'git stash list' to see all saved stashes.",
            "'git stash show -p stash@{0}' to preview what's saved before popping."
        ]
        mistake_rescue = [
            "1. Forgot what you stashed? Run: git stash list  or  git stash show -p",
            "2. Stash pop conflict? Resolve the conflict manually, then: git stash drop",
            "3. Lost a stash? Run: git fsck --no-reflog to find dangling stash commits!"
        ]

    elif subcmd == "tag":
        cat = "SAFE"; score = 1.0
        is_delete = "-d" in args or "--delete" in args_str
        is_annotated = "-a" in args or "--annotate" in args_str
        if is_delete:
            warning = "Deletes a tag reference — the commits themselves are NOT deleted."
            simulated_output = f"$ git {cmd_str}\nDeleted tag 'v1.0.0' (was a1b2c3d)"
            when_to_use = ["When you tagged the wrong commit or mislabeled a release."]
            mistake_rescue = ["Commits are safe. Re-tag: git tag -a v1.0.0 <correct-hash>"]
        elif is_annotated:
            warning = "Creates a permanent annotated release tag with metadata stored in Git."
            tag_name = next((a for a in args if not a.startswith("-")), "v1.0.0")
            simulated_output = f"$ git {cmd_str}\n(Annotated tag '{tag_name}' created — push with 'git push origin {tag_name}')"
            when_to_use = [
                "To mark software version releases (v1.0, v2.1) or lab submission checkpoints.",
                "Annotated tags store tagger, date, message — better than lightweight tags for releases."
            ]
            mistake_rescue = ["Wrong commit? Delete: git tag -d <tag-name>  then re-tag the right commit."]
        else:
            warning = "Lists all existing tags or creates a lightweight tag."
            simulated_output = f"$ git {cmd_str}\nv0.1.0\nv1.0.0\nv1.1.0\nv2.0.0-beta"
            when_to_use = [
                "'git tag' (no args) lists all tags.",
                "Use 'git tag -a v1.0 -m \"Release\"' for annotated tags."
            ]
            mistake_rescue = ["Safe and read-only when listing tags."]

    elif subcmd == "remote":
        cat = "SAFE"; score = 1.0
        sub = args[0].lower() if args else ""
        if sub == "add":
            warning = "Registers a new remote repository URL under a nickname."
            simulated_output = f"$ git {cmd_str}\n(Remote 'origin' now points to GitHub repository)"
        elif sub in ("remove", "rm"):
            cat = "CAUTION"; score = 3.0
            warning = "Removes a registered remote — all remote tracking branches for it are deleted too."
            simulated_output = f"$ git {cmd_str}\n(Remote 'origin' removed from .git/config)"
        elif sub == "set-url":
            warning = "Updates the URL a remote points to (useful after renaming GitHub repos)."
            simulated_output = f"$ git {cmd_str}\n(URL for remote 'origin' updated in .git/config)"
        else:
            warning = "Lists all registered remote repository nicknames and their URLs."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "origin  https://github.com/Ghost5400/OILS-3.git (fetch)\n"
                "origin  https://github.com/Ghost5400/OILS-3.git (push)"
            )
        when_to_use = [
            "'git remote -v' to verify where your repo is pointing on GitHub.",
            "'git remote add origin <url>' when connecting a new local repo to GitHub for the first time.",
            "'git remote set-url origin <new-url>' after renaming the GitHub repository."
        ]
        mistake_rescue = [
            "1. Added wrong URL? git remote set-url origin <correct-url>",
            "2. Accidentally removed remote? git remote add origin <url>"
        ]

    elif subcmd == "branch":
        cat = "SAFE"; score = 2.0
        is_rename = "-m" in args or "-M" in args or "--move" in args_str
        if is_rename:
            warning = "Renames a branch locally — remember to update on remote too!"
            simulated_output = f"$ git {cmd_str}\n(Branch renamed successfully)"
            when_to_use = ["To fix a typo in a branch name. Push new name: git push origin <new-name>"]
            mistake_rescue = ["Rename it back: git branch -m <new-name> <old-name>"]
        else:
            warning = "Lists, creates, or inspects branches — mostly safe!"
            simulated_output = (
                f"$ git {cmd_str}\n"
                "* main\n"
                "  feature-auth\n"
                "  feature-dsa-visualizer\n"
                "  hotfix-login-bug"
            )
            when_to_use = [
                "'git branch' (no args) lists all local branches.",
                "'git branch -a' shows ALL branches including remote-tracking ones.",
                "'git branch <name>' creates a new branch WITHOUT switching to it."
            ]
            mistake_rescue = ["Safe and read-only when listing branches."]

    elif subcmd == "worktree":
        cat = "SAFE"; score = 2.0
        sub = args[0].lower() if args else ""
        if sub == "add":
            warning = "Creates a new working tree at a path, allowing parallel branch checkouts!"
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Preparing worktree (new branch 'feature-branch')\n"
                "HEAD is now at 9b8c7d6 feat(dsa): add AVL tree"
            )
        elif sub == "list":
            warning = "Lists all currently active working trees for this repository."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "c:/Users/Student/Documents/OILS-3  9b8c7d6 [main]\n"
                "c:/Users/Student/Documents/OILS-3-feature  3a4b5c6 [feature-auth]"
            )
        elif sub == "remove":
            cat = "CAUTION"; score = 3.0
            warning = "Removes a linked working tree — does NOT delete the branch itself."
            simulated_output = f"$ git {cmd_str}\n(Linked worktree removed)"
        else:
            warning = "Manages multiple parallel working trees linked to the same repository."
            simulated_output = f"$ git {cmd_str}\n(Working tree operation completed)"
        when_to_use = [
            "To review or test a different branch without stashing current work!",
            "Monorepo workflows where multiple branches need simultaneous editing.",
            "Great for: checking out a release branch to hotfix while keeping main open."
        ]
        mistake_rescue = [
            "1. Remove a worktree: git worktree remove <path>",
            "2. Worktrees are just linked directories — the branch and all commits are unaffected."
        ]

    elif subcmd == "submodule":
        cat = "CAUTION"; score = 4.0
        sub = args[0].lower() if args else ""
        if sub == "add":
            warning = "Embeds an external repository as a pinned sub-project inside your repository."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Cloning into 'libs/external-lib'...\n"
                "(Submodule registered in .gitmodules)"
            )
        elif sub in ("init", "update"):
            warning = "Initializes/updates registered submodules to their pinned commit versions."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Submodule path 'libs/external-lib': checked out 'a1b2c3d...'"
            )
        elif sub == "deinit":
            cat = "DANGER"; score = 7.0
            warning = "Removes submodule initialization — submodule files are deleted from working tree!"
            simulated_output = f"$ git {cmd_str}\nCleared directory 'libs/external-lib'"
        else:
            warning = "Manages embedded Git sub-repositories within the parent repository."
            simulated_output = f"$ git {cmd_str}\n a1b2c3d libs/external-lib (v2.1.0-4-ga1b2c3d)"
        when_to_use = [
            "When your project depends on a specific version of an external library's source code.",
            "Common in C/C++ projects, game engines, and large frameworks.",
            "Cloning a project with submodules: git clone --recurse-submodules <url>"
        ]
        mistake_rescue = [
            "1. Accidentally added wrong submodule? git submodule deinit <path> then git rm <path>",
            "2. Submodule not initialized after clone? git submodule init && git submodule update"
        ]

    elif subcmd == "notes":
        cat = "SAFE"; score = 1.5
        sub = args[0].lower() if args else ""
        if sub == "add":
            warning = "Attaches a note to a commit — stored separately, doesn't change the commit SHA!"
            simulated_output = f"$ git {cmd_str}\n(Note attached to commit without altering its SHA)"
        elif sub in ("remove", "prune"):
            cat = "CAUTION"; score = 3.0
            warning = "Removes attached notes from commits."
            simulated_output = f"$ git {cmd_str}\n(Note removed from commit)"
        else:
            warning = "Shows or manages annotation notes attached to commits."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Code Review Note: needs performance optimization in O(n^2) loops"
            )
        when_to_use = [
            "To annotate commits with review notes, bug IDs, or deployment records WITHOUT changing the commit SHA.",
            "CI/CD pipelines use notes to attach build/test results to specific commits."
        ]
        mistake_rescue = [
            "1. Notes don't change commit SHAs so there's no history rewrite risk.",
            "2. Notes are stored in a separate ref: refs/notes/commits"
        ]

    elif subcmd == "archive":
        cat = "SAFE"; score = 0.5
        warning = "Creates a zip or tar archive of a repository tree — read-only export, no .git/ folder included!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "(Writing archive... done!)\n"
            "Created: project-v1.0.zip (excludes .git/ directory)"
        )
        when_to_use = [
            "To export a clean release snapshot for distribution without exposing the .git/ metadata.",
            "'git archive --format=zip HEAD > project.zip' creates a zip of the current commit.",
            "'git archive v1.0.0 | tar -xf - -C /releases/' exports a tagged version."
        ]
        mistake_rescue = ["Read-only export. No recovery needed."]

    elif subcmd == "bisect":
        cat = "SAFE"; score = 1.0
        sub = args[0].lower() if args else ""
        if sub == "start":
            warning = "Starts binary-search mode — Git will checkout midpoint commits for you to test."
            simulated_output = f"$ git {cmd_str}\n(Bisect started. Mark commits as good or bad.)"
        elif sub == "bad":
            warning = "Marks current commit as BAD (broken). Git narrows the search range."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Bisecting: 6 revisions left to test (roughly 3 steps)\n"
                "[3a4b5c6] refactor(cache): switch to redis cluster"
            )
        elif sub == "good":
            warning = "Marks current commit as GOOD (working). Git narrows the search range."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Bisecting: 3 revisions left to test (roughly 2 steps)\n"
                "[7d8e9f0] feat(auth): add session timeout"
            )
        elif sub == "reset":
            warning = "Ends bisect session and returns to your original branch."
            simulated_output = (
                f"$ git {cmd_str}\n"
                "Previous HEAD position was 3a4b5c6 refactor(cache): switch to redis\n"
                "Switched to branch 'main'"
            )
        else:
            warning = "Manages git bisect binary-search bug hunting session."
            simulated_output = f"$ git {cmd_str}\n(Bisect operation completed)"
        when_to_use = [
            "When something worked last week but is broken now across dozens of commits — bisect finds EXACTLY which commit broke it!",
            "'git bisect start' → mark bad commit → mark last known good commit → Git auto-checks midpoints!",
            "O(log N) algorithm — finds the bad commit in just ~7 steps even across 100 commits!"
        ]
        mistake_rescue = [
            "1. Confused mid-bisect? git bisect reset (safely returns to original branch)",
            "2. Skip a commit that can't be tested: git bisect skip"
        ]

    elif subcmd == "gc":
        cat = "SAFE"; score = 2.0
        warning = "Runs Garbage Collection — compresses loose objects and removes expired reflog entries."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Enumerating objects: 184, done.\n"
            "Counting objects: 100% (184/184), done.\n"
            "Compressing objects: 100% (142/142), done.\n"
            "Total 184 (delta 48), reused 0 (delta 0), pack-reused 0"
        )
        when_to_use = [
            "To clean up and compress the repository database after many commits or rebases.",
            "Automatically runs in background — you rarely need to run it manually.",
            "'git gc --aggressive' does a deeper compression (slower but smaller .git/ folder)."
        ]
        mistake_rescue = [
            "1. GC DOES permanently remove expired reflog entries — but default expiry is 90 days.",
            "2. Run 'git gc --prune=now' only if you intentionally want to prune all dangling objects."
        ]

    elif subcmd == "rerere":
        cat = "SAFE"; score = 1.0
        warning = "Reuse Recorded Resolution — remembers your merge conflict fixes and auto-applies them next time!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Recorded resolution for 'src/app.py'.\n"
            "(Next time this conflict appears, Git will auto-resolve it!)"
        )
        when_to_use = [
            "Enable once: git config --global rerere.enabled true",
            "Invaluable when rebasing many commits that repeatedly hit the same conflict.",
            "Saves enormous time in long-running feature branches that must be frequently rebased."
        ]
        mistake_rescue = [
            "1. If a recorded resolution is wrong: git rerere forget <file>",
            "2. All recorded resolutions stored in .git/rr-cache/"
        ]

    elif subcmd == "sparse-checkout":
        cat = "CAUTION"; score = 3.0
        warning = "Reduces working tree size by checking out only specified directories from large monorepos."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "(Working tree now only shows selected directories)"
        )
        when_to_use = [
            "In massive monorepos where checking out the full tree would take forever.",
            "'git sparse-checkout set src/myapp docs/' to only see those folders.",
            "Saves disk space and speeds up 'git status' on huge repos."
        ]
        mistake_rescue = [
            "1. To disable sparse checkout and see everything: git sparse-checkout disable",
            "2. Files you can't see are still in the repo — just not checked out locally."
        ]

    elif subcmd == "format-patch":
        cat = "SAFE"; score = 0.5
        warning = "Exports commits as email-ready .patch files — read-only snapshot export."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "0001-feat-dsa-add-AVL-tree-visualizer.patch\n"
            "0002-fix-java-resolve-thread-deadlock.patch"
        )
        when_to_use = [
            "To share individual commits as patch files via email (Linux kernel development style).",
            "'git format-patch HEAD~3' creates 3 patch files for the last 3 commits."
        ]
        mistake_rescue = ["Read-only export. No recovery needed."]

    elif subcmd == "am":
        cat = "CAUTION"; score = 4.0
        warning = "Applies a patch file (from git format-patch or email) as a commit onto current branch."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Applying: feat(dsa): add AVL tree visualizer\n"
            "[main 9b8c7d6] feat(dsa): add AVL tree visualizer\n"
            " 1 file changed, 48 insertions(+)"
        )
        when_to_use = [
            "To apply patches received via email or file from contributors.",
            "Preserves original author info and commit message from the patch."
        ]
        mistake_rescue = [
            "1. Conflict mid-apply? git am --abort (cancels apply, restores branch)",
            "2. Skip a failed patch: git am --skip"
        ]

    elif subcmd == "apply":
        cat = "CAUTION"; score = 4.0
        warning = "Applies a diff/patch to files without creating a commit."
        simulated_output = f"$ git {cmd_str}\n(Patch applied to working directory — changes not yet staged or committed)"
        when_to_use = [
            "To apply raw diff/patch files to your working directory without committing.",
            "'git apply --check <patch>' does a dry-run to verify the patch would apply cleanly."
        ]
        mistake_rescue = [
            "1. If the apply went wrong: git checkout . (restores working tree to index state)",
            "2. If patch partially applied: git apply --reverse <same-patch> to undo it."
        ]

    elif subcmd == "range-diff":
        cat = "SAFE"; score = 0.0
        warning = "Compares two series of commits — like a diff of diffs."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "1:  a1b2c3d = 1:  d3c2b1a feat: add login form validation\n"
            "2:  e4f5a6b ! 2:  b6a5f4e fix: improve error messages\n"
            "    @@ error_handler.py @@\n"
            "    -    raise ValueError('bad input')\n"
            "    +    raise ValueError(f'Invalid input: {value}')"
        )
        when_to_use = [
            "To compare two versions of a rebased patch series side by side.",
            "Incredibly useful for code reviewers to see how a PR was revised."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "bundle":
        cat = "SAFE"; score = 1.0
        warning = "Packages repository objects into a portable archive — like a git clone but offline!"
        simulated_output = (
            f"$ git {cmd_str}\n"
            "Enumerating objects: 184, done.\n"
            "Counting objects: 100% (184/184), done.\n"
            "Writing objects: 100% (184/184), 2.45 MiB, done.\n"
            "(Bundle written to repo.bundle)"
        )
        when_to_use = [
            "To share a full repository with someone who has no internet connection.",
            "'git clone repo.bundle' or 'git fetch repo.bundle' to restore."
        ]
        mistake_rescue = ["Read-only export. No recovery needed."]

    elif subcmd == "maintenance":
        cat = "SAFE"; score = 1.0
        warning = "Registers and runs background repository maintenance tasks (gc, prefetch, commit-graph)."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "(Maintenance task completed. Repository optimized.)"
        )
        when_to_use = [
            "'git maintenance start' schedules background optimization for large repos.",
            "Automatically runs fetch, gc, commit-graph writes in the background."
        ]
        mistake_rescue = ["Safe background operation. No recovery needed."]

    elif subcmd in ("for-each-ref", "show-ref"):
        cat = "SAFE"; score = 0.0
        warning = "Plumbing: lists all references (branches, tags, remote-tracking) with metadata."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "9b8c7d6e refs/heads/main\n"
            "3a4b5c6d refs/heads/feature-auth\n"
            "a1b2c3d4 refs/tags/v1.0.0\n"
            "9b8c7d6e refs/remotes/origin/main"
        )
        when_to_use = [
            "To iterate over all refs programmatically in shell scripts.",
            "'git for-each-ref --sort=-creatordate' lists branches by most recent activity."
        ]
        mistake_rescue = ["Read-only. No recovery needed."]

    elif subcmd == "hash-object":
        cat = "SAFE"; score = 0.5
        warning = "Computes the Git SHA-1 object ID for a file without storing it (unless -w flag)."
        simulated_output = f"$ git {cmd_str}\ne2cdd2e842918414197e42d768114f6b28c89b41"
        when_to_use = [
            "To compute what SHA Git would assign to a file's contents.",
            "With '-w' flag: also writes the blob object to .git/objects."
        ]
        mistake_rescue = ["Read-only without -w flag. With -w: creates a loose object (harmless)."]

    elif subcmd == "credential":
        cat = "SAFE"; score = 1.0
        warning = "Retrieves or stores Git credentials — the credential helper interface."
        simulated_output = f"$ git {cmd_str}\n(Credential helper operation completed)"
        when_to_use = [
            "'git credential-manager' (Windows) or 'git credential-osxkeychain' (macOS) stores passwords securely.",
            "Run 'git config --global credential.helper manager' to enable Windows Credential Manager."
        ]
        mistake_rescue = ["If credentials are wrong, re-run git push and enter correct credentials."]

    elif subcmd in ("verify-commit", "verify-tag"):
        cat = "SAFE"; score = 0.0
        warning = "Verifies the GPG cryptographic signature on a commit or tag."
        simulated_output = (
            f"$ git {cmd_str}\n"
            "gpg: Signature made Fri Nov 14 10:00:00 2026 IST\n"
            "gpg: Good signature from \"Prajwal Chonnad <prajwal@example.com>\""
        )
        when_to_use = [
            "To verify that a commit was signed by the expected GPG key.",
            "Used in security-sensitive projects to authenticate authorship."
        ]
        mistake_rescue = ["Read-only verification. No recovery needed."]

    elif subcmd == "reflog" and "expire" in args_str:
        cat = "DANGER"; score = 8.0
        warning = "DANGER! Manually expires and deletes reflog entries — reduces your safety net!"
        simulated_output = f"$ git {cmd_str}\n(Reflog entries before specified date purged)"
        when_to_use = ["Almost never! Only when deliberately shrinking repository size."]
        mistake_rescue = [
            "1. Expired reflog entries are GONE — no recovery possible through Git.",
            "2. Only run this if you intentionally want to remove old safety-net entries."
        ]

    # Fallback for truly obscure/plumbing commands
    else:
        if not warning:
            if cat == "DANGER":
                warning = "HIGH RISK! Modifies or removes repository state — read the manual carefully before running!"
            elif cat == "CAUTION":
                warning = "Alters repository state or working tree — double-check flags before running!"
            else:
                warning = "Likely SAFE — inspects repository data or performs low-level plumbing operations."

        if not simulated_output:
            simulated_output = (
                f"$ git {cmd_str}\n"
                f"('{subcmd}' is a valid Git command.\n"
                f" This is a less common or advanced plumbing command.\n"
                f" Type 'git help {subcmd}' in a real terminal for full documentation.)"
            )

        if not when_to_use:
            when_to_use = [
                "Used in advanced Git workflows, scripts, or plumbing-level operations.",
                f"Type 'git help {subcmd}' in a real terminal to read the full manual page."
            ]

        if not mistake_rescue:
            if cat == "DANGER":
                mistake_rescue = [
                    "1. Check 'git reflog' to see if commit pointers can be restored to pre-command state.",
                    "2. Check IDE Local History (VS Code Timeline / JetBrains Local History) for file recovery."
                ]
            elif cat == "CAUTION":
                mistake_rescue = [
                    "1. If files were staged: git restore --staged . (unstage all)",
                    "2. If a commit was made: git reset --soft HEAD~1 (uncommit without losing code)",
                    "3. Use 'git reflog' to find any branch pointer changes."
                ]
            else:
                mistake_rescue = ["This command is read-only and safe. No recovery action needed!"]
    risk_title = "🔴 DANGER ZONE / HIGH RISK" if cat == "DANGER" else "🟡 CAUTION / STATE CHANGE" if cat == "CAUTION" else "🟢 SAFE & READ-ONLY"

    return {
        "raw_cmd": f"git {cmd_str}",
        "subcmd": subcmd,
        "category": cat,
        "risk_score": score,
        "risk_title": risk_title,
        "warning": warning,
        "summary": base_desc,
        "detail": base_desc,
        "simulated_output": simulated_output,
        "when_to_use": when_to_use,
        "mistake_rescue": mistake_rescue
    }


def _radar_risk_bar(score):
    filled = int(round(score))
    empty  = 10 - filled
    if score >= 8:
        bar_color = Color.RED
    elif score >= 4:
        bar_color = Color.YELLOW
    else:
        bar_color = Color.GREEN
    bar = bar_color + "\u2588" * filled + Color.DIM + "\u2591" * empty + Color.RESET
    return f"  Risk Score : {bar}  {bar_color}{Color.BOLD}{score:4.1f}/10{Color.RESET}"


def _radar_category_color(cat):
    if cat == "DANGER":
        return Color.RED
    if cat == "CAUTION":
        return Color.YELLOW
    return Color.GREEN


def _radar_show_entry(entry):
    clear_screen()
    cc = _radar_category_color(entry["category"])
    sep = "\u2550" * 72
    print(f"\n{cc}{Color.BOLD}\u2554{sep}\u2557{Color.RESET}")
    title_line = f"⚡ GIT COMMAND RADAR: {entry['raw_cmd']}"
    if len(title_line) > 70:
        title_line = title_line[:67] + "..."
    print(f"{cc}{Color.BOLD}\u2551  {title_line:<70}\u2551{Color.RESET}")
    print(f"{cc}{Color.BOLD}\u255a{sep}\u255d{Color.RESET}\n")

    print(f"  {Color.BOLD}Command   :{Color.RESET}  {Color.CYAN}{Color.BOLD}{entry['raw_cmd']}{Color.RESET}")
    print(f"  {Color.BOLD}Risk Level:{Color.RESET}  {cc}{Color.BOLD}{entry['risk_title']}{Color.RESET}")
    print(_radar_risk_bar(entry["risk_score"]))
    print(f"  {Color.YELLOW}{Color.BOLD}\u26a0\ufe0f  {entry['warning']}{Color.RESET}\n")

    print(f"{Color.CYAN}{Color.BOLD}\U0001f4cb WHAT THIS COMMAND DOES{Color.RESET}")
    print(f"  {Color.WHITE}{entry['summary']}{Color.RESET}\n")
    if entry.get("detail") and entry["detail"] != entry["summary"]:
        print(f"{Color.DIM}  {entry['detail']}{Color.RESET}\n")

    print(f"{Color.GREEN}{Color.BOLD}\U0001f5a5\ufe0f  SIMULATED TERMINAL OUTPUT{Color.RESET}")
    for line in entry["simulated_output"].split("\n"):
        print(f"  {Color.DIM}{line}{Color.RESET}")
    print()

    print(f"{Color.BLUE}{Color.BOLD}\U0001f4a1 WHEN TO RUN THIS COMMAND{Color.RESET}")
    for tip in entry["when_to_use"]:
        print(f"  {Color.WHITE}\u2022 {tip}{Color.RESET}")
    print()

    if entry["category"] in ("DANGER", "CAUTION"):
        print(f"{Color.RED}{Color.BOLD}\U0001f6a8 IF YOU ACCIDENTALLY RAN THIS  \u2014  MISTAKE RESCUE PLAN:{Color.RESET}")
    else:
        print(f"{Color.GREEN}{Color.BOLD}\U0001f4dd SAFETY & USAGE NOTES:{Color.RESET}")
    for step in entry["mistake_rescue"]:
        print(f"  {Color.YELLOW}{step}{Color.RESET}")

    print(f"\n{Color.DIM}{chr(0x2500) * 72}{Color.RESET}")
    prompt_input(f"  {Color.DIM}Press Enter to return to Terminal...{Color.RESET}")


def _show_git_manual_cheatsheet():
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}\u2554{chr(0x2550)*72}\u2557{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}\u2551  \U0001f4da  GIT COMMANDS HANDBOOK & CHEATSHEET (from GIT_COMMANDS.md)      \u2551{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}\u255a{chr(0x2550)*72}\u255d{Color.RESET}\n")
    print(f"  {Color.BOLD}You can type ANY of these commands into the Terminal right now:{Color.RESET}\n")

    sections = [
        ("🔴 DANGER ZONE & HIGH RISK", [
            ("git reset --hard HEAD~1", "Rewinds commits & destroys uncommitted edits"),
            ("git push --force origin main", "Overwrites remote branch history"),
            ("git clean -fd", "Deletes untracked files with ZERO backup"),
            ("git branch -D <name>", "Force-deletes unmerged branch"),
            ("git rebase -i HEAD~3", "Rewrites, squashes, or drops commit history"),
            ("git checkout . / restore .", "Wipes all unstaged edits in tracked files"),
            ("git stash drop stash@{0}", "Deletes stashed work commit from queue"),
            ("git filter-branch ...", "Rewrites commit trees across whole history")
        ]),
        ("🟡 EVERYDAY WORKFLOW & STATE CHANGES", [
            ("git commit -m 'message'", "Snapshots staged files into repository history"),
            ("git commit --amend", "Replaces latest commit with staged fixes"),
            ("git diff / diff --staged", "Line-by-line diff of modifications (+ / -)"),
            ("git reflog", "The Time Machine: records every HEAD movement!"),
            ("git blame <file>", "Annotates each line with its author & commit"),
            ("git switch <branch>", "Safely switches to an existing branch"),
            ("git restore --staged <file>", "Unstages files without touching disk code"),
            ("git revert <hash>", "Safe public undo: creates new inverse commit"),
            ("git tag -a v1.0 -m 'v1.0'", "Tags release version milestone on commit"),
            ("git bisect start", "Binary search through history to isolate bugs"),
            ("git cat-file -p HEAD", "Pretty-prints internal object in .git/objects"),
            ("git worktree add ../path", "Checks out branches in parallel folders")
        ])
    ]

    for title, cmds in sections:
        print(f"  {Color.BOLD}{title}:{Color.RESET}")
        for cmd, desc in cmds:
            print(f"    {Color.CYAN}{cmd:<32}{Color.RESET} {Color.DIM}— {desc}{Color.RESET}")
        print()

    prompt_input(f"  {Color.DIM}Press Enter to return to the Terminal prompt...{Color.RESET}")


def mode_git_command_sandbox():
    """
    Universal Git Command Sandbox & Danger Radar.
    User can type ANY Git command in existence directly into the interactive terminal prompt.
    """
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}\u2554{chr(0x2550)*72}\u2557{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}\u2551  \U0001f9ea  UNIVERSAL GIT COMMAND TERMINAL & DANGER RADAR{Color.RESET}{Color.GREEN}{Color.BOLD}{'':>25}\u2551{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}\u255a{chr(0x2550)*72}\u255d{Color.RESET}\n")

        print(f"  {Color.WHITE}Type {Color.BOLD}ANY Git command{Color.RESET}{Color.WHITE} in the entire world (e.g. {Color.CYAN}git reset --hard{Color.WHITE}, {Color.CYAN}push -f{Color.WHITE},")
        print(f"  {Color.CYAN}git clean -fd{Color.WHITE}, {Color.CYAN}status{Color.WHITE}, {Color.CYAN}git rebase -i{Color.WHITE}, {Color.CYAN}branch -D{Color.WHITE}, {Color.CYAN}git bisect{Color.WHITE}, etc.):{Color.RESET}\n")

        print(f"  {Color.DIM}• See simulated terminal output")
        print("  • Inspect danger rating (0-10) & what it does under the hood")
        print(f"  • Read exactly when to run it, and what to do if you ran it by mistake!{Color.RESET}\n")

        print(f"  {Color.DIM}Commands: Type 'help' or 'list' for manual cheatsheet · Press Enter or '0' to exit{Color.RESET}")
        print(f"  {Color.DIM}{chr(0x2500)*72}{Color.RESET}\n")

        cmd_input = prompt_input(f"  {Color.GREEN}{Color.BOLD}git-sandbox:~/oils-project (main) ${Color.RESET} ").strip()

        if cmd_input in ("0", "exit", "quit", "q", "back", ""):
            break
        elif cmd_input.lower() in ("help", "list", "commands", "cheatsheet", "manual", "?"):
            _show_git_manual_cheatsheet()
        else:
            entry = analyze_universal_git_command(cmd_input)
            if entry:
                _unlock_badge("git_basics")
                _radar_show_entry(entry)
            else:
                clear_screen()
                print(f"\n  {Color.YELLOW}\U0001f914 Could not parse '{cmd_input}'. Try typing a git command like:  git status{Color.RESET}\n")
                prompt_input(f"  {Color.DIM}Press Enter to try again...{Color.RESET}")


