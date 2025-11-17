"""Views for accounts app: protected admin-like views for user management."""
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Profile
from .forms import ProfileForm, UserAdminForm

User = get_user_model()


def is_admin(user):
    """Return True if user has admin (staff or superuser) privileges."""
    return user.is_active and user.is_staff


@user_passes_test(is_admin)
def users_list(request):
    """Kullanıcı listesi (admin yetkisi gerektirir)."""
    users = User.objects.select_related("profile").all()
    return render(request, "accounts/users_list.html", {"users": users})


@user_passes_test(is_admin)
def user_edit(request, user_id):
    """Kullanıcı oluşturma / düzenleme görünümü."""
    user = get_object_or_404(User, pk=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)
    if request.method == "POST":
        uform = UserAdminForm(request.POST, instance=user)
        pform = ProfileForm(
            request.POST, request.FILES, instance=profile
        )
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Kullanıcı kaydedildi")
            return redirect(reverse("accounts:users_list"))
    else:
        uform = UserAdminForm(instance=user)
        pform = ProfileForm(instance=profile)
    context = {
        "uform": uform,
        "pform": pform,
        "user_obj": user,
    }
    return render(request, "accounts/user_edit.html", context)


@user_passes_test(is_admin)
def user_add(request):
    """Yeni kullanıcı ekleme (mevcut User tablosuna ekleme/senkronizasyon).

    Not: Django auth user oluşturma işlemi ayrı olabilir; burada var olan kullanıcılardan
    seçme veya yeni oluşturma imkanı sunulabilir.
    """
    if request.method == "POST":
        # basit: yeni User oluştur
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if not username or not email:
            messages.error(request, "Kullanıcı adı ve e-posta gereklidir")
        else:
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            )
            Profile.objects.create(user=user)
            messages.success(request, "Yeni kullanıcı oluşturuldu (pasif)")
            return redirect(reverse("accounts:users_list"))
    return render(request, "accounts/user_add.html")
