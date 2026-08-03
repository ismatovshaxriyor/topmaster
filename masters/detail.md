# Usta profili (batafsil)

`GET /api/v1/masters/{id}/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hech kim (ochiq) |
| **Sahifalash** | Yo'q |
| **Throttle** | anon: 60/min, user: 1000/min |

## Tavsif

Bitta ustaning to'liq profilini qaytaradi (`MasterDetailSerializer`). Kategoriyalar,
ko'nikmalar, portfolio va so'nggi 5 ta sharh kiritilgan. **Yon ta'sir:** har bir
muvaffaqiyatli so'rovda `views_count` maydoniga `+1` qo'shiladi (veritabaga
atomik `UPDATE` orqali).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | MasterProfile PK |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "id": 12,
  "name": "Jasur Karimov",
  "avatar": "http://localhost:8000/media/avatars/user_3/photo.jpg",
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
  "reviews_count": 37,
  "min_price": 50000,
  "status": "free",
  "is_verified": true,
  "is_top": false,
  "views_count": 813,
  "distance_km": null,
  "bio": "10 yillik tajribaga ega santexnik. Toshkent va viloyatlarda xizmat ko'rsataman.",
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

**`MasterDetailSerializer` qo'shimcha maydonlari (`MasterSummarySerializer`ga nisbatan):**

| Maydon | Tur | Tavsif |
|---|---|---|
| `bio` | string | Usta haqida matn (bo'sh bo'lishi mumkin) |
| `categories` | array | `CategorySerializer` — `{id, key, label, icon}` |
| `skills` | array | `SkillSerializer` ro'yxati |
| `portfolio` | array | `PortfolioItemSerializer` ro'yxati |
| `recent_reviews` | array | So'nggi 5 ta sharh: `{author_name, rating, text, created_at}` |

**Yon ta'sir:** `views_count` qiymati bu so'rovdan so'ng `+1` oshadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `404` | Berilgan `id` bilan usta topilmadi |
| `429` | So'rovlar limitidan oshib ketdi |

## Misol

```bash
curl "http://localhost:8000/api/v1/masters/12/"
```
