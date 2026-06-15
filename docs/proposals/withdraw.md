# Taklifni qaytarib olish

`POST /api/v1/proposals/{id}/withdraw/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Faqat taklif egasi (usta) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Usta o'zi yuborgan taklifni qaytarib oladi. Yon ta'sir:

1. Taklif holati `pending → withdrawn` ga o'tadi; `responded_at` o'rnatiladi.

Bildirishnoma yuborilmaydi; `job.proposals_count` o'zgarmaydi; `job.status` ham
o'zgarmaydi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Qaytarib olinadigan taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

Yangilangan taklif `ProposalSerializer` formatida qaytariladi.

```json
{
  "id": 15,
  "job": 7,
  "job_title": "Santexnik kerak",
  "master": {
    "id": 4,
    "name": "Jasur Toshmatov",
    "avatar": "http://localhost:8000/media/avatars/jasur.jpg",
    "spec": "Santexnik",
    "city": {"id": 1, "name": "Toshkent", "slug": "toshkent", "latitude": 41.2995, "longitude": 69.2401},
    "experience_years": 5,
    "rating_avg": "4.80",
    "reviews_count": 23,
    "min_price": 50000,
    "status": "active",
    "is_verified": true,
    "is_top": false,
    "views_count": 140,
    "distance_km": null
  },
  "message": "Men bu ishni bajarishga tayyorman.",
  "proposed_price": 120000,
  "status": "withdrawn",
  "status_display": "Qaytarib olindi",
  "created_at": "2026-06-15T10:23:00Z",
  "responded_at": "2026-06-15T10:50:00Z"
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Taklif `pending` holatida emas — `{"status": "Faqat kutilayotgan taklifni qaytarib olish mumkin."}` |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi ushbu taklifning egasi emas |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/proposals/15/withdraw/" \
  -H "Authorization: Bearer $ACCESS"
```
