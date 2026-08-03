# FAQ mavzulari ro'yxati

`GET /api/v1/support/topics/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Ha (20 ta/sahifa) |
| **Throttle** | anon: 60/min |

## Tavsif

Barcha FAQ mavzularini (FaqTopic) ichida joylashgan FAQ yozuvlari bilan birga qaytaradi. Har bir mavzu ob'ekti `faqs` massivini o'z ichiga oladi — shu mavzuga tegishli barcha savollar ichki ko'rinishda (nested) beriladi. Natijalar `order` va `label` bo'yicha tartiblanadi.

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
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "key": "general",
      "label": "Umumiy savollar",
      "icon": "help-circle",
      "faqs": [
        {
          "id": 1,
          "question": "TopMaster nima?",
          "answer": "TopMaster — usta va mijozlarni bog'lovchi platforma.",
          "order": 0
        },
        {
          "id": 2,
          "question": "Ro'yxatdan o'tish bepulmi?",
          "answer": "Ha, ro'yxatdan o'tish mutlaqo bepul.",
          "order": 1
        }
      ]
    },
    {
      "id": 2,
      "key": "payments",
      "label": "To'lovlar",
      "icon": "credit-card",
      "faqs": []
    }
  ]
}
```

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `key` | Mavzuning noyob slug kaliti (filtrda ishlatiladi, qarang: `faqs.md`) |
| `label` | Mavzu nomi (ko'rsatish uchun) |
| `icon` | Ikonka nomi (standart: `help-circle`) |
| `faqs` | Shu mavzuga tegishli FAQ yozuvlari — bo'sh bo'lishi ham mumkin |
| `faqs[].order` | Mavzu ichida tartib raqami |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/support/topics/"
```
