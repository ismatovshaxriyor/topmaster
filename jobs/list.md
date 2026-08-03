# Buyurtmalar ro'yxati

`GET /api/v1/jobs/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha (20 ta/sahifa) |
| **Throttle** | user: 1000/min |

## Tavsif

Ochiq buyurtmalar taxtasini qaytaradi. `status` query parametri berilmasa, faqat `open` holатidagi buyurtmalar ko'rsatiladi. `?q` parametri orqali sarlavha va tavsif bo'yicha to'liq-matnli qidiruv (PostgreSQL GIN indeksi, websearch sintaksisi) amalga oshiriladi — natijalar dolzarblik tartibida (`rank DESC`) beriladi. `?lat` va `?lng` berilsa, har bir buyurtmada `distance_km` annotatsiyasi qo'shiladi va natijalar masofaga ko'ra saralanadi (koordinatlar mavjud bo'lmasa, buyurtmaning shahri koordinatlaridan foydalaniladi).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |
| `q` | string | Yo'q | To'liq-matnli qidiruv — sarlavha va tavsif bo'yicha (GIN). Websearch sintaksisi: `"aniq ibora"`, `OR`, `-istisno` |
| `lat` | float | Yo'q | Qidiruv markazi kengligi (yaqindagi buyurtmalar uchun) |
| `lng` | float | Yo'q | Qidiruv markazi uzunligi (yaqindagi buyurtmalar uchun) |
| `radius_km` | float | Yo'q | Qidiruv radiusi km da (standart: tizim sozlamasi) |
| `category` | string | Yo'q | Kategoriya kaliti (`category__key`) bo'yicha filtrlash |
| `city` | integer | Yo'q | Shahar ID si bo'yicha filtrlash |
| `price_type` | string | Yo'q | Narx turi: `fixed` yoki `negotiable` |
| `status` | string | Yo'q | Holat: `open`, `in_progress`, `awaiting_confirmation`, `completed`, `cancelled`. Berilmasa faqat `open` ko'rsatiladi |
| `urgent` | boolean | Yo'q | Shoshilinch buyurtmalar: `true` yoki `false` |
| `ordering` | string | Yo'q | Saralash: `created_at`, `-created_at`, `due_date`, `-due_date`, `price_amount`, `-price_amount`, `urgent`, `-urgent` |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 84,
  "next": "http://localhost:8000/api/v1/jobs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 12,
      "title": "Uy ta'mirlash ishlari",
      "category": {
        "id": 3,
        "key": "repair",
        "name": "Ta'mirlash"
      },
      "city": {
        "id": 1,
        "name": "Toshkent",
        "slug": "toshkent",
        "latitude": 41.2995,
        "longitude": 69.2401
      },
      "price_type": "fixed",
      "price_amount": 500000,
      "when_choice": "this_week",
      "due_date": "2026-06-20",
      "urgent": false,
      "status": "open",
      "status_display": "Ochiq",
      "proposals_count": 3,
      "created_at": "2026-06-14T10:22:00Z",
      "client": {
        "id": 7,
        "full_name": "Alisher Karimov",
        "avatar": "http://localhost:8000/media/avatars/7.jpg"
      },
      "distance_km": null
    }
  ]
}
```

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `proposals_count` | Ushbu buyurtmaga yuborilgan takliflar soni (denormalizatsiya qilingan hisoblagich) |
| `distance_km` | `?lat&lng` berilgandagina to'ldiriladi, aks holda `null` |
| `status_display` | `status` ning o'qilishi mumkin bo'lgan Uzbekcha ko'rinishi |
| `price_amount` | Faqat ma'lumot — hech qanday to'lov yoki tranzaksiya amalga oshirilmaydi |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
# Oddiy ro'yxat
curl -X GET "http://localhost:8000/api/v1/jobs/" \
  -H "Authorization: Bearer $ACCESS"

# To'liq-matnli qidiruv
curl -X GET "http://localhost:8000/api/v1/jobs/?q=uy+ta%27mirlash" \
  -H "Authorization: Bearer $ACCESS"

# Yaqindagi buyurtmalar (5 km radius)
curl -X GET "http://localhost:8000/api/v1/jobs/?lat=41.2995&lng=69.2401&radius_km=5" \
  -H "Authorization: Bearer $ACCESS"

# Kategoriya va shahar bo'yicha filtrlash
curl -X GET "http://localhost:8000/api/v1/jobs/?category=repair&city=1&status=open" \
  -H "Authorization: Bearer $ACCESS"
```
