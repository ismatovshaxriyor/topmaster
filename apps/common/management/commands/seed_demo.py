"""Idempotent development seed for TopMaster — populates EVERY domain model.

Mirrors / extends the frontend mock data in
``TopMaster Design System/ui_kits/web/data.js`` and gives every model at least
a few realistic Uzbek-Latin rows so the admin and API are never empty:

* accounts:      3 clients + 6 masters (+ auto UserSettings) + FCM Devices
* catalog:       relies on seed_catalog (cities + categories)
* masters:       MasterProfile, Skill, PortfolioItem (with images),
                 VerificationRequest + VerificationDocument (varied states)
* jobs:          Job (open / in_progress / completed / cancelled),
                 JobImage, JobEvent timelines
* proposals:     Proposal (pending + accepted)
* reviews:       Review on completed jobs (rating signal recomputes masters)
* chat:          Conversation + ConversationParticipant + Message (2 threads)
* notifications: Notification for a client and a master (all types)
* favorites:     SavedMaster

Run order matters — run ``seed_catalog`` (and ``seed_support``) first::

    python manage.py seed_catalog
    python manage.py seed_support
    python manage.py seed_demo

Re-running is safe: every object is created via get_or_create / guards.
All seeded users share the password ``topmaster123``.
"""
from datetime import date
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Device
from apps.catalog.models import Category, City
from apps.chat.models import Conversation, ConversationParticipant, Message
from apps.favorites.models import SavedMaster
from apps.jobs.models import Job, JobEvent, JobImage, JobStatus, PriceType, WhenChoice
from apps.masters.models import (
    AvailabilityStatus,
    MasterProfile,
    PortfolioItem,
    Skill,
    VerificationDocument,
    VerificationRequest,
)
from apps.notifications.models import Notification
from apps.proposals.models import Proposal
from apps.reports.models import Report
from apps.reviews.models import Review
from apps.support.models import SupportMessage, SupportThread

try:  # Pillow ships in requirements; degrade gracefully if ever missing.
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

User = get_user_model()

DEMO_PASSWORD = "topmaster123"

# ── Clients (mijozlar) ─────────────────────────────────────────────
CLIENTS = [
    {"email": "bekzod@topmaster.uz", "name": "Bekzod Murodov",
     "phone": "+998 90 123 45 67", "city": "Toshkent", "verified": True},
    {"email": "malika@topmaster.uz", "name": "Malika Rashidova",
     "phone": "+998 90 111 22 33", "city": "Toshkent", "verified": True},
    {"email": "oybek@topmaster.uz", "name": "Oybek Tursunov",
     "phone": "+998 93 555 66 77", "city": "Samarqand", "verified": False},
]
CLIENT_EMAIL = CLIENTS[0]["email"]

