# Tizimga kirish

`POST /api/v1/auth/login/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `login`: 10/min (IP bo'yicha) |

## Tavsif

Email va parol orqali JWT token juftini oladi. Javob `access`, `refresh` tokenlar va foydalanuvchining `UserSummarySerializer` ko'rinishidagi ma'lumotlarini o'z ichiga oladi. SimpleJWT sozlamasiga ko'ra `UPDATE_LAST_LOGIN=True` — har muvaffaqiyatli kirishda `last_login` yangilanadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string | Ha | Ro'yxatdan o'tilgan email manzil |
| `password` | string | Ha | Hisob paroli |

## Javob

### `200 OK`

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 42,
    "full_name": "Jasur Karimov",
    "role": "usta",
    "is_verified": true,
    "avatar": "http://localhost:8000/media/avatars/user_42/foto.jpg",
    "city": {
      "id": 1,
      "name": "Toshkent",
      "slug": "toshkent",
      "latitude": 41.2995,
      "longitude": 69.2401
    }
  }
}
```

| Maydon | Tavsif |
|---|---|
| `access` | Qisqa muddatli JWT (standart: 60 daqiqa) — `Authorization: Bearer <access>` sifatida yuboriladi |
| `refresh` | Uzoq muddatli JWT (standart: 14 kun) — yangi `access` olish yoki logout uchun ishlatiladi |
| `user` | `UserSummarySerializer`: `id`, `full_name`, `role`, `is_verified`, `avatar`, `city` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Email yoki parol noto'g'ri; majburiy maydon yo'q |
| `401` | Hisob faol emas |
| `429` | Throttle limiti oshildi (10 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jasur@example.com",
    "password": "Quvvat2024!"
  }'
```
