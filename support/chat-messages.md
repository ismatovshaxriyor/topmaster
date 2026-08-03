# Suhbat xabarlarini olish

`GET /api/v1/support/chat/messages/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha (20 ta/sahifa) |
| **Throttle** | user: 1000/min |

## Tavsif

Joriy foydalanuvchining faol threadidagi barcha xabarlarni vaqt tartibida (`created_at` o'sish tartibida) sahifalab qaytaradi. Yon ta'sir: so'rov yuborilishi bilanoq barcha o'qilmagan xodim xabarlariga `read_at` vaqt tamg'asi qo'yiladi va `user_unread` hisoblagichi nolga tushiriladi (qarang: `chat-read.md`). Agar faol thread mavjud bo'lmasa, xatosiz bo'sh sahifalangan javob qaytariladi (`count: 0`).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK` — faol thread mavjud

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "is_staff": false,
      "text": "Salom, hisobimga kirish muammosi bor.",
      "attachment": null,
      "read_at": "2026-06-14T13:05:00Z",
      "created_at": "2026-06-14T12:30:00Z"
    },
    {
      "id": 11,
      "is_staff": true,
      "text": "Salom! Qanday muammo yuzaga keldi, batafsil aytib bering.",
      "attachment": "http://localhost:8000/media/support/thread_3/screenshot.png",
      "read_at": "2026-06-15T09:05:00Z",
      "created_at": "2026-06-14T13:00:00Z"
    }
  ]
}
```

### `200 OK` — faol thread yo'q

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `is_staff` | `true` — xodim javob yozgan; `false` — foydalanuvchi yozgan |
| `text` | Xabar matni (bo'sh bo'lishi mumkin, agar `attachment` bor bo'lsa) |
| `attachment` | Fayl URL manzili yoki `null`. Fayllar `support/thread_<id>/` yo'liga saqlanadi |
| `read_at` | Xabar o'qilgan vaqt damgasi (`null` — hali o'qilmagan). Foydalanuvchi xabarlari (`is_staff: false`) uchun xodim tomonidan o'qilganini bildiradi; xodim xabarlari (`is_staff: true`) uchun foydalanuvchi tomonidan o'qilganini bildiradi |
| `created_at` | Xabar yuborilgan vaqt |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/support/chat/messages/" \
  -H "Authorization: Bearer $ACCESS"

# 2-sahifa
curl -X GET "http://localhost:8000/api/v1/support/chat/messages/?page=2" \
  -H "Authorization: Bearer $ACCESS"
```
