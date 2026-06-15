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
    {"key": "payments", "label": "Toʻlov & narxlar", "icon": "wallet"},
    {"key": "trust", "label": "Ishonch & xavfsizlik", "icon": "shield-check"},
    {"key": "reviews", "label": "Sharhlar & reyting", "icon": "star"},
    {"key": "masters", "label": "Ustalar uchun", "icon": "wrench"},
    {"key": "account", "label": "Hisob & sozlamalar", "icon": "settings"},
]

FAQS = [
    # ── Boshlash ──────────────────────────────────────────────────
    {"topic": "getting-started", "question": "TopMaster nima?",
     "answer": "TopMaster — Oʻzbekiston boʻylab malakali ustalar (elektrik, santexnik, "
     "repetitor, duradgor va boshqalar) bilan mijozlarni bogʻlovchi xizmatlar platformasi."},
    {"topic": "getting-started", "question": "TopMaster qanday ishlaydi?",
     "answer": "Usta qidiring yoki buyurtma joylang → ustalar taklif yuboradi → chat orqali "
     "narx va vaqtni kelishing → ish bajarilgach reyting va sharh qoldiring."},
    {"topic": "getting-started", "question": "Foydalanish pullikmi?",
     "answer": "Mijozlar uchun qidiruv, buyurtma berish va ustalar bilan bogʻlanish butunlay "
     "bepul. Ustalar uchun roʻyxatdan oʻtish va profil ham bepul."},
    {"topic": "getting-started", "question": "Qaysi shaharlarda ishlaydi?",
     "answer": "Platforma butun Oʻzbekiston boʻylab — barcha viloyat markazlari va yirik "
     "shaharlarda ishlaydi. Shahringizni qidiruvda tanlang."},
    {"topic": "getting-started", "question": "Mobil ilova bormi?",
     "answer": "Ha, TopMaster mobil qurilmalar uchun moslashtirilgan — telefon orqali ham "
     "qulay foydalanishingiz mumkin."},

    # ── Buyurtmalar ───────────────────────────────────────────────
    {"topic": "orders", "question": "Qanday qilib buyurtma beraman?",
     "answer": "“Buyurtma berish” tugmasini bosing, ishni tavsiflang, yoʻnalish, manzil va "
     "vaqtni kiriting. Ustalar sizga taklif yuboradi — eng mosini tanlaysiz."},
    {"topic": "orders", "question": "Buyurtmani bekor qila olamanmi?",
     "answer": "Ha. Ish boshlanmaguncha buyurtmani istalgan vaqtda, hech qanday majburiyatsiz "
     "bekor qilishingiz mumkin."},
    {"topic": "orders", "question": "Buyurtmamni tahrirlay olamanmi?",
     "answer": "Buyurtma hali ochiq (usta tanlanmagan) boʻlsa, tafsilot, manzil va byudjetni "
     "tahrirlashingiz mumkin."},
    {"topic": "orders", "question": "Nechta taklif olaman?",
     "answer": "Cheklov yoʻq — buyurtmangizga bir nechta mos usta taklif yuborishi mumkin. "
     "Reyting, narx va portfolio boʻyicha solishtirib tanlaysiz."},
    {"topic": "orders", "question": "Buyurtma holatini qanday kuzataman?",
     "answer": "Har bir buyurtmaning bosqichlari koʻrsatiladi: joylandi → usta qabul qildi → "
     "ish boshlandi → bajarilmoqda → yakunlandi."},
    {"topic": "orders", "question": "Shoshilinch buyurtma berish mumkinmi?",
     "answer": "Ha. Buyurtma berishda “Shoshilinch” belgisini qoʻysangiz, eʼloningiz tepada "
     "koʻrsatiladi va tezroq taklif oladi."},

    # ── Takliflar ─────────────────────────────────────────────────
    {"topic": "proposals", "question": "Taklif nima?",
     "answer": "Taklif — usta sizning buyurtmangizga yuboradigan javob: narx, qisqa xabar va "
     "shartlar bilan. Siz takliflar ichidan birini tanlaysiz."},
    {"topic": "proposals", "question": "Taklifni qanday qabul qilaman?",
     "answer": "Buyurtma sahifasidagi taklifni koʻrib chiqing va “Qabul qilish” tugmasini "
     "bosing. Shu zahoti usta tayinlanadi va ish boshlanadi."},
    {"topic": "proposals", "question": "Bir nechta taklifni qabul qila olamanmi?",
     "answer": "Yoʻq. Har bir buyurtmaga faqat bitta taklif qabul qilinadi — qabul qilganingizda "
     "qolgan takliflar avtomatik rad etiladi."},
    {"topic": "proposals", "question": "Taklifni rad qilsam nima boʻladi?",
     "answer": "Usta xabardor qilinadi. Bu odatiy holat — boshqa mos ustani bemalol tanlashingiz "
     "mumkin."},
    {"topic": "proposals", "question": "Usta sifatida qancha taklif yubora olaman?",
     "answer": "Cheklov yoʻq, lekin har bir taklifni aniq va ishonchli yozing — bu qabul qilinish "
     "ehtimolini oshiradi."},

    # ── Toʻlov & narxlar (escrow YOʻQ) ────────────────────────────
    {"topic": "payments", "question": "Toʻlov qanday amalga oshadi?",
     "answer": "Toʻlov bevosita siz va usta oʻrtasida amalga oshadi. TopMaster pul "
     "oʻtkazmaydi va saqlamaydi — toʻlov usuli va shartlarini oʻzaro kelishasiz."},
    {"topic": "payments", "question": "TopMaster toʻlovni ushlab turadimi (Escrow)?",
     "answer": "Yoʻq. Platformada Escrow yoki ichki hisob yoʻq. Narx kelishuvi va toʻlov "
     "toʻliq tomonlar zimmasida — biz faqat ustani topishda yordam beramiz."},
    {"topic": "payments", "question": "Narxlar qanday belgilanadi?",
     "answer": "Buyurtma berishda belgilangan summa koʻrsatishingiz yoki “Kelishiladi” deb "
     "qoldirishingiz mumkin — bu holda ustalar oʻz narxini taklif qiladi."},
    {"topic": "payments", "question": "Narxlar qaysi valyutada?",
     "answer": "Barcha narxlar Oʻzbekiston soʻmida (soʻm) koʻrsatiladi, masalan: 450 000 soʻm."},
    {"topic": "payments", "question": "Ishdan keyin chek yoki shartnoma beriladimi?",
     "answer": "Rasmiy hujjatlar tomonlar oʻrtasida kelishiladi. Platformada esa buyurtma "
     "tarixi va yozishmalar saqlanadi."},

    # ── Ishonch & xavfsizlik ──────────────────────────────────────
    {"topic": "trust", "question": "Ustalar tekshiriladimi?",
     "answer": "Ha. Har bir usta pasport va mutaxassislik hujjatlari orqali tekshiriladi. "
     "Tasdiqlangan ustalarda ✓ belgisi boʻladi."},
    {"topic": "trust", "question": "Sharhlar haqiqiymi?",
     "answer": "Sharhni faqat ish yakunlangan mijozlar qoldira oladi — shu sababli reyting "
     "ishonchli va soxta sharhlardan himoyalangan."},
    {"topic": "trust", "question": "Xavfsiz ishlash uchun maslahatlar bormi?",
     "answer": "Kelishuvni chat orqali yozma qiling, ustaning profili va sharhlarini tekshiring, "
     "imkon qadar tanish yoki jamoat joyida uchrashing."},
    {"topic": "trust", "question": "Shubhali profil yoki muammoni qanday xabar qilaman?",
     "answer": "Buyurtma sahifasidagi “Muammo” tugmasi yoki qoʻllab-quvvatlash orqali bizga "
     "xabar bering — tez orada koʻrib chiqamiz."},
    {"topic": "trust", "question": "Hujjatlarim himoyalanganmi?",
     "answer": "Ha. Yuklangan hujjatlar shifrlanadi va faqat tekshiruv uchun ishlatiladi, "
     "boshqa foydalanuvchilarga koʻrsatilmaydi."},

    # ── Sharhlar & reyting ────────────────────────────────────────
    {"topic": "reviews", "question": "Qanday sharh qoldiraman?",
     "answer": "Ish yakunlangach buyurtma sahifasida ustaga 1–5 yulduz reyting va matn sharh "
     "qoldirishingiz mumkin."},
    {"topic": "reviews", "question": "Reyting qanday hisoblanadi?",
     "answer": "Ustaning reytingi barcha sharhlardagi yulduzlar oʻrtachasi sifatida avtomatik "
     "hisoblanadi."},
    {"topic": "reviews", "question": "Salbiy sharh qoldira olamanmi?",
     "answer": "Ha — halol va xolis fikringizni bildiring. Sharhlar boshqa mijozlarga toʻgʻri "
     "tanlov qilishda yordam beradi."},
    {"topic": "reviews", "question": "Bitta ishga necha marta sharh qoldira olaman?",
     "answer": "Har bir yakunlangan buyurtmaga bitta sharh qoldiriladi. Tahrir kerak boʻlsa "
     "qoʻllab-quvvatlashga murojaat qiling."},

    # ── Ustalar uchun ─────────────────────────────────────────────
    {"topic": "masters", "question": "Usta sifatida qanday roʻyxatdan oʻtaman?",
     "answer": "“Usta boʻling” sahifasiga oʻting, profil va koʻnikmalaringizni kiriting, "
     "hujjatlarni yuklang. 1–2 ish kunida tasdiqlanasiz."},
    {"topic": "masters", "question": "Profilimni qanday tasdiqlataman?",
     "answer": "Boshqaruv panelidagi “Tasdiqlash” boʻlimida pasport/ID, selfi va (ixtiyoriy) "
     "diplom hujjatlarini yuklang. Tasdiqlangach profilingizda ✓ paydo boʻladi."},
    {"topic": "masters", "question": "Buyurtmalarni qanday topaman?",
     "answer": "“Buyurtmalar” boʻlimida ochiq ishlarni koʻring va yoʻnalish/shahar boʻyicha "
     "filtrlab, mos buyurtmalarga taklif yuboring."},
    {"topic": "masters", "question": "Bandlik holatimni qanday belgilayman?",
     "answer": "Profilingizda holatni “Boʻsh” yoki “Band” deb belgilashingiz mumkin — bu "
     "mijozlarga sizning mavjudligingizni koʻrsatadi."},
    {"topic": "masters", "question": "Portfoliomga nechta rasm qoʻsha olaman?",
     "answer": "Portfoliongizga 10 tagacha bajarilgan ish rasmini qoʻshib, koʻproq mijoz "
     "jalb qilishingiz mumkin."},
    {"topic": "masters", "question": "Xizmatdan foydalanish ustalar uchun pullikmi?",
     "answer": "Roʻyxatdan oʻtish, profil va buyurtmalarga taklif yuborish bepul. Xizmat haqi "
     "shartlari, agar boʻlsa, alohida koʻrsatiladi."},

    # ── Hisob & sozlamalar ────────────────────────────────────────
    {"topic": "account", "question": "Roʻyxatdan qanday oʻtaman?",
     "answer": "Email va parol bilan bir necha soniyada roʻyxatdan oʻting. Roʻyxatdan oʻtishda "
     "mijoz yoki usta sifatida kirishni tanlaysiz."},
    {"topic": "account", "question": "Parolimni unutib qoʻysam nima qilaman?",
     "answer": "Kirish sahifasidagi “Parolni tiklash” orqali emailingizga yuborilgan "
     "koʻrsatmalar bilan yangi parol oʻrnatasiz."},
    {"topic": "account", "question": "Bildirishnomalarni qanday boshqaraman?",
     "answer": "Sozlamalar → Bildirishnomalar boʻlimida push, email va SMS xabarlarni alohida "
     "yoqib/oʻchirib qoʻyishingiz mumkin."},
    {"topic": "account", "question": "Tilni oʻzgartira olamanmi?",
     "answer": "Ha. Sozlamalar → Til va koʻrinish boʻlimidan Oʻzbek, Rus yoki Ingliz tilini "
     "tanlashingiz mumkin."},
    {"topic": "account", "question": "Hisobimni qanday oʻchiraman?",
     "answer": "Sozlamalar → Xavfsizlik boʻlimidagi “Akkauntni oʻchirish” orqali hisobingizni "
     "butunlay oʻchirib tashlashingiz mumkin."},
    {"topic": "account", "question": "Bir hisobda ham mijoz, ham usta boʻla olamanmi?",
     "answer": "Hisobingiz tanlangan rol (mijoz yoki usta) asosida ishlaydi. Usta boʻlish uchun "
     "“Usta boʻling” boʻlimidan professional profil yarating."},
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
