# Branch Strategy

## Quick reference

- [Branch Types & Examples](#branch-types--examples)
- [Branch Naming Rules](#branch-naming-rules)
- [Pull Request (PR) Workflow](#pull-request-pr-workflow)
- [Labels Policy](#labels-policy)
- [Clean History & Rebasing Policy](#clean-history--rebasing-policy)
- [Hotfix Flow (Urgent Production Issues)](#hotfix-flow-urgent-production-issues)

## Overview

This document describes the branch strategy for this repository.
It focuses only on branch naming, branch lifecycle, PR workflow, and
branch hygiene — release, tagging, and deployment are documented separately
in [Release Process](release_process.md).

The goals:
- Keep `main` always deployable and stable.
- Avoid long-lived branches.
- Keep history clean and reviewable.
- Maintain traceability via Pull Requests.

Why this strategy? It follows a simplified GitHub Flow, ideal for solo or small teams, ensuring fast iteration while maintaining stability.

## Core Principles

1. **One task = one branch.** Create a single branch per feature, fix, or doc change.  
2. **No direct commits to `main`.** All changes must be merged via PR.  
3. **Short-lived branches.** Prefer branches that live hours–days, not weeks.  
4. **Clean history before merge.** Rebase, fixup, or squash before merging.  
5. **`main` is always production-ready.**

## Branch Types & Examples

All topic branches are created from `main`.

### `main`
- Production branch (always stable).
- Protected from direct pushes (recommended).

### `feature/<short-description>`
For new features or enhancements.

Examples:
```
feature/add-email-verification
feature/payment-integration
feature/user-profile-avatar
```

Rules:
- Branch from `main`.
- One feature per branch.
- Keep short-lived.
- Open a PR to `main` when ready.

### `fix/<short-description>`
For non-urgent bug fixes.

Examples:
```
fix/profile-null-response
fix/login-validation-error
```

Rules:
- Branch from `main`.
- Include tests if applicable.
- Open PR to `main`.

### `hotfix/<short-description>`
For urgent production fixes.

Examples:
```
hotfix/security-patch
hotfix/payment-timeout
```

Rules:
- Branch from `main`.
- Prioritize quick verification and merge.
- Merge immediately after verification.
- After merge: optionally tag and document the fix (see [Release Process](release_process.md)).

## Branch Naming Rules

- **Lowercase only.**
- **Use hyphen (`-`) as separator.**
- **Do not use underscores.**
- **Be concise but descriptive.**

Good:
```
feature/add-payment-gateway
fix/null-response-auth
feature/commit-convention
```

Bad:
```
Feature_NewAuth
bugFix1
feature_user_auth
```

## Pull Request (PR) Workflow

Use PRs to:
- Summarize intent.
- Document reasoning.
- Serve as a checkpoint before merging.

PR rules:
- **PR target:** `main`.
- **PR title:** Follow [Commit Message Convention](commit_convention.md) (e.g., `feat(auth): add oauth support`).
- **Hotfix PRs:** Must include both the `hotfix` label and a `priority:*` label.
- **PR description:** Explain *what* changed, *why*, and list any manual steps (e.g., migrations, database changes).
- **Tests & checks:** Run locally before opening PR; CI will enforce on merge.
- **Merge method:** **Squash & merge** is recommended (keeps history tidy with a single, clean commit message). Alternatives: Rebase merge for linear history.
- **Delete branch** after merge.

Recommended:
- Add a short checklist in PR body (e.g., tests passed, migrations applied, docs updated).
- Link related issues using `Fixes #<number>` in PR body or merge commit.

## Labels Policy

Labels are used to classify issues and pull requests for prioritization and clarity.
They are used for triage, filtering.

### Priority labels
- `priority:critical` – Production-breaking or security issues (highest urgency).
- `priority:high` – Important functionality affecting users; high urgency.
- `priority:medium` – Standard improvements or non-urgent fixes.
- `priority:low` – Minor improvements, refactors, or documentation.

### Special labels

- `hotfix` – Indicates urgent production fixes and must be handled with highest priority.
- `ci/cd` – Marks changes related to CI/CD: workflows, reusable workflows, composite actions,
CI configuration, deployment automation, and related infra (GitHub Actions, pipelines, etc.).
- `refactor` – Marks pull requests or issues that restructure or improve existing code without changing external behavior or functionality.
- `chore` – Marks maintenance tasks that do not affect application logic, such as updating dependencies, modifying build configuration, or improving project tooling.

Guidelines:
- **Every issue and PR must have one `priority:*` label.**
- **Hotfix PRs must include both `hotfix` and an appropriate `priority:*` label.**
  - Use `priority:critical` for security / production-breaking fixes.
  - Use `priority:high` for urgent but non-breaking fixes.
- Labels improve traceability and planning but do not replace branch naming conventions.
- Other labels (bug, enhancement, docs, etc.) can be used as standard GitHub labels.

## Clean History & Rebasing Policy

Before requesting merge:
- Rebase your branch on latest `main` to minimize merge conflicts and keep history linear:

    ```bash
    git checkout main
    git pull origin main
    git checkout feature/your-branch
    git rebase main

    # Resolve conflicts if any
    git push --force-with-lease
    ```
- Use `git commit --fixup=<SHA>` and `git rebase -i --autosquash` to tidy WIP/fixup commits.
- If force-push is not desirable (e.g., to preserve CI history), merge `main` into the branch instead:

    ```bash
    git fetch origin
    git merge origin/main
    git push
    ```

- Rebasing is preferred for a linear, clean history. When force-pushing, always use `--force-with-lease` to avoid overwriting others' work.

Troubleshooting:
- Conflicts during rebase: Use `git rebase --continue` after resolving, or `git rebase --abort` to cancel.
- If history too messy: Squash via GitHub PR interface.

## Hotfix Flow (Urgent Production Issues)

1. Create hotfix branch from `main`:

    ```bash
    git checkout -b hotfix/short-description main
    ```

2. Implement fix, test locally.
3. Open PR to `main` and mark as high priority via labels.
4. Merge (squash/merge) after verification and deploy as needed.
5. Document the fix and, if applicable, tag a patch release (see [Release Process](release_process.md)).

## Branch Protection & Repository Settings (Recommended)

Enable repository protections:
- Protect `main`: Disallow direct pushes.
- Require PR reviews or at least self-approval for traceability.
- Require status checks (e.g., CI via GitHub Actions) to pass before merge.
- Enable force-push prevention on protected branches.

## Helpful Git Commands (Cheat Sheet)

Create & push a new feature branch:

```bash
git checkout -b feature/add-email-verification main
git push -u origin feature/add-email-verification
```

Rebase branch on latest main:

```bash
git checkout main
git pull origin main
git checkout feature/your-branch
git rebase main
git push --force-with-lease
```

Use fixup and autosquash:

```bash
git commit --fixup=<SHA>
git rebase -i --autosquash main
git push --force-with-lease
```

# Conclusion

This strategy ensures a stable, traceable, and efficient workflow. It minimizes errors, supports growth to team environments, and keeps your repository clean and readable.