# Real-vaqt bildirishnomalar (WebSocket)

`WS /ws/notifications/`

| | |
|---|---|
| **Bo'lim** | Notifications |
| **Autentifikatsiya** | JWT — query-param `?token=<access_token>` yoki `Authorization: Bearer <access_token>` sarlavhasi |
| **Ruxsat** | Faqat autentifikatsiya qilingan foydalanuvchilar |
| **Protokol** | WebSocket (JSON xabarlar) |

## Tavsif

`NotificationConsumer` har bir foydalanuvchi uchun ajratilgan `user_<id>` guruhiga qo'shiladi. Server yangi bildirishnoma yoki o'qilmagan son o'zgarganda xabar yuboradi — mijozdan hech qanday kiruvchi xabar kutilmaydi (faqat o'qish rejimi).

Ulanish o'rnatilishi bilanoq server joriy o'qilmagan bildirishnomalar sonini yuboradi (`unread` eventi).

## Autentifikatsiya

`JWTAuthMiddleware` ikkita usulni qo'llab-quvvatlaydi (birinchi topilgan ishlatiladi):

1. **Query param (tavsiya etiladi):** `?token=<access_token>`
2. **HTTP sarlavha:** `Authorization: Bearer <access_token>` (ulanish bosqichida)

Token yaroqsiz yoki ko'rsatilmagan bo'lsa, ulanish darhol yopiladi (`close()`).

## URL

```
ws://localhost:8000/ws/notifications/?token=<access_token>
wss://example.com/ws/notifications/?token=<access_token>
```

## Server yuboradigan xabarlar

### `unread` — O'qilmagan bildirishnomalar soni

Ulanish o'rnatilganda va unread son o'zgarganda yuboriladi.

```json
{
  "event": "unread",
  "unread": 5
}
```

| Maydon | Tur | Tavsif |
|---|---|---|
| `event` | string | Har doim `"unread"` |
| `unread` | integer | Hozirgi o'qilmagan bildirishnomalar soni |

### `notify` — Yangi bildirishnoma

Foydalanuvchiga yangi bildirishnoma yaratilganda server `notify_message` handler orqali `event["payload"]` ni to'g'ridan-to'g'ri yuboradi. Payload tuzilishi server tomonida belgilanadi (odatda `NotificationSerializer` maydonlarini o'z ichiga oladi):

```json
{
  "event": "notify",
  "id": 18,
  "type": "chat",
  "type_display": "Xabar",
  "title": "Yangi xabar",
  "body": "Assalomu alaykum!",
  "data": { "chat_id": 7 },
  "read": false,
  "created_at": "2026-06-15T11:00:00Z"
}
```

> **Eslatma:** `notify_message` handler `event["payload"]` ni filtrsiz yuboradi. Aniq payload tuzilishi bildirishnoma yuboradigan servis (`notify()` funksiyasi yoki signal) tomonidan shakllantiriladi va yuqoridagi maydonlarni o'z ichiga olishi kutiladi.

## Mijozdan xabar yuborish

Kutilmaydi. Consumer kiruvchi xabarlarni qayta ishlamaydi.

## Ulanish va uzilish

| Holat | Tavsif |
|---|---|
| Ulanish muvaffaqiyatli | `unread` eventi darhol yuboriladi |
| Token yaroqsiz / ko'rsatilmagan | Ulanish darhol yopiladi |
| Uzilish | `user_<id>` guruhidan chiqariladi |

## Misol (JavaScript)

```javascript
const token = "<access_token>";
const ws = new WebSocket(`wss://example.com/ws/notifications/?token=${token}`);

ws.onopen = () => {
  console.log("Ulandi");
};

ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);

  if (msg.event === "unread") {
    // O'qilmagan son yangilash
    updateBadge(msg.unread);
  } else if (msg.event === "notify") {
    // Yangi bildirishnoma ko'rsatish
    showNotification(msg.title, msg.body);
    updateBadge((prev) => prev + 1);
  }
};

ws.onclose = (e) => {
  console.log("Uzildi, kod:", e.code);
};
```

## Misol (wscat CLI)

```bash
wscat -c "ws://localhost:8000/ws/notifications/?token=$ACCESS"
```
