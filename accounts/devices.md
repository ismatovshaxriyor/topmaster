# Qurilmalar (FCM tokenlar)

`GET    /api/v1/auth/devices/`  
`POST   /api/v1/auth/devices/`  
`GET    /api/v1/auth/devices/{id}/`  
`PUT    /api/v1/auth/devices/{id}/`  
`PATCH  /api/v1/auth/devices/{id}/`  
`DELETE /api/v1/auth/devices/{id}/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated (faqat o'z qurilmalari) |
| **Sahifalash** | Ha (`?page=<n>`, sahifa hajmi 20) |
| **Throttle** | Yo'q (global `user`: 1000/min) |

## Tavsif

Foydalanuvchining push bildirishnoma uchun ro'yxatdan o'tgan FCM qurilma tokenlarini boshqaradi. `POST` so'rovi `registration_id` bo'yicha upsert amalga oshiradi: agar token allaqachon shu foydalanuvchiga tegishli bo'lsa, yangilanadi (`200`); yangi bo'lsa, yaratiladi (`201`). Agar `registration_id` boshqa foydalanuvchiga tegishli bo'lsa, `409 Conflict` qaytariladi — bir token ikki hisobga biriktirilmaydi. `GET` (ro'yxat va detail), `PUT`, `PATCH`, `DELETE` faqat joriy foydalanuvchining o'z qurilmalariga ishlaydi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Qurilma yozuvi `id` si (detail, PUT, PATCH, DELETE uchun) |

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (faqat `GET` ro'yxat uchun) |

### Tana (request body) — POST / PUT / PATCH

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `registration_id` | string | Ha | FCM qurilma tokeni (noyob, matn) |
| `platform` | string | Yo'q | `android`, `ios`, `web` (standart: `android`) |
| `active` | boolean | Yo'q | Token faolmi (standart: `true`) |

## Javob

### `200 OK` (mavjud token yangilandi — POST upsert)

```json
{
  "id": 7,
  "registration_id": "fCm_token_xyz...",
  "platform": "android",
  "active": true
}
```

### `201 Created` (yangi qurilma qo'shildi — POST)

```json
{
  "id": 8,
  "registration_id": "fCm_token_abc...",
  "platform": "ios",
  "active": true
}
```

### `200 OK` (GET ro'yxat)

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 7,
      "registration_id": "fCm_token_xyz...",
      "platform": "android",
      "active": true
    },
    {
      "id": 6,
      "registration_id": "fCm_token_old...",
      "platform": "web",
      "active": false
    }
  ]
}
```

### `204 No Content` (DELETE)

Tana bo'sh.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `registration_id` maydoni yo'q; `platform` noto'g'ri qiymat |
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Qurilma topilmadi yoki boshqa foydalanuvchiga tegishli |
| `409` | `registration_id` boshqa foydalanuvchiga biriktirilgan |

## Misol

```bash
# Qurilma ro'yxatdan o'tkazish (upsert)
curl -X POST "http://localhost:8000/api/v1/auth/devices/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": "fCm_token_xyz...",
    "platform": "android",
    "active": true
  }'

# Qurilmalarni ko'rish
curl "http://localhost:8000/api/v1/auth/devices/" \
  -H "Authorization: Bearer $ACCESS"

# Qurilmani o'chirish
curl -X DELETE "http://localhost:8000/api/v1/auth/devices/7/" \
  -H "Authorization: Bearer $ACCESS"
```
