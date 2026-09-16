# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/0.1.1/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Type checking: `mypy` + `django-stubs`, wired into `pyproject.toml` and
  the pre-commit hooks. `ForeignKeyLinkMixin` now inherits from
  `ModelAdmin` (rather than staying a bare mixin) purely so `self`/`super()`
  are typed for free — behavior is unchanged.
- Compatibility matrix via tox (`[tool.tox]` in `pyproject.toml`, using
  [tox-uv](https://github.com/tox-dev/tox-uv)): tests every Django series
  in `classifiers` (2.2 through 6.0) against its oldest and newest
  supported Python, within this package's own floor. `uv run tox run`
  locally, a separate `compat-matrix.yml` CI workflow.
- `CONTRIBUTING.md`.

### Changed

- Build backend: `setuptools` → `hatchling`.
- Linting: dropped `black`/`isort`, ruff (`ruff check` + `ruff format`)
  only.
- Coverage config moved from a standalone `.coveragerc` into
  `[tool.coverage]` in `pyproject.toml`.
- pre-commit hooks pinned to frozen SHAs, added `django-upgrade` and
  `pyproject-fmt`.

### Fixed

- `pytest-cov` was missing from the dev dependencies and `addopts` had no
  `--cov` flag, so `uv run pytest` silently ran with no coverage report at
  all.

---

## [0.1.2] - 2026-09-15

### Added
- Type hints across `ForeignKeyLinkMixin` and a `py.typed` marker for static type checking support.
- Docstrings for `ForeignKeyLinkMixin`, `_build_fk_link_callable`, and the generated `fk_link` callable.
- Before/after screenshots of the admin changelist in the README.

---

## [0.1.1] - 2025-12-06

### Added
- `ForeignKeyLinkMixin` to render `ForeignKey` fields in `list_display` on the `ModelAdmin` as clickable links to the related admin change view.
- Support for default `admin.site` and custom `AdminSite` instances (via `self.admin_site.name`)
