# Takliflar ro'yxati

`GET /api/v1/proposals/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha (20 ta / sahifa) |
| **Throttle** | yo'q |

## Tavsif

Joriy foydalanuvchiga ko'rinadigan barcha takliflarni qaytaradi. Ko'rinish doirasi:
foydalanuvchi taklifni ko'radi **agar** u taklif bergan usta bo'lsa **yoki** taklif
tegishli buyurtma egasi bo'lsa. `?job=<id>` query-parametri orqali bitta buyurtmaga
tegishli takliflarni filtrlash mumkin.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |
| `job` | integer | Yo'q | Buyurtma IDsi bo'yicha filtrlash |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 12,
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
  ]
}
```

**Javob maydonlari:**

| Maydon | Tavsif |
|---|---|
| `id` | Taklif IDsi |
| `job` | Buyurtma IDsi (FK) |
| `job_title` | Buyurtma sarlavhasi (denormalizatsiya) |
| `master` | Usta profili — `MasterSummarySerializer` (ichma-ich) |
| `message` | Ustaning xabari |
| `proposed_price` | Usta taklif qilgan narx (so'm); faqat ma'lumot, tranzaksiya yo'q |
| `status` | `pending` \| `accepted` \| `rejected` \| `withdrawn` |
| `status_display` | Holatning o'zbek tildagi nomi |
| `created_at` | Taklif yuborilgan vaqt (ISO 8601) |
| `responded_at` | Javob berilgan vaqt; hali javob bo'lmasa `null` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
# Barcha ko'rinadigan takliflar
curl "http://localhost:8000/api/v1/proposals/" \
  -H "Authorization: Bearer $ACCESS"

# Faqat 7-buyurtmaga tegishli takliflar
curl "http://localhost:8000/api/v1/proposals/?job=7" \
  -H "Authorization: Bearer $ACCESS"
```
