# Support — bo'lim indeksi

Bazaviy yo'l: `/api/v1/support/`

Ushbu bo'lim ikki qismdan iborat: **Yordam markazi (FAQ)** — ommaviy, autentifikatsiyasiz; va **Qo'llab-quvvatlash chati** — faqat autentifikatsiyalangan foydalanuvchilar uchun. Qo'llab-quvvatlash jamoasi foydalanuvchi xabarlariga **Django admin paneli** orqali javob beradi; foydalanuvchi tomonida xabar yuborish va o'qish uchun quyidagi endpointlar ishlatiladi.

## Endpointlar

### Yordam markazi (FAQ)

| Metod | Yo'l | Fayl | Tavsif |
|---|---|---|---|
| `GET` | `topics/` | [topics.md](topics.md) | FAQ mavzulari (ichida nested faqs) |
| `GET` | `faqs/` | [faqs.md](faqs.md) | FAQ yozuvlari; `?topic=<key>` filtri |

### Qo'llab-quvvatlash chati

| Metod | Yo'l | Fayl | Tavsif |
|---|---|---|---|
| `GET` | `chat/thread/` | [chat-thread.md](chat-thread.md) | Faol threadni olish (yo'q bo'lsa ochadi) |
| `GET` | `chat/messages/` | [chat-messages.md](chat-messages.md) | Thread xabarlari; xodim javoblarini o'qilgan deb belgilaydi |
| `POST` | `chat/send/` | [chat-send.md](chat-send.md) | Xabar yuborish; thread ochadi/qayta ochadi |
| `POST` | `chat/read/` | [chat-read.md](chat-read.md) | Xodim xabarlarini o'qilgan deb belgilaydi |

## Autentifikatsiya

- FAQ endpointlari (`topics/`, `faqs/`) — **ommaviy**, token talab qilinmaydi.
- Chat endpointlari — **Bearer JWT** talab qilinadi: `Authorization: Bearer <access_token>`.

## Thread holatlari

| Holat | Ma'nosi |
|---|---|
| `open` | Foydalanuvchi xabar yubordi, xodim javobi kutilmoqda |
| `pending` | Xodim javob berdi, foydalanuvchi javobi kutilmoqda |
| `resolved` | Muammo hal qilindi |
| `closed` | Thread yopilgan |

> Foydalanuvchi `resolved`/`closed` threadga yangi xabar yuborganda thread avtomatik `open` holatiga o'tkaziladi.

## Throttle (limitlar)

| Scope | Limit | Qo'llaniladi |
|---|---|---|
| `anon` | 60/min | FAQ endpointlari (autentifikatsiyasiz) |
| `user` | 1000/min | Chat `thread/`, `messages/`, `read/` |
| `support_send` | 30/min | Chat `send/` |
