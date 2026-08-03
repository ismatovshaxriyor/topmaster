# Shaharlar ro'yxati

`GET /api/v1/catalog/cities/`

|                      |                    |
| -------------------- | ------------------ |
| **Bo'lim**           | Catalog            |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat**           | Hamma              |
| **Sahifalash**       | Ha                 |
| **Throttle**         | Yo'q               |

## Tavsif

Platforma xizmat ko'rsatadigan barcha shaharlar (yoki viloyatlar) ro'yxatini
qaytaradi. Endpoint ochiq — autentifikatsiya talab etilmaydi. Shaharlar
`order` bo'yicha, so'ngra `name` bo'yicha tartiblangan holda keladi.

Har bir shahar `latitude` / `longitude` (markaz koordinatalari) bilan keladi —
ular shaharlarni xaritada ko'rsatish va "yaqindagi" qidiruvni mijoz tomonida
qo'llab-quvvatlash uchun. Koordinatasi kiritilmagan shaharlarda ular `null`
bo'ladi (asosiy shaharlar seed orqali to'ldirilgan).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur     | Majburiy | Tavsif                      |
| -------- | ------- | -------- | --------------------------- |
| `page`   | integer | Yo'q     | Sahifa raqami (standart: 1) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Toshkent",
      "slug": "toshkent",
      "latitude": 41.2995,
      "longitude": 69.2401
    },
    {
      "id": 2,
      "name": "Samarqand",
      "slug": "samarqand",
      "latitude": 39.627,
      "longitude": 66.975
    }
  ]
}
```

| Maydon      | Tur          | Tavsif                                               |
| ----------- | ------------ | ---------------------------------------------------- |
| `id`        | integer      | Shaharga unikal identifikator                        |
| `name`      | string       | Shahar nomi (o'qish uchun)                           |
| `slug`      | string       | URL-moslashtirilgan nomi (unikal)                    |
| `latitude`  | number\|null | Markaz kengligi (WGS-84); kiritilmagan bo'lsa `null` |
| `longitude` | number\|null | Markaz uzunligi (WGS-84); kiritilmagan bo'lsa `null` |

### Xato javoblari

| Kod   | Sabab                           |
| ----- | ------------------------------- |
| `404` | Ko'rsatilgan sahifa mavjud emas |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/catalog/cities/" \
  -H "Accept: application/json"
```

Ikkinchi sahifani olish:

```bash
curl -X GET "http://localhost:8000/api/v1/catalog/cities/?page=2" \
  -H "Accept: application/json"
```
