# Bildirishnomani o'qilgan deb belgilash

`POST /api/v1/notifications/{id}/mark_read/`

| | |
|---|---|
| **Bo'lim** | Notifications |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated; faqat bildirishnoma egasi |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Bitta bildirishnomani `read=true` holga keltiradi. Agar bildirishnoma allaqachon o'qilgan bo'lsa, hech qanday o'zgarish amalga oshirilmaydi, lekin so'rov muvaffaqiyatli qaytariladi. DRF `get_object()` orqali so'ralgan `{id}` foydalanuvchining o'z bildirishnomalariga tegishli ekanligini tekshiradi — boshqaning bildirishnomasiga `404` qaytariladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Bildirishnoma identifikatori |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

O'qilgan (yoki avval ham o'qilgan) bildirishnomaning to'liq serializer ko'rinishi qaytariladi.

```json
{
  "id": 17,
  "type": "order",
  "type_display": "Buyurtma",
  "title": "Yangi buyurtma keldi",
  "body": "Santexnika bo'yicha usta kerak",
  "data": { "job_id": 42 },
  "read": true,
  "created_at": "2026-06-15T10:23:00Z"
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Bildirishnoma topilmadi yoki foydalanuvchiga tegishli emas |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/notifications/17/mark_read/" \
  -H "Authorization: Bearer $ACCESS"
```
