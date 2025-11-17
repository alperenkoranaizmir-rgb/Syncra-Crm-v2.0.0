"""Accounts models: Department, Title, Profile.

Profile extends the existing User model with HR fields required by the
Kullanıcı Yönetimi module.
"""
import logging

from django.conf import settings
from django.db import models
from django.db import DatabaseError
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    """Departmanlar (ör: İnsan Kaynakları, Muhasebe).

    # Kullanım: departmanlar admin arayüzünden eklenip güncellenebilir.
    """
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Departman"
        verbose_name_plural = "Departmanlar"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Ünvan listesi (ör: Proje Yöneticisi, Uzman).

    # Kullanım: ünvanlar admin arayüzünden yönetilecek.
    """
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Ünvan"
        verbose_name_plural = "Ünvanlar"

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Kullanıcı profili - IK bilgileri ile genişletilmiş User.

    Bu model `settings.AUTH_USER_MODEL` ile ilişkili `OneToOneField` içerir
    ve kullanıcıya ait ek bilgileri tutar.
    # Kullanıcı oluşturma görünümü
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    gms = models.CharField("GMS", max_length=100, blank=True)
    phone_fixed = models.CharField("Sabit Telefon", max_length=30, blank=True)
    birth_date = models.DateField("Doğum Tarihi", null=True, blank=True)
    tc_no = models.CharField("TC Kimlik No", max_length=20, blank=True)
    address = models.TextField("Adres", blank=True)
    photo = models.ImageField(
        "Vesikalık Resim",
        upload_to="accounts/photos/",
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profiles",
    )

    title = models.ForeignKey(
        Title,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profiles",
    )

    record_date = models.DateField("Kayıt Tarihi", auto_now_add=True)

    job_start = models.DateField("İş Giriş Tarihi", null=True, blank=True)

    job_end = models.DateField("İş Çıkış Tarihi", null=True, blank=True)

    is_active_employee = models.BooleanField(
        "Kullanım Durumu",
        default=False,
        help_text="Aktif kullanıcı sisteme giriş yapabilir.",
    )

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def save(self, *args, **kwargs):
        # Eğer iş çıkış tarihi varsa otomatik pasif yap
        if self.job_end:
            self.is_active_employee = False
            # Ayrıca User modelinin is_active alanını da pasife çek
            try:
                self.user.is_active = False
                self.user.save(update_fields=[
                    "is_active",
                ])
            except DatabaseError:
                logging.getLogger(__name__).debug(
                    "Could not update related User.is_active for %r",
                    self.user,
                )
        else:
            # yeni eklenen kullanıcılar otomatik pasif kalsın (spec)
            if not self.pk:
                self.is_active_employee = False
        super().save(*args, **kwargs)
