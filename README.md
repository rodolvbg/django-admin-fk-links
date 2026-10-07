# django-admin-fk-links

[![Build status](https://github.com/rodolvbg/django-admin-fk-links/actions/workflows/pytest.yml/badge.svg)](https://github.com/rodolvbg/django-admin-fk-links/actions/workflows/pytest.yml)
[![PyPI version](https://img.shields.io/pypi/v/django-admin-fk-links.svg)](https://pypi.org/project/django-admin-fk-links/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-admin-fk-links)](https://pypi.org/project/django-admin-fk-links/)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-admin-fk-links)](https://pypi.org/project/django-admin-fk-links/)
[![Downloads](https://static.pepy.tech/personalized-badge/django-admin-fk-links?period=month&units=international_system&left_color=black&right_color=blue&left_text=Downloads/month)](https://pepy.tech/project/django-admin-fk-links)

Reusable Django admin mixin that turns `ForeignKey` fields into direct clickable links to their related admin change views.

---

## ✨ Features

- ✅ Converts `ForeignKey` fields into clickable links in `list_display`
- ✅ Works with the default Django admin and custom `AdminSite`
- ✅ Zero configuration
- ✅ No need to add to `INSTALLED_APPS`
- ✅ Fully compatible with Django 2.2+
<!-- - ✅ Tested with `pytest` and `pytest-django` -->

---

## 📦 Installation

```bash
pip install django-admin-fk-links
```

## 🚀 Quick Usage
```python
from django.contrib import admin
from django_admin_fk_links import ForeignKeyLinkMixin

@admin.register(Book)
class BookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
    list_display = ("title", "author")
    list_display_foreign_key_links = ("author",)
```
That’s it.
The author column will now be a direct link to its admin change view.

---

## 🖼️ Screenshots

**Before** — `author` rendered as plain text:

![Book changelist without the mixin](docs/screenshots/book_changelist_before.png)

**After** — `author` rendered as a clickable link to its change view:

![Book changelist with the mixin](docs/screenshots/book_changelist.png)

---

## ⚙️ How It Works
The mixin dynamically replaces the fields listed in:
```python
list_display_foreign_key_links = ("field_name",)
```

with callables that render an `<a>` tag pointing to the related object’s admin change view.

It also supports:
- Sorting via admin_order_field
- Automatic verbose_name resolution
- Custom AdminSite namespaces

### Customizing the link

Override `get_foreign_key_link()` to change the markup — return safe HTML
(`format_html()`), since the admin escapes plain strings:

```python
from django.utils.html import format_html


class BookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
    list_display = ("title", "author")
    list_display_foreign_key_links = ("author",)

    def get_foreign_key_link(self, obj, field_name, related, url):
        return format_html('<a class="button" target="_blank" href="{}">{}</a>', url, related)
```

Or render it from a template, with `obj`, `related`, `url`, `field_name`
and `link_class` in its context:

```python
class BookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
    list_display = ("title", "author")
    list_display_foreign_key_links = ("author",)
    foreign_key_link_template = "admin/book_author_link.html"
```

```django
{# templates/admin/book_author_link.html #}
<a class="fk-link" href="{{ url }}" title="{{ obj }}">{{ related }}</a>
```

To only add a CSS class, set `foreign_key_link_class = "my-link"`.

---
## 🎨 Themes

- [django-unfold](docs/themes/unfold.md): works as it is, with Unfold's
  link colors.

---
## ✅ Compatibility
- Django 2.2+
- Python 3.7+
- Default admin.site ✅
- Custom AdminSite(name="custom") ✅

---
## 🪪 License

This project is licensed under the MIT License.

---
## 🤝 Contributing

Contributions, issues and feature requests are welcome.
Feel free to open a PR or issue.

## ⭐ If you find it useful

Please consider giving the project a ⭐ on GitHub — it really helps!
