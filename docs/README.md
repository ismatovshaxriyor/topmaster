# TopMaster API — hujjatlar

TopMaster backend REST API uchun toʻliq hujjatlar. Har bir **boʻlim** alohida
papkada, har bir **endpoint** alohida `.md` faylda hujjatlangan.

> Interaktiv (jonli) hujjat: **Swagger UI** — `/api/docs/`, OpenAPI sxema — `/api/schema/`.
> Ushbu papka esa oflayn, batafsil maʼlumotnoma.

## Asoslar

| | |
|---|---|
| **Bazaviy URL** | `/api/v1/` |
| **Format** | JSON (UTF-8) |
| **Autentifikatsiya** | JWT — `Authorization: Bearer <access_token>` |
| **Sahifalash** | `?page=` (sahifa hajmi 20); javob: `{count, next, previous, results}` |
| **Til** | Xabarlar va izohlar oʻzbekcha; maydon nomlari inglizcha |
| **Toʻlov** | ❌ Yoʻq — narx maydonlari faqat maʼlumot xarakterida |

Umumiy konvensiyalar va har bir fayl formati: [`_TEMPLATE.md`](_TEMPLATE.md).

## Boʻlimlar

| Boʻlim | Bazaviy yoʻl | Endpointlar |
|---|---|---|
| [Auth & Accounts](accounts/README.md) | `/api/v1/auth/` | roʻyxatdan oʻtish, kirish, JWT, profil, sozlamalar, parol, qurilmalar |
| [Catalog](catalog/README.md) | `/api/v1/catalog/` | shaharlar, yoʻnalishlar |
| [Masters](masters/README.md) | `/api/v1/masters/` | usta katalogi, profil, koʻnikma, portfolio, tasdiqlash, dashboard |
| [Jobs](jobs/README.md) | `/api/v1/jobs/` | buyurtmalar, qidiruv, geo, hayotiy sikl |
| [Proposals](proposals/README.md) | `/api/v1/proposals/` | takliflar, qabul/rad/qaytarish |
| [Reviews](reviews/README.md) | `/api/v1/reviews/` | sharhlar |
| [Chat](chat/README.md) | `/api/v1/chat/` | suhbatlar, xabarlar (+ WebSocket) |
| [Notifications](notifications/README.md) | `/api/v1/notifications/` | bildirishnomalar (+ WebSocket) |
| [Favorites](favorites/README.md) | `/api/v1/favorites/` | saqlangan ustalar |
| [Support](support/README.md) | `/api/v1/support/` | FAQ, qoʻllab-quvvatlash chati |
| [Reports](reports/README.md) | `/api/v1/reports/` | shikoyatlar |
| [Meta](meta/README.md) | `/` | sxema, Swagger, healthcheck |

## Autentifikatsiya oqimi (qisqacha)

1. `POST /api/v1/auth/register/` — hisob yaratish (`role`: `mijoz` yoki `usta`).
2. `POST /api/v1/auth/login/` — `access` + `refresh` tokenlarni olish.
3. Har bir himoyalangan soʻrovda: `Authorization: Bearer <access>`.
4. `POST /api/v1/auth/token/refresh/` — `access`ni yangilash.
5. `POST /api/v1/auth/logout/` — `refresh`ni bekor qilish (blacklist).
