# Taklifni rad etish

`POST /api/v1/proposals/{id}/reject/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Mijoz bitta taklifni rad etadi. Yon ta'sirlar:

1. Taklif holati `pending → rejected` ga o'tadi; `responded_at` o'rnatiladi.
2. Taklif bergan ustaga `type="rejected"` bildirishnomasi yuboriladi.

`accept` action'idan farqli o'laroq, bu yerda buyurtma holati (`job.status`) va
boshqa takliflar o'zgarmaydi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Rad etiladigan taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

Yangilangan taklif `ProposalSerializer` formatida qaytariladi.

```json
{
  "id": 16,
  "job": 7,
  "job_title": "Santexnik kerak",
  "master": {
    "id": 5,
    "name": "Bobur Yusupov",
    "avatar": null,
    "spec": "Santexnik",
    "city": {"id": 1, "name": "Toshkent", "slug": "toshkent", "latitude": 41.2995, "longitude": 69.2401},
    "experience_years": 2,
    "rating_avg": "4.20",
    "reviews_count": 8,
    "min_price": 40000,
    "status": "active",
    "is_verified": false,
    "is_top": false,
    "views_count": 55,
    "distance_km": null
  },
  "message": "Bugun kelishim mumkin.",
  "proposed_price": 100000,
  "status": "rejected",
  "status_display": "Rad etildi",
  "created_at": "2026-06-15T10:30:00Z",
  "responded_at": "2026-06-15T11:10:00Z"
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Taklif `pending` holatida emas — `{"status": "Bu taklif kutilayotgan holatda emas."}` |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/proposals/16/reject/" \
  -H "Authorization: Bearer $ACCESS"
```
