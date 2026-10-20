# Commit Message Documentation

## Commit Message Format

Each commit message should follow a strict format to maintain clarity and consistency and to enable automation like CHANGELOG generation.

### Header (Subject Line)

Format: 
`<type>(<scope>): <short summary>`

Example:
`feat(auth): add Google OAuth support`

Requirements:
- type — required, lowercase (see allowed types).
- scope — optional, lowercase, single token (e.g., auth, ui, api).
- subject — imperative (present tense), brief, no trailing period.
- Header must be a single line. Recommended max length: <= 100 characters.

### Body (Optional / Required per-type)

- Leave one blank line after the header.
- Explain why the change was made and important details.
- Required for feature and fix commits; optional for docs.
- Wrap lines at ~100 characters.
- Use bullet points for multiple items.
- Use backticks for technical terms: `UserService`, `fetchProfile()`.

### Footer

- Use for issue references and breaking changes.
- Issue references example: Fixes #123
- Breaking changes: must include a line starting with "BREAKING CHANGE:" and migration notes.

Example:
```
BREAKING CHANGE: /v1/login replaced with /v2/login; clients must include `force=true`.
Fixes #789
```

## Quoting Technical Terms

- Use backticks in the body and footer for classes, methods, files and flags.
- Avoid backticks in the header unless necessary (e.g., CLI flags like `--force`).

## Types of Commit Messages

Allowed types (lowercase):
- feat — new feature
- fix — bug fix
- docs — documentation only
- style — formatting (no code change)
- refactor — refactoring (no functional changes)
- perf — performance improvement
- test — tests
- build — build system / dependencies
- ci — CI config
- chore — other tasks

## Scope Guidelines

- Scope indicates module/package/subsystem affected: e.g., auth, api, core.
- Omit scope for global changes.

## Breaking Changes

- Include "BREAKING CHANGE:" in footer with detailed migration steps.
- Breaking changes generally cause a major semver bump.

## Examples

### Feature:
```
feat(session): add support for multiple concurrent sessions

Added `SessionManager` to support storing multiple sessions per user.
Previously sessions overwrote each other which caused unexpected logout
on other devices. `SessionManager` stores sessions keyed by device id,
introduces conflict detection and graceful eviction.

Fixes #123
```

### Fix:
```
fix(profile): handle null response from profile API

`fetchProfile()` now validates the response and uses fallback values when
the profile API returns `null`. This prevents crashes during profile load.
```

### Docs:
```
docs: update API documentation for authentication endpoints

Added examples for `/login` and `/logout` endpoints.
```

### Refactor:
```
refactor(core): extract user creation logic into UserService

Moved logic to improve separation of concerns. No functional changes.
```

### Performance (perf)
```
perf(search): optimize product search query to reduce DB time (#239)

Added composite index and moved expensive filters to DB layer which
reduces query time from ~500ms to ~120ms on large datasets.
```

### Chore/Deps:
```
chore(deps): bump axios to 0.21.1

Updated dependency for security; verified compatibility.
```

### Build (build)
```
build: update webpack to 5.72.0 and adjust loader config (#241)

Updated webpack and loader config to support new asset pipeline.
Rebuilt assets and verified dev and prod builds.
```

### CI (ci)
```
ci: add GitHub Actions workflow for integration tests (#242)

Added integration-tests.yml that runs on push and pull_request to
execute integration test suite against a test DB container.
```

### Breaking example:
```
feat(api): migrate to v2 authentication

BREAKING CHANGE: auth token format changed; clients must request new tokens
using /v2/token. See docs/migrations/v2-auth.md.
```

## Enforcement & Tooling

- Enforce message format in CI.
- Use semantic-release or standard-version for changelogs and version bumps.

## Checklist (before commit)

- Header format correct: type(scope): subject
- Subject is imperative and without trailing period
- Body explains why and how (if needed)
- Backticks for technical terms
- Footer contains Fixes # or BREAKING CHANGE: if needed

# Conclusion

This documentation follows Angular / Conventional Commits conventions: use strict header format with optional scope, require clear bodies for feature/fix commits, use BREAKING CHANGE: for major changes. Following this will keep commit history consistent and enable automated releases and changelog generation.