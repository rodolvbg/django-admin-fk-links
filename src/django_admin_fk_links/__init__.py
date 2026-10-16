"""django-admin-fk-links is now part of django-admin-tables.

This last release has no code: install django-admin-tables instead.
"""

raise ImportError(
    "django-admin-fk-links is now part of django-admin-tables, and this last "
    "release has no code. Uninstall it, install django-admin-tables, put "
    "'django_admin_tables' in INSTALLED_APPS, and import ForeignKeyLinkMixin "
    "(or AdminTablesMixin) from django_admin_tables: "
    "https://github.com/rodolvbg/django-admin-tables"
)
