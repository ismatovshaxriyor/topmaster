# Shikoyat yuborish

`POST /api/v1/reports/`

|                      |                 |
| -------------------- | --------------- |
| **Bo'lim**           | Reports         |
| **Autentifikatsiya** | Bearer JWT      |
| **Ruxsat**           | IsAuthenticated |
| **Sahifalash**       | Yo'q            |
| **Throttle**         | report: 20/soat |

## Tavsif

Autentifikatsiya qilingan foydalanuvchi tizimda mavjud bo'lgan obyekt (usta
profili, ish e'loni, sharh yoki foydalanuvchi) ustidan shikoyat yuboradi.

Shikoyat qabul qilinganda `status` avtomatik `open` (yangi) qiymatiga
o'rnatiladi. Keyingi moderatsiya — holat o'zgartirish, ko'rib chiqish va hal
qilish — faqat **Django admin** paneli orqali amalga oshiriladi; APIda bu
amallar mavjud emas.

Bir foydalanuvchi bir obyektga faqat bitta shikoyat yuborishi mumkin —
`(reporter, content_type, object_id)` ustida DB darajasida `UniqueConstraint`
bor. Takror urinish `400` qaytaradi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

| Maydon        | Tur     | Majburiy | Tavsif                                                                                                |
| ------------- | ------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `target_type` | string  | Ha       | Shikoyat qilinayotgan obyekt turi. Ruxsat etilgan qiymatlar: `master`, `job`, `review`, `user`        |
| `target_id`   | integer | Ha       | Shu tur bo'yicha obyekt ID'si (musbat son). Bazada mavjudligi tekshiriladi                            |
| `reason`      | string  | Ha       | Shikoyat sababi. Ruxsat etilgan qiymatlar: `spam`, `fraud`, `inappropriate`, `fake`, `abuse`, `other` |
| `description` | string  | Yo'q     | Qo'shimcha tavsif; bo'sh string ham qabul qilinadi                                                    |

**Validatsiya qoidalari:**

- `target_type` qiymati faqat `master`, `job`, `review`, `user` dan biri
  bo'lishi shart — boshqa turlar rad etiladi (`400`).
- `target_id` musbat butun son bo'lishi va tegishli jadvalda mavjud bo'lishi
  kerak; topilmasa `400` qaytaradi.
- Bir xil `(foydalanuvchi, target_type, target_id)` juftligi uchun takror
  shikoyat `400` qaytaradi.

## Javob

### `201 Created`

```json
{
  "id": 42,
  "target_label": "MasterProfile #7",
  "reason": "spam",
  "reason_display": "Spam / reklama",
  "description": "Profilda to'liq narx o'rniga reklama havolalari bor.",
  "status": "open",
  "status_display": "Yangi",
  "created_at": "2025-03-10T09:15:00Z"
}
```

**Asosiy javob maydonlari:**

| Maydon           | Tavsif                                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `id`             | Shikoyat ID'si                                                                                                 |
| `target_label`   | Shikoyat qilingan obyektning `str()` ko'rinishi; obyekt o'chirilgan bo'lsa `"<model> #<id>"` formatida qaytadi |
| `reason`         | Kiritilgan sabab kodi                                                                                          |
| `reason_display` | Sababning o'zbek tilidagi to'liq nomi                                                                          |
| `status`         | Har doim `open` — yangi shikoyatning boshlang'ich holati                                                       |
| `status_display` | Holatning o'zbek tilidagi to'liq nomi                                                                          |
| `created_at`     | ISO 8601 formatida yaratilgan vaqt                                                                             |

So'rovdagi `target_type` va `target_id` maydonlari `write_only` — javobda
qaytmaydi.

### Xato javoblari

| Kod   | Sabab                                                                                                                |
| ----- | -------------------------------------------------------------------------------------------------------------------- |
| `400` | `target_type` noto'g'ri; `target_id` topilmadi; shu obyektga allaqachon shikoyat qilingan; `reason` noto'g'ri qiymat |
| `401` | Autentifikatsiya talab qilinadi                                                                                      |
| `429` | So'rovlar limiti oshib ketdi (20 shikoyat/soat)                                                                      |

**400 xatolariga misollar:**

```json
{ "target_type": ["Noto'g'ri obyekt turi."] }
{ "target_id": ["Obyekt topilmadi."] }
{ "non_field_errors": ["Siz bu obyekt ustidan allaqachon shikoyat qilgansiz."] }
{ "reason": ["\"invalid_value\" is not a valid choice."] }
```

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/reports/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "master",
    "target_id": 7,
    "reason": "spam",
    "description": "Profilda to'\''liq narx o'\''rniga reklama havolalari bor."
  }'
```