# ── Masters (mirrors window.TM_DATA.masters, skills/portfolio for all) ──
V = VerificationDocument.State
MASTERS = [
    {
        "email": "akmal@topmaster.uz", "name": "Akmal Yusupov", "category": "elektrik",
        "city": "Toshkent", "exp": 8, "rating": "4.90", "reviews": 128, "min": 150000,
        "status": AvailabilityStatus.FREE, "verified": True, "top": True, "views": 1248,
        "phone": "+998 90 200 10 10",
        "bio": "8 yillik tajribaga ega malakali elektrik. Uy va ofis simlash, "
               "rozetka va avtomatlar oʻrnatish.",
        "verify": ("approved", {"id": V.VERIFIED, "selfie": V.VERIFIED, "diploma": V.VERIFIED}),
        "skills": [
            {"title": "Toʻliq simlash", "price_min": 800000, "price_max": 2500000, "years": 8},
            {"title": "Rozetka / vyklyuchatel", "price_min": 50000, "price_max": 150000, "years": 8},
            {"title": "Avtomat va shchit", "price_min": 200000, "price_max": 600000, "years": 6},
            {"title": "Lyustra oʻrnatish", "price_min": 100000, "price_max": 300000, "years": 8},
        ],
        "portfolio": [
            {"title": "Ofis uchun toʻliq simlash", "location": "Toshkent",
             "completed_at": date(2026, 3, 1), "featured": True, "hue": (38, 92, 160)},
            {"title": "Restoran yoritish tizimi", "location": "Toshkent",
             "completed_at": date(2026, 1, 1), "hue": (222, 115, 32)},
        ],
    },
    {
        "email": "dilnoza@topmaster.uz", "name": "Dilnoza Karimova", "category": "repetitor",
        "city": "Toshkent", "exp": 5, "rating": "4.80", "reviews": 64, "min": 80000,
        "status": AvailabilityStatus.BUSY, "verified": True, "top": False, "views": 642,
        "phone": "+998 90 301 20 20",
        "bio": "Ingliz tili va matematika oʻqituvchisi. IELTS tayyorlov. 5 yil tajriba.",
        "verify": ("approved", {"id": V.VERIFIED, "selfie": V.VERIFIED, "diploma": V.VERIFIED}),
        "skills": [
            {"title": "Ingliz tili (IELTS)", "price_min": 200000, "price_max": 400000, "years": 5},
            {"title": "Matematika", "price_min": 80000, "price_max": 150000, "years": 5},
            {"title": "Fizika", "price_min": 100000, "price_max": 180000, "years": 4},
        ],
        "portfolio": [
            {"title": "IELTS 7.5 — oʻquvchi natijasi", "location": "Toshkent",
             "completed_at": date(2026, 2, 1), "featured": True, "hue": (31, 138, 91)},
        ],
    },
    {
        "email": "sardor@topmaster.uz", "name": "Sardor Aliyev", "category": "santexnik",
        "city": "Samarqand", "exp": 12, "rating": "5.00", "reviews": 210, "min": 120000,
        "status": AvailabilityStatus.FREE, "verified": True, "top": True, "views": 2103,
        "phone": "+998 91 400 30 30",
        "bio": "Suv va kanalizatsiya tizimlari boʻyicha mutaxassis. Tezkor va kafolatli xizmat.",
        "verify": ("approved", {"id": V.VERIFIED, "selfie": V.VERIFIED}),
        "skills": [
            {"title": "Quvur almashtirish", "price_min": 150000, "price_max": 500000, "years": 12},
            {"title": "Smesitel oʻrnatish", "price_min": 80000, "price_max": 200000, "years": 12},
            {"title": "Kanalizatsiya tozalash", "price_min": 120000, "price_max": 300000, "years": 10},
        ],
        "portfolio": [
            {"title": "Kottej suv tizimi", "location": "Samarqand",
             "completed_at": date(2026, 2, 15), "featured": True, "hue": (46, 100, 136)},
            {"title": "Hammom toʻliq remont", "location": "Samarqand",
             "completed_at": date(2025, 11, 10), "hue": (20, 120, 130)},
        ],
    },
    {
        "email": "gulnora@topmaster.uz", "name": "Gulnora Hasanova", "category": "tozalash",
        "city": "Toshkent", "exp": 3, "rating": "4.70", "reviews": 38, "min": 200000,
        "status": AvailabilityStatus.FREE, "verified": False, "top": False, "views": 421,
        "phone": "+998 90 505 40 40",
        "bio": "Kvartira va ofislarni chuqur tozalash. Koʻchganda generalniy uborka.",
        "verify": ("pending", {"id": V.UPLOADED, "selfie": V.PENDING}),
        "skills": [
            {"title": "Kvartira tozalash", "price_min": 200000, "price_max": 500000, "years": 3},
            {"title": "Generalniy uborka", "price_min": 350000, "price_max": 800000, "years": 3},
            {"title": "Deraza tozalash", "price_min": 50000, "price_max": 120000, "years": 2},
        ],
        "portfolio": [
            {"title": "3 xonali kvartira generalniy", "location": "Toshkent",
             "completed_at": date(2026, 1, 20), "hue": (120, 90, 60)},
        ],
    },
    {
        "email": "jasur@topmaster.uz", "name": "Jasur Toʻraev", "category": "duradgor",
        "city": "Andijon", "exp": 15, "rating": "4.90", "reviews": 156, "min": 300000,
        "status": AvailabilityStatus.BUSY, "verified": True, "top": True, "views": 1789,
        "phone": "+998 93 606 50 50",
        "bio": "Mebel yasash va taʼmirlash. Buyurtma asosida shkaf, eshik, oshxona.",
        "verify": ("approved", {"id": V.VERIFIED, "selfie": V.VERIFIED, "diploma": V.VERIFIED}),
        "skills": [
            {"title": "Mebel yigʻish", "price_min": 300000, "price_max": 900000, "years": 15},
            {"title": "Shkaf-kupe yasash", "price_min": 1200000, "price_max": 4000000, "years": 15},
            {"title": "Eshik oʻrnatish", "price_min": 250000, "price_max": 600000, "years": 12},
        ],
        "portfolio": [
            {"title": "Oshxona mebeli (loyiha asosida)", "location": "Andijon",
             "completed_at": date(2026, 3, 5), "featured": True, "hue": (150, 90, 40)},
            {"title": "Yotoqxona shkaf-kupe", "location": "Andijon",
             "completed_at": date(2025, 12, 18), "hue": (90, 70, 45)},
        ],
    },
    {
        "email": "nodira@topmaster.uz", "name": "Nodira Yoʻldosheva", "category": "bo-yoqchi",
        "city": "Buxoro", "exp": 6, "rating": "4.60", "reviews": 51, "min": 180000,
        "status": AvailabilityStatus.FREE, "verified": True, "top": False, "views": 588,
        "phone": "+998 91 707 60 60",
        "bio": "Devor boʻyash, oboi yopishtirish, dekorativ shtukaturka.",
        "verify": ("approved", {"id": V.VERIFIED, "selfie": V.VERIFIED}),
        "skills": [
            {"title": "Devor boʻyash", "price_min": 180000, "price_max": 500000, "years": 6},
            {"title": "Oboi yopishtirish", "price_min": 120000, "price_max": 350000, "years": 6},
            {"title": "Dekorativ shtukaturka", "price_min": 300000, "price_max": 700000, "years": 4},
        ],
        "portfolio": [
            {"title": "Mehmonxona devor dekori", "location": "Buxoro",
             "completed_at": date(2026, 2, 8), "featured": True, "hue": (210, 80, 120)},
        ],
    },
]

