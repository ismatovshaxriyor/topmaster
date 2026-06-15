# O'qilmagan bildirishnomalar soni

`GET /api/v1/notifications/unread_count/`

| | |
|---|---|
| **Bo'lim** | Notifications |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Hozirda tizimga kirgan foydalanuvchining o'qilmagan bildirishnomalari sonini qaytaradi. Faqat `read=false` bo'lgan bildirishnomalar hisobga olinadi. Natija har doim butun son bo'lib, WebSocket orqali ham ushbu qiymat yangilanadi.

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
  "unread": 5
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `unread` | integer | O'qilmagan bildirishnomalar soni (noldan katta yoki teng) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/notifications/unread_count/" \
  -H "Authorization: Bearer $ACCESS"
```
