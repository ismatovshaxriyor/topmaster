# Yangi buyurtma yaratish

`POST /api/v1/jobs/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Rol: mijoz (`user.is_client`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Yangi buyurtma (ish topshiriq) yaratadi. Faqat `is_client=True` bo'lgan foydalanuvchilar buyurtma joylashi mumkin — usta rolida kirgan foydalanuvchi `403` oladi. Yaratilgandan so'ng avtomatik ravishda `JobEvent(type=created)` yozuvi hosil qilinadi va `notify_matching_masters` Celery vazifasi navbatga qo'yiladi — mos ustalar push/SMS bildirishnoma oladi.

**Yon ta'sirlar:**
- `JobEvent(type="created", actor=foydalanuvchi)` yozuvi yaratiladi.
- `notify_matching_masters.delay(job.id)` — Celery orqali mos ustalarga bildirishnoma yuboriladi.
- `status` maydon avtomatik `open` qiymatini oladi va bu yerda o'zgartirib bo'lmaydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `category` | integer | Ha | Kategoriya ID si (`Category` jadvalidan) |
| `city` | integer | Ha | Shahar ID si (`City` jadvalidan) |
| `title` | string | Ha | Buyurtma sarlavhasi, maks. 160 belgi |
| `description` | string | Ha | Buyurtma to'liq tavsifi |
| `address` | string | Yo'q | Aniq manzil (ixtiyoriy), maks. 200 belgi |
| `price_type` | string | Ha | Narx turi: `fixed` (belgilangan) yoki `negotiable` (kelishiladi) |
| `price_amount` | integer | Yo'q | Taklif qilingan byudjet (so'm) — faqat ma'lumot, hech qanday to'lov amalga oshirilmaydi |
| `payment_timing` | string | Yo'q | To'lov vaqti: `on_completion`, `staged`, `prepaid` |
| `when_choice` | string | Yo'q | Qachon kerak: `asap`, `today`, `tomorrow`, `this_week`, `exact` (standart: `this_week`) |
| `due_date` | date | Yo'q | Aniq sana (`YYYY-MM-DD`), `when_choice=exact` bo'lganda to'ldiriladi |
| `urgent` | boolean | Yo'q | Shoshilinch buyurtma (standart: `false`) |
| `latitude` | float | Yo'q | Buyurtma joylashgan joy kengligi (aniq koordinatlar) |
| `longitude` | float | Yo'q | Buyurtma joylashgan joy uzunligi (aniq koordinatlar) |

## Javob

### `201 Created`

```json
{
  "id": 42,
  "category": 3,
  "city": 1,
  "title": "Uy ta'mirlash ishlari",
  "description": "Xona devorlarini bo'yash kerak, 3 xona.",
  "address": "Chilonzor tumani, 14-kvartal",
  "price_type": "fixed",
  "price_amount": 500000,
  "payment_timing": "on_completion",
  "when_choice": "this_week",
  "due_date": "2026-06-20",
  "urgent": false,
  "latitude": 41.2850,
  "longitude": 69.2100
}
```

> Javob `JobCreateSerializer` maydonlarini qaytaradi. To'liq ma'lumot (rasmlar, voqealar, tayinlangan usta) uchun `GET /api/v1/jobs/{id}/` ga murojaat qiling.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Majburiy maydon yo'q yoki qiymat noto'g'ri |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi mijoz emas (`is_client=False`) |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/jobs/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "category": 3,
    "city": 1,
    "title": "Uy ta'\''mirlash ishlari",
    "description": "Xona devorlarini bo'\''yash kerak, 3 xona.",
    "address": "Chilonzor tumani, 14-kvartal",
    "price_type": "fixed",
    "price_amount": 500000,
    "payment_timing": "on_completion",
    "when_choice": "this_week",
    "due_date": "2026-06-20",
    "urgent": false,
    "latitude": 41.2850,
    "longitude": 69.2100
  }'
```
