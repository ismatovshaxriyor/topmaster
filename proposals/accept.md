# Taklifni qabul qilish

`POST /api/v1/proposals/{id}/accept/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Mijoz taklifni qabul qiladi. Bir nechta yon ta'sir atomik tranzaksiya ichida
bajariladi:

1. Taklif holati `pending → accepted` ga o'tadi; `responded_at` o'rnatiladi.
2. Bir xil buyurtmadagi **barcha qolgan** `pending` takliflar `rejected` holatiga
   o'tkaziladi (bir vaqtda `responded_at` bilan).
3. `job.assigned_master` taklif bergan ustaga o'rnatiladi.
4. `job.status` `open → in_progress` ga o'tadi.
5. `JobEvent(type=ACCEPTED, actor=mijoz)` yozuvi yaratiladi.
6. Taklif bergan ustaga `type="accepted"` bildirishnomasi yuboriladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Qabul qilinadigan taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

Yangilangan taklif `ProposalSerializer` formatida qaytariladi.

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
  "status": "accepted",
  "status_display": "Qabul qilindi",
  "created_at": "2026-06-15T10:23:00Z",
  "responded_at": "2026-06-15T11:05:00Z"
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Buyurtma `open` holatida emas — `{"job": "Bu buyurtma uchun taklif qabul qilib bo'lmaydi."}` |
| `400` | Taklif `pending` holatida emas — `{"status": "Bu taklif kutilayotgan holatda emas."}` |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/proposals/15/accept/" \
  -H "Authorization: Bearer $ACCESS"
```
