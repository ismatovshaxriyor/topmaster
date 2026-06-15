# Suhbat tafsiloti

`GET /api/v1/chat/conversations/{id}/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated; faqat o'zi ishtirok etadigan suhbat |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Bitta suhbat haqida to'liq ma'lumot qaytaradi. Foydalanuvchi ushbu suhbatning ishtirokchisi bo'lmasa, `404` qaytaradi (queryset faqat o'z suhbatlarini filtrlaydi).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Suhbat identifikatori |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
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
  "unread": 2,
  "job": 5,
  "updated_at": "2026-06-15T10:22:00Z"
}
```

**Asosiy javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Suhbat identifikatori |
| `other` | object | Suhbatning ikkinchi ishtirokchisi (`UserSummarySerializer`) |
| `last_message` | object\|null | So'nggi xabar (`MessageSerializer`); yo'q bo'lsa `null` |
| `unread` | integer | Joriy foydalanuvchi uchun o'qilmagan xabarlar soni |
| `job` | integer\|null | Suhbat bog'liq bo'lgan ish buyurtmasi ID'si; bog'liq bo'lmasa `null` |
| `updated_at` | datetime | So'nggi yangilanish vaqti (ISO 8601) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Suhbat topilmadi yoki foydalanuvchi uning ishtirokchisi emas |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/chat/conversations/12/" \
  -H "Authorization: Bearer $ACCESS"
```
