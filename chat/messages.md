# Suhbat xabarlari ro'yxati

`GET /api/v1/chat/conversations/{id}/messages/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated; faqat o'zi ishtirok etadigan suhbat |
| **Sahifalash** | Ha (eng eski xabar birinchi) |
| **Throttle** | user: 1000/min |

## Tavsif

Suhbatdagi barcha xabarlarni `created_at` bo'yicha o'suvchi tartibda (eng eski birinchi) sahifalab qaytaradi. Endpoint chaqirilgan zahoti quyidagi yon ta'sirlar yuzaga keladi:

- Kiruvchi (boshqa foydalanuvchi yuborgan) va hali o'qilmagan (`read_at IS NULL`) xabarlar o'qilgan deb belgilanadi — `read_at` maydoni hozirgi vaqt bilan to'ldiriladi.
- Joriy foydalanuvchining `ConversationParticipant.unread_count` `0` ga tenglashtiriladi va `last_read_at` yangilanadi.
- `chat.read` hodisasi WebSocket guruhiga broadcast qilinadi — ikkinchi ishtirokchi o'qilganlik holatini real vaqtda ko'radi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Suhbat identifikatori |

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (default: 1) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 47,
  "next": "http://localhost:8000/api/v1/chat/conversations/12/messages/?page=3",
  "previous": "http://localhost:8000/api/v1/chat/conversations/12/messages/?page=1",
  "results": [
    {
      "id": 61,
      "sender": 3,
      "sender_name": "Alisher Umarov",
      "type": "text",
      "text": "Salom, qachon bo'sha olasiz?",
      "attachment": null,
      "created_at": "2026-06-14T08:15:00Z",
      "read_at": "2026-06-14T08:20:00Z",
      "is_mine": true
    },
    {
      "id": 62,
      "sender": 7,
      "sender_name": "Jasur Karimov",
      "type": "text",
      "text": "Ertaga ertalab.",
      "attachment": null,
      "created_at": "2026-06-14T08:30:00Z",
      "read_at": "2026-06-15T10:22:45Z",
      "is_mine": false
    }
  ]
}
```

**`MessageSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Xabar identifikatori |
| `sender` | integer | Yuboruvchi foydalanuvchi ID'si |
| `sender_name` | string | Yuboruvchining to'liq ismi (`sender.full_name`) |
| `type` | string | Xabar turi: `"text"`, `"system"`, `"file"` |
| `text` | string | Xabar matni |
| `attachment` | string\|null | Fayl URL'i (mavjud bo'lsa); aks holda `null` |
| `created_at` | datetime | Xabar yaratilgan vaqt (ISO 8601) |
| `read_at` | datetime\|null | Xabar o'qilgan vaqt; o'qilmagan bo'lsa `null` |
| `is_mine` | boolean | Xabarni joriy foydalanuvchi yuborganmi (`true`/`false`) |

**Yon ta'sirlar:**

| Ta'sir | Tavsif |
|---|---|
| `read_at` yangilanadi | Kiruvchi o'qilmagan xabarlar `read_at = now()` bilan belgilanadi |
| `unread_count = 0` | Joriy foydalanuvchining `ConversationParticipant.unread_count` nolga tenglashadi |
| `last_read_at` yangilanadi | `ConversationParticipant.last_read_at = now()` |
| WebSocket broadcast | `chat.read` hodisasi guruhga yuboriladi: `{"event": "read", "conversation_id": 12, "user_id": 3}` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Suhbat topilmadi yoki foydalanuvchi uning ishtirokchisi emas |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/chat/conversations/12/messages/" \
  -H "Authorization: Bearer $ACCESS"
```

```bash
# Ikkinchi sahifa
curl -X GET "http://localhost:8000/api/v1/chat/conversations/12/messages/?page=2" \
  -H "Authorization: Bearer $ACCESS"
```
