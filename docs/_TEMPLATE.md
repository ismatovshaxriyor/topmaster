# Hujjat formati va konvensiyalar

Bu fayl har bir endpoint `.md` fayli uchun **majburiy shablon** va loyihaning
umumiy konvensiyalarini belgilaydi. Har bir endpoint fayli aynan shu tuzilishga
amal qilishi kerak.

## Umumiy konvensiyalar

- **Bazaviy URL:** barcha yoʻllar `/api/v1/` bilan boshlanadi.
- **Autentifikatsiya:** `Authorization: Bearer <access_token>` (ommaviy
  endpointlardan tashqari).
- **Sahifalash:** roʻyxat (list) endpointlari sahifalanadi — `?page=<n>`,
  sahifa hajmi `20`. Javob koʻrinishi:
  ```json
  { "count": 42, "next": "<url|null>", "previous": "<url|null>", "results": [ ... ] }
  ```
- **Xato formati (DRF):**
  - Umumiy: `{ "detail": "Xabar" }`
  - Maydon xatolari: `{ "field_name": ["Xabar"] }`
  - Autentifikatsiya yoʻq: `401`; ruxsat yoʻq: `403`; topilmadi: `404`;
    limitdan oshish: `429`.
- **Throttling (limit):** global `anon 60/min`, `user 1000/min`; ayrim
  endpointlarda qatʼiyroq scoped limitlar (har faylda koʻrsatiladi).
- **Toʻlov yoʻq:** narx maydonlari (`price_amount`, `proposed_price`, `min_price`)
  faqat maʼlumot; hech qanday tranzaksiya/balans yoʻq.

## Har bir endpoint fayli shabloni

````markdown
# <Inson oʻqiy oladigan sarlavha>

`<METHOD> /api/v1/<toʻliq/yoʻl>/`

| | |
|---|---|
| **Boʻlim** | <Tag, masalan: Masters> |
| **Autentifikatsiya** | <Ommaviy (AllowAny) / Bearer JWT> |
| **Ruxsat** | <IsAuthenticated / Rol: usta / Rol: mijoz / egasi / ...> |
| **Sahifalash** | <Ha / Yoʻq> |
| **Throttle** | <yoʻq / scope nomi: rate> |

## Tavsif

<Endpoint nima qilishi — 1-3 jumla. Muhim xulq-atvor, yon taʼsirlar
(masalan: hodisa yozish, bildirishnoma yuborish, hisoblagich oshirish).>

## Soʻrov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | ... |

<yoki: "Yoʻq.">

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yoʻq | Sahifa raqami |

<yoki: "Yoʻq.">

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `email` | string | Ha | ... |

<yoki: "Yoʻq.">

## Javob

### `200 OK` (yoki `201 Created`)

```json
{ ... haqiqiy serializer maydonlariga mos misol ... }
```

<Kerak boʻlsa, asosiy javob maydonlarining qisqa izohi.>

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | ... |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Ruxsat yoʻq |

## Misol

```bash
curl -X <METHOD> "http://localhost:8000/api/v1/<yoʻl>/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```
````

## Maslahatlar

- JSON misollar **haqiqiy serializer maydonlariga** asoslansin (kodni oʻqib
  tekshiring) — taxminiy maydon nomlaridan foydalanmang.
- Yon taʼsirlarni yozing: hodisa (`JobEvent`), bildirishnoma (`notify`),
  denormalizatsiya (`proposals_count`, `views_count`, `rating_avg`).
- Rol cheklovlarini aniq koʻrsating (mijoz/usta/egasi).
