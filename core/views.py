from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    return redirect("core:dashboard")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def sample_list(request):
    # placeholder list view for a sample app
    items = [
        {"id": 1, "name": "Örnek Kayıt 1"},
        {"id": 2, "name": "Örnek Kayıt 2"},
    ]
    return render(request, "sample_list.html", {"items": items})


@login_required
def sample_detail(request, pk):
    items = {
        1: {"id": 1, "name": "Örnek Kayıt 1", "desc": "Detay 1"},
        2: {"id": 2, "name": "Örnek Kayıt 2", "desc": "Detay 2"},
    }
    item = get_object_or_404(items, pk=int(pk))
    return render(request, "sample_detail.html", {"item": item})


@login_required
def forms_general(request):
    return render(request, "forms/general.html")


@login_required
def forms_advanced(request):
    return render(request, "forms/advanced.html")


@login_required
def forms_validation(request):
    return render(request, "forms/validation.html")


@login_required
def charts_chartjs(request):
    return render(request, "pages/charts/chartjs.html")


@login_required
def tables_datatables(request):
    return render(request, "pages/tables/data.html")


@login_required
def examples_projects(request):
    # sample projects data for demo page
    projects = [
        {
            "id": 1,
            "title": "Sürüm 1.0 Hazırlığı",
            "description": "Önemli özelliklerin tamamlanması ve testlerin yapılması.",
            "status": "completed",
            "progress": 100,
            "members": ["Ahmet", "Ayşe"],
            "due": "2025-11-01",
        },
        {
            "id": 2,
            "title": "Mobil Uyum Rekonfigürasyonu",
            "description": "Mobil görünüm iyileştirmeleri ve responsive düzeltmeler.",
            "status": "in-progress",
            "progress": 60,
            "members": ["Mehmet"],
            "due": "2025-12-15",
        },
        {
            "id": 3,
            "title": "Raporlama Modülü",
            "description": "Yeni raporlama ekranları ve PDF export.",
            "status": "on-hold",
            "progress": 25,
            "members": ["Fatma", "Can"],
            "due": "2026-01-30",
        },
    ]
    return render(request, "pages/examples/projects.html", {"projects": projects})


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


def handler403(request, exception=None):
    return render(request, "403.html", status=403)


def handler400(request, exception=None):
    return render(request, "400.html", status=400)
