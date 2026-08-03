# WebSocket: Real vaqt chat

`WS /ws/chat/{conversation_id}/`

| | |
|---|---|
| **Bo'lim** | Chat |
| **Autentifikatsiya** | JWT — `?token=<access_token>` query parametri (`JWTAuthMiddleware`) |
| **Ruxsat** | Faqat suhbat ishtirokchisi; aks holda ulanish yopiladi |
| **Protokol** | `AsyncJsonWebsocketConsumer` (Django Channels) |
| **Guruh** | `chat_<conversation_id>` — ikki tomonlama broadcast |

## Tavsif

Suhbat uchun doimiy WebSocket ulanishi o'rnatadi. Bir suhbatga har ikkala ishtirokchi alohida ulanishi mumkin — ular bir `chat_<conversation_id>` guruhiga qo'shiladi va hodisalar ikkalasiga ham broadcast qilinadi.

**Autentifikatsiya mexanizmi (`JWTAuthMiddleware`):**

1. `?token=<access_token>` query parametri tekshiriladi.
2. Topilmasa — `Authorization: Bearer <token>` sarlavhasi tekshiriladi.
3. Token noto'g'ri yoki yo'q bo'lsa — `scope["user"]` `AnonymousUser` ga tenglashadi va consumer ulanishni yopadi.

**Ulanish tekshiruvi (consumer `connect`):**

1. Foydalanuvchi autentifikatsiyadan o'tganmi — yo'q bo'lsa yopiladi.
2. Foydalanuvchi suhbatning ishtirokchisimi (`ConversationParticipant`) — yo'q bo'lsa yopiladi.

## Ulanish

```
ws://localhost:8000/ws/chat/12/?token=<access_token>
```

```javascript
const ws = new WebSocket(
  `ws://localhost:8000/ws/chat/12/?token=${accessToken}`
);
```

## Mijozdan serverga yuboriladigan hodisalar (receive)

Barcha xabarlar JSON formatida yuboriladi. `action` maydoni hodisa turini belgilaydi.

### `action: "message"` — xabar yuborish

Yangi matnli xabar jo'natadi. Matn bo'sh bo'lsa, server uni e'tiborsiz qoldiradi.

```json
{
  "action": "message",
  "text": "Salom, qachon bo'shasiz?"
}
```

**Ta'sirlar:**
- Xabar ma'lumotlar bazasiga saqlonadi (`Message.type = "text"`).
- `Conversation.last_message` va `updated_at` yangilanadi.
- Ikkinchi ishtirokchining `unread_count` bittaga oshiriladi.
- `chat.message` hodisasi guruhga broadcast qilinadi.
- Ikkinchi ishtirokchiga push bildiruv yuboriladi (`type="chat"`).

---

### `action: "typing"` — yozilmoqda belgisi

Foydalanuvchi hozir yozayotganini boshqa ishtirokchiga bildiradi. Hech qanday ma'lumot saqlanmaydi — faqat broadcast.

```json
{
  "action": "typing"
}
```

**Ta'sirlar:**
- `chat.typing` hodisasi guruhga broadcast qilinadi.

---

### `action: "read"` — xabarlarni o'qilgan deb belgilash

Joriy foydalanuvchi uchun kiruvchi o'qilmagan xabarlarni o'qilgan deb belgilaydi.

```json
{
  "action": "read"
}
```

**Ta'sirlar:**
- Kiruvchi `read_at IS NULL` xabarlar `read_at = now()` bilan yangilanadi.
- `ConversationParticipant.unread_count = 0`, `last_read_at = now()`.
- `chat.read` hodisasi guruhga broadcast qilinadi.

---

## Serverdan mijozga yuboriladigan hodisalar (send)

Server JSON formatida hodisa yuboradi. `event` maydoni hodisa turini belgilaydi.

### `event: "message"` — yangi xabar

Yangi xabar kelganida — REST `/send/` yoki WS `action: "message"` orqali — guruhning barcha ulanishlariga yuboriladi.

```json
{
  "event": "message",
  "conversation_id": 12,
  "message": {
    "id": 89,
    "sender": 3,
    "sender_name": "Alisher Umarov",
    "type": "text",
    "text": "Salom, qachon bo'shasiz?",
    "attachment": null,
    "created_at": "2026-06-15T11:05:00Z",
    "read_at": null,
    "is_mine": false
  }
}
```

> **Eslatma:** `is_mine` maydoni WS orqali yuborilganda `false` bo'ladi, chunki serializer kontekstida `request` obyekti mavjud emas. REST `/send/` javobi esa jo'natuvchi uchun `is_mine: true` qaytaradi.

---

### `event: "typing"` — yozilmoqda belgisi

Ikkinchi ishtirokchi yozayotganida broadcast qilinadi.

```json
{
  "event": "typing",
  "conversation_id": 12,
  "user_id": 7
}
```

---

### `event: "read"` — o'qilganlik holati

Bir ishtirokchi xabarlarni o'qiganda (WS `action: "read"` yoki REST `GET /messages/`) guruhga broadcast qilinadi.

```json
{
  "event": "read",
  "conversation_id": 12,
  "user_id": 3
}
```

---

## Ulanish to'xtatilishi (disconnect)

Consumer `disconnect` hodisasida `chat_<conversation_id>` guruhidan chiqadi. Hech qanday ma'lumot o'zgartirilmaydi.

## Xatolar

| Holat | Natija |
|---|---|
| Token yo'q yoki noto'g'ri | Ulanish qabul qilinmaydi (yopiladi) |
| Foydalanuvchi suhbat ishtirokchisi emas | Ulanish qabul qilinmaydi (yopiladi) |
| Noto'g'ri `action` | Server e'tiborsiz qoldiradi |
| `action: "message"` bilan bo'sh `text` | Server e'tiborsiz qoldiradi |

## To'liq misol (JavaScript)

```javascript
const ws = new WebSocket(
  `ws://localhost:8000/ws/chat/12/?token=${accessToken}`
);

ws.onopen = () => {
  // Yozilmoqda belgisi
  ws.send(JSON.stringify({ action: "typing" }));

  // Xabar yuborish
  ws.send(JSON.stringify({ action: "message", text: "Salom!" }));
};

ws.onmessage = (e) => {
  const payload = JSON.parse(e.data);
  switch (payload.event) {
    case "message":
      console.log("Yangi xabar:", payload.message);
      // O'qilgan deb belgilash
      ws.send(JSON.stringify({ action: "read" }));
      break;
    case "typing":
      console.log(`Foydalanuvchi ${payload.user_id} yozmoqda...`);
      break;
    case "read":
      console.log(`Foydalanuvchi ${payload.user_id} xabarlarni o'qidi`);
      break;
  }
};
```
