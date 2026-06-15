# Ustalar ro'yxati

`GET /api/v1/masters/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hech kim (ochiq) |
| **Sahifalash** | Ha |
| **Throttle** | anon: 60/min, user: 1000/min |

## Tavsif

Barcha ustalarning ommaviy katalogini sahifalab qaytaradi. `MasterSummarySerializer`
ishlatiladi. `?q` parametri to'liq matnli qidiruv o'tkazadi (ism, bio, yo'nalish
yorlig'i, ko'nikma sarlavhasi bo'yicha). `?lat&lng` parametrlari yaqindagi ustalarni
masofaga qarab saralaydi — aniq koordinatalar bo'lmasa, usta shahri koordinatalariga
murojaat qilinadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |
| `city` | integer | Yo'q | Shahar ID si bo'yicha filtrlash (`user__city_id`) |
| `category` | string | Yo'q | Kategoriya `key` qiymatiga filtrlash |
| `status` | string | Yo'q | Holat: `free` / `busy` / `off` |
| `verified` | boolean | Yo'q | `true` — faqat tasdiqlangan ustalar |
| `top` | boolean | Yo'q | `true` — faqat top ustalar |
| `rating_min` | number | Yo'q | Minimal reyting (masalan: `4.0`) |
| `q` | string | Yo'q | To'liq matnli qidiruv: ism, bio, yo'nalish, ko'nikma |
| `lat` | number | Yo'q | Qidiruv markazi — kenglik (WGS-84) |
| `lng` | number | Yo'q | Qidiruv markazi — uzunlik (WGS-84) |
| `radius_km` | number | Yo'q | Qidiruv radiusi km da (standart server tomonidan belgilanadi) |
| `ordering` | string | Yo'q | Saralash maydoni: `rating_avg`, `-rating_avg`, `reviews_count`, `-reviews_count`, `min_price`, `-min_price`, `experience_years`, `-experience_years` |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 84,
  "next": "http://localhost:8000/api/v1/masters/?page=2",
  "previous": null,
  "results": [
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
      "views_count": 812,
      "distance_km": 2.3
    }
  ]
}
```

**Asosiy maydonlar:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | MasterProfile PK |
| `name` | string | `user.full_name` |
| `avatar` | string\|null | Foydalanuvchi avatarining mutlaq URL si |
| `spec` | string | Birinchi kategoriya yorlig'i (bo'sh bo'lishi mumkin) |
| `city` | object\|null | `{id, name, slug, latitude, longitude}` |
| `experience_years` | integer | Tajriba yillari |
| `rating_avg` | string | O'rtacha reyting (0.00–5.00) |
| `reviews_count` | integer | Sharhlar soni (denormallashtirilgan) |
| `min_price` | integer | Minimal narx (so'm) |
| `status` | string | `free` / `busy` / `off` |
| `is_verified` | boolean | Hujjatlar tasdiqlangan |
| `is_top` | boolean | Reklamalangan / tanlab olingan |
| `views_count` | integer | Profil ko'rishlar soni (denormallashtirilgan) |
| `distance_km` | number\|null | `?lat&lng` so'rovida hisoblanadi; aks holda `null` |

**`?q` ishlatilganda** saralash tartibiga e'tibor bering: avval `is_top=true`,
keyin matnli qidiruv reytingi, so'ng `rating_avg` bo'yicha kamayish tartibida.

**`?lat&lng` ishlatilganda** natijalar masofaga qarab saralanadi va har bir
elementda `distance_km` qiymati to'ldiriladi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `429` | So'rovlar limitidan oshib ketdi |

## Misol

```bash
# Oddiy ro'yxat
curl "http://localhost:8000/api/v1/masters/"

# Filtrlash: Toshkentdagi bo'sh, tasdiqlangan ustalar, reyting >= 4
curl "http://localhost:8000/api/v1/masters/?city=1&status=free&verified=true&rating_min=4"

# To'liq matnli qidiruv
curl "http://localhost:8000/api/v1/masters/?q=santexnik"

# Yaqindagi ustalar (2 km radius)
curl "http://localhost:8000/api/v1/masters/?lat=41.299&lng=69.240&radius_km=2"
```
