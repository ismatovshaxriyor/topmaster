# Barcha bildirishnomalarni o'qilgan deb belgilash

`POST /api/v1/notifications/mark_all_read/`

| | |
|---|---|
| **Bo'lim** | Notifications |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Hozirda tizimga kirgan foydalanuvchining barcha o'qilmagan bildirishnomalarini bir vaqtda `read=true` holga keltiradi. Bulk `UPDATE` so'rovi orqali amalga oshiriladi. Javobda yangilangan yozuvlar soni qaytariladi; agar o'qilmagan bildirishnoma bo'lmasa, `{"updated": 0}` qaytariladi.

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
  "updated": 12
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `updated` | integer | O'qilgan deb belgilangan bildirishnomalar soni |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/notifications/mark_all_read/" \
  -H "Authorization: Bearer $ACCESS"
```
