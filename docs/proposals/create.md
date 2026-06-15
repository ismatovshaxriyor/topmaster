# Taklif yuborish

`POST /api/v1/proposals/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Usta mijozning ochiq buyurtmasiga taklif yuboradi. So'rov muvaffaqiyatli
bo'lganda bir nechta yon ta'sir yuz beradi:

1. `job.proposals_count` 1 ga oshiriladi (atomik `F()` yangilanish).
2. Buyurtma egasi (mijoz)ga `type="order"` bildirishnomasi yuboriladi.

**Cheklovlar:**
- Faqat `status=open` bo'lgan buyurtmalarga taklif berish mumkin.
- Har bir usta bitta buyurtmaga faqat bitta taklif bera oladi
  (`uniq_proposal_per_master` constraint).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `job` | integer | Ha | Buyurtma IDsi |
| `message` | string | Yo'q | Ustaning xabari / tavsifi |
| `proposed_price` | integer | Yo'q | Taklif qilingan narx (so'm); faqat ma'lumot |

## Javob

### `201 Created`

Yaratilgan taklif to'liq `ProposalSerializer` formatida qaytariladi.

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
| `400` | `job` ochiq emas — `{"job": "Bu buyurtma takliflar uchun ochiq emas."}` |
| `400` | Takroriy taklif — `{"job": "Siz ushbu buyurtmaga allaqachon taklif yuborgansiz."}` |
| `400` | Majburiy maydon yo'q (`job`) |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta emas |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/proposals/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "job": 7,
    "message": "Men bu ishni bajarishga tayyorman.",
    "proposed_price": 120000
  }'
```