# FCM device tokens (one per platform).
DEVICES = [
    {"email": "bekzod@topmaster.uz", "registration_id": "demo-fcm-bekzod-android",
     "platform": Device.Platform.ANDROID},
    {"email": "akmal@topmaster.uz", "registration_id": "demo-fcm-akmal-ios",
     "platform": Device.Platform.IOS},
    {"email": "sardor@topmaster.uz", "registration_id": "demo-fcm-sardor-web",
     "platform": Device.Platform.WEB},
]

# ── Jobs (open + in_progress + completed + cancelled) ──────────────
JOBS = [
    {"slug": "job-101", "client": "bekzod@topmaster.uz", "title": "Uch xonali kvartirani toʻliq simlash kerak",
     "category": "elektrik", "city": "Toshkent", "address": "Yunusobod, 4-kvartal",
     "price_type": PriceType.FIXED, "price_amount": 1800000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.OPEN, "image": (38, 92, 160),
     "description": "Yangi qurilgan 3 xonali kvartirada toʻliq elektr simlash ishlari. "
                    "Materiallar bizdan. Tajribali usta kerak."},
    {"slug": "job-102", "client": "bekzod@topmaster.uz", "title": "Hammomda suv quvurini almashtirish",
     "category": "santexnik", "city": "Toshkent", "address": "Chilonzor, 19-kvartal",
     "price_type": PriceType.NEGOTIABLE, "price_amount": None, "when_choice": WhenChoice.ASAP,
     "urgent": True, "status": JobStatus.OPEN,
     "description": "Eski quvurlar oqayapti. Toʻliq almashtirish va yangi smesitel oʻrnatish kerak."},
    {"slug": "job-103", "client": "malika@topmaster.uz", "title": "Bolaga matematikadan repetitor",
     "category": "repetitor", "city": "Toshkent", "address": "Mirzo Ulugʻbek tumani",
     "price_type": PriceType.FIXED, "price_amount": 600000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.OPEN,
     "description": "7-sinf oʻquvchisi uchun haftada 3 marta matematika. Uyga kelib dars berish."},
    {"slug": "job-104", "client": "oybek@topmaster.uz", "title": "Oshxona mebelini yigʻish",
     "category": "duradgor", "city": "Samarqand", "address": "Registon koʻchasi",
     "price_type": PriceType.FIXED, "price_amount": 900000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.IN_PROGRESS, "assigned": "jasur@topmaster.uz",
     "description": "IKEA uslubidagi oshxona mebelini yetkazib berilgan, yigʻish va oʻrnatish kerak."},
    {"slug": "job-105", "client": "malika@topmaster.uz", "title": "Oshxona rozetkalarini almashtirish",
     "category": "elektrik", "city": "Toshkent", "address": "Yakkasaroy, 2-tor koʻcha",
     "price_type": PriceType.FIXED, "price_amount": 350000, "when_choice": WhenChoice.TODAY,
     "status": JobStatus.COMPLETED, "assigned": "akmal@topmaster.uz",
     "description": "Oshxonadagi 4 ta rozetkani yangisiga almashtirish kerak."},
    {"slug": "job-106", "client": "oybek@topmaster.uz", "title": "Yotoqxona uchun shkaf-kupe",
     "category": "duradgor", "city": "Samarqand", "address": "Registon koʻchasi 12",
     "price_type": PriceType.FIXED, "price_amount": 2800000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.COMPLETED, "assigned": "jasur@topmaster.uz",
     "description": "3 metrli shkaf-kupe yasash va oʻrnatish."},
    {"slug": "job-107", "client": "bekzod@topmaster.uz", "title": "Koʻchishdan oldin generalniy tozalash",
     "category": "tozalash", "city": "Toshkent", "address": "Sergeli, 7-kvartal",
     "price_type": PriceType.FIXED, "price_amount": 500000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.CANCELLED,
     "description": "Koʻchishdan oldin kvartirani chuqur tozalash kerak edi."},
    {"slug": "job-hammom", "client": "bekzod@topmaster.uz", "title": "Hammom remonti (yakunlangan)",
     "category": "santexnik", "city": "Toshkent", "address": "Chilonzor, 19-kvartal",
     "price_type": PriceType.FIXED, "price_amount": 1200000, "when_choice": WhenChoice.THIS_WEEK,
     "status": JobStatus.COMPLETED, "assigned": "sardor@topmaster.uz",
     "description": "Hammomdagi suv quvurlari almashtirildi va yangi smesitel oʻrnatildi."},
]

