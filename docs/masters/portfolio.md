# Portfolio CRUD

`GET /api/v1/masters/me/portfolio/`  
`POST /api/v1/masters/me/portfolio/`  
`GET /api/v1/masters/me/portfolio/{id}/`  
`PUT /api/v1/masters/me/portfolio/{id}/`  
`PATCH /api/v1/masters/me/portfolio/{id}/`  
`DELETE /api/v1/masters/me/portfolio/{id}/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Ustaning portfolio elementlari ustidagi to'liq CRUD (`PortfolioViewSet`).
Rasm yuklash uchun `multipart/form-data` ishlatish kerak; rasm bo'lmasa
`application/json` ham qabul qilinadi. Yangi element yaratilganda `master`
maydoni avtomatik tizimga kirgan ustaga bog'lanadi. Fayllar
`media/portfolio/master_{id}/` katalogiga saqlanadi.

## So'rov

### Path parametrlari

`/{id}/` endpointlari uchun:

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | PortfolioItem PK |

### Query parametrlari

Yo'q.

### Tana (request body) — POST / PUT / PATCH

`Content-Type: multipart/form-data` (rasm yuklash uchun) yoki
`application/json` (rasm holda).

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `title` | string | Ha (POST/PUT) | Ish nomi (maks 140 belgi) |
| `location` | string | Yo'q | Ish joylashuvi (maks 120 belgi) |
| `completed_at` | date | Yo'q | Tugallanish sanasi (`YYYY-MM-DD`) |
| `image` | file | Yo'q | Rasm fayli (multipart); null ruxsat etiladi |
| `category` | integer\|null | Yo'q | Kategoriya PK |
| `featured` | boolean | Yo'q | Ko'zga ko'rinadigan qilish (standart: `false`) |
| `order` | integer | Yo'q | Tartib raqami (standart: 0) |

## Javob

### `200 OK` — ro'yxat (GET /me/portfolio/)

```json
[
  {
    "id": 2,
    "title": "Hammom ta'miri",
    "location": "Chilonzor, Toshkent",
    "completed_at": "2024-03-15",
    "image": "http://localhost:8000/media/portfolio/master_12/hammom.jpg",
    "category": 3,
    "featured": true,
    "order": 0
  },
  {
    "id": 3,
    "title": "Oshxona quvurlari",
    "location": "",
    "completed_at": null,
    "image": null,
    "category": null,
    "featured": false,
    "order": 1
  }
]
```

### `201 Created` — yaratish (POST)

```json
{
  "id": 4,
  "title": "Yangi loyiha",
  "location": "Yunusobod, Toshkent",
  "completed_at": "2025-10-01",
  "image": "http://localhost:8000/media/portfolio/master_12/loyiha.jpg",
  "category": 3,
  "featured": false,
  "order": 2
}
```

### `200 OK` — yangilash (PUT / PATCH)

Yangilangan `PortfolioItemSerializer` ob'ekti.

### `204 No Content` — o'chirish (DELETE)

So'rov tanasi qaytarilmaydi.

**`PortfolioItemSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | PortfolioItem PK |
| `title` | string | Ish nomi |
| `location` | string | Joylashuv (bo'sh bo'lishi mumkin) |
| `completed_at` | date\|null | Tugallanish sanasi |
| `image` | string\|null | Rasm URL si (null bo'lishi mumkin) |
| `category` | integer\|null | Kategoriya PK |
| `featured` | boolean | Ko'zga ko'rinadigan belgi |
| `order` | integer | Tartib raqami (o'sish, keyin yaratilish sanasi bo'yicha saralanadi) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `title` ko'rsatilmagan; noto'g'ri sana formati yoki fayl xatosi |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |
| `404` | Berilgan `id` bilan portfolio elementi topilmadi (yoki boshqa ustaga tegishli) |

## Misol

```bash
# Ro'yxatni olish
curl "http://localhost:8000/api/v1/masters/me/portfolio/" \
  -H "Authorization: Bearer $ACCESS"

# Rasmli yangi element yaratish (multipart)
curl -X POST "http://localhost:8000/api/v1/masters/me/portfolio/" \
  -H "Authorization: Bearer $ACCESS" \
  -F "title=Hammom ta'miri" \
  -F "location=Chilonzor, Toshkent" \
  -F "completed_at=2024-03-15" \
  -F "category=3" \
  -F "featured=true" \
  -F "order=0" \
  -F "image=@/path/to/hammom.jpg"

# Rasm olmay JSON bilan yaratish
curl -X POST "http://localhost:8000/api/v1/masters/me/portfolio/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"title": "Oshxona quvurlari", "order": 1}'

# O'chirish
curl -X DELETE "http://localhost:8000/api/v1/masters/me/portfolio/2/" \
  -H "Authorization: Bearer $ACCESS"
```
