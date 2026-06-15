# Jobs — Buyurtmalar bo'limi

**Bazaviy URL:** `/api/v1/jobs/`
**OpenAPI tegi:** `Jobs`

Mijozlar (clients) tomonidan joylanadigan ish topshiriqlari (buyurtmalar). Har bir buyurtmaning o'z hayot sikli bor — holatlar faqat maxsus lifecycle action endpointlari orqali o'zgartiriladi; oddiy `PATCH` orqali `status` o'zgarmaydi.

---

## Endpointlar ro'yxati

| Metod | URL | Tavsif | Fayl |
|---|---|---|---|
| `GET` | `/api/v1/jobs/` | Ochiq buyurtmalar taxtasi (sahifalangan, filtrlanadi) | [list.md](list.md) |
| `POST` | `/api/v1/jobs/` | Yangi buyurtma yaratish (faqat mijoz) | [create.md](create.md) |
| `GET` | `/api/v1/jobs/{id}/` | Bitta buyurtma tafsilotlari (rasmlar, voqealar, usta) | [detail.md](detail.md) |
| `PATCH` | `/api/v1/jobs/{id}/` | Buyurtma maydonlarini yangilash (faqat egasi) | [update.md](update.md) |
| `DELETE` | `/api/v1/jobs/{id}/` | Buyurtmani o'chirish (faqat egasi) | [delete.md](delete.md) |
| `GET` | `/api/v1/jobs/my_jobs/` | Joriy foydalanuvchining barcha buyurtmalari | [my-jobs.md](my-jobs.md) |
| `POST` | `/api/v1/jobs/{id}/images/` | Buyurtmaga rasm biriktirish (faqat egasi) | [images.md](images.md) |
| `POST` | `/api/v1/jobs/{id}/mark_awaiting/` | Usta ishni yakunlab, tasdiqlashga yuboradi | [mark-awaiting.md](mark-awaiting.md) |
| `POST` | `/api/v1/jobs/{id}/complete/` | Mijoz ishni qabul qiladi va yakunlaydi | [complete.md](complete.md) |
| `POST` | `/api/v1/jobs/{id}/cancel/` | Mijoz buyurtmani bekor qiladi | [cancel.md](cancel.md) |

---

## Buyurtma hayot sikli (status oqimi)

```
                  ┌─────────────────────────────────────────────┐
                  │                                             │
                  ▼                                             │
           [YARATILDI]                                    bekor qilish
                  │                                       (mijoz)
                  ▼                                             │
              ┌──────┐                                          │
              │ open │ ◄──── sukut holat, takliflar qabul qilinadi
              └──────┘                                          │
                  │                                             │
          taklif qabul qilinadi                                 │
          (proposals bo'limi)                                    │
                  │                                             │
                  ▼                                             │
          ┌─────────────┐                                       │
          │ in_progress │ ──────────────────────────────────────┤
          └─────────────┘                                       │
                  │                                             │
         mark_awaiting/                                         │
         (tayinlangan usta)                                      │
                  │                                             │
                  ▼                                             │
  ┌──────────────────────────┐                                  │
  │ awaiting_confirmation    │ ─────────────────────────────────┤
  └──────────────────────────┘                                  │
                  │                                             │
            complete/                                           │
            (mijoz)                                             │
                  │                                             │
                  ▼                                             │
          ┌───────────┐                                         │
          │ completed │ (yakuniy holat)                         │
          └───────────┘                                         │
                                                                │
          ┌───────────┐                                         │
          │ cancelled │ ◄───────────────────────────────────────┘
          └───────────┘ (yakuniy holat)
```

### Holat qiymatlari

| Qiymat | Ko'rinish | Tavsif |
|---|---|---|
| `open` | Ochiq | Yangi buyurtma, takliflar kutilmoqda |
| `in_progress` | Bajarilmoqda | Usta tayinlangan va ish boshlangan |
| `awaiting_confirmation` | Tasdiqlash kutilmoqda | Usta tugadi deb belgiladi, mijoz tasdiqlashi kerak |
| `completed` | Yakunlandi | Mijoz ishni qabul qildi (yakuniy holat) |
| `cancelled` | Bekor qilindi | Mijoz tomonidan bekor qilindi (yakuniy holat) |

### Muhim qoidalar

- **`status` PATCH orqali o'zgarmaydi** — faqat lifecycle action endpointlari (`mark_awaiting`, `complete`, `cancel`) orqali.
- `completed` va `cancelled` **yakuniy holatlar** — bu holatlardan chiqib bo'lmaydi.
- Buyurtma bekor qilinganda, barcha `pending` takliflar avtomatik `rejected` holatiga o'tkaziladi.
- `price_amount` faqat ma'lumot — hech qanday to'lov tranzaksiyasi amalga oshirilmaydi.

---

## Serializer xaritasi

| Action | Serializer |
|---|---|
| `list`, `my_jobs` | `JobListSerializer` |
| `retrieve`, lifecycle javoblari | `JobDetailSerializer` |
| `create`, `update`, `partial_update` | `JobCreateSerializer` |
| `images` | `JobImageSerializer` |

---

## Filtrlash va qidiruv

| Parametr | Tur | Xulq |
|---|---|---|
| `?q=<matn>` | To'liq-matn | PostgreSQL GIN indeksi, sarlavha+tavsif, websearch sintaksisi |
| `?lat=&lng=[&radius_km=]` | Geo | Yaqindagi buyurtmalar, `distance_km` annotatsiyasi qo'shiladi |
| `?category=<key>` | Filtr | `category__key` bo'yicha |
| `?city=<id>` | Filtr | `city_id` bo'yicha |
| `?price_type=` | Filtr | `fixed` yoki `negotiable` |
| `?status=` | Filtr | Holat (berilmasa sukut `open`) |
| `?urgent=` | Filtr | `true` yoki `false` |
| `?ordering=` | Saralash | `created_at`, `due_date`, `price_amount`, `urgent` (minus belgisi teskari tartib) |
