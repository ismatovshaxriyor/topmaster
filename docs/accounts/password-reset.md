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

Foydalanuvchi emailiga parol tiklash havolasini yuboradi. Email ma'lumotlar bazasida mavjud bo'lmasa ham har doim `200` qaytariladi — bu email manzillarini sanab chiqish (enumeration) hujumlarini oldini oladi. Agar hisob topilsa, `uid` (Base64 kodlangan `pk`) va `token` (Django standart token generatori) o'z ichiga olgan deep-link email orqali yuboriladi. Havola `settings.FRONTEND_PASSWORD_RESET_URL` ga yo'naltiriladi.

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
  "detail": "Agar hisob mavjud bo'lsa, ko'rsatmalar yuborildi."
}
```

Email hisob mavjud bo'lganda quyidagi ma'lumotlarni o'z ichiga oladi:
- To'g'ridan-to'g'ri deep-link: `{FRONTEND_PASSWORD_RESET_URL}?uid=<uid>&token=<token>`
- Ilovada qo'lda kiritish uchun `uid` va `token` alohida ko'rsatiladi

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
