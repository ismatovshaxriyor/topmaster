# TopMaster API — hujjatlar

TopMaster backend REST API uchun to'liq hujjatlar. Har bir **bo'lim** alohida
papkada, har bir **endpoint** alohida `.md` faylda hujjatlangan.

> Interaktiv (jonli) hujjat: **Swagger UI** — `/api/docs/`, OpenAPI sxema — `/api/schema/`.
> Ushbu papka esa oflayn, batafsil maʼlumotnoma.

## Asoslar

|                      |                                                                       |
| -------------------- | --------------------------------------------------------------------- |
| **Bazaviy URL**      | `/api/v1/`                                                            |
| **Format**           | JSON (UTF-8)                                                          |
| **Autentifikatsiya** | JWT — `Authorization: Bearer <access_token>`                          |
| **Sahifalash**       | `?page=` (sahifa hajmi 20); javob: `{count, next, previous, results}` |
| **Til**              | Xabarlar va izohlar o'zbekcha; maydon nomlari inglizcha               |
| **To'lov**           | ❌ Yo'q — narx maydonlari faqat maʼlumot xarakterida                  |

Umumiy konvensiyalar va har bir fayl formati: [`_TEMPLATE.md`](_TEMPLATE.md).

## Bo'limlar

| Bo'lim                                   | Bazaviy yo'l             | Endpointlar                                                           |
| ---------------------------------------- | ------------------------ | --------------------------------------------------------------------- |
| [Auth & Accounts](accounts/README.md)    | `/api/v1/auth/`          | ro'yxatdan o'tish, kirish, JWT, profil, sozlamalar, parol, qurilmalar |
| [Catalog](catalog/README.md)             | `/api/v1/catalog/`       | shaharlar, yo'nalishlar                                               |
| [Masters](masters/README.md)             | `/api/v1/masters/`       | usta katalogi, profil, ko'nikma, portfolio, tasdiqlash, dashboard     |
| [Jobs](jobs/README.md)                   | `/api/v1/jobs/`          | buyurtmalar, qidiruv, geo, hayotiy sikl                               |
| [Proposals](proposals/README.md)         | `/api/v1/proposals/`     | takliflar, qabul/rad/qaytarish                                        |
| [Reviews](reviews/README.md)             | `/api/v1/reviews/`       | sharhlar                                                              |
| [Chat](chat/README.md)                   | `/api/v1/chat/`          | suhbatlar, xabarlar (+ WebSocket)                                     |
| [Notifications](notifications/README.md) | `/api/v1/notifications/` | bildirishnomalar (+ WebSocket)                                        |
| [Favorites](favorites/README.md)         | `/api/v1/favorites/`     | saqlangan ustalar                                                     |
| [Support](support/README.md)             | `/api/v1/support/`       | FAQ, qo'llab-quvvatlash chati                                         |
| [Reports](reports/README.md)             | `/api/v1/reports/`       | shikoyatlar                                                           |
| [Meta](meta/README.md)                   | `/`                      | sxema, Swagger, healthcheck                                           |

## Autentifikatsiya oqimi (qisqacha)

1. `POST /api/v1/auth/register/` — hisob yaratish (`role`: `mijoz` yoki `usta`); emailga 6 xonali tasdiqlash kodi yuboriladi.
2. `POST /api/v1/auth/verify-email/` — email + kod → tasdiqlash (+ `access`/`refresh` qaytadi, auto-login). Login tasdiqsiz ham ishlaydi.
3. `POST /api/v1/auth/login/` — `access` + `refresh` tokenlarni olish.
4. Har bir himoyalangan so'rovda: `Authorization: Bearer <access>`.
5. `POST /api/v1/auth/token/refresh/` — `access`ni yangilash.
6. `POST /api/v1/auth/logout/` — `refresh`ni bekor qilish (blacklist).
