"""django-admin-fk-links is now part of django-admin-rows.

This package only keeps the old imports working: use ``django_admin_rows``
(``from django_admin_rows import ForeignKeyLinkMixin``) instead.
"""

import warnings

from django_admin_rows.fk_links import ForeignKeyLinkMixin

warnings.warn(
    "django-admin-fk-links is now part of django-admin-rows: install "
    "django-admin-rows and import from django_admin_rows instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ForeignKeyLinkMixin"]

__version__ = "0.1.5"
