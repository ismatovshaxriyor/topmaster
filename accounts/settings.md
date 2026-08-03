# Foydalanuvchi sozlamalari

`GET /api/v1/auth/settings/`  
`PATCH /api/v1/auth/settings/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | Yo'q (global `user`: 1000/min) |

## Tavsif

Autentifikatsiya qilingan foydalanuvchining bildirishnoma va interfeys sozlamalarini (`UserSettings`) o'qish yoki qisman yangilash. `UserSettings` ob'ekti mavjud bo'lmasa, so'rov paytida avtomatik yaratiladi (`get_or_create`).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body) — faqat PATCH

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `notif_push` | boolean | Yo'q | Push bildirishnomalari (standart: `true`) |
| `notif_email` | boolean | Yo'q | Email bildirishnomalari (standart: `false`) |
| `notif_sms` | boolean | Yo'q | SMS bildirishnomalari (standart: `true`) |
| `notif_promo` | boolean | Yo'q | Reklama va aksiya bildirishnomalari (standart: `false`) |
| `language` | string | Yo'q | Interfeys tili: `uz`, `ru`, `en` (standart: `uz`) |
| `theme` | string | Yo'q | Mavzu: `light`, `dark` (standart: `light`) |
| `twofa` | boolean | Yo'q | Ikki bosqichli autentifikatsiya (standart: `false`) |

## Javob

### `200 OK`

```json
{
  "notif_push": true,
  "notif_email": false,
  "notif_sms": true,
  "notif_promo": false,
  "language": "uz",
  "theme": "light",
  "twofa": false
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `language` yoki `theme` uchun noto'g'ri qiymat |
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
# Sozlamalarni o'qish
curl "http://localhost:8000/api/v1/auth/settings/" \
  -H "Authorization: Bearer $ACCESS"

# Sozlamalarni yangilash
curl -X PATCH "http://localhost:8000/api/v1/auth/settings/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "ru",
    "theme": "dark",
    "notif_push": false
  }'
```
