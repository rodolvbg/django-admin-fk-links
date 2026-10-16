# django-admin-fk-links

[![Current version on PyPI](https://img.shields.io/pypi/v/django-admin-fk-links.svg)](https://pypi.org/project/django-admin-fk-links/)

> **This package is now part of
> [django-admin-rows](https://github.com/rodolvbg/django-admin-rows)**,
> with the same `ForeignKeyLinkMixin` and other row-level extras for the
> Django admin. This last release only keeps the old imports working, with a
> `DeprecationWarning`; it gets no new features.

## Migrating

```bash
pip uninstall django-admin-fk-links
pip install django-admin-rows
```

| Before | After |
|---|---|
| `from django_admin_fk_links import ForeignKeyLinkMixin` | `from django_admin_rows import ForeignKeyLinkMixin` |
| `django_admin_fk_links.admin_mixins` | `django_admin_rows.fk_links.mixins` |
| — | `"django_admin_rows"` in `INSTALLED_APPS` |

The options (`list_display_foreign_key_links`,
`get_foreign_key_link()`, `foreign_key_link_template`,
`foreign_key_link_class`) and the behavior are the same: see
[django-admin-rows' README](https://github.com/rodolvbg/django-admin-rows#foreign-key-links).

django-admin-rows requires Django 4.2+ and Python 3.10+; so does this
release, which installs it and keeps working until you migrate.
