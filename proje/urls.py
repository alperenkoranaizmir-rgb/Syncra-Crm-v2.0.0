from django.urls import path

from proje import views

app_name = "proje"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("add/", views.ProjectCreateView.as_view(), name="project_add"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:project_pk>/owner/add/", views.owner_create, name="owner_add"),
    path("<int:project_pk>/unit/add/", views.unit_create, name="unit_add"),
    path(
        "unit/<int:unit_pk>/agreement/add/",
        views.agreement_create,
        name="agreement_add",
    ),
    path(
        "<int:project_pk>/documents/upload/",
        views.document_upload,
        name="document_upload",
    ),
    path("documents/", views.DocumentListView.as_view(), name="documents"),
    path(
        "reports/download/<path:filename>/",
        views.report_download,
        name="report_download",
    ),
]
