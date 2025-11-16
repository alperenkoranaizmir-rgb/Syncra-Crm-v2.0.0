from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from proje.forms import (AgreementForm, DocumentForm, OwnerForm, ProjectForm,
                         UnitForm)
from proje.models import Document, Project, Unit


def user_is_project_member(user, project_id):
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
    # Check membership based on project or unit
    if project_pk:
        if not user_is_project_member(request.user, project_pk):
            from django.http import HttpResponseForbidden

            return HttpResponseForbidden("Bu proje için yetkiniz yok.")
    if unit_pk:
        try:
            unit = Unit.objects.get(pk=unit_pk)
        except Exception:
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


class DocumentListView(generic.ListView):
    model = Document
    template_name = "proje/document_list.html"
