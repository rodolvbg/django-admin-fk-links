"""The compatibility layer over django-admin-rows."""

import importlib

import pytest
from django_admin_rows import fk_links

import django_admin_fk_links


def test_importing_it_warns():
    with pytest.warns(DeprecationWarning, match="django-admin-rows"):
        importlib.reload(django_admin_fk_links)


def test_the_old_imports_are_django_admin_rows_objects():
    from django_admin_fk_links import ForeignKeyLinkMixin
    from django_admin_fk_links.admin_mixins import (
        UNFOLD_LINK_CLASS,
    )
    from django_admin_fk_links.admin_mixins import (
        ForeignKeyLinkMixin as FromModule,
    )

    assert ForeignKeyLinkMixin is FromModule is fk_links.ForeignKeyLinkMixin
    assert UNFOLD_LINK_CLASS == fk_links.UNFOLD_LINK_CLASS
