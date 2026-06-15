# Parol tiklash so'rovi

`POST /api/v1/auth/password/reset/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `password_reset`: 5/min (IP bo'yicha) |

## Tavsif

Foydalanuvchi emailiga parol tiklash uchun **6 xonali kod** yuboradi. Email ma'lumotlar bazasida mavjud bo'lmasa ham har doim `200` qaytariladi — bu email manzillarini sanab chiqish (enumeration) hujumlarini oldini oladi. Agar hisob topilsa, kod generatsiya qilinib cache'da **15 daqiqa** saqlanadi va brendlangan HTML email orqali yuboriladi (Celery, async). Kod bilan tiklashni yakunlash uchun `POST /auth/password/reset/confirm/` ga murojaat qiling.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string (email) | Ha | Hisob bilan bog'liq email manzil |

## Javob

### `200 OK`

```json
{
  "detail": "Agar hisob mavjud bo'lsa, kod yuborildi."
}
```

Hisob mavjud bo'lganda emailga 6 xonali kod yuboriladi (15 daqiqa amal qiladi).

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `email` maydoni yo'q yoki noto'g'ri format |
| `429` | Throttle limiti oshildi (5 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/password/reset/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jasur@example.com"
  }'
```
