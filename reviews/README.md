# Reviews — Bo'lim indeksi

Bazaviy yo'l: `/api/v1/reviews/`

Mijozlar yakunlangan buyurtmalaridan so'ng ustalarni baholaydi. Har bir
buyurtmaga faqat bitta sharh qoldirilishi mumkin (`OneToOneField`). Sharh
yaratilganda usta profilidagi `rating_avg` va `reviews_count` maydonlari
`post_save` signal orqali avtomatik yangilanadi.

## Endpointlar

| Metod | Yo'l | Tavsif | Ruxsat |
|---|---|---|---|
| `GET` | `/api/v1/reviews/` | [Sharhlar ro'yxati](list.md) | Ommaviy |
| `POST` | `/api/v1/reviews/` | [Sharh yaratish](create.md) | Rol: mijoz |
| `GET` | `/api/v1/reviews/{id}/` | [Sharh tafsiloti](detail.md) | Ommaviy |

## Serialayzerlar

| Serialayzer | Ishlatiladi | Maydonlar |
|---|---|---|
| `ReviewSerializer` | `list`, `retrieve`, `create` javobi | `id`, `author`, `master`, `rating`, `text`, `recommend`, `created_at` |
| `ReviewCreateSerializer` | `create` so'rovi | `job`, `rating`, `text`, `recommend` |

## Eslatmalar

- `author` — `UserSummarySerializer` orqali kengaytirilgan ob'ekt (aloqa
  ma'lumotlari — email/telefon — kiritilmagan; ommaviy endpointlarda xavfsiz).
- `master` — `MasterProfile` ga FK, javobda faqat integer ID sifatida keladi.
- Ro'yxat `?master=<id>` va `?job=<id>` filtrlash parametrlarini qo'llab-quvvatlaydi.
- Ro'yxat `created_at` bo'yicha teskari tartibda saralanadi (eng yangi birinchi).
