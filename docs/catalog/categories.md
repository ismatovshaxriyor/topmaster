# Xizmat kategoriyalari roʻyxati

`GET /api/v1/catalog/categories/`

| | |
|---|---|
| **Boʻlim** | Catalog |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Ha |
| **Throttle** | Yoʻq |

## Tavsif

Faol xizmat yoʻnalishlari (kategoriyalar) roʻyxatini qaytaradi. Faqat
`is_active=True` boʻlgan yozuvlar chiqariladi — nofaol kategoriyalar
filtrdan oʻtkaziladi. Kategoriyalar `order` boʻyicha, soʻngra `label`
boʻyicha tartiblangan. `icon` maydoni frontend tomonida Lucide ikonkasining
nomini saqlaydi.

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

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Kategoriyaga unikal identifikator |
| `key` | string | Slug-formatdagi texnik kalit (unikal); filter va routing uchun ishlatiladi |
| `label` | string | Foydalanuvchiga koʻrsatiladigan nom |
| `icon` | string | Lucide ikonka nomi (frontend uchun) |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `404` | Koʻrsatilgan sahifa mavjud emas |

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
