"""Idempotent seed of a comprehensive FAQ help-center (topics + entries).

Extends the original design-system FAQ (data.js) into full coverage across 8
topics. Payment answers reflect the real product: TopMaster does NOT process
money or hold escrow — pricing/payment is arranged directly between the client
and the master. Existing topic keys (orders, payments, trust, masters) are kept.
"""
from django.core.management.base import BaseCommand

from apps.support.models import Faq, FaqTopic

FAQ_TOPICS = [
    {"key": "getting-started", "label": "Boshlash", "icon": "rocket"},
    {"key": "orders", "label": "Buyurtmalar", "icon": "clipboard-list"},
    {"key": "proposals", "label": "Takliflar", "icon": "file-signature"},
    {"key": "payments", "label": "To'lov & narxlar", "icon": "wallet"},
    {"key": "trust", "label": "Ishonch & xavfsizlik", "icon": "shield-check"},
    {"key": "reviews", "label": "Sharhlar & reyting", "icon": "star"},
    {"key": "masters", "label": "Ustalar uchun", "icon": "wrench"},
    {"key": "account", "label": "Hisob & sozlamalar", "icon": "settings"},
]

FAQS = [
    # ── Boshlash ──────────────────────────────────────────────────
    {"topic": "getting-started", "question": "TopMaster nima?",
     "answer": "TopMaster — O'zbekiston bo'ylab malakali ustalar (elektrik, santexnik, "
     "repetitor, duradgor va boshqalar) bilan mijozlarni bog'lovchi xizmatlar platformasi."},
    {"topic": "getting-started", "question": "TopMaster qanday ishlaydi?",
     "answer": "Usta qidiring yoki buyurtma joylang → ustalar taklif yuboradi → chat orqali "
     "narx va vaqtni kelishing → ish bajarilgach reyting va sharh qoldiring."},
    {"topic": "getting-started", "question": "Foydalanish pullikmi?",
     "answer": "Mijozlar uchun qidiruv, buyurtma berish va ustalar bilan bog'lanish butunlay "
     "bepul. Ustalar uchun ro'yxatdan o'tish va profil ham bepul."},
    {"topic": "getting-started", "question": "Qaysi shaharlarda ishlaydi?",
     "answer": "Platforma butun O'zbekiston bo'ylab — barcha viloyat markazlari va yirik "
     "shaharlarda ishlaydi. Shahringizni qidiruvda tanlang."},
    {"topic": "getting-started", "question": "Mobil ilova bormi?",
     "answer": "Ha, TopMaster mobil qurilmalar uchun moslashtirilgan — telefon orqali ham "
     "qulay foydalanishingiz mumkin."},

    # ── Buyurtmalar ───────────────────────────────────────────────
    {"topic": "orders", "question": "Qanday qilib buyurtma beraman?",
     "answer": "“Buyurtma berish” tugmasini bosing, ishni tavsiflang, yo'nalish, manzil va "
     "vaqtni kiriting. Ustalar sizga taklif yuboradi — eng mosini tanlaysiz."},
    {"topic": "orders", "question": "Buyurtmani bekor qila olamanmi?",
     "answer": "Ha. Ish boshlanmaguncha buyurtmani istalgan vaqtda, hech qanday majburiyatsiz "
     "bekor qilishingiz mumkin."},
    {"topic": "orders", "question": "Buyurtmamni tahrirlay olamanmi?",
     "answer": "Buyurtma hali ochiq (usta tanlanmagan) bo'lsa, tafsilot, manzil va byudjetni "
     "tahrirlashingiz mumkin."},
    {"topic": "orders", "question": "Nechta taklif olaman?",
     "answer": "Cheklov yo'q — buyurtmangizga bir nechta mos usta taklif yuborishi mumkin. "
     "Reyting, narx va portfolio bo'yicha solishtirib tanlaysiz."},
    {"topic": "orders", "question": "Buyurtma holatini qanday kuzataman?",
     "answer": "Har bir buyurtmaning bosqichlari ko'rsatiladi: joylandi → usta qabul qildi → "
     "ish boshlandi → bajarilmoqda → yakunlandi."},
    {"topic": "orders", "question": "Shoshilinch buyurtma berish mumkinmi?",
     "answer": "Ha. Buyurtma berishda “Shoshilinch” belgisini qo'ysangiz, eʼloningiz tepada "
     "ko'rsatiladi va tezroq taklif oladi."},

    # ── Takliflar ─────────────────────────────────────────────────
    {"topic": "proposals", "question": "Taklif nima?",
     "answer": "Taklif — usta sizning buyurtmangizga yuboradigan javob: narx, qisqa xabar va "
     "shartlar bilan. Siz takliflar ichidan birini tanlaysiz."},
    {"topic": "proposals", "question": "Taklifni qanday qabul qilaman?",
     "answer": "Buyurtma sahifasidagi taklifni ko'rib chiqing va “Qabul qilish” tugmasini "
     "bosing. Shu zahoti usta tayinlanadi va ish boshlanadi."},
    {"topic": "proposals", "question": "Bir nechta taklifni qabul qila olamanmi?",
     "answer": "Yo'q. Har bir buyurtmaga faqat bitta taklif qabul qilinadi — qabul qilganingizda "
     "qolgan takliflar avtomatik rad etiladi."},
    {"topic": "proposals", "question": "Taklifni rad qilsam nima bo'ladi?",
     "answer": "Usta xabardor qilinadi. Bu odatiy holat — boshqa mos ustani bemalol tanlashingiz "
     "mumkin."},
    {"topic": "proposals", "question": "Usta sifatida qancha taklif yubora olaman?",
     "answer": "Cheklov yo'q, lekin har bir taklifni aniq va ishonchli yozing — bu qabul qilinish "
     "ehtimolini oshiradi."},

    # ── To'lov & narxlar (escrow YO'Q) ────────────────────────────
    {"topic": "payments", "question": "To'lov qanday amalga oshadi?",
     "answer": "To'lov bevosita siz va usta o'rtasida amalga oshadi. TopMaster pul "
     "o'tkazmaydi va saqlamaydi — to'lov usuli va shartlarini o'zaro kelishasiz."},
    {"topic": "payments", "question": "TopMaster to'lovni ushlab turadimi (Escrow)?",
     "answer": "Yo'q. Platformada Escrow yoki ichki hisob yo'q. Narx kelishuvi va to'lov "
     "to'liq tomonlar zimmasida — biz faqat ustani topishda yordam beramiz."},
    {"topic": "payments", "question": "Narxlar qanday belgilanadi?",
     "answer": "Buyurtma berishda belgilangan summa ko'rsatishingiz yoki “Kelishiladi” deb "
     "qoldirishingiz mumkin — bu holda ustalar o'z narxini taklif qiladi."},
    {"topic": "payments", "question": "Narxlar qaysi valyutada?",
     "answer": "Barcha narxlar O'zbekiston so'mida (so'm) ko'rsatiladi, masalan: 450 000 so'm."},
    {"topic": "payments", "question": "Ishdan keyin chek yoki shartnoma beriladimi?",
     "answer": "Rasmiy hujjatlar tomonlar o'rtasida kelishiladi. Platformada esa buyurtma "
     "tarixi va yozishmalar saqlanadi."},

    # ── Ishonch & xavfsizlik ──────────────────────────────────────
    {"topic": "trust", "question": "Ustalar tekshiriladimi?",
     "answer": "Ha. Har bir usta pasport va mutaxassislik hujjatlari orqali tekshiriladi. "
     "Tasdiqlangan ustalarda ✓ belgisi bo'ladi."},
    {"topic": "trust", "question": "Sharhlar haqiqiymi?",
     "answer": "Sharhni faqat ish yakunlangan mijozlar qoldira oladi — shu sababli reyting "
     "ishonchli va soxta sharhlardan himoyalangan."},
    {"topic": "trust", "question": "Xavfsiz ishlash uchun maslahatlar bormi?",
     "answer": "Kelishuvni chat orqali yozma qiling, ustaning profili va sharhlarini tekshiring, "
     "imkon qadar tanish yoki jamoat joyida uchrashing."},
    {"topic": "trust", "question": "Shubhali profil yoki muammoni qanday xabar qilaman?",
     "answer": "Buyurtma sahifasidagi “Muammo” tugmasi yoki qo'llab-quvvatlash orqali bizga "
     "xabar bering — tez orada ko'rib chiqamiz."},
    {"topic": "trust", "question": "Hujjatlarim himoyalanganmi?",
     "answer": "Ha. Yuklangan hujjatlar shifrlanadi va faqat tekshiruv uchun ishlatiladi, "
     "boshqa foydalanuvchilarga ko'rsatilmaydi."},

    # ── Sharhlar & reyting ────────────────────────────────────────
    {"topic": "reviews", "question": "Qanday sharh qoldiraman?",
     "answer": "Ish yakunlangach buyurtma sahifasida ustaga 1–5 yulduz reyting va matn sharh "
     "qoldirishingiz mumkin."},
    {"topic": "reviews", "question": "Reyting qanday hisoblanadi?",
     "answer": "Ustaning reytingi barcha sharhlardagi yulduzlar o'rtachasi sifatida avtomatik "
     "hisoblanadi."},
    {"topic": "reviews", "question": "Salbiy sharh qoldira olamanmi?",
     "answer": "Ha — halol va xolis fikringizni bildiring. Sharhlar boshqa mijozlarga to'g'ri "
     "tanlov qilishda yordam beradi."},
    {"topic": "reviews", "question": "Bitta ishga necha marta sharh qoldira olaman?",
     "answer": "Har bir yakunlangan buyurtmaga bitta sharh qoldiriladi. Tahrir kerak bo'lsa "
     "qo'llab-quvvatlashga murojaat qiling."},

    # ── Ustalar uchun ─────────────────────────────────────────────
    {"topic": "masters", "question": "Usta sifatida qanday ro'yxatdan o'taman?",
     "answer": "“Usta bo'ling” sahifasiga o'ting, profil va ko'nikmalaringizni kiriting, "
     "hujjatlarni yuklang. 1–2 ish kunida tasdiqlanasiz."},
    {"topic": "masters", "question": "Profilimni qanday tasdiqlataman?",
     "answer": "Boshqaruv panelidagi “Tasdiqlash” bo'limida pasport/ID, selfi va (ixtiyoriy) "
     "diplom hujjatlarini yuklang. Tasdiqlangach profilingizda ✓ paydo bo'ladi."},
    {"topic": "masters", "question": "Buyurtmalarni qanday topaman?",
     "answer": "“Buyurtmalar” bo'limida ochiq ishlarni ko'ring va yo'nalish/shahar bo'yicha "
     "filtrlab, mos buyurtmalarga taklif yuboring."},
    {"topic": "masters", "question": "Bandlik holatimni qanday belgilayman?",
     "answer": "Profilingizda holatni “Bo'sh” yoki “Band” deb belgilashingiz mumkin — bu "
     "mijozlarga sizning mavjudligingizni ko'rsatadi."},
    {"topic": "masters", "question": "Portfoliomga nechta rasm qo'sha olaman?",
     "answer": "Portfoliongizga 10 tagacha bajarilgan ish rasmini qo'shib, ko'proq mijoz "
     "jalb qilishingiz mumkin."},
    {"topic": "masters", "question": "Xizmatdan foydalanish ustalar uchun pullikmi?",
     "answer": "Ro'yxatdan o'tish, profil va buyurtmalarga taklif yuborish bepul. Xizmat haqi "
     "shartlari, agar bo'lsa, alohida ko'rsatiladi."},

    # ── Hisob & sozlamalar ────────────────────────────────────────
    {"topic": "account", "question": "Ro'yxatdan qanday o'taman?",
     "answer": "Email va parol bilan bir necha soniyada ro'yxatdan o'ting. Ro'yxatdan o'tishda "
     "mijoz yoki usta sifatida kirishni tanlaysiz."},
    {"topic": "account", "question": "Parolimni unutib qo'ysam nima qilaman?",
     "answer": "Kirish sahifasidagi “Parolni tiklash” orqali emailingizga yuborilgan "
     "ko'rsatmalar bilan yangi parol o'rnatasiz."},
    {"topic": "account", "question": "Bildirishnomalarni qanday boshqaraman?",
     "answer": "Sozlamalar → Bildirishnomalar bo'limida push, email va SMS xabarlarni alohida "
     "yoqib/o'chirib qo'yishingiz mumkin."},
    {"topic": "account", "question": "Tilni o'zgartira olamanmi?",
     "answer": "Ha. Sozlamalar → Til va ko'rinish bo'limidan O'zbek, Rus yoki Ingliz tilini "
     "tanlashingiz mumkin."},
    {"topic": "account", "question": "Hisobimni qanday o'chiraman?",
     "answer": "Sozlamalar → Xavfsizlik bo'limidagi “Akkauntni o'chirish” orqali hisobingizni "
     "butunlay o'chirib tashlashingiz mumkin."},
    {"topic": "account", "question": "Bir hisobda ham mijoz, ham usta bo'la olamanmi?",
     "answer": "Hisobingiz tanlangan rol (mijoz yoki usta) asosida ishlaydi. Usta bo'lish uchun "
     "“Usta bo'ling” bo'limidan professional profil yarating."},
]


