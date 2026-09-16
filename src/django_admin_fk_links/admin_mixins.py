from __future__ import annotations

from typing import Any, Callable, Sequence

from django.contrib.admin import ModelAdmin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString


class ForeignKeyLinkMixin(ModelAdmin):
    """ModelAdmin mixin rendering chosen FK fields in list_display as links
    to their change view.

    Inherits from ``ModelAdmin`` (rather than staying a bare mixin) purely
    so ``self``/``super()`` are typed for free — ``get_list_display``,
    ``list_editable``, ``model``, and ``admin_site`` all live there. Meant
    to sit before ``admin.ModelAdmin`` in a subclass's bases, e.g.
    ``class BookAdmin(ForeignKeyLinkMixin, admin.ModelAdmin)``; Python's
    MRO resolves ``super()`` calls to the concrete ``ModelAdmin`` subclass
    exactly as before, since both share the same underlying class.
    """

    list_display_foreign_key_links: Sequence[str] = ()

    def get_list_display_foreign_key_links(self, request: HttpRequest) -> Sequence[str]:
        return self.list_display_foreign_key_links

    def get_list_display(self, request: HttpRequest) -> list[Any]:
        base = list(super().get_list_display(request))
        result: list[Any] = []

        for item in base:
            if (
                isinstance(item, str)
                and item in self.get_list_display_foreign_key_links(request)
                and item not in self.list_editable
            ):
                result.append(self._build_fk_link_callable(item))
            else:
                result.append(item)

        return result

    def _build_fk_link_callable(self, field_name: str) -> Callable[[Any], str]:
        """Build the list_display callable that links to field_name's related object."""
        try:
            field = self.model._meta.get_field(field_name)
            verbose = field.verbose_name
            order_field: str | None = field_name
        except Exception:
            verbose = field_name.replace("_", " ")
            order_field = None

        def fk_link(obj: Any) -> str | SafeString:
            """Return an <a> tag to obj's related change view, or '-' if unset."""
            related = getattr(obj, field_name, None)
            if not related:
                return "-"

            rel_meta = related._meta
            url = reverse(
                f"{self.admin_site.name}:{rel_meta.app_label}_{rel_meta.model_name}_change",
                args=[related.pk],
            )
            return format_html('<a href="{}">{}</a>', url, related)

        fk_link.__name__ = f"{field_name}_link"
        # short_description/admin_order_field are Django's own convention
        # for annotating a list_display callable; there's no stub for
        # attributes bolted onto a plain function like this.
        fk_link.short_description = verbose  # type: ignore[attr-defined]
        if order_field:
            fk_link.admin_order_field = order_field  # type: ignore[attr-defined]

        return fk_link
