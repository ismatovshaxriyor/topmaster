# Onboarding (birinchi sozlash)

`POST /api/v1/masters/me/onboarding/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Usta akkaunt yaratilgandan so'ng birinchi marta profilini to'ldirish uchun
ishlatiladi (`OnboardingSerializer`). Shahar, asosiy bio ma'lumotlar, kategoriyalar
va dastlabki ko'nikmalar bir so'rovda o'rnatiladi. Muvaffaqiyatli bo'lganda
to'liq profil (`MasterDetailSerializer`) qaytariladi.

**Yon ta'sirlar:**
- `city` berilsa — `user.city` yangilanadi.
- `category_keys` berilsa — ustaning `categories` to'plami `key` bo'yicha
  topilgan kategoriyalar bilan **to'liq almashtiriladi**.
- `skills` berilsa — har bir element uchun yangi `Skill` yaratiladi
  (`title` bo'sh bo'lsa o'tkazib yuboriladi).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `city` | integer | Yo'q | Shahar PK (null ruxsat etiladi) |
| `bio` | string | Yo'q | Usta haqida qisqacha matn |
| `experience_years` | integer | Yo'q | Tajriba yillari (≥ 0) |
| `min_price` | integer | Yo'q | Minimal narx so'mda (≥ 0) |
| `category_keys` | array[string] | Yo'q | Kategoriya `key` qiymatlari ro'yxati (slug) |
| `skills` | array[object] | Yo'q | Ko'nikmalar ro'yxati (quyida ko'ring) |

**`skills` massivi elementi:**

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `title` | string | Ha | Ko'nikma nomi (bo'sh bo'lsa o'tkazib yuboriladi) |
| `price_min` | integer | Yo'q | Minimal narx (standart: 0) |
| `price_max` | integer | Yo'q | Maksimal narx (null ruxsat etiladi) |
| `years` | integer | Yo'q | Tajriba yillari (standart: 0) |

## Javob

### `200 OK`

To'liq profil (`MasterDetailSerializer`) — `detail.md` ga qarang.

```json
{
  "id": 12,
  "name": "Jasur Karimov",
  "avatar": null,
  "spec": "Santexnik",
  "city": { "id": 1, "name": "Toshkent", "slug": "toshkent", "latitude": 41.2995, "longitude": 69.2401 },
  "experience_years": 5,
  "rating_avg": "0.00",
  "reviews_count": 0,
  "min_price": 50000,
  "status": "free",
  "is_verified": false,
  "is_top": false,
  "views_count": 0,
  "distance_km": null,
  "bio": "10 yillik tajribaga ega santexnik.",
  "categories": [
    { "id": 3, "key": "santexnik", "label": "Santexnik", "icon": null }
  ],
  "skills": [
    {
      "id": 8,
      "category": null,
      "category_label": null,
      "title": "Quvur ta'miri",
      "price_min": 40000,
      "price_max": 100000,
      "years": 3,
      "order": 0
    }
  ],
  "portfolio": [],
  "recent_reviews": []
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Validatsiya xatosi (masalan: `experience_years` manfiy qiymat) |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/masters/me/onboarding/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "city": 1,
    "bio": "10 yillik tajribaga ega santexnik.",
    "experience_years": 5,
    "min_price": 50000,
    "category_keys": ["santexnik"],
    "skills": [
      { "title": "Kran almashtirish", "price_min": 30000, "price_max": 80000, "years": 4 },
      { "title": "Quvur ta'\''miri", "price_min": 40000, "years": 3 }
    ]
  }'
```
