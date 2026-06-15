# Hujjat formati va konvensiyalar

Bu fayl har bir endpoint `.md` fayli uchun **majburiy shablon** va loyihaning
umumiy konvensiyalarini belgilaydi. Har bir endpoint fayli aynan shu tuzilishga
amal qilishi kerak.

## Umumiy konvensiyalar

- **Bazaviy URL:** barcha yo'llar `/api/v1/` bilan boshlanadi.
- **Autentifikatsiya:** `Authorization: Bearer <access_token>` (ommaviy
  endpointlardan tashqari).
- **Sahifalash:** ro'yxat (list) endpointlari sahifalanadi — `?page=<n>`,
  sahifa hajmi `20`. Javob ko'rinishi:
  ```json
  { "count": 42, "next": "<url|null>", "previous": "<url|null>", "results": [ ... ] }
  ```
- **Xato formati (DRF):**
  - Umumiy: `{ "detail": "Xabar" }`
  - Maydon xatolari: `{ "field_name": ["Xabar"] }`
  - Autentifikatsiya yo'q: `401`; ruxsat yo'q: `403`; topilmadi: `404`;
    limitdan oshish: `429`.
- **Throttling (limit):** global `anon 60/min`, `user 1000/min`; ayrim
  endpointlarda qatʼiyroq scoped limitlar (har faylda ko'rsatiladi).
- **To'lov yo'q:** narx maydonlari (`price_amount`, `proposed_price`, `min_price`)
  faqat maʼlumot; hech qanday tranzaksiya/balans yo'q.

## Har bir endpoint fayli shabloni

````markdown
# <Inson o'qiy oladigan sarlavha>

`<METHOD> /api/v1/<to'liq/yo'l>/`

|                      |                                                          |
| -------------------- | -------------------------------------------------------- |
| **Bo'lim**           | <Tag, masalan: Masters>                                  |
| **Autentifikatsiya** | <Ommaviy (AllowAny) / Bearer JWT>                        |
| **Ruxsat**           | <IsAuthenticated / Rol: usta / Rol: mijoz / egasi / ...> |
| **Sahifalash**       | <Ha / Yo'q>                                              |
| **Throttle**         | <yo'q / scope nomi: rate>                                |

## Tavsif

<Endpoint nima qilishi — 1-3 jumla. Muhim xulq-atvor, yon taʼsirlar
(masalan: hodisa yozish, bildirishnoma yuborish, hisoblagich oshirish).>

## So'rov

### Path parametrlari

| Parametr | Tur     | Tavsif |
| -------- | ------- | ------ |
| `id`     | integer | ...    |

<yoki: "Yo'q.">

### Query parametrlari

| Parametr | Tur     | Majburiy | Tavsif        |
| -------- | ------- | -------- | ------------- |
| `page`   | integer | Yo'q     | Sahifa raqami |

<yoki: "Yo'q.">

### Tana (request body)

| Maydon  | Tur    | Majburiy | Tavsif |
| ------- | ------ | -------- | ------ |
| `email` | string | Ha       | ...    |

<yoki: "Yo'q.">

## Javob

### `200 OK` (yoki `201 Created`)

```json
{ ... haqiqiy serializer maydonlariga mos misol ... }
```

<Kerak bo'lsa, asosiy javob maydonlarining qisqa izohi.>

### Xato javoblari

| Kod   | Sabab                           |
| ----- | ------------------------------- |
| `400` | ...                             |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Ruxsat yo'q                     |

## Misol

```bash
curl -X <METHOD> "http://localhost:8000/api/v1/<yo'l>/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```
````

## Maslahatlar

- JSON misollar **haqiqiy serializer maydonlariga** asoslansin (kodni o'qib
  tekshiring) — taxminiy maydon nomlaridan foydalanmang.
- Yon taʼsirlarni yozing: hodisa (`JobEvent`), bildirishnoma (`notify`),
  denormalizatsiya (`proposals_count`, `views_count`, `rating_avg`).
- Rol cheklovlarini aniq ko'rsating (mijoz/usta/egasi).
