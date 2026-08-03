# Tasdiqlashga yuborish (usta)

`POST /api/v1/jobs/{id}/mark_awaiting/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat shu buyurtmaga tayinlangan usta |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Tayinlangan usta ishni bajarib bo'lgach, buyurtmani `in_progress` → `awaiting_confirmation` holatiga o'tkazadi. Faqat `is_master=True` bo'lgan va ushbu buyurtmaga `assigned_master` sifatida tayinlangan foydalanuvchi bu amalni bajarishi mumkin. Holat o'zgargandan so'ng `JobEvent(type="awaiting")` yoziladi va buyurtma egasi (mijoz) ga `"Tasdiqlash kutilmoqda"` push bildirishnomasi yuboriladi.

**Ruxsat shartlari:**
1. `request.user.is_master` bo'lishi kerak.
2. `job.assigned_master` mavjud bo'lishi kerak.
3. `job.assigned_master.user_id == request.user.id` bo'lishi kerak.

**Holat o'tishi:** `in_progress` → `awaiting_confirmation`

**Yon ta'sirlar:**
- `JobEvent(type="awaiting", actor=usta)` yozuvi yaratiladi.
- Mijozga `notify(job.client, type="system", title="Tasdiqlash kutilmoqda")` bildirishnomasi yuboriladi.

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
  "status": "awaiting_confirmation",
  "status_display": "Tasdiqlash kutilmoqda",
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
| `400` | Buyurtma `in_progress` holatida emas |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi shu buyurtmaga tayinlangan usta emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/jobs/42/mark_awaiting/" \
  -H "Authorization: Bearer $MASTER_ACCESS"
```
