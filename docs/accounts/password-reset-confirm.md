# Parol tiklashni tasdiqlash

`POST /api/v1/auth/password/reset/confirm/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `password_reset`: 5/min (IP bo'yicha) |

## Tavsif

Email manzil va emailga yuborilgan **6 xonali kod**ni tekshirib, yangi parol o'rnatadi. Kod noto'g'ri yoki muddati o'tgan bo'lsa `400` qaytariladi. Muvaffaqiyatli so'rovdan so'ng xavfsizlik maqsadida foydalanuvchining barcha mavjud refresh tokenlari blacklist'ga qo'shiladi (barcha qurilmalardagi sessiyalar bekor qilinadi) va kod cache'dan o'chiriladi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string (email) | Ha | Hisob email manzili |
| `code` | string | Ha | Emailga yuborilgan 6 xonali kod |
| `new_password` | string | Ha | Yangi parol — Django parol validatsiyasidan o'tadi |

## Javob

### `200 OK`

```json
{
  "detail": "Parol muvaffaqiyatli o'zgartirildi."
}
```

Yon ta'sir: foydalanuvchining barcha mavjud `OutstandingToken` lari `BlacklistedToken` jadvaliga qo'shiladi — bu barcha qurilmalarda sessiyalarni tugatan hisoblanadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Kod noto'g'ri yoki muddati o'tgan; `new_password` validatsiya talablarini qondirmaydi; majburiy maydon yo'q |
| `429` | Throttle limiti oshildi (5 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/password/reset/confirm/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jasur@example.com",
    "code": "482913",
    "new_password": "YangiXavsizParol2025!"
  }'
```
