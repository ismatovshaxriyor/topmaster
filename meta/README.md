# Meta / Infratuzilma

Bu bo'lim versiyalanmagan infratuzilma endpointlarini hujjatlaydi.

> **Eslatma:** Bu bo'limdagi barcha yo'llar `/api/v1/` prefiksi **olmaydi** —
> ular to'g'ridan-to'g'ri domenning ildizidan boshlanadi.

## Endpointlar

| Endpoint | Fayl | Tavsif |
|---|---|---|
| `GET /api/schema/` | [openapi-schema.md](openapi-schema.md) | OpenAPI 3 sxemasi (YAML/JSON) |
| `GET /api/docs/` | [swagger-ui.md](swagger-ui.md) | Interaktiv Swagger UI |
| `GET /health/` | [health.md](health.md) | Konteyner healthcheck |

## Yo'llar haqida eslatma

| Bo'lim | Prefiks |
|---|---|
| Barcha API endpointlari | `/api/v1/` |
| OpenAPI sxema va Swagger UI | `/api/` (versiyasiz) |
| Healthcheck | `/` (ildiz) |

`/api/schema/` va `/api/docs/` yo'llari `/api/v1/` emas, balki `/api/` dan boshlanishini
e'tiborga oling — bu drf-spectacular ning standart yondashuvi bo'lib, sxema URL qoidasi
emas, infratuzilma qismi sifatida ko'rib chiqiladi.
