from django import forms


class AdminBootstrapMixin:
    """Mixin to add Bootstrap/AdminLTE classes to ModelAdmin forms and inlines.

    Use by inheriting before `admin.ModelAdmin` or `admin.TabularInline`.
    """

    def _add_bootstrap(self, form):
        for field in getattr(form, "base_fields", {}).values():
            widget = field.widget
            try:
                # File inputs should use form-control-file
                if isinstance(widget, forms.FileInput):
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-control-file").strip()
                # Checkbox inputs get form-check-input
                elif isinstance(widget, forms.CheckboxInput):
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-check-input").strip()
                else:
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-control").strip()
            except (AttributeError, TypeError):
                # best-effort: if widget lacks attrs or is unexpected, don't break admin
                pass

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # apply classes to form fields
        try:
            self._add_bootstrap(form)
        except (AttributeError, TypeError):
            # best-effort application of classes; don't fail admin rendering
            pass
        return form
