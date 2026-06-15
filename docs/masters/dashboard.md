# Dashboard statistikasi

`GET /api/v1/masters/me/dashboard/`

| | |
|---|---|
| **Bo'lim** | Masters |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: usta (`IsMaster`) |
| **Sahifalash** | Yo'q |
| **Throttle** | user: 1000/min |

## Tavsif

Ustaning bosh ekrani uchun jamlangan statistik ko'rsatkichlarni qaytaradi
(`DashboardStatsSerializer`). Barcha sonlar hozirgi holat bo'yicha hisoblanadi:
buyurtmalar `master.assigned_jobs` orqali, kutilayotgan takliflar
`Proposal.status=pending` bo'yicha olinadi.

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
  "total_orders": 52,
  "completed": 48,
  "rating_avg": "4.80",
  "views": 813,
  "new_proposals": 3
}
```

**`DashboardStatsSerializer` maydonlari:**

| Maydon | Tur | Tavsif |
|---|---|---|
| `total_orders` | integer | Ustaga biriktirilgan barcha buyurtmalar soni |
| `completed` | integer | `status=completed` buyurtmalar soni |
| `rating_avg` | string | O'rtacha reyting (0.00–5.00); denormallashtirilgan qiymat |
| `views` | integer | Profilga tashrif buyurganlar soni (`views_count`) |
| `new_proposals` | integer | `status=pending` holatidagi takliflar soni |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi usta roliga ega emas |

## Misol

```bash
curl "http://localhost:8000/api/v1/masters/me/dashboard/" \
  -H "Authorization: Bearer $ACCESS"
```
