# Tasdiqlash holati

`GET /api/v1/masters/me/verification/`  
`POST /api/v1/masters/me/verification/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

`GET` — ustaning joriy KYC (tasdiqlash) so'rovi holatini va yuklangan hujjatlar
ro'yxatini qaytaradi (`VerificationRequestSerializer`). Tasdiqlash so'rovi mavjud
bo'lmasa, avtomatik ravishda `status=none` holati bilan yaratiladi.

`POST` — mavjud tasdiqlash so'rovini `pending` holatiga o'tkazadi va
`submitted_at` ni hozirgi vaqt bilan belgilaydi. So'rov tanasi talab qilinmaydi.
Hujjatlar `POST me/verification/documents/` orqali alohida yuklanadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q (GET va POST uchun ham).

## Javob

### `200 OK` (GET va POST uchun)

```json
{
  "status": "pending",
  "submitted_at": "2025-12-01T09:15:00Z",
  "reviewed_at": null,
  "documents": [
    {
      "id": 5,
      "doc_type": "id",
      "file": "http://localhost:8000/media/verification/master_12/id/pasport.jpg",
      "required": true,
      "state": "uploaded"
    },
    {
      "id": 6,
      "doc_type": "selfie",
      "file": null,
      "required": true,
      "state": "none"
    }
  ]
}
```

**`VerificationRequestSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `status` | string | `none` / `pending` / `approved` / `rejected` |
| `submitted_at` | datetime\|null | POST yuborilgan vaqt |
| `reviewed_at` | datetime\|null | Admin ko'rib chiqqan vaqt |
| `documents` | array | Har bir hujjat uchun `VerificationDocumentSerializer` |

**`documents` elementi (`VerificationDocumentSerializer`):**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Hujjat PK |
| `doc_type` | string | `id` / `selfie` / `diploma` / `address` |
| `file` | string\|null | Fayl URL si (yuklanmagan bo'lsa `null`) |
| `required` | boolean | Admin tomonidan belgilangan majburiylik |
| `state` | string | `none` / `uploaded` / `pending` / `verified` / `rejected` |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
# Holat va hujjatlarni ko'rish
curl "http://localhost:8000/api/v1/masters/me/verification/" \
  -H "Authorization: Bearer $ACCESS"

# Tasdiqlash uchun yuborish (so'rov tanasi yo'q)
curl -X POST "http://localhost:8000/api/v1/masters/me/verification/" \
  -H "Authorization: Bearer $ACCESS"
```
