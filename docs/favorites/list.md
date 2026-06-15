# Saqlangan ustalar ro'yxati

`GET /api/v1/favorites/`

| | |
|---|---|
| **Bo'lim** | Favorites |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha |
| **Throttle** | yo'q |

## Tavsif

Autentifikatsiya qilingan foydalanuvchining saqlangan (yoqtirgan) ustalar ro'yxatini qaytaradi. Faqat o'z yozuvlari ko'rinadi — boshqa foydalanuvchilarning saqlanganlariga kirish mumkin emas. Natijalar oxirgi saqlangan birinchi bo'lib (`-created_at`) tartiblanadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 14,
      "master": {
        "id": 7,
        "name": "Bobur Yusupov",
        "avatar": "http://localhost:8000/media/avatars/bobby.jpg",
        "spec": "Santexnik",
        "city": {
          "id": 1,
          "name": "Toshkent",
          "slug": "toshkent",
          "latitude": 41.2995,
          "longitude": 69.2401
        },
        "experience_years": 5,
        "rating_avg": "4.80",
        "reviews_count": 23,
        "min_price": "50000.00",
        "status": "available",
        "is_verified": true,
        "is_top": false,
        "views_count": 312,
        "distance_km": null
      },
      "created_at": "2025-11-03T09:14:22.831Z"
    },
    {
      "id": 9,
      "master": {
        "id": 3,
        "name": "Zafar Toshmatov",
        "avatar": null,
        "spec": "Elektrik",
        "city": {
          "id": 1,
          "name": "Toshkent",
          "slug": "toshkent",
          "latitude": 41.2995,
          "longitude": 69.2401
        },
        "experience_years": 10,
        "rating_avg": "4.60",
        "reviews_count": 47,
        "min_price": "80000.00",
        "status": "busy",
        "is_verified": true,
        "is_top": true,
        "views_count": 890,
        "distance_km": null
      },
      "created_at": "2025-10-18T14:05:10.412Z"
    }
  ]
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Saqlangan yozuvning identifikatori |
| `master` | object | Usta qisqacha kartochkasi (`MasterSummarySerializer`) |
| `master.id` | integer | `MasterProfile` identifikatori |
| `master.name` | string | Ustaning to'liq ismi |
| `master.avatar` | string\|null | Avatar URL yoki `null` |
| `master.spec` | string | Mutaxassislik nomi |
| `master.city` | object | Shahar: `id`, `name`, `slug`, `latitude`, `longitude` |
| `master.experience_years` | integer | Ish tajribasi (yillarda) |
| `master.rating_avg` | string | O'rtacha reyting |
| `master.reviews_count` | integer | Sharhlar soni |
| `master.min_price` | string | Minimal narx (faqat ma'lumot, tranzaksiya yo'q) |
| `master.status` | string | Mavjudlik holati (`available`, `busy`, `inactive`) |
| `master.is_verified` | boolean | KYC tasdiqlangan |
| `master.is_top` | boolean | TOP usta belgisi |
| `master.views_count` | integer | Profilni ko'rishlar soni |
| `master.distance_km` | number\|null | Yaqinlik (yaqindagilar qidiruvida — aks holda `null`) |
| `created_at` | string (ISO 8601) | Saqlanish vaqti |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/favorites/?page=1" \
  -H "Authorization: Bearer $ACCESS"
```
