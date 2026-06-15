# Buyurtmaga rasm biriktirish

`POST /api/v1/jobs/{id}/images/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Buyurtmaga yangi rasm yuklaydi. Faqat buyurtmani yaratgan mijoz rasm qo'sha oladi — boshqa foydalanuvchi `403` oladi. So'rov `multipart/form-data` formatida yuboriladi. `JobImageSerializer` ishlatiladi. Rasmlar `order` maydoni bo'yicha saralanadi — kichik qiymat birinchi ko'rsatiladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Buyurtma ID si |

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: multipart/form-data`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `image` | file | Ha | Rasm fayli (JPEG, PNG va boshqalar) |
| `order` | integer | Yo'q | Ko'rsatish tartibi (standart: 0). Kichik son — ko'proq oldinda |

## Javob

### `201 Created`

```json
{
  "id": 5,
  "image": "http://localhost:8000/media/jobs/job_42/photo3.jpg",
  "order": 2
}
```

**Yuklangan fayl yo'li:** `media/jobs/job_{id}/{filename}` shaklida saqlanadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `image` maydoni yo'q yoki yaroqsiz fayl formati |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/jobs/42/images/" \
  -H "Authorization: Bearer $ACCESS" \
  -F "image=@/path/to/photo.jpg" \
  -F "order=2"
```
