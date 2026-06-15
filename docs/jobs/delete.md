# Buyurtmani o'chirish

`DELETE /api/v1/jobs/{id}/`

| | |
|---|---|
| **Bo'lim** | Jobs |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated · Faqat buyurtma egasi (mijoz) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Buyurtmani bazadan butunlay o'chiradi. Faqat buyurtmani yaratgan mijoz o'chira oladi — boshqa foydalanuvchi `403` oladi. O'chirish qaytarib bo'lmaydigan amal: bog'liq rasmlar (`JobImage`), voqealar (`JobEvent`) va takliflar (`Proposal`) kaskad orqali ham o'chiriladi.

> **Eslatma:** Buyurtmani bekor qilmoqchi bo'lsangiz, o'chirish o'rniga `POST /api/v1/jobs/{id}/cancel/` dan foydalaning — bu holat tarixini saqlaydi va ustalarga xabar beradi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | O'chiriladigan buyurtma ID si |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `204 No Content`

Muvaffaqiyatli o'chirilganda tana bo'sh qaytadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi buyurtma egasi emas |
| `404` | Buyurtma topilmadi |
| `429` | So'rovlar limitidan oshildi |

## Misol

```bash
curl -X DELETE "http://localhost:8000/api/v1/jobs/42/" \
  -H "Authorization: Bearer $ACCESS"
```
