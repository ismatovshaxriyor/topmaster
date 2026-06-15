# Tizimdan chiqish

`POST /api/v1/auth/logout/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | Yo'q (global `user`: 1000/min) |

## Tavsif

Berilgan `refresh` tokenni blacklist'ga qo'shadi va uni haqiqiy bo'lmagan holga keltiradi. `access` token muddati tugaguncha texnik jihatdan amal qiladi, ammo qisqa muddatli (60 daqiqa) bo'lgani uchun bu amalda muammo emas. Muvaffaqiyatli chiqishda `205 Reset Content` qaytariladi — tana bo'sh.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `refresh` | string | Ha | Blacklist qilinadigan refresh token |

## Javob

### `205 Reset Content`

Tana bo'sh. Klient saqlangan tokenlarni o'chirishi va login sahifasiga yo'naltirilishi kerak.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `refresh` maydoni yo'q; token yaroqsiz yoki muddati o'tgan |
| `401` | `Authorization` sarlavhasi yo'q yoki `access` token yaroqsiz |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```
