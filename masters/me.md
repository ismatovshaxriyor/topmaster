# O'z profilim (usta)

`GET /api/v1/masters/me/`  
`PATCH /api/v1/masters/me/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

`GET` — tizimga kirgan ustaning to'liq profilini `MasterDetailSerializer` orqali
qaytaradi (ro'yxat uchun ishlatiluvchi `MasterSummarySerializer` emas).
`PATCH` — ustaning o'z profilini qisman yangilaydi (`MasterProfileUpdateSerializer`).
`views_count` bu endpoint orqali oshirilmaydi (faqat ommaviy `GET /{id}/` orqali oshadi).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body) — faqat PATCH

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `bio` | string | Yo'q | Usta haqida matn |
| `experience_years` | integer | Yo'q | Tajriba yillari (≥ 0) |
| `min_price` | integer | Yo'q | Minimal buyurtma narxi so'mda (≥ 0) |
| `status` | string | Yo'q | `free` / `busy` / `off` |
| `categories` | array[integer] | Yo'q | Kategoriya PK lari ro'yxati (to'liq almashtiriladi) |
| `latitude` | number | Yo'q | Aniq joylashuv — kenglik (WGS-84) |
| `longitude` | number | Yo'q | Aniq joylashuv — uzunlik (WGS-84) |

## Javob

### `200 OK` (GET va PATCH uchun)

GET — `MasterDetailSerializer` (to'liq profil):

```json
{
  "id": 12,
  "name": "Jasur Karimov",
  "avatar": "http://localhost:8000/media/avatars/user_3/photo.jpg",
  "spec": "Santexnik",
  "city": { "id": 1, "name": "Toshkent", "slug": "toshkent", "latitude": 41.2995, "longitude": 69.2401 },
  "experience_years": 5,
  "rating_avg": "4.80",
  "reviews_count": 37,
  "min_price": 50000,
  "status": "free",
  "is_verified": true,
  "is_top": false,
  "views_count": 813,
  "distance_km": null,
  "bio": "10 yillik tajribaga ega santexnik.",
  "categories": [
    { "id": 3, "key": "santexnik", "label": "Santexnik", "icon": null }
  ],
  "skills": [
    {
      "id": 7,
      "category": 3,
      "category_label": "Santexnik",
      "title": "Kran almashtirish",
      "price_min": 30000,
      "price_max": 80000,
      "years": 4,
      "order": 0
    }
  ],
  "portfolio": [
    {
      "id": 2,
      "title": "Hammom ta'miri",
      "location": "Chilonzor, Toshkent",
      "completed_at": "2024-03-15",
      "image": "http://localhost:8000/media/portfolio/master_12/hammom.jpg",
      "category": 3,
      "featured": true,
      "order": 0
    }
  ],
  "recent_reviews": [
    {
      "author_name": "Bobur T.",
      "rating": 5,
      "text": "Juda tez va sifatli ish qildi.",
      "created_at": "2025-11-20T14:30:00Z"
    }
  ]
}
```

PATCH — yangilangandan so'ng ham xuddi shu `MasterDetailSerializer` javob qaytariladi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Maydon validatsiya xatosi |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
# GET — o'z profilini olish
curl "http://localhost:8000/api/v1/masters/me/" \
  -H "Authorization: Bearer $ACCESS"

# PATCH — bio va narxni yangilash
curl -X PATCH "http://localhost:8000/api/v1/masters/me/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Yangi bio matni.",
    "min_price": 60000,
    "categories": [3, 5]
  }'
```
