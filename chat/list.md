# Suhbatlar ro'yxati

`GET /api/v1/chat/conversations/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha |
| **Throttle** | user: 1000/min |

## Tavsif

Joriy foydalanuvchining barcha suhbatlarini qaytaradi. Faqat o'zi ishtirok etadigan suhbatlar ko'rsatiladi — boshqa foydalanuvchilarniki ko'rinmaydi. Suhbatlar `updated_at` bo'yicha teskari tartibda (eng so'nggisi birinchi) sahifalanadi.

## So'rov

### Path parametrlari

Yo'q.

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
  "count": 3,
  "next": "http://localhost:8000/api/v1/chat/conversations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 12,
      "other": {
        "id": 7,
        "full_name": "Jasur Karimov",
        "role": "master",
        "is_verified": true,
        "avatar": "http://localhost:8000/media/avatars/jasur.jpg",
        "city": {
          "id": 1,
          "name": "Toshkent",
          "slug": "toshkent",
          "latitude": 41.2995,
          "longitude": 69.2401
        }
      },
      "last_message": {
        "id": 88,
        "sender": 7,
        "sender_name": "Jasur Karimov",
        "type": "text",
        "text": "Xabar qabul qilindi.",
        "attachment": null,
        "created_at": "2026-06-15T10:22:00Z",
        "read_at": "2026-06-15T10:22:45Z",
        "is_mine": false
      },
      "unread": 0,
      "job": 5,
      "updated_at": "2026-06-15T10:22:00Z"
    }
  ]
}
```

**Asosiy javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Suhbat identifikatori |
| `other` | object | Suhbatning ikkinchi ishtirokchisi (`UserSummarySerializer`) |
| `last_message` | object\|null | So'nggi xabar (`MessageSerializer`); yo'q bo'lsa `null` |
| `unread` | integer | Joriy foydalanuvchi uchun o'qilmagan xabarlar soni (`ConversationParticipant.unread_count`) |
| `job` | integer\|null | Suhbat bog'liq bo'lgan ish buyurtmasi ID'si; bog'liq bo'lmasa `null` |
| `updated_at` | datetime | So'nggi xabar yuborilgan vaqt (ISO 8601) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/chat/conversations/" \
  -H "Authorization: Bearer $ACCESS"
```
