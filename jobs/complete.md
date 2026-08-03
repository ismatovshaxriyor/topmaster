# Buyurtmani yakunlash (mijoz)

`POST /api/v1/jobs/{id}/complete/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Mijoz ishni qabul qilib, buyurtmani `completed` holatiga o'tkazadi. Buyurtma `in_progress` yoki `awaiting_confirmation` holatida bo'lishi kerak. Yakunlangandan so'ng `JobEvent(type="completed")` yoziladi; agar ustasi tayinlangan bo'lsa, ustaga `"Buyurtma yakunlandi"` push bildirishnomasi yuboriladi. Yakunlangan buyurtmani bekor qilib bo'lmaydi.

**Holat o'tishi:** `in_progress` | `awaiting_confirmation` → `completed`

**Yon ta'sirlar:**
- `JobEvent(type="completed", actor=mijoz)` yozuvi yaratiladi.
- Tayinlangan usta mavjud bo'lsa: `notify(assigned_master.user, type="system", title="Buyurtma yakunlandi")` bildirishnomasi yuboriladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Buyurtma ID si |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

`JobDetailSerializer` formatida to'liq buyurtma ma'lumotlari qaytariladi.

```json
{
  "id": 42,
  "title": "Uy ta'mirlash ishlari",
  "category": {
    "id": 3,
    "key": "repair",
    "name": "Ta'mirlash"
  },
  "city": {
    "id": 1,
    "name": "Toshkent",
    "slug": "toshkent",
    "latitude": 41.2995,
    "longitude": 69.2401
  },
  "price_type": "fixed",
  "price_amount": 500000,
  "when_choice": "this_week",
  "due_date": "2026-06-20",
  "urgent": false,
  "status": "completed",
  "status_display": "Yakunlandi",
  "proposals_count": 5,
  "created_at": "2026-06-14T10:22:00Z",
  "client": {
    "id": 7,
    "full_name": "Alisher Karimov",
    "avatar": "http://localhost:8000/media/avatars/7.jpg"
  },
  "distance_km": null,
  "description": "Xona devorlarini bo'yash kerak, 3 xona.",
  "address": "Chilonzor tumani, 14-kvartal",
  "payment_timing": "on_completion",
  "images": [],
  "events": [
    {
      "id": 101,
      "type": "created",
      "type_display": "Buyurtma joylandi",
      "note": "",
      "actor": 7,
      "created_at": "2026-06-14T10:22:00Z"
    },
    {
      "id": 115,
      "type": "awaiting",
      "type_display": "Tasdiqlash kutilmoqda",
      "note": "",
      "actor": 15,
      "created_at": "2026-06-15T14:30:00Z"
    },
    {
      "id": 120,
      "type": "completed",
      "type_display": "Ish yakunlandi",
      "note": "",
      "actor": 7,
      "created_at": "2026-06-15T16:00:00Z"
    }
  ],
  "assigned_master": {
    "id": 9,
    "user_id": 15,
    "full_name": "Bobur Toshmatov",
    "avatar": "http://localhost:8000/media/avatars/15.jpg",
    "rating_avg": 4.7,
    "reviews_count": 23
  }
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Buyurtma `in_progress` yoki `awaiting_confirmation` holatida emas |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/jobs/42/complete/" \
  -H "Authorization: Bearer $ACCESS"
```
