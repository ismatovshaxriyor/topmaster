# Swagger UI

`GET /api/docs/`

| | |
|---|---|
| **Bo'lim** | Meta / Infratuzilma |
| **Autentifikatsiya** | Ommaviy (AllowAny) |
| **Ruxsat** | Hamma |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

drf-spectacular tomonidan taqdim etilgan interaktiv Swagger UI sahifasini ko'rsatadi. Sxema manbai sifatida `url_name="schema"` orqali `/api/schema/` endpointi ulangan. Brauzerda endpointlarni ko'rish, parametrlarni sinab ko'rish va JWT token kiritib so'rovlarni yuborish mumkin. Bu endpoint HTML sahifasini qaytaradi — API mijozlari tomonidan emas, brauzer orqali ishlatilishi mo'ljallangan.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `200 OK`

Brauzer uchun HTML sahifasi qaytadi. Sahifada:

- Barcha API endpointlarining ro'yxati (bo'limlar bo'yicha guruhlab)
- Har bir endpoint uchun so'rov/javob sxemasi va misollari
- "Authorize" tugmasi — `Bearer <access_token>` kiritish va saqlab qo'yish imkoniyati
- "Try it out" — to'g'ridan-to'g'ri brauzerdan so'rov yuborish

Sxema manbai: `/api/schema/` (har sahifa yuklanganda dinamik ravishda olinadi).

### Xato javoblari

Yo'q (ommaviy endpoint, autentifikatsiya talab qilinmaydi).

## Misol

```bash
# Brauzerda ochish
open "http://localhost:8000/api/docs/"
```

JWT autentifikatsiyasini Swagger UI orqali ulash uchun:

1. `POST /api/v1/auth/login/` orqali `access` tokenni oling.
2. "Authorize" tugmasini bosing.
3. `Value` maydoniga `Bearer <access_token>` kiriting va saqlang.
4. Endi barcha himoyalangan endpointlarni "Try it out" orqali sinab ko'rish mumkin.
