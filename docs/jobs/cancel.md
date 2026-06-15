# Buyurtmani bekor qilish (mijoz)

`POST /api/v1/jobs/{id}/cancel/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Mijoz buyurtmani bekor qiladi. Buyurtma `completed` yoki allaqachon `cancelled` holatida bo'lsa, xato qaytariladi. Muvaffaqiyatli bekor qilingandan so'ng `JobEvent(type="cancelled")` yoziladi va ushbu buyurtmaga bog'liq barcha `pending` (kutilayotgan) takliflar avtomatik ravishda `rejected` holatiga o'tkaziladi — bu bekor qilingan buyurtma orqali ustalarga yangi ishlarga yo'l ochilishini oldini oladi.

**Holat o'tishi:** `open` | `in_progress` | `awaiting_confirmation` → `cancelled`

**Yon ta'sirlar:**
- `JobEvent(type="cancelled", actor=mijoz)` yozuvi yaratiladi.
- `Proposal.objects.filter(job=job, status="pending").update(status="rejected", responded_at=now())` — barcha kutilayotgan takliflar rad etiladi.

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
  "status": "cancelled",
  "status_display": "Bekor qilindi",
  "proposals_count": 3,
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
      "id": 122,
      "type": "cancelled",
      "type_display": "Bekor qilindi",
      "note": "",
      "actor": 7,
      "created_at": "2026-06-15T09:00:00Z"
    }
  ],
  "assigned_master": null
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Buyurtma allaqachon `completed` yoki `cancelled` holatida |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/jobs/42/cancel/" \
  -H "Authorization: Bearer $ACCESS"
```
