"""Views for the `proje` application.

Contains class-based and function-based views used by the `proje` app,
including project CRUD, owner/unit/agreement creation and helper utilities
like report file downloads.
"""

from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from proje.forms import (AgreementForm, DocumentForm, OwnerForm, ProjectForm,
                         UnitForm)
from proje.models import Document, Project, Unit


def user_is_project_member(user, project_id):
    """Return True if `user` is a manager or staff member of the project.

    Superusers bypass the check.
    """
    if user.is_superuser:
        return True
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return False
    return user == project.manager or user in project.staff.all()


class ProjectListView(generic.ListView):
    model = Project
    template_name = "proje/project_list.html"


class ProjectCreateView(generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "proje/project_form.html"
    success_url = reverse_lazy("proje:project_list")

    # Only superusers can create new projects (per requirement)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Sadece yönetici yeni proje oluşturabilir.")
        return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "proje/project_form.html"
    success_url = reverse_lazy("proje:project_list")


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = "proje/project_detail.html"


@login_required
def owner_create(request, project_pk):
    """Create an `Owner` for the given `Project`.

    Only project members or superusers may create owners.
    """
    project = get_object_or_404(Project, pk=project_pk)
    # Only project members (or superuser) can add owners
    if not user_is_project_member(request.user, project.pk):
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if request.method == "POST":
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.project = project
            owner.save()
            return redirect("proje:project_detail", pk=project.pk)
    else:
        form = OwnerForm()
    return render(request, "proje/owner_form.html", {"form": form, "project": project})


@login_required
def unit_create(request, project_pk):
    """Create a `Unit` within a `Project` (protected to project members)."""
    project = get_object_or_404(Project, pk=project_pk)
    # Only project members (or superuser) can add units
    if not user_is_project_member(request.user, project.pk):
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.project = project
            unit.save()
            return redirect("proje:project_detail", pk=project.pk)
    else:
        form = UnitForm(initial={"project": project})
    return render(request, "proje/unit_form.html", {"form": form, "project": project})


@login_required
def agreement_create(request, unit_pk):
    """Create an `Agreement` related to a `Unit`.

    Access is restricted to project members or superusers.
    """
    unit = get_object_or_404(Unit, pk=unit_pk)
    # Only project members (or superuser) can add agreements
    if not user_is_project_member(request.user, unit.project.pk):
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if request.method == "POST":
        form = AgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("proje:project_detail", pk=unit.project.pk)
    else:
        form = AgreementForm(initial={"unit": unit})
    return render(request, "proje/agreement_form.html", {"form": form, "unit": unit})


@login_required
def document_upload(request, project_pk=None, unit_pk=None):
    """Handle upload of `Document` files for a project or unit.

    Validates membership and stores uploaded files, setting `uploaded_by`.
    """
    # Check membership based on project or unit
    if project_pk:
        if not user_is_project_member(request.user, project_pk):
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if unit_pk:
        try:
            unit = Unit.objects.get(pk=unit_pk)
        except (Unit.DoesNotExist, ValueError, TypeError):
            unit = None
        if unit and not user_is_project_member(request.user, unit.project.pk):
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            return redirect(
                "proje:project_detail",
                pk=doc.project.pk if doc.project else doc.unit.project.pk,
            )
    else:
        form = DocumentForm(initial={"project": project_pk, "unit": unit_pk})
    return render(request, "proje/document_form.html", {"form": form})


@login_required
def report_download(request, filename):
    """Serve a report file from MEDIA_ROOT/reports/ for staff users.

    URL pattern passes a relative `filename` (may include subdirs). We ensure the
    resolved path is under MEDIA_ROOT/reports to prevent traversal.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        from django.http import HttpResponseForbidden

        return HttpResponseForbidden()

    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        raise Http404("Reports not available (MEDIA_ROOT not configured)")

    base = Path(media_root)
    target = base / filename
    try:
        target_resolved = target.resolve()
    except (OSError, RuntimeError) as exc:
        raise Http404("Invalid file") from exc

    try:
        base_resolved = base.resolve()
    except (OSError, RuntimeError) as exc:
        raise Http404("Invalid media root") from exc

    if (
        base_resolved not in target_resolved.parents
        and base_resolved != target_resolved.parent
        and base_resolved != target_resolved
    ):
        # ensure target is inside media_root
        raise Http404("File not found")

    if not target_resolved.exists() or not target_resolved.is_file():
        raise Http404("File not found")

    return FileResponse(
        open(target_resolved, "rb"), as_attachment=True, filename=target_resolved.name
    )


class DocumentListView(generic.ListView):
    model = Document
    template_name = "proje/document_list.html"
