# Faol suhbat threadini olish

`GET /api/v1/support/chat/thread/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Joriy foydalanuvchining faol qo'llab-quvvatlash threadini qaytaradi. Faol thread — `open` yoki `pending` holatidagi eng so'nggi thread hisoblanadi. Agar bunday thread mavjud bo'lmasa, yangi `open` holатidagi thread avtomatik tarzda yaratiladi va qaytariladi. Qo'llab-quvvatlash jamoasi foydalanuvchi tomonidan yuborilgan xabarlarga Django admin paneli orqali javob beradi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "id": 3,
  "subject": "To'lov haqida savol",
  "status": "pending",
  "user_unread": 1,
  "last_message": {
    "id": 17,
    "is_staff": true,
    "text": "Salom! Savolingizni aniqroq yozib bersangiz yordam beramiz.",
    "attachment": null,
    "read_at": null,
    "created_at": "2026-06-15T09:00:00Z"
  },
  "created_at": "2026-06-14T12:30:00Z",
  "updated_at": "2026-06-15T09:00:00Z"
}
```

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `id` | Thread identifikatori |
| `subject` | Murojaat mavzusi (ixtiyoriy, bo'sh bo'lishi mumkin) |
| `status` | Thread holati: `open` — qo'llab-quvvatlash javobi kutilmoqda; `pending` — foydalanuvchi javobi kutilmoqda; `resolved` — hal qilindi; `closed` — yopilgan |
| `user_unread` | Foydalanuvchi ko'rmagan xodim xabarlarining soni (denormalizatsiya qilingan hisoblagich) |
| `last_message` | Threaddagi oxirgi xabar (`SupportMessageSerializer`); hech qanday xabar bo'lmasa `null` |
| `last_message.is_staff` | `true` — xodim javob yozgan; `false` — foydalanuvchi yozgan |
| `last_message.read_at` | Foydalanuvchi xabarni o'qigan vaqti (`null` — hali o'qilmagan) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/support/chat/thread/" \
  -H "Authorization: Bearer $ACCESS"
```
