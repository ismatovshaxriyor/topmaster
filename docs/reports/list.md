# O'z shikoyatlarim ro'yxati

`GET /api/v1/reports/`

| | |
|---|---|
| **Bo'lim** | Reports |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Ha |
| **Throttle** | report: 20/soat |

## Tavsif

Joriy foydalanuvchi tomonidan yuborilgan barcha shikoyatlarni sahifalangan
holda qaytaradi. Queryset `reporter=request.user` filtri bilan cheklangan —
boshqa foydalanuvchilarning shikoyatlariga kirish imkoni yo'q. Ro'yxat
`created_at` bo'yicha teskari tartibda saralanadi (eng yangi birinchi).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1); sahifa hajmi 20 ta |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 42,
      "target_label": "MasterProfile #7",
      "reason": "spam",
      "reason_display": "Spam / reklama",
      "description": "Profilda to'liq narx o'rniga reklama havolalari bor.",
      "status": "open",
      "status_display": "Yangi",
      "created_at": "2025-03-10T09:15:00Z"
    },
    {
      "id": 38,
      "target_label": "Job #23",
      "reason": "fraud",
      "reason_display": "Firibgarlik",
      "description": "",
      "status": "resolved",
      "status_display": "Hal qilindi",
      "created_at": "2025-02-28T17:40:00Z"
    },
    {
      "id": 31,
      "target_label": "Review #5",
      "reason": "fake",
      "reason_display": "Soxta profil / ma'lumot",
      "description": "Bu sharh to'g'ri emas.",
      "status": "dismissed",
      "status_display": "Rad etildi",
      "created_at": "2025-01-15T11:00:00Z"
    }
  ]
}
```

**Har bir element maydoni:**

| Maydon | Tavsif |
|---|---|
| `id` | Shikoyat ID'si |
| `target_label` | Shikoyat qilingan obyektning `str()` ko'rinishi |
| `reason` | Sabab kodi (`spam`, `fraud`, `inappropriate`, `fake`, `abuse`, `other`) |
| `reason_display` | Sababning o'zbek tilidagi to'liq nomi |
| `description` | Foydalanuvchi yozgan qo'shimcha tavsif (bo'sh bo'lishi mumkin) |
| `status` | Joriy holat kodi (`open`, `reviewing`, `resolved`, `dismissed`) |
| `status_display` | Holatning o'zbek tilidagi to'liq nomi |
| `created_at` | ISO 8601 formatida yaratilgan vaqt |

`target_type` va `target_id` write_only maydonlar bo'lganligi sababli javobda
qaytmaydi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `429` | So'rovlar limiti oshib ketdi (20/soat) |

## Misol

```bash
curl "http://localhost:8000/api/v1/reports/" \
  -H "Authorization: Bearer $ACCESS"
```

Ikkinchi sahifa:

```bash
curl "http://localhost:8000/api/v1/reports/?page=2" \
  -H "Authorization: Bearer $ACCESS"
```
