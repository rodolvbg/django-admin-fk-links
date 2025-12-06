from django.urls import reverse
from django.utils.html import format_html


class ForeignKeyLinkMixin:

    list_display_foreign_key_links = ()

    def get_list_display_foreign_key_links(self, request):
        return self.list_display_foreign_key_links

    def get_list_display(self, request):
        base = list(super().get_list_display(request))
        result = []

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

    def _build_fk_link_callable(self, field_name):
        try:
            field = self.model._meta.get_field(field_name)
            verbose = field.verbose_name
            order_field = field_name
        except Exception:
            verbose = field_name.replace("_", " ")
            order_field = None

        def fk_link(obj):
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
        fk_link.short_description = verbose
        if order_field:
            fk_link.admin_order_field = order_field

        return fk_link
