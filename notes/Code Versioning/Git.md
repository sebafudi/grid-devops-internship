VCS - version control system
Subversion, CVS, Mercurial - other vcs
by Linus Torvalds

Git - local
GitHub - hosts Git repositories

`git config --global user.name "<first name> <last name>`
`git config --global user.email "email@example.com"`

`git status`
`git init`

`git add <file>`
`git commit [-m <message>]`
`git log`
`git add .` stage all changes at once

`git config --global core.editor "code --wait"`

`git log --oneline`
`git log --pretty oneline --abbrev-commit`
`git commit --ammend` do this after `git commit` and `git add` to add changes to last commit or change the commit message

`.gitignore`

`git branch` show branches
`git branch <name>` create, but not switch to it
`git switch <branch name>` switch to branch (new command, rather than checkout)

`git commit -a` add all files

`git checkout <branch name>` swiss army, does more things

`git switch -c <name>` create and switch
`git checkout -b <name>` create and switch

`git branch -d <name>` delete branch
`git branch -m <name>` move/rename current branch

fast forward merge - move to newer commit
![[Screenshot 2024-06-27 at 16.03.55.png]]

1. Switch to destination branch
2. `git merge <branch>` merge it to current branch

auto merge

auto merge with conflicts

switch
merge
fix conficts
remove markers
add
commit

`git diff`
`diff --git a/file.txt b/file.txt` compare files from (old and new)

hunk header
`@@ -3,4 +3,5 @@`
4 lines from 3
5 lines from 3

diff default shows changes that are not staged

`git diff HEAD` shows staged files too

`git diff --staged` show only staged

`git diff --cached`

`git diff <file>`
`git diff master..<branch>` compare branches (you can omit the .. and use a space)

`git diff <hash>..<hash>` compare two commits (can also use a space)

`git diff HEAD/--cached/--staged <hash>..<hash>`

`git stash` create stash
`git stash pop` apply stash and delete it
`git stash apply` doesn't delete the stash
`git stash list`
`git stash apply stash@{2}` apply second stash
`git stash drop stash@{2}` delete without applyinh
`git stash clear` clear entire stash

HEAD should point to a branch
if HEAD points to particular commit - DETACHED HEAD
`git checkout <hash>` move HEAD to commit

`git checkout HEAD~1` previous commit

`git switch -` change to last branch

`git checkout HEAD <file>` reset file to HEAD version
`git checkout -- <file>` reset file to HEAD version
`git restore <file>` restore file, defaults to HEAD
`git restore --source HEAD~2 <file>` 2 commits back

`git restore --staged <file>` unstage file

`git reset <commit hash>` reset repo to that commit, but keep the changes in local files
`git reset --hard <commit>` reset repo and remove changes

`git revert <hash>` revert changes with new commit

`git clone <url>`

`ssh-keygen -t ed25519 -C "email@example.com"` keygen with comment

`pbpaste`
`pbcopy`

`git remote [-v]` show remotes
`git remote add <name> <url>` standard name is `origin`
`git remote rename <old> <new>`
`git remove remove <name>`

`git push <remote> <branch>`
`git push origin master`

`git push origin <local branch>:<remote branch>` push branch to different branch on remote

`git push -u origin master` sets the upstream of a branch - run `git push` without asking for remote, short for `--set-upstream`

`git branch -M main` change branch name to main

remote tracking branch `origin/master` pointer to where to master was at the point of last sync with remote

`git branch -r` show remote branches

`git switch <remote branch without origin>` makes local branch and set track remote

`git checkout --track origin/<remote branch>` old way of doing this, track remote branch

![[Screenshot 2024-06-28 at 15.16.49.png]]

`git fetch <remote>` just fetch, don't apply to local workspace
`git pull <remote> <branch>` fetch and apply to local workspace

# Markdown.md
[markdown-it demo](https://markdown-it.github.io/)

# Git Workflows
## Centralized
Only work on master
## Feature Branches
Create new branches for each new feature

## Fork & clone
Fork the repo and work on the fork 
`origin` - your repo
`upstream` - original repo
then create a pull request to merge it
pull changes from upstream

# rebase
change to branch
`git rebase master` or any other branch
resolve conflicts, don't commit
`git rebase --continue`

## interactive rebase
`git rebase -i HEAD~4`

pick - use the commit
reword - use the commit, but edit the commit message
edit - use commit, but stop for amending
fixup - use commit contents but meld it into previous commit and discard the commit message
drop - remove commit

# tags
`git tag` list tags
`git tag -l "*beta*"` filter
`git checkout <tag>`
`git diff <tag> <tag>`

`git tag <tag>` tag at current HEAD (lightweight tag)
`git tag -a <tag>` create an annotated tag (annotated tag)
`git show <tag>` info about tag

`git tag <name> <commit hash>` tag commit other than current HEAD

`git tag -f <name> <hash>` force the tag, move it

`git tag -d <tag>` delete tag
`git push <remote> --tags` push all tags
`git push <remote> <tag>` push single tag


`git config --local user.name <...>` config local

# hashing
git uses SHA-1
40 char output
`git hash-object <file>`
`echo 'hello' | git hash-object --stdin`
`git hash-object <file> -w` save the hash to `.git`

`git cat-file -p <obj hash>`

`git cat-file -p <obj hash> > file.txt` restore file

# blobs
binary large objects

# trees
![[Screenshot 2024-06-28 at 22.02.32.png]]

![[Screenshot 2024-06-28 at 22.02.57.png]]

`git cat-file -p master^{tree}` show tree
`git cat-file -t <hash>` show type of obj

# commits
![[Screenshot 2024-06-28 at 22.05.53.png]]

![[Screenshot 2024-06-28 at 22.06.34.png]]

![[Screenshot 2024-06-28 at 22.08.39.png]]

# reflog
about 90 days by default
`git reflog show HEAD`
`git reflog show <branch/something>`

`HEAD@{13}` reflog reference
`git reflog master@{one.week.ago}`
`git reflog bugfix@{2.days.ago}`
`git diff master@{0} master@{yesterday}`

`git reset --hard master@{1}` rescue deleted commit (works only on local repo)

# config files
local - in repo `.git`
global `~/.gitconfig` or `~/.config/git/config`
global system wide - ?

`git config --global user.name`
`git config --global user.name "..."`

# aliases
in global config files
```
[alias]
	s = status
	l = log
```
`git confog --global alias.s status`
### with arguments
```
[alias]
	cm = commit -m
```

`git cm "<message>"`

https://github.com/GitAlias/gitalias
https://www.durdn.com/blog/2012/11/22/must-have-git-aliases-advanced-examples/
https://gist.github.com/mwhite/6887990

you can run shell in aliases with `!` at the start

# more
- [Presentation “Git in Action”](https://drive.google.com/file/d/1x6jdgxEBej9fMUYRwXy_0YRLXz8nWhQC/view)
- [Git tutorial by vogella.com](https://www.vogella.com/tutorials/Git/article.html#gitdefintion_tools1)
- [http://think-like-a-git.net/](https://think-like-a-git.net/)- A lighthearted overview of git.
- [http://gitimmersion.com/](https://gitimmersion.com/) - An in-depth git tutorial.
- [http://pcottle.github.io/learnGitBranching](https://learngitbranching.js.org/) - An interactive/graphical demo on how git handles commits, branches, and shows the operations git performs on them.
- Article [Getting Started with Git Rebase –onto](https://tanzu.vmware.com/content/tech-guides/getting-started-with-git-rebase-onto-for-specific-commits)

