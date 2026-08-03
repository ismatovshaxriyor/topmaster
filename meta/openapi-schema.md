# OpenAPI sxemasi

`GET /api/schema/`

| | |
|---|---|
| **Bo'lim** | Meta / Infratuzilma |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

drf-spectacular tomonidan avtomatik generatsiya qilinadigan OpenAPI 3 sxemasini qaytaradi. Sxema barcha `/api/v1/` endpointlarini, serializerlarni va autentifikatsiya talablarini o'z ichiga oladi. `SPECTACULAR_SETTINGS` ichida `SERVE_INCLUDE_SCHEMA: False` o'rnatilganligi sababli bu endpoint o'zi sxemaga kiritilmagan. So'rov `Accept` sarlavhasiga qarab YAML yoki JSON formatida javob beradi; standart format YAML.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

| Parametr | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `format` | string | Yo'q | Chiqish formati: `json` yoki `yaml` (standart: `yaml`) |

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

`Accept: application/json` yuborganda:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "TopMaster API",
    "version": "1.0.0",
    "description": "TopMaster — O'zbekiston xizmatlar marketplace backend API."
  },
  "paths": {
    "/api/v1/auth/login/": { "...": "..." }
  },
  "components": {
    "schemas": { "...": "..." },
    "securitySchemes": {
      "jwtAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    }
  }
}
```

`Accept: application/yaml` (standart) yuborganda esa yuqoridagi tuzilish YAML formatida qaytadi.

| Maydon | Tavsif |
|---|---|
| `info.title` | `"TopMaster API"` — `SPECTACULAR_SETTINGS["TITLE"]` dan olinadi |
| `info.version` | `"1.0.0"` — `SPECTACULAR_SETTINGS["VERSION"]` dan olinadi |
| `paths` | Barcha ro'yxatdan o'tgan `/api/v1/` marshrutlari |
| `components.securitySchemes` | `jwtAuth` — Bearer JWT autentifikatsiya sxemasi |

### Xato javoblari

Yo'q (ommaviy endpoint, autentifikatsiya talab qilinmaydi).

## Misol

```bash
# YAML (standart)
curl "http://localhost:8000/api/schema/"

# JSON formatida
curl "http://localhost:8000/api/schema/?format=json" \
  -H "Accept: application/json"
```
