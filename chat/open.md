# Suhbat ochish yoki topish

`POST /api/v1/chat/conversations/open/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Ikki foydalanuvchi o'rtasida 1:1 suhbat ochadi. Agar aynan shu ikkala foydalanuvchi va bir xil `job` bilan suhbat allaqachon mavjud bo'lsa, yangi suhbat yaratilmaydi — mavjud suhbat qaytariladi. Foydalanuvchi o'zi bilan suhbat ochishga urinsa, `400` xato qaytaradi. `job` ixtiyoriy bo'lib, suhbatni muayyan ish buyurtmasiga bog'laydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `user` | integer | Ha | Suhbat ochilayotgan ikkinchi foydalanuvchining ID'si |
| `job` | integer | Yo'q | Suhbat bog'lanadigan ish buyurtmasi ID'si |

## Javob

### `200 OK`

Mavjud yoki yangi yaratilgan suhbat `ConversationSerializer` formatida qaytariladi (har ikkala holatda ham `200`).

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
  "last_message": null,
  "unread": 0,
  "job": 5,
  "updated_at": "2026-06-15T09:00:00Z"
}
```

**Mantiq:**

1. `user == request.user` bo'lsa — `400` qaytaradi.
2. `user` ID mavjud bo'lmasa — `400` qaytaradi.
3. Aynan ikkita ishtirokchi va bir xil `job_id` bilan suhbat mavjud bo'lsa — mavjudini qaytaradi.
4. Aks holda — yangi `Conversation` va ikkita `ConversationParticipant` yaratadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `user` maydoni yo'q yoki noto'g'ri; o'zi bilan suhbat ochishga urinish (`"O'zingiz bilan suhbat ochib bo'lmaydi."`); foydalanuvchi topilmadi |
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
# Yangi suhbat yoki mavjudini qaytarish
curl -X POST "http://localhost:8000/api/v1/chat/conversations/open/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"user": 7, "job": 5}'
```

```bash
# job ko'rsatmasdan oddiy 1:1 suhbat
curl -X POST "http://localhost:8000/api/v1/chat/conversations/open/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"user": 7}'
```
