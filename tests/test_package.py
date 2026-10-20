import importlib

import pytest


class TestPackage:
    """The retired package."""

    def test_importing_it_says_where_it_moved(self):
        with pytest.raises(ImportError, match="now part of django-admin-tables"):
            importlib.import_module("django_admin_fk_links")
