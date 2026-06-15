# Saqlangan ustalar identifikatorlari

`GET /api/v1/favorites/ids/`

| | |
|---|---|
| **Bo'lim** | Favorites |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Autentifikatsiya qilingan foydalanuvchining saqlangan ustalar ro'yxatidagi barcha `MasterProfile` identifikatorlarini yig'ma massiv sifatida qaytaradi. Bu endpoint klient tomonida tezkor tekshiruv uchun mo'ljallangan: masalan, usta kartochkasida "saqlangan" belgisini ko'rsatish uchun to'liq ro'yxatni yuklamasdan bir so'rov bilan barcha `id`larni olish mumkin.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "ids": [7, 3, 19]
}
```

**Javob maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `ids` | integer[] | Saqlangan `MasterProfile` `id`lari ro'yxati. Bo'sh bo'lishi mumkin: `[]` |

Tartib `SavedMaster` ning standart tartibiga mos (`-created_at` — oxirgi saqlangan birinchi).

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |

## Misol

```bash
curl -X GET "http://localhost:8000/api/v1/favorites/ids/" \
  -H "Authorization: Bearer $ACCESS"
```
