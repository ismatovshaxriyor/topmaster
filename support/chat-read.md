# Xodim xabarlarini o'qilgan deb belgilash

`POST /api/v1/support/chat/read/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Joriy foydalanuvchining faol threadidagi barcha xodim xabarlarini (`is_staff: true`, `read_at: null`) o'qilgan deb belgilaydi: har birining `read_at` maydoniga joriy vaqt qo'yiladi va thread `user_unread` hisoblagichi nolga tushiriladi. Yangilangan thread ma'lumotlarini qaytaradi. Agar foydalanuvchining faol threadi mavjud bo'lmasa, `404` qaytariladi. Ushbu operatsiya `GET chat/messages/` endpointi tomonidan ham avtomatik bajariladi — bu endpoint esa faqat alohida belgilash kerak bo'lganda (masalan, xabarlar ro'yxatini ochmasdan faqat bildirishnomani o'chirish uchun) ishlatiladi.

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
  "subject": "Profil muammosi",
  "status": "pending",
  "user_unread": 0,
  "last_message": {
    "id": 17,
    "is_staff": true,
    "text": "Muammoingiz hal qilindi, tekshirib ko'ring.",
    "attachment": null,
    "read_at": "2026-06-15T10:05:00Z",
    "created_at": "2026-06-15T09:50:00Z"
  },
  "created_at": "2026-06-14T12:30:00Z",
  "updated_at": "2026-06-15T10:05:00Z"
}
```

Yangilangan `SupportThread` ob'ekti qaytariladi. `user_unread` har doim `0` bo'ladi muvaffaqiyatli so'rovdan so'ng.

**Yon ta'sirlar:**

- Barcha `is_staff: true, read_at: null` xabarlariga hozirgi vaqt (`read_at`) qo'yiladi.
- Thread `user_unread` hisoblagichi `0` ga tushiriladi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Foydalanuvchining faol (`open`/`pending`) threadi topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/support/chat/read/" \
  -H "Authorization: Bearer $ACCESS"
```
