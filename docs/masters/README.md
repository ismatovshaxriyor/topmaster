# Masters — bo'lim indeksi

**Bazaviy URL:** `/api/v1/masters/`  
**Bo'lim tegi:** `Masters`

Usta katalogi, o'z-o'ziga xizmat ko'rsatish (profil, ko'nikmalar, portfolio),
KYC tasdiqlash va dashboard statistikasi.

## Endpointlar

| Metod | URL | Fayl | Tavsif | Ommaviy |
|---|---|---|---|---|
| `GET` | `/api/v1/masters/` | [list.md](list.md) | Ustalar katalogi (filtrlar, qidiruv, yaqindagilar) | Ha |
| `GET` | `/api/v1/masters/{id}/` | [detail.md](detail.md) | Usta to'liq profili (+`views_count`) | Ha |
| `GET` | `/api/v1/masters/me/` | [me.md](me.md) | O'z profilini ko'rish | Yo'q |
| `PATCH` | `/api/v1/masters/me/` | [me.md](me.md) | O'z profilini yangilash | Yo'q |
| `PATCH` | `/api/v1/masters/me/availability/` | [availability.md](availability.md) | Mavjudlik holatini almashtirish | Yo'q |
| `POST` | `/api/v1/masters/me/onboarding/` | [onboarding.md](onboarding.md) | Birinchi marta profil to'ldirish | Yo'q |
| `GET` | `/api/v1/masters/me/verification/` | [verification.md](verification.md) | KYC holati va hujjatlar | Yo'q |
| `POST` | `/api/v1/masters/me/verification/` | [verification.md](verification.md) | Tasdiqlash uchun yuborish | Yo'q |
| `POST` | `/api/v1/masters/me/verification/documents/` | [verification-documents.md](verification-documents.md) | KYC hujjatini yuklash (upsert) | Yo'q |
| `GET` | `/api/v1/masters/me/dashboard/` | [dashboard.md](dashboard.md) | Dashboard statistikasi | Yo'q |
| `GET` | `/api/v1/masters/me/skills/` | [skills.md](skills.md) | Ko'nikmalar ro'yxati | Yo'q |
| `POST` | `/api/v1/masters/me/skills/` | [skills.md](skills.md) | Ko'nikma yaratish | Yo'q |
| `GET` | `/api/v1/masters/me/skills/{id}/` | [skills.md](skills.md) | Ko'nikma ko'rish | Yo'q |
| `PUT` | `/api/v1/masters/me/skills/{id}/` | [skills.md](skills.md) | Ko'nikmani to'liq yangilash | Yo'q |
| `PATCH` | `/api/v1/masters/me/skills/{id}/` | [skills.md](skills.md) | Ko'nikmani qisman yangilash | Yo'q |
| `DELETE` | `/api/v1/masters/me/skills/{id}/` | [skills.md](skills.md) | Ko'nikmani o'chirish | Yo'q |
| `GET` | `/api/v1/masters/me/portfolio/` | [portfolio.md](portfolio.md) | Portfolio ro'yxati | Yo'q |
| `POST` | `/api/v1/masters/me/portfolio/` | [portfolio.md](portfolio.md) | Portfolio elementi yaratish (multipart) | Yo'q |
| `GET` | `/api/v1/masters/me/portfolio/{id}/` | [portfolio.md](portfolio.md) | Portfolio elementini ko'rish | Yo'q |
| `PUT` | `/api/v1/masters/me/portfolio/{id}/` | [portfolio.md](portfolio.md) | Portfolio elementini to'liq yangilash | Yo'q |
| `PATCH` | `/api/v1/masters/me/portfolio/{id}/` | [portfolio.md](portfolio.md) | Portfolio elementini qisman yangilash | Yo'q |
| `DELETE` | `/api/v1/masters/me/portfolio/{id}/` | [portfolio.md](portfolio.md) | Portfolio elementini o'chirish | Yo'q |

## Asosiy serialayzerlar

| Serialayzer | Ishlatiladi | Maydonlar |
|---|---|---|
| `MasterSummarySerializer` | `GET /` (ro'yxat) | `id, name, avatar, spec, city, experience_years, rating_avg, reviews_count, min_price, status, is_verified, is_top, views_count, distance_km` |
| `MasterDetailSerializer` | `GET /{id}/`, `GET me/`, `PATCH me/` javobi | Yuqoridagi + `bio, categories, skills, portfolio, recent_reviews` |
| `MasterProfileUpdateSerializer` | `PATCH me/` tanasi | `bio, experience_years, min_price, status, categories, latitude, longitude` |
| `AvailabilitySerializer` | `PATCH me/availability/` | `status` |
| `OnboardingSerializer` | `POST me/onboarding/` tanasi | `city, bio, experience_years, min_price, category_keys, skills` |
| `VerificationRequestSerializer` | `GET/POST me/verification/` | `status, submitted_at, reviewed_at, documents[]` |
| `VerificationDocumentSerializer` | `POST me/verification/documents/` | `id, doc_type, file, required, state` |
| `DashboardStatsSerializer` | `GET me/dashboard/` | `total_orders, completed, rating_avg, views, new_proposals` |
| `SkillSerializer` | `me/skills/` | `id, category, category_label, title, price_min, price_max, years, order` |
| `PortfolioItemSerializer` | `me/portfolio/` | `id, title, location, completed_at, image, category, featured, order` |

## Ruxsatlar

- Ommaviy endpointlar (`GET /`, `GET /{id}/`) — autentifikatsiya talab etilmaydi.
- `me/` va barcha ichki endpointlar — `Authorization: Bearer <access_token>` va
  `role=usta` talab qilinadi (`IsMaster` ruxsat sinfi).

## Muhim yon ta'sirlar

- `GET /{id}/` — `views_count` atomik `+1` oshadi.
- `POST me/verification/` — `status=pending`, `submitted_at` belgilanadi.
- `POST me/verification/documents/` — hujjat `state=uploaded` ga o'rnatiladi (upsert).
- `POST me/onboarding/` — `category_keys` berilsa, kategoriyalar to'plami to'liq almashtiriladi.
