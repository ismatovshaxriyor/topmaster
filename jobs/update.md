# Buyurtmani tahrirlash

`PATCH /api/v1/jobs/{id}/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Buyurtmaning tanlangan maydonlarini yangilaydi. Faqat buyurtmani yaratgan mijoz o'zgartirish kiritishi mumkin — boshqa foydalanuvchi `403` oladi. `JobCreateSerializer` ishlatiladi, shuning uchun barcha `create` maydonlari qabul qilinadi. **`status` maydoni bu endpoint orqali hech qachon o'zgartirilmaydi** — holat faqat maxsus lifecycle action endpointlari orqali o'zgaradi (`mark_awaiting`, `complete`, `cancel`).

> `PUT` (to'liq almashtirish) ham mavjud, lekin `PATCH` tavsiya etiladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Buyurtma ID si |

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json` — faqat o'zgartiriladigan maydonlar yuboriladi.

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `category` | integer | Yo'q | Yangi kategoriya ID si |
| `city` | integer | Yo'q | Yangi shahar ID si |
| `title` | string | Yo'q | Yangi sarlavha, maks. 160 belgi |
| `description` | string | Yo'q | Yangi tavsif |
| `address` | string | Yo'q | Yangi manzil, maks. 200 belgi |
| `price_type` | string | Yo'q | `fixed` yoki `negotiable` |
| `price_amount` | integer | Yo'q | Yangi byudjet (so'm) — faqat ma'lumot |
| `payment_timing` | string | Yo'q | `on_completion`, `staged`, `prepaid` |
| `when_choice` | string | Yo'q | `asap`, `today`, `tomorrow`, `this_week`, `exact` |
| `due_date` | date | Yo'q | `YYYY-MM-DD` |
| `urgent` | boolean | Yo'q | Shoshilinchlik holati |
| `latitude` | float | Yo'q | Aniq joylashuv kengligi |
| `longitude` | float | Yo'q | Aniq joylashuv uzunligi |

## Javob

### `200 OK`

```json
{
  "id": 42,
  "category": 3,
  "city": 1,
  "title": "Uy ta'mirlash — yangilangan sarlavha",
  "description": "Xona devorlarini bo'yash kerak, 3 xona. Sifatli bo'yoq talab qilinadi.",
  "address": "Chilonzor tumani, 14-kvartal",
  "price_type": "fixed",
  "price_amount": 600000,
  "payment_timing": "on_completion",
  "when_choice": "exact",
  "due_date": "2026-06-22",
  "urgent": true,
  "latitude": 41.2850,
  "longitude": 69.2100
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Maydon qiymati noto'g'ri (masalan, mavjud bo'lmagan `category` ID) |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X PATCH "http://localhost:8000/api/v1/jobs/42/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Uy ta'\''mirlash — yangilangan sarlavha",
    "price_amount": 600000,
    "urgent": true
  }'
```
