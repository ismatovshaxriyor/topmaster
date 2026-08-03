# Ustani saqlash

`POST /api/v1/favorites/`

| | |
|---|---|
| **Bo'lim** | Favorites |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: mijoz (`IsClient`) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Mijoz foydalanuvchi usta profilini o'z saqlanganlari ro'yxatiga qo'shadi. So'rov **idempotent**: agar berilgan usta allaqachon saqlangan bo'lsa, mavjud yozuv qaytariladi va `200 OK` qaytariladi; yangi yozuv yaratilsa — `201 Created`. Faqat `role=mijoz` bo'lgan foydalanuvchilar ushbu endpointdan foydalanishi mumkin.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `master` | integer | Ha | Saqlanadigan `MasterProfile` ning `id` raqami |

```json
{
  "master": 7
}
```

## Javob

### `201 Created` — yangi yozuv yaratildi

```json
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
}
```

### `200 OK` — usta allaqachon saqlangan (idempotent)

Javob tuzilishi yuqoridagi `201` bilan bir xil — mavjud `SavedMaster` yozuvi qaytariladi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `master` maydoni ko'rsatilmagan yoki mavjud bo'lmagan `id` |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi roli mijoz emas (`IsClient` rad etdi) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/favorites/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"master": 7}'
```
