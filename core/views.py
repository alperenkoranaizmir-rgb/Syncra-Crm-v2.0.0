from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def sample_list(request):
    # placeholder list view for a sample app
    items = [
        {'id': 1, 'name': 'Örnek Kayıt 1'},
        {'id': 2, 'name': 'Örnek Kayıt 2'},
    ]
    return render(request, 'sample_list.html', {'items': items})


@login_required
def sample_detail(request, pk):
    items = {
        1: {'id': 1, 'name': 'Örnek Kayıt 1', 'desc': 'Detay 1'},
        2: {'id': 2, 'name': 'Örnek Kayıt 2', 'desc': 'Detay 2'},
    }
    item = get_object_or_404(items, pk=int(pk))
    return render(request, 'sample_detail.html', {'item': item})


def handler404(request, exception=None):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def handler403(request, exception=None):
    return render(request, '403.html', status=403)


def handler400(request, exception=None):
    return render(request, '400.html', status=400)
