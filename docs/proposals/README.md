# Proposals — Bo'lim indeksi

**Bo'lim tegi:** `Proposals`  
**Bazaviy yo'l:** `/api/v1/proposals/`

Usta mijozning ochiq buyurtmasiga taklif yuboradi; mijoz taklifni qabul qiladi
yoki rad etadi; usta taklifni qaytarib olishi mumkin.

---

## Endpointlar

| Metod | Yo'l | Fayl | Qisqacha tavsif |
|---|---|---|---|
| `GET` | `/` | [list.md](list.md) | Ko'rinadigan takliflar ro'yxati (sahifalangan) |
| `POST` | `/` | [create.md](create.md) | Yangi taklif yuborish (faqat usta) |
| `GET` | `/{id}/` | [detail.md](detail.md) | Bitta taklifni ko'rish |
| `PUT` | `/{id}/` | [update.md](update.md) | Taklifni to'liq yangilash |
| `PATCH` | `/{id}/` | [update.md](update.md) | Taklifni qisman yangilash |
| `DELETE` | `/{id}/` | [delete.md](delete.md) | Taklifni o'chirish |
| `POST` | `/{id}/accept/` | [accept.md](accept.md) | Taklifni qabul qilish (faqat buyurtma egasi) |
| `POST` | `/{id}/reject/` | [reject.md](reject.md) | Taklifni rad etish (faqat buyurtma egasi) |
| `POST` | `/{id}/withdraw/` | [withdraw.md](withdraw.md) | Taklifni qaytarib olish (faqat taklif egasi) |

---

## Ko'rinish doirasi

Foydalanuvchi taklifni ko'ra oladi **agar**:
- u taklif bergan **usta** bo'lsa, **yoki**
- taklif tegishli buyurtmaning **egasi (mijoz)** bo'lsa.

Shart bajarilmagan holda, hatto taklif mavjud bo'lsa ham, `404` qaytariladi.

---

## Taklif hayotiy sikli

```
           [usta POST /]
                │
                ▼
            PENDING
           /    |    \
          /     |     \
         ▼      ▼      ▼
     ACCEPTED REJECTED WITHDRAWN
   (mijoz     (mijoz   (usta
    accept)    reject)  withdraw)
```

| Holat | Qiymat | Tavsif |
|---|---|---|
| `pending` | `"pending"` | Mijoz hali javob bermagan |
| `accepted` | `"accepted"` | Mijoz taklifni qabul qildi |
| `rejected` | `"rejected"` | Mijoz taklifni rad etdi (yoki boshqa taklif qabul qilinganida avtomatik) |
| `withdrawn` | `"withdrawn"` | Usta taklifni qaytarib oldi |

### Holat o'tishlari va yon ta'sirlar

| O'tish | Endpoint | Yon ta'sirlar |
|---|---|---|
| — → `pending` | `POST /` | `job.proposals_count + 1`; mijozga `notify(type="order")` |
| `pending` → `accepted` | `POST /{id}/accept/` | `job.assigned_master = usta`; `job.status → in_progress`; qolgan `pending` takliflar `rejected`; `JobEvent(ACCEPTED)` yozuvi; ustaga `notify(type="accepted")` |
| `pending` → `rejected` | `POST /{id}/reject/` | Ustaga `notify(type="rejected")` |
| `pending` → `withdrawn` | `POST /{id}/withdraw/` | Bildirishnoma yo'q; `proposals_count` o'zgarmaydi |

---

## Umumiy xatolar

| Kod | Sabab |
|---|---|
| `400` | Buyurtma `open` emas; takroriy taklif; noto'g'ri holat o'tishi |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Rol yoki egasi tekshiruvi o'tmadi |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |
