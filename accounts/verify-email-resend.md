# Tasdiqlash kodini qayta yuborish

`POST /api/v1/auth/verify-email/resend/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `email_verify`: 15/min (IP bo'yicha) |

## Tavsif

Tasdiqlanmagan hisob uchun **yangi 6 xonali kod** generatsiya qilib emailga yuboradi (eski kod almashtiriladi). Email enumeration'ning oldini olish uchun **har doim `200`** qaytaradi — agar email mavjud bo'lmasa yoki allaqachon tasdiqlangan bo'lsa, hech qanday xat yuborilmaydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string (email) | Ha | Hisob email manzili |

## Javob

### `200 OK`

```json
{ "detail": "Agar hisob mavjud va tasdiqlanmagan bo'lsa, kod yuborildi." }
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `email` maydoni yo'q yoki noto'g'ri format |
| `429` | Throttle limiti oshildi (15 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify-email/resend/" \
  -H "Content-Type: application/json" \
  -d '{ "email": "jasur@example.com" }'
```
