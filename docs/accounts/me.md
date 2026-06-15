# O'z profil ma'lumotlari

`GET /api/v1/auth/me/`  
`PATCH /api/v1/auth/me/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated (faqat o'z profili) |
| **Sahifalash** | Yo'q |
| **Throttle** | Yo'q (global `user`: 1000/min) |

## Tavsif

Autentifikatsiya qilingan foydalanuvchining o'z profil ma'lumotlarini o'qish (`GET`) yoki qisman yangilash (`PATCH`) uchun ishlatiladi. `MeSerializer` shaxsiy aloqa ma'lumotlarini (email, telefon) ham qaytaradi — `UserSummarySerializer` dan farqli o'laroq. Faqat o'qiladigan maydonlar: `id`, `email`, `role`, `is_verified`, `is_master`.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body) — faqat PATCH

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `full_name` | string | Yo'q | To'liq ism (maks. 150 belgi) |
| `phone` | string | Yo'q | Telefon raqami (maks. 32 belgi) |
| `city_id` | integer | Yo'q | `City` ob'ektining `id` si (yozish uchun, o'qishda `city` obyekt ko'rinishida) |
| `avatar` | file/null | Yo'q | Profil rasmi (multipart/form-data yoki `null` — o'chirish) |

Faqat o'qiladigan maydonlarni (`id`, `email`, `role`, `is_verified`, `is_master`) yuborish e'tiborga olinmaydi.

## Javob

### `200 OK`

```json
{
  "id": 42,
  "email": "jasur@example.com",
  "full_name": "Jasur Karimov",
  "phone": "+998901234567",
  "role": "usta",
  "is_verified": true,
  "avatar": "http://localhost:8000/media/avatars/user_42/foto.jpg",
  "city": {
    "id": 1,
    "name": "Toshkent",
    "slug": "toshkent",
    "latitude": 41.2995,
    "longitude": 69.2401
  },
  "city_id": null,
  "is_master": true,
  "has_master_profile": true,
  "settings": {
    "notif_push": true,
    "notif_email": false,
    "notif_sms": true,
    "notif_promo": false,
    "language": "uz",
    "theme": "light",
    "twofa": false
  }
}
```

| Maydon | Tavsif |
|---|---|
| `id`, `email`, `role`, `is_verified`, `is_master` | Faqat o'qiladi — o'zgartirib bo'lmaydi |
| `city` | `CitySerializer` ko'rinishida: `id`, `name` (faqat o'qiladi) |
| `city_id` | Shaharni o'zgartirish uchun yoziladigan maydon (faqat PATCH) |
| `has_master_profile` | `true` — `master_profile` bog'langan ustalar uchun |
| `settings` | `UserSettingsSerializer` ko'rinishida ichki ob'ekt (faqat o'qiladi; alohida `PATCH /settings/` bilan o'zgartiriladi) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Noto'g'ri maydon qiymati (masalan, mavjud bo'lmagan `city_id`) |
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
# Profil o'qish
curl "http://localhost:8000/api/v1/auth/me/" \
  -H "Authorization: Bearer $ACCESS"

# Profil yangilash
curl -X PATCH "http://localhost:8000/api/v1/auth/me/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jasur Karimov",
    "phone": "+998901234567",
    "city_id": 2
  }'
```
