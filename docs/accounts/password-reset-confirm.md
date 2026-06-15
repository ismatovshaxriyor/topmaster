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

`uid` va `token` (email orqali olingan) ni tekshirib, yangi parol o'rnatadi. `uid` noto'g'ri yoki `token` yaroqsiz/muddati o'tgan bo'lsa, xuddi bir xil xato qaytariladi — token yoki `uid` dan qaysi biri noto'g'ri ekanligi oshkor qilinmaydi. Muvaffaqiyatli so'rovdan so'ng xavfsizlik maqsadida foydalanuvchining barcha mavjud refresh tokenlari blacklist'ga qo'shiladi (barcha qurilmalardagi sessiyalar bekor qilinadi).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `uid` | string | Ha | Emaildagi Base64 kodlangan foydalanuvchi `pk` |
| `token` | string | Ha | Emaildagi Django token generatori tomonidan yaratilgan token |
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
| `400` | `uid` noto'g'ri; `token` yaroqsiz yoki muddati o'tgan; `new_password` validatsiya talablarini qondirmaydi; majburiy maydon yo'q |
| `429` | Throttle limiti oshildi (5 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/password/reset/confirm/" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "NDI",
    "token": "bff07c-a1b2c3d4e5f6...",
    "new_password": "YangiXavsizParol2025!"
  }'
```
