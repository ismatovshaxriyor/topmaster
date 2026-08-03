# Qo'llab-quvvatlashga xabar yuborish

`POST /api/v1/support/chat/send/`

| | |
|---|---|
| **Bo'lim** | Support |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated |
| **Sahifalash** | Yo'q |
| **Throttle** | support_send: 30/min |

## Tavsif

Foydalanuvchi tomonidan qo'llab-quvvatlash jamoasiga xabar yuboradi. Agar foydalanuvchining faol (`open` yoki `pending`) threadi mavjud bo'lsa, xabar shu threadga qo'shiladi; aks holda yangi thread yaratiladi. Agar thread avval `resolved` yoki `closed` holatda bo'lsa, endpoint yangi thread ochadi. Xabar yuborilgandan so'ng thread holati `open` ga o'rnatiladi (to'pi xodim tomonida) va xodimlar tomonidagi o'qilmagan xabarlar hisoblagichi (`staff_unread`) 1 ga oshiriladi. `subject` maydoni faqat thread yaratilayotganda yoki mavzusi bo'sh bo'lganda qabul qilinadi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `text` | string | Ha | Xabar matni (bo'sh bo'lmasligi kerak; bosh-dum bo'shliqlar avtomatik kesiladi) |
| `subject` | string | Yo'q | Murojaat mavzusi — maksimal 160 belgi. Agar thread allaqachon mavjud bo'lsa va uning mavzusi bo'sh bo'lmasa, e'tiborga olinmaydi |

## Javob

### `201 Created`

```json
{
  "id": 18,
  "is_staff": false,
  "text": "Profilimni tahrirlashda xatolik chiqyapti.",
  "attachment": null,
  "read_at": null,
  "created_at": "2026-06-15T10:00:00Z"
}
```

Yangi yaratilgan `SupportMessage` ob'ekti qaytariladi.

**Asosiy maydonlar:**

| Maydon | Tavsif |
|---|---|
| `id` | Yangi xabarning identifikatori |
| `is_staff` | Har doim `false` — foydalanuvchi xabari |
| `text` | Yuborilgan xabar matni |
| `attachment` | Har doim `null` — bu endpoint orqali fayl yuklash qo'llab-quvvatlanmaydi |
| `read_at` | Har doim `null` — yangi xabar hali o'qilmagan |

**Yon ta'sirlar:**

- Thread holati `open` ga o'rnatiladi (agar `resolved`/`closed` bo'lsa qayta ochiladi).
- `staff_unread` hisoblagichi 1 ga oshiriladi.
- Thread `last_message` maydoni yangi xabarni ko'rsatadi.

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `text` maydoni bo'sh yoki berilmagan |
| `401` | Autentifikatsiya talab qilinadi |
| `429` | Limitdan oshildi — 30 xabardan ortiq/daqiqa |

## Misol

```bash
# Birinchi xabar (yangi thread ochadi)
curl -X POST "http://localhost:8000/api/v1/support/chat/send/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"text": "Profilimni tahrirlashda xatolik chiqyapti.", "subject": "Profil muammosi"}'

# Mavjud threadga xabar
curl -X POST "http://localhost:8000/api/v1/support/chat/send/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"text": "Muammo hali ham davom etyapti."}'
```