# Proposals: (job slug, master email, message, price, status).
PROPOSALS = [
    ("job-101", "akmal@topmaster.uz", "Tajribali elektrikman, 10 kun ichida bajaraman.", 1750000, "pending"),
    ("job-102", "sardor@topmaster.uz", "Bugun kelib koʻraman, kafolat bilan ishlayman.", None, "pending"),
    ("job-103", "dilnoza@topmaster.uz", "Matematikadan 5 yillik tajriba. Haftada 3 kun mos.", 600000, "pending"),
    ("job-104", "jasur@topmaster.uz", "Mebel yigʻishda 15 yillik tajriba. Bir kunda tugataman.", 850000, "accepted"),
    ("job-105", "akmal@topmaster.uz", "Rozetkalarni bugunoq almashtirib beraman.", 320000, "accepted"),
    ("job-106", "jasur@topmaster.uz", "Shkaf-kupeni oʻlchov olib, 5 kunda tayyorlayman.", 2700000, "accepted"),
    ("job-hammom", "sardor@topmaster.uz", "Quvurlarni toʻliq almashtiraman, kafolat 1 yil.", 1200000, "accepted"),
]

# Reviews on completed jobs: (job slug, author email, master email, rating, text, recommend).
REVIEWS = [
    ("job-hammom", "bekzod@topmaster.uz", "sardor@topmaster.uz", 5,
     "Juda ishbilarmon usta. Vaqtida keldi, hamma narsani toza qildi. Tavsiya qilaman!", True),
    ("job-105", "malika@topmaster.uz", "akmal@topmaster.uz", 5,
     "Rozetkalarni almashtirib berdi, narxi ham hamyonbop. Rahmat!", True),
    ("job-106", "oybek@topmaster.uz", "jasur@topmaster.uz", 4,
     "Yaxshi bajardi, lekin biroz kechikdi. Umuman olganda mamnunman.", True),
]

