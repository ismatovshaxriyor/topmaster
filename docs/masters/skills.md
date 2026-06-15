# Ko'nikmalar (Skills) CRUD

`GET /api/v1/masters/me/skills/`  
`POST /api/v1/masters/me/skills/`  
`GET /api/v1/masters/me/skills/{id}/`  
`PUT /api/v1/masters/me/skills/{id}/`  
`PATCH /api/v1/masters/me/skills/{id}/`  
`DELETE /api/v1/masters/me/skills/{id}/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q (DRF ModelViewSet, sahifalash o'chirilmagan) |
| **Throttle** | user: 1000/min |

## Tavsif

Ustaning ko'nikmalar ro'yxati ustidagi to'liq CRUD (`SkillViewSet`).
Ro'yxat va yaratish faqat tizimga kirgan ustaning o'z ko'nikmalariga qaratiladi
(`master.skills.all()`). Yangi ko'nikma yaratilganda `master` maydoni avtomatik
tizimga kirgan ustaga bog'lanadi (so'rov tanasida ko'rsatilmaydi).

## So'rov

### Path parametrlari

`/{id}/` endpointlari uchun:

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Skill PK |

### Query parametrlari

Yo'q.

### Tana (request body) — POST / PUT / PATCH

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `category` | integer\|null | Yo'q | Kategoriya PK (null ruxsat etiladi) |
| `title` | string | Ha (POST/PUT) | Ko'nikma nomi (maks 120 belgi) |
| `price_min` | integer | Ha (POST/PUT) | Minimal narx so'mda (≥ 0) |
| `price_max` | integer\|null | Yo'q | Maksimal narx (null ruxsat etiladi) |
| `years` | integer | Yo'q | Bu ko'nikmada tajriba yillari (standart: 0) |
| `order` | integer | Yo'q | Tartib raqami (standart: 0) |

## Javob

### `200 OK` — ro'yxat (GET /me/skills/)

```json
[
  {
    "id": 7,
    "category": 3,
    "category_label": "Santexnik",
    "title": "Kran almashtirish",
    "price_min": 30000,
    "price_max": 80000,
    "years": 4,
    "order": 0
  },
  {
    "id": 8,
    "category": null,
    "category_label": null,
    "title": "Quvur ta'miri",
    "price_min": 40000,
    "price_max": null,
    "years": 3,
    "order": 1
  }
]
```

### `201 Created` — yaratish (POST)

```json
{
  "id": 9,
  "category": 3,
  "category_label": "Santexnik",
  "title": "Bojxona ishlar",
  "price_min": 20000,
  "price_max": 50000,
  "years": 2,
  "order": 0
}
```

### `200 OK` — yangilash (PUT / PATCH)

Yangilangan `SkillSerializer` ob'ekti.

### `204 No Content` — o'chirish (DELETE)

So'rov tanasi qaytarilmaydi.

**`SkillSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Skill PK |
| `category` | integer\|null | Kategoriya PK |
| `category_label` | string\|null | Kategoriya yorlig'i (faqat o'qish) |
| `title` | string | Ko'nikma nomi |
| `price_min` | integer | Minimal narx so'mda |
| `price_max` | integer\|null | Maksimal narx (null bo'lishi mumkin) |
| `years` | integer | Tajriba yillari |
| `order` | integer | Tartib raqami (o'sish bo'yicha saralanadi) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `title` yoki `price_min` ko'rsatilmagan; validatsiya xatosi |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |
| `404` | Berilgan `id` bilan ko'nikma topilmadi (yoki boshqa ustaga tegishli) |

## Misol

```bash
# Ro'yxatni olish
curl "http://localhost:8000/api/v1/masters/me/skills/" \
  -H "Authorization: Bearer $ACCESS"

# Yangi ko'nikma yaratish
curl -X POST "http://localhost:8000/api/v1/masters/me/skills/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "category": 3,
    "title": "Kran almashtirish",
    "price_min": 30000,
    "price_max": 80000,
    "years": 4,
    "order": 0
  }'

# Qisman yangilash
curl -X PATCH "http://localhost:8000/api/v1/masters/me/skills/7/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"price_min": 35000}'

# O'chirish
curl -X DELETE "http://localhost:8000/api/v1/masters/me/skills/7/" \
  -H "Authorization: Bearer $ACCESS"
```
