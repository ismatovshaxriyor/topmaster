# Reports — Bo'lim indeksi

Bazaviy yo'l: `/api/v1/reports/`

Foydalanuvchilar tizimda mavjud bo'lgan obyektlar (usta profili, ish e'loni,
sharh yoki foydalanuvchi) ustidan shikoyat yuborishi mumkin. Har bir
foydalanuvchi bir obyektga faqat bitta shikoyat yuborishi mumkin.

Shikoyatlarni ko'rib chiqish, holat o'zgartirish va hal qilish faqat
**Django admin** paneli orqali amalga oshiriladi — APIda moderatsiya amallari
mavjud emas.

## Endpointlar

| Metod | Yo'l | Tavsif | Ruxsat |
|---|---|---|---|
| `POST` | `/api/v1/reports/` | [Shikoyat yuborish](create.md) | Bearer JWT |
| `GET` | `/api/v1/reports/` | [O'z shikoyatlarim ro'yxati](list.md) | Bearer JWT |

## Throttle

Ikkala endpoint ham `ReportRateThrottle` (scope: `report`) bilan himoyalangan —
**20 shikoyat/soat** (foydalanuvchi bo'yicha).

## Shikoyat sabablari (`reason`)

| Kod | O'zbek nomi |
|---|---|
| `spam` | Spam / reklama |
| `fraud` | Firibgarlik |
| `inappropriate` | Nomaqbul kontent |
| `fake` | Soxta profil / ma'lumot |
| `abuse` | Haqorat / tahdid |
| `other` | Boshqa |

## Shikoyat holatlari (`status`)

| Kod | O'zbek nomi | Tavsif |
|---|---|---|
| `open` | Yangi | Yangi shikoyat; moderator ko'rmagan |
| `reviewing` | Ko'rib chiqilmoqda | Moderator tomonidan ko'rib chiqilmoqda |
| `resolved` | Hal qilindi | Shikoyat asosli topildi va chora ko'rildi |
| `dismissed` | Rad etildi | Shikoyat asossiz topildi yoki bekor qilindi |

Holat qiymatlari faqat Django admin orqali o'zgartiriladi. API orqali faqat
`open` holat qaytarilishi mumkin (yaratilgan zahoti).

## Reportable obyektlar (`target_type`)

| API kaliti | Model |
|---|---|
| `master` | `masters.MasterProfile` |
| `job` | `jobs.Job` |
| `review` | `reviews.Review` |
| `user` | `accounts.User` |

Boshqa `target_type` qiymatlari har doim `400` qaytaradi — shikoyatlar
ixtiyoriy jadvalga yo'naltirilishi oldini olish uchun whitelist qo'llaniladi.
