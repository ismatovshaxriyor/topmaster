# Shaharlar roʻyxati

`GET /api/v1/catalog/cities/`

| | |
|---|---|
| **Boʻlim** | Catalog |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Ha |
| **Throttle** | Yoʻq |

## Tavsif

Platforma xizmat koʻrsatadigan barcha shaharlar (yoki viloyatlar) roʻyxatini
qaytaradi. Endpoint ochiq — autentifikatsiya talab etilmaydi. Shaharlar
`order` boʻyicha, soʻngra `name` boʻyicha tartiblangan holda keladi.

Har bir shahar `latitude` / `longitude` (markaz koordinatalari) bilan keladi —
ular shaharlarni xaritada koʻrsatish va "yaqindagi" qidiruvni mijoz tomonida
qoʻllab-quvvatlash uchun. Koordinatasi kiritilmagan shaharlarda ular `null`
boʻladi (asosiy shaharlar seed orqali toʻldirilgan).

## Soʻrov

### Path parametrlari

Yoʻq.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `page` | integer | Yoʻq | Sahifa raqami (standart: 1) |

### Tana (request body)

Yoʻq.

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

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Shaharga unikal identifikator |
| `name` | string | Shahar nomi (oʻqish uchun) |
| `slug` | string | URL-moslashtirilgan nomi (unikal) |
| `latitude` | number\|null | Markaz kengligi (WGS-84); kiritilmagan boʻlsa `null` |
| `longitude` | number\|null | Markaz uzunligi (WGS-84); kiritilmagan boʻlsa `null` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `404` | Koʻrsatilgan sahifa mavjud emas |

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