# Notifications for the client (mirrors window.TM_DATA.notifications).
CLIENT_NOTIFS = [
    ("order", "Yangi taklif keldi", "Uch xonali kvartirani simlash — Akmal Yusupov", False),
    ("accepted", "Taklifingiz qabul qilindi", "Hammomda suv quvurini almashtirish", False),
    ("chat", "Sardor Aliyev yozdi", "Ertaga soat 10:00 da kelaman", False),
    ("system", "Profilingiz tasdiqlandi", "TopMaster jamoasi tomonidan tekshirildi", True),
    ("rejected", "Taklif rad etildi", "Koʻchishdan oldin tozalash — bekor qilindi", True),
]
# Notifications for a master (Akmal).
MASTER_NOTIFS = [
    ("order", "Sizga mos yangi buyurtma", "Uch xonali kvartirani simlash — Yunusobod", False),
    ("accepted", "Taklifingiz qabul qilindi", "Oshxona rozetkalarini almashtirish", True),
    ("system", "Profilingiz tasdiqlandi ✓", "Hujjatlaringiz tekshiruvdan oʻtdi", True),
]

# Two chat threads: (client email, master email, job slug, [(who, text), ...]).
CONVERSATIONS = [
    ("bekzod@topmaster.uz", "sardor@topmaster.uz", "job-102", [
        ("master", "Assalomu alaykum! Buyurtmangizni koʻrdim."),
        ("client", "Vaalaykum assalom! Ha, hammomdagi quvurni almashtirish kerak."),
        ("master", "Tushunarli. Qachon kelishim mumkin? Bugun yoki ertaga boʻsh man."),
        ("system", "Taklif qabul qilindi. Ish boshlandi."),
        ("client", "Ertaga ertalab qulay. Soat 10 boʻladimi?"),
        ("master", "Ertaga soat 10:00 da kelaman"),
    ], 2),
    ("bekzod@topmaster.uz", "akmal@topmaster.uz", "job-101", [
        ("client", "Salom! Kvartirani simlash boʻyicha taklif yubordingizmi?"),
        ("master", "Ha, yubordim. Materiallarni oʻzingiz olasizmi yoki men olaymi?"),
        ("client", "Oʻzimiz olamiz. Qachon boshlasak boʻladi?"),
    ], 1),
]

SAVED = [
    ("bekzod@topmaster.uz", ["akmal@topmaster.uz", "sardor@topmaster.uz", "jasur@topmaster.uz"]),
    ("malika@topmaster.uz", ["akmal@topmaster.uz"]),
]


def _png(rgb):
    """A small placeholder PNG ContentFile, or None if Pillow is unavailable."""
    if Image is None:
        return None
    buf = BytesIO()
    Image.new("RGB", (480, 320), tuple(rgb)).save(buf, format="PNG")
    return ContentFile(buf.getvalue(), name="seed.png")


