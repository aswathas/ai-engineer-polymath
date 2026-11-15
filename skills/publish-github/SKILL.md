---
name: publish-github
description: Use when a change is ready to be shipped to GitHub, so the branch, the push, the documentation check and the pull request happen in a safe order.
---

# Publish GitHub

## When to use

Use this skill when work is ready to leave the local machine and land in the shared
repository. It covers the order of the operations and the checks that must run before
the push. The repository rules are in [AGENTS.md](../../AGENTS.md) and the review
workflow in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Inputs

- The branch name and the change it carries.
- The working tree, already validated.
- The remote `origin`, pointing at `aswathas/ai-engineer-polymath`.

## Procedure

1. Scan the working tree for secrets before anything is staged: keys, tokens, `.env`
   files, connection strings. Remove anything secret and confirm `.env` is ignored. A
   secret is never committed, not even once, not even to fix a mistake.
2. Run the full validation suite: `python tools/validators/run_all.py` and
   `python -m pytest -q`. Both must exit 0.
3. Run the push-time documentation checker, which is the documentation half of the
   validator suite, so no change lands with stale or missing documentation:
   `python tools/validators/run_all.py`. It must exit 0 before the push.
4. Create the branch before the push, so the default branch never carries work in
   progress: `git checkout -b <type>/<short-description>`.
5. Stage and commit with a message that states the outcome and names the validator
   codes that were checked.
6. Push the branch to the remote: `git push -u origin <branch>`. Never amend a commit
   that has already been published; amend only locally and only before the push, and
   otherwise push a follow-up commit.
7. Open the pull request against the default branch, filling in what changed, why, and
   which validators ran.
8. Ask for review, and do not merge your own pull request without a second reader.

## Outputs

- A pushed branch on the remote.
- A pull request describing the change, the validators that ran and the evidence.
- A clean secret scan result.

## Verification

- `python tools/validators/run_all.py` and `python -m pytest -q` both exit 0.
- The documentation checker exits 0.
- The secret scan reports nothing.
- The pull request is open against the default branch, and the history on the remote
  contains no rewritten commits.
