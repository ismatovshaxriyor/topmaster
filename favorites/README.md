# Favorites — bo'lim indeksi

**Bazaviy URL:** `/api/v1/favorites/`
**Bo'lim tegi:** `Favorites`

Mijoz foydalanuvchilarning saqlangan (yoqtirgan) ustalar ro'yxatini boshqaradi. Ro'yxatga qo'shish, ko'rish, o'chirish va tezkor identifikator so'rovi endpointlarini o'z ichiga oladi.

## Endpointlar

| Metod | URL | Fayl | Tavsif | Ommaviy |
|---|---|---|---|---|
| `GET` | `/api/v1/favorites/` | [list.md](list.md) | Saqlangan ustalar ro'yxati (sahifalangan) | Yo'q |
| `POST` | `/api/v1/favorites/` | [create.md](create.md) | Ustani saqlash (idempotent) | Yo'q |
| `DELETE` | `/api/v1/favorites/{id}/` | [delete.md](delete.md) | Saqlangan yozuvni o'chirish | Yo'q |
| `GET` | `/api/v1/favorites/ids/` | [ids.md](ids.md) | Saqlangan ustalar `id`lari (tezkor tekshiruv) | Yo'q |

## Asosiy serialayzerlar

| Serialayzer | Ishlatiladi | Maydonlar |
|---|---|---|
| `SavedMasterSerializer` | `GET /`, `GET /{id}/`, `POST` javobi | `id, master{MasterSummarySerializer}, created_at` |
| `SavedMasterCreateSerializer` | `POST` tanasi | `master` (MasterProfile PK) |
| `MasterSummarySerializer` | `master` ichida joylashtirilgan | `id, name, avatar, spec, city, experience_years, rating_avg, reviews_count, min_price, status, is_verified, is_top, views_count, distance_km` |

## Ruxsatlar

- Barcha endpointlar autentifikatsiyani talab qiladi (`Authorization: Bearer <access_token>`).
- `POST /` — faqat `role=mijoz` foydalanuvchilarga ruxsat (`IsClient`). Ustalar va boshqa rollar `403` oladi.
- `GET`, `DELETE` — autentifikatsiya qilingan har qanday foydalanuvchi; queryset avtomatik ravishda faqat o'z yozuvlarini qaytaradi.

## Muhim xulq-atvorlar

- `POST /` **idempotent**: mavjud yozuv bo'lsa `200 OK` + mavjud ob'ekt; yangi yozuv bo'lsa `201 Created`.
- `DELETE /{id}/` — `id` bu `SavedMaster.id` (usta `id`si emas). Boshqa foydalanuvchining yozuviga murojaat → `404`.
- `GET ids/` — `MasterProfile.id` larni qaytaradi (saqlangan yozuv `id` larini emas). Klient-side "saqlangan" holat tekshiruvi uchun optimallashtirilgan.
