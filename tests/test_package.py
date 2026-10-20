import importlib
from unittest import TestCase


class TestPackage(TestCase):
    """The retired package."""

    def test_importing_it_says_where_it_moved(self):
        with self.assertRaisesRegex(ImportError, "now part of django-admin-tables"):
            importlib.import_module("django_admin_fk_links")
