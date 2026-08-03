# Xabar yuborish

`POST /api/v1/chat/conversations/{id}/send/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated; faqat o'zi ishtirok etadigan suhbat |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Suhbatga yangi matnli xabar yuboradi. Xabar ma'lumotlar bazasiga saqlanadi, suhbatning `last_message` va `updated_at` maydonlari yangilanadi, ikkinchi ishtirokchining o'qilmagan xabarlar hisoblagichi oshiriladi, va bir qator real vaqt ta'sirlari yuzaga keladi:

- **`chat.message` WebSocket broadcast** — suhbatning barcha ulangan ishtirokchilariga yangi xabar haqida darhol bildiruv yuboriladi.
- **Push bildiruv (`notify`)** — ikkinchi ishtirokchiga `type="chat"` bildiruvi yuboriladi; sarlavha — jo'natuvchining ismi, tana — xabar matni (maks. 120 belgi).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Suhbat identifikatori |

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `text` | string | Ha | Xabar matni (bo'sh bo'lishi mumkin emas; bosh/oxir bo'shliqlar avtomatik tozalanadi) |

## Javob

### `201 Created`

Yangi yaratilgan xabar `MessageSerializer` formatida qaytariladi.

```json
{
  "id": 89,
  "sender": 3,
  "sender_name": "Alisher Umarov",
  "type": "text",
  "text": "Ertaga soat 10 da kelaman.",
  "attachment": null,
  "created_at": "2026-06-15T11:05:00Z",
  "read_at": null,
  "is_mine": true
}
```

**`MessageSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Xabar identifikatori |
| `sender` | integer | Yuboruvchi foydalanuvchi ID'si |
| `sender_name` | string | Yuboruvchining to'liq ismi |
| `type` | string | Xabar turi: `"text"` (bu endpoint doim `text`) |
| `text` | string | Xabar matni |
| `attachment` | null | Ushbu endpoint fayl yuklashni qo'llab-quvvatlamaydi |
| `created_at` | datetime | Xabar yaratilgan vaqt (ISO 8601) |
| `read_at` | null | Yangi yuborilgan xabar o'qilmagan bo'ladi |
| `is_mine` | boolean | Jo'natuvchi uchun har doim `true` |

**Yon ta'sirlar:**

| Ta'sir | Tavsif |
|---|---|
| `Conversation.last_message` | So'nggi xabarga ko'rsatkich yangilanadi |
| `Conversation.updated_at` | Hozirgi vaqtga yangilanadi |
| `unread_count + 1` | Ikkinchi ishtirokchining `ConversationParticipant.unread_count` bittaga oshiriladi |
| WebSocket broadcast | `chat.message` hodisasi `chat_<id>` guruhiga yuboriladi |
| Push bildiruv | Ikkinchi ishtirokchiga `type="chat"` bildiruvi yuboriladi |

**WebSocket broadcast formati:**

```json
{
  "event": "message",
  "conversation_id": 12,
  "message": { "id": 89, "sender": 3, "sender_name": "Alisher Umarov", "type": "text", "text": "Ertaga soat 10 da kelaman.", "attachment": null, "created_at": "2026-06-15T11:05:00Z", "read_at": null, "is_mine": false }
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `text` maydoni yo'q yoki bo'sh |
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Suhbat topilmadi yoki foydalanuvchi uning ishtirokchisi emas |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/chat/conversations/12/send/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ertaga soat 10 da kelaman."}'
```
