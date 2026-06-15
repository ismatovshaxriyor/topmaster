# Ro'yxatdan o'tish

`POST /api/v1/auth/register/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | `register`: 5/min (IP bo'yicha) |

## Tavsif

Yangi foydalanuvchi hisobi yaratadi. `role` maydoni `mijoz` (standart) yoki `usta` bo'lishi mumkin. Agar `role=usta` bo'lsa, avtomatik ravishda `MasterProfile`, `VerificationRequest` (holati `none`) va to'rtta `VerificationDocument` (ID, selfie, diploma, manzil) yaratiladi. Javob `UserSummarySerializer` ko'rinishida qaytadi — shaxsiy aloqa ma'lumotlari (email, telefon) kiritilmagan.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string | Ha | Noyob email manzil |
| `password` | string | Ha | Django parol validatsiyasidan o'tadi |
| `full_name` | string | Yo'q | To'liq ism (maks. 150 belgi) |
| `phone` | string | Yo'q | Telefon raqami (maks. 32 belgi) |
| `city` | integer | Yo'q | `City` ob'ektining `id` si |
| `role` | string | Yo'q | `mijoz` yoki `usta` (standart: `mijoz`) |

## Javob

### `201 Created`

```json
{
  "id": 42,
  "full_name": "Jasur Karimov",
  "role": "usta",
  "is_verified": false,
  "avatar": null,
  "city": {
    "id": 1,
    "name": "Toshkent",
    "slug": "toshkent",
    "latitude": 41.2995,
    "longitude": 69.2401
  }
}
```

Javob `UserSummarySerializer` maydonlarini o'z ichiga oladi: `id`, `full_name`, `role`, `is_verified`, `avatar`, `city`. Email va telefon raqami qaytarilmaydi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Email allaqachon mavjud; parol validatsiya talablarini qondirmaydi; `role` noto'g'ri qiymat |
| `429` | Throttle limiti oshildi (5 so'rov/daqiqa) |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jasur@example.com",
    "password": "Quvvat2024!",
    "full_name": "Jasur Karimov",
    "phone": "+998901234567",
    "city": 1,
    "role": "usta"
  }'
```
