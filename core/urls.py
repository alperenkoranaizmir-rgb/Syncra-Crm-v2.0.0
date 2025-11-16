from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("samples/", views.sample_list, name="sample_list"),
    path("samples/<int:pk>/", views.sample_detail, name="sample_detail"),
    path("forms/general/", views.forms_general, name="forms_general"),
    path("forms/advanced/", views.forms_advanced, name="forms_advanced"),
    path("forms/validation/", views.forms_validation, name="forms_validation"),
    # AdminLTE demo pages (some use TemplateView for static demo templates)
    path("charts/chartjs/", views.charts_chartjs, name="charts_chartjs"),
    path(
        "charts/flot/",
        login_required(TemplateView.as_view(template_name="pages/charts/flot.html")),
        name="charts_flot",
    ),
    path(
        "charts/inline/",
        login_required(TemplateView.as_view(template_name="pages/charts/inline.html")),
        name="charts_inline",
    ),
    path(
        "charts/uplot/",
        login_required(TemplateView.as_view(template_name="pages/charts/uplot.html")),
        name="charts_uplot",
    ),
    path(
        "widgets/",
        login_required(TemplateView.as_view(template_name="pages/widgets.html")),
        name="widgets",
    ),
    path(
        "ui/general/",
        login_required(TemplateView.as_view(template_name="pages/ui/general.html")),
        name="ui_general",
    ),
    path(
        "ui/buttons/",
        login_required(TemplateView.as_view(template_name="pages/ui/buttons.html")),
        name="ui_buttons",
    ),
    path(
        "ui/sliders/",
        login_required(TemplateView.as_view(template_name="pages/ui/sliders.html")),
        name="ui_sliders",
    ),
    path(
        "ui/modals/",
        login_required(TemplateView.as_view(template_name="pages/ui/modals.html")),
        name="ui_modals",
    ),
    path(
        "ui/navbar/",
        login_required(TemplateView.as_view(template_name="pages/ui/navbar.html")),
        name="ui_navbar",
    ),
    path(
        "ui/timeline/",
        login_required(TemplateView.as_view(template_name="pages/ui/timeline.html")),
        name="ui_timeline",
    ),
    path(
        "ui/ribbons/",
        login_required(TemplateView.as_view(template_name="pages/ui/ribbons.html")),
        name="ui_ribbons",
    ),
    path(
        "forms/editors/",
        login_required(TemplateView.as_view(template_name="pages/forms/editors.html")),
        name="forms_editors",
    ),
    path("tables/data/", views.tables_datatables, name="tables_datatables"),
    path(
        "calendar/",
        login_required(TemplateView.as_view(template_name="pages/calendar.html")),
        name="calendar",
    ),
    path(
        "gallery/",
        login_required(TemplateView.as_view(template_name="pages/gallery.html")),
        name="gallery",
    ),
    path(
        "kanban/",
        login_required(TemplateView.as_view(template_name="pages/kanban.html")),
        name="kanban",
    ),
    path(
        "mailbox/",
        login_required(
            TemplateView.as_view(template_name="pages/mailbox/mailbox.html")
        ),
        name="mailbox",
    ),
    path(
        "mailbox/compose/",
        login_required(
            TemplateView.as_view(template_name="pages/mailbox/compose.html")
        ),
        name="mailbox_compose",
    ),
    path(
        "mailbox/read-mail/",
        login_required(
            TemplateView.as_view(template_name="pages/mailbox/read-mail.html")
        ),
        name="mailbox_read",
    ),
    path(
        "examples/invoice/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/invoice.html")
        ),
        name="examples_invoice",
    ),
    path(
        "examples/profile/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/profile.html")
        ),
        name="examples_profile",
    ),
    path("examples/projects/", views.examples_projects, name="examples_projects"),
    path(
        "examples/project-add/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/project-add.html")
        ),
        name="examples_project_add",
    ),
    path(
        "examples/project-edit/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/project-edit.html")
        ),
        name="examples_project_edit",
    ),
    path(
        "examples/project-detail/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/project-detail.html")
        ),
        name="examples_project_detail",
    ),
    path(
        "examples/contacts/",
        login_required(
            TemplateView.as_view(template_name="pages/examples/contacts.html")
        ),
        name="examples_contacts",
    ),
    path(
        "examples/faq/",
        login_required(TemplateView.as_view(template_name="pages/examples/faq.html")),
        name="examples_faq",
    ),
    path(
        "index/",
        login_required(TemplateView.as_view(template_name="pages/index.html")),
        name="index",
    ),
]
