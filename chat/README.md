# Chat bo'limi

**Bazaviy URL (REST):** `/api/v1/chat/`
**WebSocket:** `ws://<host>/ws/chat/<conversation_id>/`

Ikki foydalanuvchi o'rtasidagi 1:1 suhbatlar uchun REST va real vaqt WebSocket interfeysi. Har bir suhbat ixtiyoriy ravishda ish buyurtmasiga (`job`) bog'lanishi mumkin.

---

## REST endpointlar

| Metod | URL | Fayl | Tavsif |
|---|---|---|---|
| `GET` | `/api/v1/chat/conversations/` | [list.md](list.md) | O'z suhbatlarini ro'yxati (sahifalangan) |
| `GET` | `/api/v1/chat/conversations/{id}/` | [detail.md](detail.md) | Bitta suhbat tafsiloti |
| `POST` | `/api/v1/chat/conversations/open/` | [open.md](open.md) | Mavjud 1:1 suhbatni topish yoki yangi ochish |
| `GET` | `/api/v1/chat/conversations/{id}/messages/` | [messages.md](messages.md) | Xabarlar ro'yxati (sahifalangan, eng eski birinchi); o'qilgan deb belgilaydi |
| `POST` | `/api/v1/chat/conversations/{id}/send/` | [send.md](send.md) | Xabar yuborish |

---

## WebSocket

| URL pattern | Fayl | Tavsif |
|---|---|---|
| `ws://<host>/ws/chat/{conversation_id}/?token=<access>` | [websocket.md](websocket.md) | Real vaqt hodisalar (message, typing, read) |

---

## Umumiy autentifikatsiya

Barcha endpointlar `Bearer JWT` talab qiladi:

```
Authorization: Bearer <access_token>
```

WebSocket uchun token query parametr sifatida uzatiladi:

```
ws://localhost:8000/ws/chat/12/?token=<access_token>
```

---

## Real vaqt hodisalar xulasasi

| Hodisa | Qayerdan keladi | Tavsif |
|---|---|---|
| `chat.message` | REST `/send/` yoki WS `action: "message"` | Yangi xabar barcha ulangan ishtirokchilarga broadcast |
| `chat.read` | REST `GET /messages/` yoki WS `action: "read"` | O'qilganlik holati broadcast |
| `chat.typing` | WS `action: "typing"` | Yozilmoqda belgisi broadcast |

---

## Yon ta'sirlar xulasasi

| Amal | Ta'sir |
|---|---|
| `GET /messages/` | Kiruvchi xabarlar o'qilgan deb belgilanadi; `unread_count = 0`; `chat.read` broadcast |
| `POST /send/` | Xabar yaratiladi; `last_message` yangilanadi; ikkinchi ishtirokchi `unread_count + 1`; `chat.message` broadcast; push bildiruv |
| WS `action: "message"` | Xabar yaratiladi; `last_message` yangilanadi; `unread_count + 1`; `chat.message` broadcast; push bildiruv |
| WS `action: "read"` | O'qilmagan xabarlar belgilanadi; `unread_count = 0`; `chat.read` broadcast |
| WS `action: "typing"` | Faqat `chat.typing` broadcast (hech narsa saqlanmaydi) |
