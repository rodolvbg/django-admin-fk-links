from django.contrib import admin

from django_admin_fk_links import ForeignKeyLinkMixin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
    list_display = ("title", "author")
    list_display_foreign_key_links = ("author",)


class CustomBookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin):
    """
    Admin NO registrado, sólo para probar override de
    get_list_display_foreign_key_links y el branch de campo inexistente.
    """

    list_display = ("id", "title", "author")

    def get_list_display_foreign_key_links(self, request):
        # aunque el atributo list_display_foreign_key_links estuviera vacío,
        # este método manda.
        return ("author",)
