# Parol o'zgartirish

`POST /api/v1/auth/password/change/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | Yo'q (global `user`: 1000/min) |

## Tavsif

Autentifikatsiya qilingan foydalanuvchi joriy parolini tasdiqlab, yangi parol o'rnatadi. `old_password` noto'g'ri bo'lsa, `400` xatosi qaytariladi. `new_password` Django'ning standart parol validatsiyasidan o'tadi. Muvaffaqiyatli so'rovdan so'ng mavjud sessiyalar (refresh tokenlar) bekor qilinmaydi — agar bu talab bo'lsa, foydalanuvchi qo'lda logout qilishi kerak.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `old_password` | string | Ha | Joriy (amaldagi) parol |
| `new_password` | string | Ha | Yangi parol — Django parol validatsiyasidan o'tadi |

## Javob

### `200 OK`

```json
{
  "detail": "Parol muvaffaqiyatli yangilandi."
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `old_password` noto'g'ri; `new_password` validatsiya talablarini qondirmaydi; majburiy maydon yo'q |
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/password/change/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "Quvvat2024!",
    "new_password": "YangiParo1_2025!"
  }'
```
