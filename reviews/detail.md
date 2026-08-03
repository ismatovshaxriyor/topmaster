# Sharh tafsiloti

`GET /api/v1/reviews/{id}/`

| | |
|---|---|
| **Bo'lim** | Reviews |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | anon 60/min, user 1000/min |

## Tavsif

Bitta sharhni ID bo'yicha qaytaradi. Endpoint ommaviy — autentifikatsiya talab
qilinmaydi. Javob `ReviewSerializer` formatida keladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Sharhning birlamchi kaliti |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "id": 17,
  "author": {
    "id": 5,
    "full_name": "Aziza Karimova",
    "role": "client",
    "is_verified": true,
    "avatar": "http://localhost:8000/media/avatars/aziza.jpg",
    "city": {
      "id": 1,
      "name": "Toshkent",
      "slug": "toshkent",
      "latitude": 41.2995,
      "longitude": 69.2401
    }
  },
  "master": 3,
  "rating": 5,
  "text": "Juda yaxshi usta, vaqtida keldi va sifatli ish qildi.",
  "recommend": true,
  "created_at": "2024-11-20T14:32:00Z"
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Sharh ID'si |
| `author` | object | Sharh muallifi (mijoz) — `UserSummarySerializer` |
| `author.id` | integer | Foydalanuvchi ID'si |
| `author.full_name` | string | To'liq ismi |
| `author.role` | string | Rol (`client` / `master`) |
| `author.is_verified` | boolean | Tasdiqlanganmi |
| `author.avatar` | string\|null | Avatar URL |
| `author.city` | object\|null | Shahar (`id`, `name`) |
| `master` | integer | Usta profil ID'si (FK) |
| `rating` | integer | Baho (1–5) |
| `text` | string | Sharh matni (bo'sh bo'lishi mumkin) |
| `recommend` | boolean | Ustani tavsiya qiladimi |
| `created_at` | datetime | Sharh yaratilgan vaqt (ISO 8601, UTC) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `404` | Berilgan ID bilan sharh topilmadi |
| `429` | So'rovlar limiti oshib ketdi |

## Misol

```bash
curl "http://localhost:8000/api/v1/reviews/17/"
```
