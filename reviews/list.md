# Sharhlar ro'yxati

`GET /api/v1/reviews/`

| | |
|---|---|
| **Bo'lim** | Reviews |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Ha |
| **Throttle** | anon 60/min, user 1000/min |

## Tavsif

Barcha sharhlarni sahifalangan ro'yxat sifatida qaytaradi. Endpoint ommaviy —
autentifikatsiya talab qilinmaydi. Ro'yxatni `?master=<id>` yoki `?job=<id>`
query parametrlari orqali filtrlash mumkin; ikkalasini birgalikda ham ishlatish
mumkin.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `master` | integer | Yo'q | Faqat shu usta ID'siga tegishli sharhlarni qaytaradi |
| `job` | integer | Yo'q | Faqat shu buyurtma ID'siga tegishli sharhni qaytaradi |
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/reviews/?page=3",
  "previous": "http://localhost:8000/api/v1/reviews/?page=1",
  "results": [
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
  ]
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
| `429` | So'rovlar limiti oshib ketdi |

## Misol

```bash
# Barcha sharhlar
curl "http://localhost:8000/api/v1/reviews/"

# Bitta usta sharhlarini ko'rish
curl "http://localhost:8000/api/v1/reviews/?master=3"

# Bitta buyurtma sharhi
curl "http://localhost:8000/api/v1/reviews/?job=12"

# Sahifalash
curl "http://localhost:8000/api/v1/reviews/?master=3&page=2"
```