class Command(BaseCommand):
    help = "Seed a comprehensive FAQ help-center (topics + entries, idempotent)."

    def handle(self, *args, **options):
        topics = {}
        topics_created = 0
        for order, data in enumerate(FAQ_TOPICS):
            topic, created = FaqTopic.objects.update_or_create(
                key=data["key"],
                defaults={"label": data["label"], "icon": data["icon"], "order": order},
            )
            topics[data["key"]] = topic
            topics_created += int(created)

        # Per-topic ordering for tidy display.
        topic_counters = {}
        faqs_created = 0
        for data in FAQS:
            topic = topics[data["topic"]]
            order = topic_counters.get(data["topic"], 0)
            topic_counters[data["topic"]] = order + 1
            _, created = Faq.objects.update_or_create(
                topic=topic,
                question=data["question"],
                defaults={"answer": data["answer"], "order": order},
            )
            faqs_created += int(created)

        # Prune stale rows so the help-center converges to EXACTLY the defined
        # set (removes outdated entries, e.g. old escrow/payment-method FAQs).
        defined_keys = {t["key"] for t in FAQ_TOPICS}
        defined_pairs = {(f["topic"], f["question"]) for f in FAQS}
        faqs_removed = 0
        for faq in Faq.objects.select_related("topic"):
            if (faq.topic.key, faq.question) not in defined_pairs:
                faq.delete()
                faqs_removed += 1
        topics_removed, _ = FaqTopic.objects.exclude(key__in=defined_keys).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Support seeded: {len(FAQ_TOPICS)} topics ({topics_created} new), "
                f"{len(FAQS)} FAQs ({faqs_created} new); "
                f"pruned {faqs_removed} stale FAQ(s), {topics_removed} stale topic obj(s)."
            )
        )
