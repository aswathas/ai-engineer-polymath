# Issue tracker: GitHub

Issues and specs for this repository live as GitHub issues in `aswathas/ai-engineer-polymath`.
Use the `gh` CLI for all operations.

**This repository's issues are learning work items.** One issue per acceptance criterion, in
series order. Issue *n* is blocked by issue *n-1*, so exactly one issue is startable at a time.

The issue list is generated from the module notes, so the notes are the source of truth:

```bash
python tools/create_issues.py --dry-run          # print the plan
python tools/create_issues.py                    # create what is missing
```

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels --jq '.[] | {number, title, labels: [.labels[].name]}'`.
- **Blocking**: GitHub's native issue dependencies. `gh issue edit <child> --add-blocked-by <blocker>`
  (gh 2.94+). Fallback for older gh: a `Blocked by: #<n>` line at the top of the child body. A
  ticket is unblocked when every blocker is closed.
- **Count open blockers**: `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by`.
- **Comment on an issue**: `gh issue comment <number> --body "..."`.
- **Apply or remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Close**: post the explanation with `gh issue comment`, then `gh issue close <number>`.

Infer the repository from `git remote -v`; `gh` does this automatically inside a clone.

File issues only into the user's own repository. Before the first `gh issue create` of a
session, check the target with `gh repo view --json nameWithOwner`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue in this repository.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.
