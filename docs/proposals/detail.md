# Taklif tafsiloti

`GET /api/v1/proposals/{id}/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated + ko'rinish doirasi |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Bitta taklifning to'liq ma'lumotlarini qaytaradi. Ko'rinish doirasi ro'yxat
endpointidagi bilan bir xil: foydalanuvchi taklifni ko'ra oladi **agar** u taklif
bergan usta bo'lsa **yoki** taklif tegishli buyurtma egasi bo'lsa. Shart bajarilmasa
`404` qaytariladi (ma'lumot sizib chiqmasligi uchun `403` emas).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

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
  "status": "pending",
  "status_display": "Kutilmoqda",
  "created_at": "2026-06-15T10:23:00Z",
  "responded_at": null
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
curl "http://localhost:8000/api/v1/proposals/15/" \
  -H "Authorization: Bearer $ACCESS"
```
