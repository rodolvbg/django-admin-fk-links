# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/0.1.1/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

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
