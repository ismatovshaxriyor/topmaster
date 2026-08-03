# Notifications bo'limi

Foydalanuvchiga tegishli barcha bildirishnomalar (in-app) va real-vaqt WebSocket oqimi.

**Bazaviy REST URL:** `/api/v1/notifications/`
**WebSocket URL:** `ws://<host>/ws/notifications/?token=<access_token>`

Barcha endpointlar `IsAuthenticated` — foydalanuvchi faqat o'z bildirishnomalarini ko'ra oladi.

## Bildirishnoma turlari (`type`)

| Qiymat | Tavsif |
|---|---|
| `order` | Yangi buyurtma |
| `accepted` | Taklif yoki buyurtma qabul qilindi |
| `rejected` | Taklif yoki buyurtma rad etildi |
| `chat` | Yangi chat xabari |
| `system` | Tizim xabari |

## Endpointlar

| Metod | URL | Fayl | Tavsif |
|---|---|---|---|
| `GET` | `/api/v1/notifications/` | [list.md](list.md) | Barcha bildirishnomalarni sahifalab olish |
| `GET` | `/api/v1/notifications/unread_count/` | [unread-count.md](unread-count.md) | O'qilmagan bildirishnomalar soni |
| `POST` | `/api/v1/notifications/{id}/mark_read/` | [mark-read.md](mark-read.md) | Bitta bildirishnomani o'qilgan deb belgilash |
| `POST` | `/api/v1/notifications/mark_all_read/` | [mark-all-read.md](mark-all-read.md) | Barchasini o'qilgan deb belgilash |
| `WS` | `/ws/notifications/` | [websocket.md](websocket.md) | Real-vaqt bildirishnoma oqimi |
