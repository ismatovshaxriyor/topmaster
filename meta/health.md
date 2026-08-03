# Tizim holati tekshiruvi

`GET /health/`

| | |
|---|---|
| **Bo'lim** | Meta / Infratuzilma |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Konteyner va infratuzilma tomonidan ishlatiladigan sodda healthcheck endpointi. Docker/Kubernetes `HEALTHCHECK` direktivasi, load balancer va monitoring tizimlari ushbu endpointga so'rov yuborib servisning tirik ekanligini tekshiradi. Endpoint DRF orqali emas, oddiy Django `JsonResponse` bilan amalga oshirilgan — shuning uchun DRF middleware (autentifikatsiya, throttling) ishlamaydi va javob har doim tez keladi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

```json
{
  "status": "ok",
  "service": "topmaster-api"
}
```

| Maydon | Tavsif |
|---|---|
| `status` | Har doim `"ok"` — server javob bersa shu qiymat qaytadi |
| `service` | Har doim `"topmaster-api"` — servis identifikatori |

### Xato javoblari

Yo'q (endpoint juda sodda; agar server ishlamasa HTTP ulanish xatosi yuzaga keladi, JSON xato emas).

## Misol

```bash
curl "http://localhost:8000/health/"
```

Docker `HEALTHCHECK` misoli:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1
```
