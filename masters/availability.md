# Mavjudlik holati

`PATCH /api/v1/masters/me/availability/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Ustaning mavjudlik holatini (`status`) alohida endpoint orqali tez o'zgartirish
imkonini beradi. Faqat `status` maydoni qabul qilinadi — boshqa profil maydonlari
o'zgartirilmaydi (`AvailabilitySerializer`).

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `status` | string | Ha | `free` — bo'sh, `busy` — band, `off` — faol emas |

## Javob

### `200 OK`

```json
{
  "status": "busy"
}
```

| Maydon | Tur | Tavsif |
|---|---|---|
| `status` | string | Yangilangan holat qiymati |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `status` qiymati noto'g'ri (ruxsat etilgan: `free`, `busy`, `off`) |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
curl -X PATCH "http://localhost:8000/api/v1/masters/me/availability/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"status": "busy"}'
```
