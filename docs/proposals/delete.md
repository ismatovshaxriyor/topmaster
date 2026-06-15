# Taklifni o'chirish

`DELETE /api/v1/proposals/{id}/`

| | |
|---|---|
| **Bo'lim** | Proposals |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated + ko'rinish doirasi |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Taklifni ma'lumotlar bazasidan butunlay o'chiradi. `ModelViewSet`ning standart
`destroy` harakati; qo'shimcha validatsiya yo'q. Foydalanuvchi faqat o'zi ko'ra
oladigan takliflarni o'chira oladi (ko'rinish doirasi).

> **Diqqat:** O'chirish `job.proposals_count` hisoblagichini **kamaytirmaydi** —
> hisoblagich faqat `POST /` orqali oshiriladi. Agar aniq hisob kerak bo'lsa,
> o'chirishdan oldin `POST /{id}/withdraw/` orqali taklifni qaytarib olish tavsiya
> etiladi.

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | Taklif IDsi |

### Query parametrlari

Yo'q.

### Tana (request body)

Yo'q.

## Javob

### `204 No Content`

Muvaffaqiyatli o'chirildi. Javob tanasi bo'sh.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `401` | Autentifikatsiya talab qilinadi |
| `404` | Taklif topilmadi yoki ko'rinish doirasidan tashqarida |

## Misol

```bash
curl -X DELETE "http://localhost:8000/api/v1/proposals/15/" \
  -H "Authorization: Bearer $ACCESS"
```
