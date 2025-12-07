import pytest
from django.contrib import admin
from django.urls import reverse

from django_admin_fk_links import ForeignKeyLinkMixin
from .core.models import Author, Book
from .core.admin import CustomBookAdmin

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
    # short_description must be 'Author' (nombre del campo)
    assert hasattr(fk_callable, "short_description")
    assert fk_callable.short_description.lower() == "author"
    assert getattr(fk_callable, "admin_order_field", None) == "author"


def test_list_editable_is_not_converted_to_link():
    """Campos en list_editable no deben convertirse en enlaces."""
    book_admin = admin.site._registry[Book]

    list_display = book_admin.get_list_display(request=None)

    # no debe haber ningún callable cuyo nombre empiece por 'status_'
    assert not any(
        callable(item) and getattr(item, "__name__", "").startswith("status_")
        for item in list_display
    )


def test_fk_link_renders_admin_change_url_for_related_object():
    """El enlace generado debe apuntar al change de Author en el admin."""
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
    """Si el FK es None, debe devolver '-'."""
    book = Book.objects.create(title="Libro sin autor", author=None)

    book_admin = admin.site._registry[Book]
    list_display = book_admin.get_list_display(request=None)

    fk_callable = next(
        item
        for item in list_display
        if callable(item) and getattr(item, "__name__", "").startswith("author_")
    )

    html = fk_callable(book)
    assert html == "-"  # branch de 'if not related'


def test_custom_get_list_display_foreign_key_links_is_used():
    """
    Si se sobreescribe get_list_display_foreign_key_links,
    debe usarse en lugar del atributo.
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
    Branch de excepción en _build_fk_link_callable:
    si el campo no existe, usa verbose fallback y sin admin_order_field.
    """
    # Creamos un admin "dummy" con modelo Author y campo inexistente
    class DummyAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
        list_display = ("id",)

    dummy_admin = DummyAdmin(Author, admin.site)

    fn = dummy_admin._build_fk_link_callable("nonexistent_field")

    # short_description = nombre del campo con guiones bajos sustituidos por espacios
    assert fn.short_description == "nonexistent field"
    # admin_order_field no se define (branch order_field=None)
    assert not hasattr(fn, "admin_order_field")