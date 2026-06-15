# Xizmat kategoriyalari ro'yxati

`GET /api/v1/catalog/categories/`

|                      |                    |
| -------------------- | ------------------ |
| **Bo'lim**           | Catalog            |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat**           | Hamma              |
| **Sahifalash**       | Ha                 |
| **Throttle**         | Yo'q               |

## Tavsif

Faol xizmat yo'nalishlari (kategoriyalar) ro'yxatini qaytaradi. Faqat
`is_active=True` bo'lgan yozuvlar chiqariladi — nofaol kategoriyalar
filtrdan o'tkaziladi. Kategoriyalar `order` bo'yicha, so'ngra `label`
bo'yicha tartiblangan. `icon` maydoni frontend tomonida Lucide ikonkasining
nomini saqlaydi.

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
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "key": "elektrik",
      "label": "Elektrik",
      "icon": "zap"
    },
    {
      "id": 2,
      "key": "santexnik",
      "label": "Santexnik",
      "icon": "droplets"
    },
    {
      "id": 3,
      "key": "duradgor",
      "label": "Duradgor",
      "icon": "wrench"
    }
  ]
}
```

| Maydon  | Tur     | Tavsif                                                                     |
| ------- | ------- | -------------------------------------------------------------------------- |
| `id`    | integer | Kategoriyaga unikal identifikator                                          |
| `key`   | string  | Slug-formatdagi texnik kalit (unikal); filter va routing uchun ishlatiladi |
| `label` | string  | Foydalanuvchiga ko'rsatiladigan nom                                        |
| `icon`  | string  | Lucide ikonka nomi (frontend uchun)                                        |

### Xato javoblari

| Kod   | Sabab                           |
| ----- | ------------------------------- |
| `404` | Ko'rsatilgan sahifa mavjud emas |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/catalog/categories/" \
  -H "Accept: application/json"
```

Ikkinchi sahifani olish:

```bash
curl -X GET "http://localhost:8000/api/v1/catalog/categories/?page=2" \
  -H "Accept: application/json"
```
