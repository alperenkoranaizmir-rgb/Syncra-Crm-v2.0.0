from django.conf import settings
from django.db import models


class Project(models.Model):
    TYPE_CHOICES = [
        ("kentsel", "Kentsel Dönüşüm"),
        ("altyapi", "Altyapı"),
        ("insaat", "İnşaat"),
    ]

    STATUS_CHOICES = [
        ("planlama", "Planlama Aşamasında"),
        ("uzlasma", "Uzlaşma Aşamasında"),
        ("tamamlandi", "Tamamlandı"),
        ("hukuk", "Hukuki Süreçte"),
        ("yikim", "Yıkım Başladı"),
    ]

    name = models.CharField("Proje Adı", max_length=200)
    code = models.CharField("Proje Kodu", max_length=50, unique=True)
    location = models.CharField("Konum", max_length=255, blank=True)
    area_m2 = models.DecimalField(
        "Proje M2", max_digits=12, decimal_places=2, null=True, blank=True
    )
    type = models.CharField(
        "Proje Tipi", max_length=50, choices=TYPE_CHOICES, default="kentsel"
    )
    est_delivery_date = models.DateField("Tahmini Teslim Tarihi", null=True, blank=True)
    est_budget = models.DecimalField(
        "Tahmini Bütçe", max_digits=14, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        "Proje Durumu", max_length=32, choices=STATUS_CHOICES, default="planlama"
    )
    start_date = models.DateField("Başlangıç Tarihi", null=True, blank=True)
    est_end_date = models.DateField("Tahmini Bitiş Tarihi", null=True, blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
    )
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="projects"
    )
    unit_count = models.PositiveIntegerField("Mevcut Bağımsız Bölüm Sayısı", default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Owner(models.Model):
    EMPLOYMENT = [
        ("calismiyor", "Çalışmıyor"),
        ("okuyor", "Okuyor"),
        ("evhanimi", "Ev Hanımı"),
        ("calisiyor", "Çalışıyor"),
        ("diger", "Diğer"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="owners"
    )
    first_name = models.CharField("Ad", max_length=100)
    last_name = models.CharField("Soyad", max_length=100)
    birth_date = models.DateField("Doğum Tarihi", null=True, blank=True)
    tc_no = models.CharField("TC", max_length=20, blank=True)
    phone = models.CharField("Telefon", max_length=30, blank=True)
    email = models.EmailField("E-Posta", blank=True)
    landline = models.CharField("Sabit Tel", max_length=30, blank=True)
    relative_phone = models.CharField("Yakını Tel", max_length=30, blank=True)
    address = models.TextField("Adres", blank=True)
    disabled = models.BooleanField("Engel Durumu", default=False)
    literate = models.BooleanField("Okur Yazar", default=True)
    education = models.CharField("Mezun Okul", max_length=200, blank=True)
    employment = models.CharField(
        "Çalışma Durumu", max_length=30, choices=EMPLOYMENT, default="calisiyor"
    )
    residence_city = models.CharField("İkamet İli", max_length=100, blank=True)
    photo = models.ImageField(
        "Vesikalık Resim", upload_to="owners/photos/", null=True, blank=True
    )
    id_scan = models.FileField(
        "Kimlik Fotokopisi", upload_to="owners/id/", null=True, blank=True
    )

    class Meta:
        verbose_name = "Malik"
        verbose_name_plural = "Malikler"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Unit(models.Model):
    TYPE = [
        ("daire", "Daire"),
        ("bina", "Bina"),
        ("dukkan", "Dükkan"),
        ("arsa", "Arsa"),
        ("tarla", "Tarla"),
        ("atil", "Atıl Durumda"),
        ("diger", "Diğer"),
    ]

    OCCUPANCY = [
        ("sahip_oturuyor", "Mülk sahibi oturuyor"),
        ("kiraci", "Kiracı Mevcut"),
        ("bos", "Boş"),
        ("kullanilmiyor", "Kullanılmıyor"),
    ]

    AGREEMENT = [
        ("beklemede", "Uzlaşma Beklemede"),
        ("saglandi", "Uzlaşma Sağlandı"),
        ("istemiyor", "Uzlaşma İstemiyor"),
        ("ulasilamadi", "Ulaşılamıyor"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="units")
    ada = models.CharField(max_length=50, blank=True)
    parsel = models.CharField(max_length=50, blank=True)
    m2 = models.DecimalField(
        "Metrekare", max_digits=10, decimal_places=2, null=True, blank=True
    )
    address = models.TextField(blank=True)
    door_outside = models.CharField("Dış Kapı No", max_length=20, blank=True)
    door_inside = models.CharField("İç Kapı No", max_length=20, blank=True)
    type = models.CharField("Tip", max_length=20, choices=TYPE, default="daire")
    current_m2 = models.DecimalField(
        "Mevcut M2", max_digits=10, decimal_places=2, null=True, blank=True
    )
    share_m2 = models.DecimalField(
        "Arsa Payı M2", max_digits=10, decimal_places=2, null=True, blank=True
    )
    occupancy = models.CharField(
        "Oturum Durumu", max_length=30, choices=OCCUPANCY, default="bos"
    )
    agreement_status = models.CharField(
        "Uzlaşma Durumu", max_length=30, choices=AGREEMENT, default="beklemede"
    )
    owners = models.ManyToManyField(
        Owner, through="Ownership", blank=True, related_name="units"
    )

    class Meta:
        verbose_name = "Bağımsız Bölüm"
        verbose_name_plural = "Bağımsız Bölümler"

    def __str__(self):
        return f"{self.project.code} - {self.ada}/{self.parsel}"


class Ownership(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    share_percent = models.DecimalField(max_digits=6, decimal_places=2, default=100)
    status = models.CharField(
        max_length=30, blank=True, help_text="Satılmış / vefaat / devir gibi durumlar"
    )

    class Meta:
        verbose_name = "Mülk Sahibi Hissesi"
        verbose_name_plural = "Mülk Sahibi Hisseleri"


class Agreement(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="agreements")
    date = models.DateField(null=True, blank=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    note = models.TextField(blank=True)
    status = models.CharField(
        max_length=30, choices=Unit.AGREEMENT, default="beklemede"
    )
    owners = models.ManyToManyField(Owner, blank=True, related_name="agreements")

    class Meta:
        verbose_name = "Uzlaşma"
        verbose_name_plural = "Uzlaşmalar"


class Document(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="documents", null=True, blank=True
    )
    file = models.FileField(upload_to="proje_documents/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proje Dosyası"
        verbose_name_plural = "Proje Dosyaları"

    def __str__(self):
        return self.file.name.split("/")[-1]