class Command(BaseCommand):
    help = "Seed realistic demo data across every model (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        self.cities = {c.name: c for c in City.objects.all()}
        self.categories = {c.key: c for c in Category.objects.all()}
        if not self.cities or not self.categories:
            self.stderr.write(self.style.ERROR(
                "Catalog boʻsh. Avval `seed_catalog` va `seed_support` ishga tushiring."
            ))
            return

        self.clients = self._seed_clients()
        self.masters = self._seed_masters()
        self._seed_devices()
        self.jobs = self._seed_jobs()
        self._seed_proposals()
        self._seed_reviews()
        self._seed_conversations()
        self._seed_notifications()
        self._seed_saved()
        self._seed_support_chat()
        self._seed_reports()

        self._report()

    # ── clients ───────────────────────────────────────────────────
    def _seed_clients(self):
        out = {}
        for data in CLIENTS:
            user = User.objects.filter(email=data["email"]).first()
            if user is None:
                user = User.objects.create_user(
                    email=data["email"], password=DEMO_PASSWORD,
                    full_name=data["name"], role="mijoz",
                )
            user.full_name = data["name"]
            user.phone = data["phone"]
            user.role = "mijoz"
            user.is_verified = data["verified"]
            user.city = self.cities.get(data["city"])
            user.save(update_fields=["full_name", "phone", "role", "is_verified", "city"])
            out[data["email"]] = user
        return out

    # ── masters ───────────────────────────────────────────────────
    def _seed_masters(self):
        out = {}
        for data in MASTERS:
            user = User.objects.filter(email=data["email"]).first()
            if user is None:
                user = User.objects.create_user(
                    email=data["email"], password=DEMO_PASSWORD,
                    full_name=data["name"], role="usta",
                )
            user.full_name = data["name"]
            user.phone = data["phone"]
            user.role = "usta"
            user.is_verified = data["verified"]
            user.city = self.cities.get(data["city"])
            user.save(update_fields=["full_name", "phone", "role", "is_verified", "city"])

            profile, _ = MasterProfile.objects.get_or_create(user=user)
            profile.bio = data["bio"]
            profile.experience_years = data["exp"]
            profile.min_price = data["min"]
            profile.status = data["status"]
            profile.is_top = data["top"]
            profile.is_verified = data["verified"]
            profile.rating_avg = data["rating"]
            profile.reviews_count = data["reviews"]
            profile.views_count = data["views"]
            profile.save()

            category = self.categories.get(data["category"])
            if category is not None:
                profile.categories.add(category)

            self._seed_skills(profile, data["skills"], category)
            self._seed_portfolio(profile, data["portfolio"], category)
            self._seed_verification(profile, *data["verify"])
            out[data["email"]] = profile
        return out

    def _seed_skills(self, profile, skills, category):
        for order, skill in enumerate(skills):
            Skill.objects.get_or_create(
                master=profile, title=skill["title"],
                defaults={"category": category, "price_min": skill["price_min"],
                          "price_max": skill["price_max"], "years": skill["years"], "order": order},
            )

    def _seed_portfolio(self, profile, items, category):
        for order, item in enumerate(items):
            obj, created = PortfolioItem.objects.get_or_create(
                master=profile, title=item["title"],
                defaults={"location": item["location"], "completed_at": item["completed_at"],
                          "category": category, "featured": item.get("featured", False), "order": order},
            )
            if not obj.image:
                img = _png(item.get("hue", (46, 100, 136)))
                if img is not None:
                    obj.image.save(f"portfolio_{obj.pk}.png", img, save=True)

    def _seed_verification(self, profile, status, doc_states):
        req, _ = VerificationRequest.objects.get_or_create(master=profile)
        req.status = status
        if status in ("pending", "approved") and req.submitted_at is None:
            req.submitted_at = timezone.now()
        if status == "approved":
            req.reviewed_at = req.reviewed_at or timezone.now()
        req.save()

        required = {"id", "selfie"}
        for doc_type in VerificationDocument.DocType.values:
            state = doc_states.get(doc_type, VerificationDocument.State.NONE)
            VerificationDocument.objects.get_or_create(
                request=req, doc_type=doc_type,
                defaults={"required": doc_type in required, "state": state},
            )

    # ── devices ───────────────────────────────────────────────────
    def _seed_devices(self):
        users = {**self.clients, **{e: p.user for e, p in self.masters.items()}}
        for data in DEVICES:
            user = users.get(data["email"])
            if user is not None:
                Device.objects.get_or_create(
                    registration_id=data["registration_id"],
                    defaults={"user": user, "platform": data["platform"]},
                )

    # ── jobs ──────────────────────────────────────────────────────
    def _seed_jobs(self):
        out = {}
        for data in JOBS:
            client = self.clients[data["client"]]
            assigned = self.masters.get(data.get("assigned"))
            job, created = Job.objects.get_or_create(
                client=client, title=data["title"],
                defaults={
                    "category": self.categories.get(data["category"]),
                    "city": self.cities.get(data["city"]),
                    "address": data["address"], "description": data["description"],
                    "price_type": data["price_type"], "price_amount": data["price_amount"],
                    "when_choice": data["when_choice"], "urgent": data.get("urgent", False),
                    "status": data["status"], "assigned_master": assigned,
                },
            )
            if created:
                self._seed_job_timeline(job, client, assigned, data["status"])
            # Image attaches idempotently even if the job pre-existed.
            if data.get("image") and not job.images.exists():
                img = _png(data["image"])
                if img is not None:
                    JobImage.objects.create(job=job, image=img, order=0)
            out[data["slug"]] = job
        return out

    def _seed_job_timeline(self, job, client, assigned, status):
        ET = JobEvent.EventType
        steps = [ET.CREATED]
        if status in (JobStatus.IN_PROGRESS, JobStatus.COMPLETED):
            steps += [ET.ACCEPTED, ET.STARTED, ET.IN_PROGRESS]
        if status == JobStatus.COMPLETED:
            steps += [ET.AWAITING, ET.COMPLETED]
        if status == JobStatus.CANCELLED:
            steps += [ET.CANCELLED]
        for step in steps:
            actor = assigned.user if (step in (ET.STARTED, ET.IN_PROGRESS, ET.AWAITING) and assigned) else client
            JobEvent.objects.create(job=job, type=step, actor=actor)

    # ── proposals ─────────────────────────────────────────────────
    def _seed_proposals(self):
        status_map = {s.value: s for s in Proposal.Status}
        for slug, email, message, price, status in PROPOSALS:
            job = self.jobs.get(slug)
            master = self.masters.get(email)
            if job is None or master is None:
                continue
            st = status_map[status]
            _, created = Proposal.objects.get_or_create(
                job=job, master=master,
                defaults={"message": message, "proposed_price": price, "status": st,
                          "responded_at": None if st == Proposal.Status.PENDING else timezone.now()},
            )
            if created:
                Job.objects.filter(pk=job.pk).update(proposals_count=job.proposals_count + 1)

    # ── reviews ───────────────────────────────────────────────────
    def _seed_reviews(self):
        for slug, author_email, master_email, rating, text, recommend in REVIEWS:
            job = self.jobs.get(slug)
            author = self.clients.get(author_email)
            master = self.masters.get(master_email)
            if job and author and master:
                Review.objects.get_or_create(
                    job=job,
                    defaults={"author": author, "master": master, "rating": rating,
                              "text": text, "recommend": recommend},
                )

    # ── conversations ─────────────────────────────────────────────
    def _seed_conversations(self):
        for client_email, master_email, slug, msgs, unread in CONVERSATIONS:
            client = self.clients[client_email]
            master_user = self.masters[master_email].user
            job = self.jobs.get(slug)
            conv = (Conversation.objects.filter(memberships__user=client)
                    .filter(memberships__user=master_user).filter(job=job).first())
            if conv is None:
                conv = Conversation.objects.create(job=job)
                ConversationParticipant.objects.bulk_create([
                    ConversationParticipant(conversation=conv, user=client),
                    ConversationParticipant(conversation=conv, user=master_user),
                ])
            if conv.messages.exists():
                continue
            last = None
            for who, text in msgs:
                if who == "system":
                    sender, mtype = None, Message.Type.SYSTEM
                elif who == "client":
                    sender, mtype = client, Message.Type.TEXT
                else:
                    sender, mtype = master_user, Message.Type.TEXT
                last = Message.objects.create(conversation=conv, sender=sender, type=mtype, text=text)
            conv.last_message = last
            conv.save(update_fields=["last_message", "updated_at"])
            ConversationParticipant.objects.filter(conversation=conv, user=client).update(unread_count=unread)

    # ── notifications ─────────────────────────────────────────────
    def _seed_notifications(self):
        self._notify(self.clients[CLIENT_EMAIL], CLIENT_NOTIFS)
        self._notify(self.masters["akmal@topmaster.uz"].user, MASTER_NOTIFS)

    def _notify(self, user, items):
        for ntype, title, body, read in items:
            Notification.objects.get_or_create(
                recipient=user, type=ntype, title=title,
                defaults={"body": body, "read": read},
            )

    # ── saved masters ─────────────────────────────────────────────
    def _seed_saved(self):
        for client_email, master_emails in SAVED:
            client = self.clients[client_email]
            for email in master_emails:
                profile = self.masters.get(email)
                if profile is not None:
                    SavedMaster.objects.get_or_create(client=client, master=profile)

    # ── support chat ──────────────────────────────────────────────
    def _seed_support_chat(self):
        client = self.clients[CLIENT_EMAIL]
        if SupportThread.objects.filter(user=client).exists():
            return
        staff = User.objects.filter(is_staff=True).first()
        thread = SupportThread.objects.create(
            user=client, subject="Buyurtma haqida savol",
            status=SupportThread.Status.PENDING,
        )
        SupportMessage.objects.create(
            thread=thread, sender=client, is_staff=False,
            text="Assalomu alaykum, buyurtmam holatini bilsam boʻladimi?",
        )
        reply = SupportMessage.objects.create(
            thread=thread, sender=staff, is_staff=True,
            text="Vaalaykum assalom! Albatta — buyurtmangiz ustaga biriktirildi, "
            "tez orada bogʻlanishadi.",
        )
        thread.last_message = reply
        thread.user_unread = 1
        thread.save(update_fields=["last_message", "user_unread", "updated_at"])

    # ── reports (trust & safety) ──────────────────────────────────
    def _seed_reports(self):
        from django.contrib.contenttypes.models import ContentType

        reporter = self.clients[CLIENT_EMAIL]
        targets = []
        master = self.masters.get("akmal@topmaster.uz")
        if master is not None:
            targets.append(
                (master, Report.Reason.SPAM, "Reklama xabarlari yuboryapti.", Report.Status.OPEN)
            )
        first_job = next(iter(self.jobs.values()), None)
        if first_job is not None:
            targets.append(
                (first_job, Report.Reason.INAPPROPRIATE, "Tavsif nomaqbul.", Report.Status.REVIEWING)
            )
        for target, reason, desc, status in targets:
            ct = ContentType.objects.get_for_model(type(target))
            Report.objects.get_or_create(
                reporter=reporter,
                content_type=ct,
                object_id=target.pk,
                defaults={"reason": reason, "description": desc, "status": status},
            )

    # ── report ────────────────────────────────────────────────────
    def _report(self):
        counts = {
            "users": User.objects.count(),
            "masters": MasterProfile.objects.count(),
            "skills": Skill.objects.count(),
            "portfolio": PortfolioItem.objects.count(),
            "verifications": VerificationRequest.objects.count(),
            "verify_docs": VerificationDocument.objects.count(),
            "devices": Device.objects.count(),
            "jobs": Job.objects.count(),
            "job_images": JobImage.objects.count(),
            "job_events": JobEvent.objects.count(),
            "proposals": Proposal.objects.count(),
            "reviews": Review.objects.count(),
            "conversations": Conversation.objects.count(),
            "messages": Message.objects.count(),
            "notifications": Notification.objects.count(),
            "saved": SavedMaster.objects.count(),
            "support_threads": SupportThread.objects.count(),
            "support_messages": SupportMessage.objects.count(),
            "reports": Report.objects.count(),
        }
        summary = ", ".join(f"{k}={v}" for k, v in counts.items())
        self.stdout.write(self.style.SUCCESS(
            f"Demo data seeded (idempotent). Parol: {DEMO_PASSWORD!r}.\n  {summary}"
        ))
