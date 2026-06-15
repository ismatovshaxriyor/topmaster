# Mening buyurtmalarim

`GET /api/v1/jobs/my_jobs/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha (20 ta/sahifa) |
| **Throttle** | user: 1000/min |

## Tavsif

Joriy autentifikatsiya qilingan foydalanuvchi yaratgan barcha buyurtmalarni qaytaradi. `JobListSerializer` ishlatiladi. Umumiy ro'yxat (`GET /api/v1/jobs/`) dan farqli ravishda, bu endpoint `status` bo'yicha sukut bo'yicha filtrlash qilmaydi — barcha holatlardagi buyurtmalar ko'rsatiladi. `JobFilter` filtrlari va `ordering` parametri shu yerda ham ishlaydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |
| `category` | string | Yo'q | Kategoriya kaliti bo'yicha filtrlash |
| `city` | integer | Yo'q | Shahar ID si bo'yicha filtrlash |
| `price_type` | string | Yo'q | `fixed` yoki `negotiable` |
| `status` | string | Yo'q | `open`, `in_progress`, `awaiting_confirmation`, `completed`, `cancelled` |
| `urgent` | boolean | Yo'q | `true` yoki `false` |
| `ordering` | string | Yo'q | `created_at`, `-created_at`, `due_date`, `-due_date`, `price_amount`, `-price_amount`, `urgent`, `-urgent` |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
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
      "status": "open",
      "status_display": "Ochiq",
      "proposals_count": 3,
      "created_at": "2026-06-14T10:22:00Z",
      "client": {
        "id": 7,
        "full_name": "Alisher Karimov",
        "avatar": "http://localhost:8000/media/avatars/7.jpg"
      },
      "distance_km": null
    }
  ]
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
# Barcha buyurtmalarim
curl -X GET "http://localhost:8000/api/v1/jobs/my_jobs/" \
  -H "Authorization: Bearer $ACCESS"

# Faqat bekor qilingan buyurtmalar
curl -X GET "http://localhost:8000/api/v1/jobs/my_jobs/?status=cancelled" \
  -H "Authorization: Bearer $ACCESS"

# Oxirgi buyurtmalar birinchi
curl -X GET "http://localhost:8000/api/v1/jobs/my_jobs/?ordering=-created_at" \
  -H "Authorization: Bearer $ACCESS"
```
