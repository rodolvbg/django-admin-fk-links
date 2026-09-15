import pytest
from django.contrib import admin
from django.urls import reverse

from django_admin_fk_links import ForeignKeyLinkMixin

from .core.admin import CustomBookAdmin
from .core.models import Author, Book

pytestmark = pytest.mark.django_db


def test_list_display_replaces_fk_with_callable_and_keeps_others():
    book_admin = admin.site._registry[Book]

    list_display = book_admin.get_list_display(request=None)

    assert "title" in list_display
    assert "author" not in list_display

    # 'author' must have been converted to a callable _link
    fk_callables = [
        item
        for item in list_display
        if callable(item) and getattr(item, "__name__", "").startswith("author_")
    ]
    assert len(fk_callables) == 1

    fk_callable = fk_callables[0]
    # short_description must be 'Author' (field name)
    assert hasattr(fk_callable, "short_description")
    assert fk_callable.short_description.lower() == "author"
    assert getattr(fk_callable, "admin_order_field", None) == "author"


def test_list_editable_is_not_converted_to_link():
    """Fields in list_editable must not be converted into links."""
    book_admin = admin.site._registry[Book]

    list_display = book_admin.get_list_display(request=None)

    # there must be no callable whose name starts with 'status_'
    assert not any(
        callable(item) and getattr(item, "__name__", "").startswith("status_")
        for item in list_display
    )


def test_fk_link_renders_admin_change_url_for_related_object():
    """The generated link must point to Author's change view in the admin."""
    author = Author.objects.create(name="Clientito")
    book = Book.objects.create(title="Libro", author=author)

    book_admin = admin.site._registry[Book]
    list_display = book_admin.get_list_display(request=None)

    fk_callable = next(
        item
        for item in list_display
        if callable(item) and getattr(item, "__name__", "").startswith("author_")
    )

    html = fk_callable(book)
    expected_url = reverse("admin:core_author_change", args=[author.pk])

    assert expected_url in html
    assert "<a" in html
    assert "href" in html
    assert "Clientito" in html


def test_fk_link_returns_dash_when_related_is_none():
    """If the FK is None, it must return '-'."""
    book = Book.objects.create(title="Libro sin autor", author=None)

    book_admin = admin.site._registry[Book]
    list_display = book_admin.get_list_display(request=None)

    fk_callable = next(
        item
        for item in list_display
        if callable(item) and getattr(item, "__name__", "").startswith("author_")
    )

    html = fk_callable(book)
    assert html == "-"  # 'if not related' branch


def test_custom_get_list_display_foreign_key_links_is_used():
    """
    If get_list_display_foreign_key_links is overridden,
    it must be used instead of the attribute.
    """
    model_admin = CustomBookAdmin(Book, admin.site)

    list_display = model_admin.get_list_display(request=None)

    fk_callables = [
        item
        for item in list_display
        if callable(item) and getattr(item, "__name__", "").startswith("author_")
    ]
    assert len(fk_callables) == 1


def test_build_fk_link_callable_with_nonexistent_field_uses_fallback_verbose():
    """
    Exception branch in _build_fk_link_callable:
    if the field doesn't exist, it uses the verbose fallback without
    admin_order_field.
    """

    # Create a "dummy" admin with the Author model and a nonexistent field
    class DummyAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
        list_display = ("id",)

    dummy_admin = DummyAdmin(Author, admin.site)

    fn = dummy_admin._build_fk_link_callable("nonexistent_field")

    # short_description = field name with underscores replaced by spaces
    assert fn.short_description == "nonexistent field"
    # admin_order_field is not set (order_field=None branch)
    assert not hasattr(fn, "admin_order_field")
