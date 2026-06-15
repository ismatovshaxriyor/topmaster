# Tasdiqlash hujjatini yuklash

`POST /api/v1/masters/me/verification/documents/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Bitta KYC hujjatini yuklaydi yoki mavjudini almashtiradi (upsert). Har bir
`doc_type` uchun yagona yozuv saqlanadi — bir xil `doc_type` qayta yuborilsa,
fayl yangilanadi va `state` `uploaded` ga o'rnatiladi. Tasdiqlash so'rovi
mavjud bo'lmasa, avtomatik yaratiladi. So'rov `multipart/form-data` formatida
yuborilishi shart.

**Yon ta'sir:** hujjat `state` qiymati `uploaded` ga o'rnatiladi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body) — `multipart/form-data`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `doc_type` | string | Ha | `id` / `selfie` / `diploma` / `address` |
| `file` | file | Ha | Yuklanaydigan fayl (rasm yoki PDF) |

**`doc_type` qiymatlari:**

| Qiymat | Tavsif |
|---|---|
| `id` | Pasport yoki ID karta |
| `selfie` | Selfi tekshiruvi |
| `diploma` | Diplom yoki sertifikat |
| `address` | Manzil tasdiq hujjati |

## Javob

### `201 Created`

```json
{
  "id": 5,
  "doc_type": "id",
  "file": "http://localhost:8000/media/verification/master_12/id/pasport.jpg",
  "required": false,
  "state": "uploaded"
}
```

**`VerificationDocumentSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `id` | integer | Hujjat PK |
| `doc_type` | string | Yuklangan hujjat turi |
| `file` | string | Fayl URL si |
| `required` | boolean | Admin tomonidan belgilangan majburiylik (standart: `false`) |
| `state` | string | Doim `uploaded` qaytariladi |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `doc_type` qiymati noto'g'ri yoki `file` ko'rsatilmagan |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/masters/me/verification/documents/" \
  -H "Authorization: Bearer $ACCESS" \
  -F "doc_type=id" \
  -F "file=@/path/to/pasport.jpg"
```
