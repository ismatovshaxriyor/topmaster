# Emailni tasdiqlash

`POST /api/v1/auth/verify-email/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `email_verify`: 15/min (IP bo'yicha) |

## Tavsif

Ro'yxatdan o'tishda emailga yuborilgan **6 xonali kod**ni tekshirib, hisobni tasdiqlaydi (`email_verified=True`). Muvaffaqiyatli tasdiqlangach foydalanuvchi **darrov tizimga kiritiladi** — javobda `access` + `refresh` tokenlar va `user` (UserSummary) qaytariladi, ya'ni alohida login qilish shart emas.

Kod cache'da **15 daqiqa** saqlanadi. Tokenlar **faqat** to'g'ri kod tasdiqlanganda beriladi — "allaqachon tasdiqlangan" holatida emas (aks holda kodsiz token olish mumkin bo'lardi).

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

## Javob

### `200 OK` — tasdiqlandi (auto-login)

```json
{
  "detail": "Email muvaffaqiyatli tasdiqlandi.",
  "access": "eyJhbGciOiJIUzI1Ni...",
  "refresh": "eyJhbGciOiJIUzI1Ni...",
  "user": {
    "id": 42,
    "full_name": "Jasur Karimov",
    "role": "mijoz",
    "is_verified": false,
    "avatar": null,
    "city": {"id": 1, "name": "Toshkent", "slug": "toshkent", "latitude": 41.2995, "longitude": 69.2401}
  }
}
```

Agar email allaqachon tasdiqlangan bo'lsa (tokensiz):

```json
{ "detail": "Email allaqachon tasdiqlangan." }
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Kod noto'g'ri yoki muddati o'tgan; majburiy maydon yo'q |
| `429` | Throttle limiti oshildi (15 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify-email/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jasur@example.com",
    "code": "482913"
  }'
```
