# Taklifni yangilash

`PUT /api/v1/proposals/{id}/`  
`PATCH /api/v1/proposals/{id}/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated + ko'rinish doirasi |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Taklif maydonlarini yangilaydi. `ModelViewSet`ning standart `update` / `partial_update`
harakatlari; qo'shimcha validatsiya yo'q.

> **ESLATMA:** Taklif **holatini** (`status`) bu endpoint orqali o'zgartirish
> **tavsiya etilmaydi**. Holat o'zgarishlari maxsus action'lar orqali amalga
> oshiriladi:
> - `pending → accepted` — `POST /{id}/accept/`
> - `pending → rejected` — `POST /{id}/reject/`
> - `pending → withdrawn` — `POST /{id}/withdraw/`

Foydalanuvchi faqat o'zi ko'ra oladigan takliflarni yangilay oladi (ko'rinish doirasi).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

`PUT` — barcha yoziladigan maydonlar majburiy; `PATCH` — faqat o'zgartiriladigan maydonlar.

`ProposalSerializer` barcha maydonlarni `read_only` deb belgilagan, shu sababli
standart serializer orqali hech qanday maydonni o'zgartirish imkonsiz. Agar backend
kelajakda yoziladigan maydonlar qo'shsa, quyidagilar kutiladi:

| Maydon | Tur | Majburiy (PUT) | Tavsif |
|---|---|---|---|
| `message` | string | Yo'q | Ustaning xabari |
| `proposed_price` | integer | Yo'q | Taklif narxi (so'm) |

## Javob

### `200 OK`

Yangilangan taklif `ProposalSerializer` formatida qaytariladi (tuzilish `GET /{id}/` bilan bir xil).

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | Maydon validatsiya xatosi |
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
# PATCH — faqat xabarni yangilash
curl -X PATCH "http://localhost:8000/api/v1/proposals/15/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"message": "Yangilangan xabar."}'
```
