# Bildirishnomalar ro'yxati

`GET /api/v1/notifications/`

| | |
|---|---|
| **Bo'lim** | Notifications |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha (20 ta / sahifa) |
| **Throttle** | yo'q |

## Tavsif

Hozirda tizimga kirgan foydalanuvchining barcha bildirishnomalari sanaladi. Faqat o'z bildirishnomalari qaytariladi — boshqa foydalanuvchilarnikiga kirish imkoni yo'q. Natijalar `created_at` bo'yicha teskari tartibda (eng yangi birinchi) sahifalanib beriladi.

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

### `200 OK`

```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/notifications/?page=3",
  "previous": "http://localhost:8000/api/v1/notifications/?page=1",
  "results": [
    {
      "id": 17,
      "type": "order",
      "type_display": "Buyurtma",
      "title": "Yangi buyurtma keldi",
      "body": "Santexnika bo'yicha usta kerak",
      "data": { "job_id": 42 },
      "read": false,
      "created_at": "2026-06-15T10:23:00Z"
    },
    {
      "id": 16,
      "type": "accepted",
      "type_display": "Qabul qilindi",
      "title": "Taklifingiz qabul qilindi",
      "body": "",
      "data": { "job_id": 38, "master_id": 5 },
      "read": true,
      "created_at": "2026-06-14T18:05:11Z"
    }
  ]
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Bildirishnoma identifikatori |
| `type` | string | Bildirishnoma turi: `order`, `accepted`, `rejected`, `chat`, `system` |
| `type_display` | string | Tur inson o'qiy oladigan ko'rinishda (masalan, `"Buyurtma"`) |
| `title` | string | Sarlavha (maks. 160 belgi) |
| `body` | string | Qo'shimcha matn (maks. 400 belgi; bo'sh bo'lishi mumkin) |
| `data` | object | Chuqur havola uchun ixtiyoriy metama'lumot (masalan, `{"job_id": 42}`) |
| `read` | boolean | `true` — o'qilgan, `false` — o'qilmagan |
| `created_at` | datetime | ISO 8601 formatida yaratilgan vaqt |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/notifications/?page=1" \
  -H "Authorization: Bearer $ACCESS"
```
