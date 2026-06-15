"""Idempotently seed catalog cities and categories.

Cities now provide full O'zbekiston coverage (all 14 regions: poytaxt,
12 viloyat va Qoraqalpog'iston Respublikasi markazlari + tuman shaharlari).
- `cities` array -> City.name (slug derived via slugify).
- `categories` array -> Category (id -> key, label, icon); first 8 keys
  mirror the frontend mock data (ui_kits/web/data.js) and must stay stable.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Category, City

# O'zbekiston shaharlari — barcha 14 hudud bo'yicha to'liq qamrov.
# (Birinchi 7 tasi data.js bilan mos; qolganlari kengaytma.)
# Imlo O'zbek-lotin (' bilan); django slugify() bo'yicha dublikatlar yo'q.
CITIES = [
    # Toshkent shahri
    "Toshkent",
    # Qoraqalpog'iston Respublikasi
    "Nukus",
    "Beruniy",
    "Chimboy",
    "Xo'jayli",
    "To'rtko'l",
    "Qo'ng'irot",
    "Taxiatosh",
    "Mang'it",
    "Mo'ynoq",
    "Taxtako'pir",
    # Andijon viloyati
    "Andijon",
    "Asaka",
    "Shahrixon",
    "Xonobod",
    "Qorasuv",
    "Marhamat",
    "Paxtaobod",
    "Qo'rg'ontepa",
    "Xo'jaobod",
    "Jalaquduq",
    "Baliqchi",
    "Poytug'",
    # Buxoro viloyati
    "Buxoro",
    "Kogon",
    "G'ijduvon",
    "Shofirkon",
    "Vobkent",
    "Qorako'l",
    "Olot",
    "Galaosiyo",
    "Romitan",
    "Qorovulbozor",
    # Farg'ona viloyati
    "Farg'ona",
    "Marg'ilon",
    "Qo'qon",
    "Quvasoy",
    "Quva",
    "Rishton",
    "Beshariq",
    "Yaypan",
    "Oltiariq",
    "Toshloq",
    "Yozyovon",
    # Jizzax viloyati
    "Jizzax",
    "Gagarin",
    "Do'stlik",
    "G'allaorol",
    "Paxtakor",
    "Zomin",
    "Dashtobod",
    # Qashqadaryo viloyati
    "Qarshi",
    "Shahrisabz",
    "Koson",
    "Kitob",
    "G'uzor",
    "Muborak",
    "Chiroqchi",
    "Yakkabog'",
    "Qamashi",
    "Beshkent",
    "Tallimarjon",
    # Namangan viloyati
    "Namangan",
    "Chust",
    "Chortoq",
    "Kosonsoy",
    "Pop",
    "To'raqo'rg'on",
    "Uchqo'rg'on",
    "Uychi",
    "Yangiqo'rg'on",
    "Haqqulobod",
    # Navoiy viloyati
    "Navoiy",
    "Zarafshon",
    "Karmana",
    "Uchquduq",
    "Nurota",
    "Qiziltepa",
    "Konimex",
    # Samarqand viloyati
    "Samarqand",
    "Kattaqo'rg'on",
    "Urgut",
    "Bulung'ur",
    "Jomboy",
    "Juma",
    "Oqtosh",
    "Ishtixon",
    "Chelak",
    "Payariq",
    # Sirdaryo viloyati
    "Guliston",
    "Yangiyer",
    "Shirin",
    "Sirdaryo",
    "Boyovut",
    "Baxt",
    # Surxondaryo viloyati
    "Termiz",
    "Denov",
    "Boysun",
    "Sho'rchi",
    "Jarqo'rg'on",
    "Sherobod",
    "Qumqo'rg'on",
    "Sariosiyo",
    "Sharg'un",
    # Toshkent viloyati
    "Nurafshon",
    "Chirchiq",
    "Angren",
    "Olmaliq",
    "Bekobod",
    "Yangiyo'l",
    "Ohangaron",
    "Chinoz",
    "Parkent",
    "Piskent",
    "Bo'ka",
    "G'azalkent",
    "Oqqo'rg'on",
    "To'ytepa",
    "Keles",
    # Xorazm viloyati
    "Urganch",
    "Xiva",
    "Xonqa",
    "Gurlan",
    "Shovot",
    "Pitnak",
    "Hazorasp",
]

# Asosiy shaharlar koordinatalari (lat, lng) — "yaqindagi" qidiruv uchun.
# Hudud markazlari + yirik shaharlar qamrab olingan; qolgan kichik shaharlar
# koordinatasiz qoladi (ular usta/ish aniq koordinatasi bo'lsagina masofaga
# kiradi). Idempotent: mavjud yozuvlarga ham backfill qilinadi.
CITY_COORDS = {
    "Toshkent": (41.2995, 69.2401),
    "Nukus": (42.4600, 59.6166),
    "Beruniy": (41.6911, 60.7522),
    "Chimboy": (42.9342, 59.7711),
    "Xo'jayli": (42.3989, 59.4486),
    "To'rtko'l": (41.5500, 61.0000),
    "Qo'ng'irot": (43.0667, 58.9000),
    "Andijon": (40.7821, 72.3442),
    "Asaka": (40.6420, 72.2370),
    "Shahrixon": (40.7110, 72.0560),
    "Xonobod": (40.8120, 73.0470),
    "Qorasuv": (40.7330, 72.8670),
    "Marhamat": (40.4800, 72.3200),
    "Buxoro": (39.7680, 64.4210),
    "Kogon": (39.7220, 64.5500),
    "G'ijduvon": (40.1030, 64.6800),
    "Vobkent": (40.0330, 64.5170),
    "Farg'ona": (40.3864, 71.7864),
    "Marg'ilon": (40.4711, 71.7242),
    "Qo'qon": (40.5286, 70.9425),
    "Quvasoy": (40.2990, 71.9760),
    "Quva": (40.5210, 72.0680),
    "Rishton": (40.3580, 71.2840),
    "Jizzax": (40.1158, 67.8420),
    "Gagarin": (40.0700, 67.0700),
    "G'allaorol": (40.0167, 67.6000),
    "Paxtakor": (40.3170, 67.9500),
    "Zomin": (39.9600, 68.4000),
    "Qarshi": (38.8606, 65.7891),
    "Shahrisabz": (39.0578, 66.8300),
    "Koson": (39.0400, 65.5800),
    "Kitob": (39.1300, 66.8800),
    "G'uzor": (38.6230, 66.2500),
    "Muborak": (39.2530, 65.1500),
    "Namangan": (41.0011, 71.6726),
    "Chust": (41.0000, 71.2333),
    "Chortoq": (41.0700, 71.8200),
    "Pop": (40.8740, 71.1080),
    "Uchqo'rg'on": (41.1130, 72.0900),
    "Navoiy": (40.0844, 65.3792),
    "Zarafshon": (41.5720, 64.2050),
    "Karmana": (40.1400, 65.3600),
    "Uchquduq": (42.1570, 63.5560),
    "Nurota": (40.5630, 65.6890),
    "Qiziltepa": (40.0300, 64.8500),
    "Samarqand": (39.6270, 66.9750),
    "Kattaqo'rg'on": (39.8990, 66.2540),
    "Urgut": (39.4030, 67.2420),
    "Bulung'ur": (39.7700, 67.2800),
    "Jomboy": (39.7100, 67.1300),
    "Guliston": (40.4897, 68.7842),
    "Yangiyer": (40.2670, 68.8170),
    "Shirin": (40.2330, 69.0830),
    "Sirdaryo": (40.8470, 68.6580),
    "Termiz": (37.2242, 67.2783),
    "Denov": (38.2670, 67.8900),
    "Boysun": (38.2060, 67.1980),
    "Sho'rchi": (37.9900, 67.7900),
    "Jarqo'rg'on": (37.5050, 67.4200),
    "Sherobod": (37.6700, 67.0000),
    "Nurafshon": (41.0167, 69.3667),
    "Chirchiq": (41.4690, 69.5820),
    "Angren": (41.0167, 70.1436),
    "Olmaliq": (40.8440, 69.5980),
    "Bekobod": (40.2200, 69.2690),
    "Yangiyo'l": (41.1120, 69.0480),
    "Ohangaron": (40.9080, 69.6390),
    "Chinoz": (40.9370, 68.7660),
    "Parkent": (41.2900, 69.6800),
    "Piskent": (40.8900, 69.3500),
    "Urganch": (41.5500, 60.6333),
    "Xiva": (41.3783, 60.3639),
    "Xonqa": (41.4670, 60.7900),
    "Gurlan": (41.8330, 60.3830),
    "Shovot": (41.6500, 60.3500),
    "Hazorasp": (41.3200, 61.0740),
}

# Xizmat yo'nalishlari (yo'nalishlar). Birinchi 8 tasi data.js bilan mos
# (kalitlar o'zgarmaydi — seed_demo / frontend ularga bog'liq); qolgani kengaytma.
CATEGORIES = [
    # ── data.js bilan mos (kalitlarni o'zgartirmang) ──
    {"key": "elektrik", "label": "Elektrik", "icon": "zap"},
    {"key": "santexnik", "label": "Santexnik", "icon": "wrench"},
    {"key": "repetitor", "label": "Repetitor", "icon": "graduation-cap"},
    {"key": "tozalash", "label": "Tozalash", "icon": "sparkles"},
    {"key": "duradgor", "label": "Duradgor", "icon": "hammer"},
    {"key": "bo-yoqchi", "label": "Bo'yoqchi", "icon": "paintbrush"},
    {"key": "konditsioner", "label": "Konditsioner", "icon": "wind"},
    {"key": "ko-chish", "label": "Ko'chirish", "icon": "truck"},
    # ── Kengaytirilgan yo'nalishlar ──
    {"key": "payvandchi", "label": "Payvandchi", "icon": "flame"},
    {"key": "kafelchi", "label": "Kafelchi (Plitka)", "icon": "grid-3x3"},
    {"key": "pardozlash", "label": "Pardozlovchi", "icon": "layers"},
    {"key": "tom-ustasi", "label": "Tom ustasi", "icon": "home"},
    {"key": "oynasoz", "label": "Oynasoz", "icon": "square"},
    {"key": "quruvchi", "label": "Quruvchi", "icon": "hard-hat"},
    {"key": "maishiy-texnika", "label": "Maishiy texnika ustasi", "icon": "washing-machine"},
    {"key": "muzlatgich", "label": "Sovutgich ustasi", "icon": "refrigerator"},
    {"key": "kompyuter", "label": "Kompyuter ustasi", "icon": "laptop"},
    {"key": "telefon-ustasi", "label": "Telefon ustasi", "icon": "smartphone"},
    {"key": "avto-usta", "label": "Avto usta", "icon": "car"},
    {"key": "bogbon", "label": "Bog'bon", "icon": "sprout"},
    {"key": "fotograf", "label": "Fotograf", "icon": "camera"},
    {"key": "sartarosh", "label": "Sartarosh", "icon": "scissors"},
    {"key": "tikuvchi", "label": "Tikuvchi", "icon": "shirt"},
    {"key": "mebel-tamiri", "label": "Mebel taʼmiri", "icon": "sofa"},
    {"key": "eshik-ustasi", "label": "Eshik-deraza ustasi", "icon": "door-open"},
    {"key": "dezinfeksiya", "label": "Dezinfeksiya", "icon": "spray-can"},
    # ── Qo'shimcha yo'nalishlar (to'liq qamrov) ──
    {"key": "gaz-ustasi", "label": "Gaz ustasi", "icon": "flame"},
    {"key": "lift-ustasi", "label": "Lift ustasi", "icon": "arrow-up-down"},
    {"key": "videokuzatuv", "label": "Videokuzatuv va signalizatsiya", "icon": "cctv"},
    {"key": "jalyuzi-pardalar", "label": "Jalyuzi va pardalar", "icon": "blinds"},
    {"key": "quduq-qazish", "label": "Quduq va skvajina qazish", "icon": "droplet"},
    {"key": "gozallik-manikur", "label": "Go'zallik va manikür", "icon": "sparkles"},
    {"key": "massaj", "label": "Massaj", "icon": "hand-helping"},
    {"key": "sport-murabbiy", "label": "Sport murabbiy", "icon": "dumbbell"},
    {"key": "enaga", "label": "Bola parvarishi (enaga)", "icon": "baby"},
    {"key": "keksalar-parvarishi", "label": "Keksalar parvarishi", "icon": "heart-pulse"},
    {"key": "veterinar", "label": "Veterinar", "icon": "stethoscope"},
    {"key": "toy-xizmatlari", "label": "To'y xizmatlari va tamada", "icon": "party-popper"},
    {"key": "konditer-tort", "label": "Konditer va tort", "icon": "cake"},
    {"key": "gul-yetkazib-berish", "label": "Gul yetkazib berish", "icon": "flower"},
    {"key": "tarjimon", "label": "Tarjimon", "icon": "languages"},
    {"key": "buxgalter", "label": "Buxgalter", "icon": "calculator"},
    {"key": "yurist", "label": "Yurist", "icon": "scale"},
    {"key": "dasturchi", "label": "IT va dasturchi", "icon": "code"},
    {"key": "smm-marketing", "label": "SMM va marketing", "icon": "megaphone"},
    {"key": "web-dizayn", "label": "Web-dizayn", "icon": "palette"},
    {"key": "poyabzal-soat", "label": "Poyabzal va soat taʼmiri", "icon": "footprints"},
    {"key": "kir-yuvish-dazmol", "label": "Kir yuvish va dazmol", "icon": "washing-machine"},
    {"key": "gruzchik", "label": "Gruzchik", "icon": "package"},
]


class Command(BaseCommand):
    help = "Seed cities and service categories (idempotent)."

    def handle(self, *args, **options):
        cities_created = 0
        for order, name in enumerate(CITIES):
            coords = CITY_COORDS.get(name)
            defaults = {"slug": slugify(name), "order": order}
            if coords:
                defaults["latitude"], defaults["longitude"] = coords
            city, created = City.objects.get_or_create(name=name, defaults=defaults)
            cities_created += int(created)
            # Backfill coordinates onto pre-existing rows (idempotent).
            if not created and coords and (city.latitude is None or city.longitude is None):
                city.latitude, city.longitude = coords
                city.save(update_fields=["latitude", "longitude"])

        cats_created = 0
        for order, cat in enumerate(CATEGORIES):
            _, created = Category.objects.get_or_create(
                key=cat["key"],
                defaults={
                    "label": cat["label"],
                    "icon": cat["icon"],
                    "order": order,
                    "is_active": True,
                },
            )
            cats_created += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Catalog seeded: cities {cities_created} new / {len(CITIES)} total, "
                f"categories {cats_created} new / {len(CATEGORIES)} total."
            )
        )
