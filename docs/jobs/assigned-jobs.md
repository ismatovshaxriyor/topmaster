# Biriktirilgan ishlarni olish (Assigned Jobs)

`GET /api/v1/jobs/assigned_jobs/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated, faqat ustalar (`user.is_master`) |
| **Sahifalash** | `?page=` (20 ta element) |
| **Throttle** | Anon: -, User: 1000/min |

## Tavsif

Tizimga kirgan usta uchun uning o'ziga biriktirilgan buyurtmalar ro'yxatini qaytaradi.
Ushbu endpoint master dashboardidagi "Menga biriktirilgan ishlar" ro'yxati uchun ishlatiladi.

**Eslatma:** Usta o'zi mijoz sifatida joylagan buyurtmalarini ko'rish uchun `my_jobs/` endpointidan foydalanadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Oddiy sahifalash va filter parametrlari ishlashi mumkin.

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami |

## Javob

### `200 OK`

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 42,
      "category": {
        "id": 3,
        "name": "Santexnika",
        "icon": "wrench"
      },
      "city": {
        "id": 1,
        "name": "Toshkent",
        "slug": "tashkent"
      },
      "client": {
        "id": 10,
        "full_name": "Aziz",
        "avatar": "https://..."
      },
      "assigned_master": {
        "id": 5,
        "user_id": 99,
        "full_name": "Javohir (Siz)"
      },
      "title": "Kran oqyapdi, tuzatish kerak",
      "status": "in_progress",
      "price_type": "negotiable",
      "price_amount": null,
      "created_at": "2026-06-15T10:00:00Z"
    }
  ]
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta emas |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/jobs/assigned_jobs/" \
  -H "Authorization: Bearer $ACCESS"
```
