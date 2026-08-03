# Buyurtma tafsilotlari

`GET /api/v1/jobs/{id}/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Bitta buyurtmaning to'liq ma'lumotlarini qaytaradi. `JobDetailSerializer` ishlatiladi — bu `JobListSerializer` ni kengaytirib, rasmlar (`images`), hayot sikli voqealari (`events` vaqt o'qi), va tayinlangan usta (`assigned_master`) ma'lumotlarini qo'shadi. Voqealar `created_at` bo'yicha o'sish tartibida beriladi.

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
  "status": "in_progress",
  "status_display": "Bajarilmoqda",
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
  "images": [
    {
      "id": 1,
      "image": "http://localhost:8000/media/jobs/job_42/photo1.jpg",
      "order": 0
    },
    {
      "id": 2,
      "image": "http://localhost:8000/media/jobs/job_42/photo2.jpg",
      "order": 1
    }
  ],
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
      "id": 108,
      "type": "accepted",
      "type_display": "Usta qabul qildi",
      "note": "",
      "actor": 15,
      "created_at": "2026-06-14T12:05:00Z"
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

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `images` | Buyurtmaga biriktirilgan rasmlar ro'yxati, `order` bo'yicha saralangan |
| `events` | Buyurtmaning hayot sikli voqealari (vaqt o'qi), `created_at` bo'yicha o'sish tartibida. `actor` — voqeani amalga oshirgan foydalanuvchi ID si |
| `assigned_master` | Tayinlangan usta profili; usta tayinlanmagan bo'lsa `null` |
| `distance_km` | Faqat `?lat&lng` bilan qilinadigan ro'yxat so'rovida to'ldiriladi; bu endpointda doim `null` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/jobs/42/" \
  -H "Authorization: Bearer $ACCESS"
```
