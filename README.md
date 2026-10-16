# django-admin-fk-links

[![Current version on PyPI](https://img.shields.io/pypi/v/django-admin-fk-links.svg)](https://pypi.org/project/django-admin-fk-links/)

> **This package is now part of
> [django-admin-tables](https://github.com/rodolvbg/django-admin-tables)**,
> with the same `ForeignKeyLinkMixin` and other extras for the Django
> admin's tables (exclusive radio fields, hideable and responsive columns,
> footer rows). This last release has **no code**: importing it raises an
> `ImportError` that says how to migrate. Pin `django-admin-fk-links<0.1.5`
> to keep using the old one until you do.

## Migrating

```bash
pip uninstall django-admin-fk-links
pip install django-admin-tables
```

| Before | After |
|---|---|
| — | `"django_admin_tables"` in `INSTALLED_APPS` |
| `from django_admin_fk_links import ForeignKeyLinkMixin` | `from django_admin_tables import ForeignKeyLinkMixin` (or `AdminTablesMixin`) |
| `django_admin_fk_links.admin_mixins` | `django_admin_tables.fk_links.mixins` |

The options (`list_display_foreign_key_links`, `get_foreign_key_link()`,
`foreign_key_link_template`, `foreign_key_link_class`) and the behavior are
the same: see
[django-admin-tables' README](https://github.com/rodolvbg/django-admin-tables#foreign-key-links).
It requires Django 4.2+ and Python 3.10+, and `ForeignKeyLinkMixin` goes
before `admin.ModelAdmin` in the bases.
