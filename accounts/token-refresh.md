# Token yangilash

`POST /api/v1/auth/token/refresh/`

| | |
|---|---|
| **Bo'lim** | Auth & Accounts |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | Yo'q (global `anon`: 60/min) |

## Tavsif

Amaldagi `refresh` tokenni yangi `access` tokenga almashtiradi. `ROTATE_REFRESH_TOKENS=True` sozlamasi yoqilgani sababli har so'rovda yangi `refresh` ham qaytariladi; `BLACKLIST_AFTER_ROTATION=True` — eski `refresh` token darhol blacklist'ga tushadi va qayta ishlatib bo'lmaydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `refresh` | string | Ha | Avvalgi login yoki refresh so'rovidan olingan refresh token |

## Javob

### `200 OK`

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

| Maydon | Tavsif |
|---|---|
| `access` | Yangi qisqa muddatli JWT (60 daqiqa) |
| `refresh` | Rotatsiya qilingan yangi refresh token (14 kun) — eski token endi yaroqsiz |

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `refresh` maydoni yo'q |
| `401` | Token yaroqsiz, muddati o'tgan yoki blacklist'da |

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token/refresh/" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```
