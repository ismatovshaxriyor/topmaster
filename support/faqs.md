# FAQ yozuvlari ro'yxati

`GET /api/v1/support/faqs/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Ha (20 ta/sahifa) |
| **Throttle** | anon: 60/min |

## Tavsif

Barcha FAQ yozuvlarini tekis ro'yxat ko'rinishida qaytaradi. Ixtiyoriy `?topic=<key>` parametri orqali faqat bitta mavzuga tegishli savollarni filtrlash mumkin. Natijalar `order` va `id` bo'yicha tartiblanadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yo'q | Sahifa raqami (standart: 1) |
| `topic` | string | Yo'q | `FaqTopic.key` qiymati — masalan, `general`, `payments`. Berilsa, faqat shu mavzudagi yozuvlar qaytariladi |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 12,
  "next": "http://localhost:8000/api/v1/support/faqs/?page=2",
  "previous": null,
  "results": [
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
}
```

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `id` | FAQ yozuvining identifikatori |
| `question` | Savol matni |
| `answer` | Javob matni (ko'p qatorli matn bo'lishi mumkin) |
| `order` | Mavzu ichida tartib raqami |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
# Barcha FAQ yozuvlari
curl -X GET "http://localhost:8000/api/v1/support/faqs/"

# Faqat "general" mavzusidagi savollar
curl -X GET "http://localhost:8000/api/v1/support/faqs/?topic=general"
```
