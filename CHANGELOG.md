# Changelog

All notable changes to Katsuo are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-11-09

### Added

- **Learn (retrospect) step.** After each change Katsuo records durable,
  project-specific lessons into `docs/memory.md` and `docs/decisions/`, and asks
  what to remember next time.
- **Start from memory.** Every run reads project memory before sizing the work,
  so Katsuo improves every day instead of re-learning the same things.
- **MIT license** and this changelog.
- A test asserting the learning loop and license are present.

### Changed

- Positioning: quality-first, test-driven, minimal, private, and it learns.

## [0.1.0] - 2026-10-06

### Added

- `/katsuo` command: size → setup → spec → test-driven build → independent
  review → Pull Request.
- Independent read-only `reviewer` agent.
- `guard_git.py` PR-only Git hook (blocks protected-branch pushes, force/bulk
  pushes, and `gh pr merge`).
- Deterministic and live end-to-end proof suite.
