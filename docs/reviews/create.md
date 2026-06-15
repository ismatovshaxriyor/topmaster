# Sharh yaratish

`POST /api/v1/reviews/`

| | |
|---|---|
| **Bo'lim** | Reviews |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | Rol: mijoz (IsClient) |
| **Sahifalash** | Yo'q |
| **Throttle** | user 1000/min |

## Tavsif

Yakunlangan buyurtmaga sharh qoldiradi. Faqat mijoz roli (`client`) ega
foydalanuvchilar chaqira oladi. Har bir buyurtmaga faqat bitta sharh qo'yish
mumkin — model darajasida `OneToOneField(job)` cheklovi bor; takror urinish
`400` qaytaradi.

Sharh muvaffaqiyatli yaratilganda ikki yon ta'sir sodir bo'ladi:

1. **Bildirishnoma:** ustaga `notify()` orqali "Yangi sharh" push-xabari
   yuboriladi (tur: `system`).
2. **Denormalizatsiya:** `post_save` signal usta profilida `rating_avg` va
   `reviews_count` maydonlarini qayta hisoblaydi va saqlaydi.

Sharh yozilganda `author` avtomatik joriy foydalanuvchidan olinadi; `master`
esa `job.assigned_master` dan olinadi — ikkalasi ham so'rov tanasida
yuborilmaydi.

## So'rov

### Path parametrlari

Yo'q.

### Query parametrlari

Yo'q.

### Tana (request body)

`Content-Type: application/json`

| Maydon | Tur | Majburiy | Tavsif |
|---|---|---|---|
| `job` | integer | Ha | Buyurtma ID'si. Faqat `status=completed`, joriy foydalanuvchi — shu buyurtma mijozi, va ustasi biriktirilgan bo'lishi shart |
| `rating` | integer | Ha | Baho: 1 dan 5 gacha (inklyuziv) |
| `text` | string | Yo'q | Sharh matni; bo'sh string ham qabul qilinadi |
| `recommend` | boolean | Yo'q | Ustani tavsiya qiladimi (standart: `true`) |

**Validatsiya qoidalari:**

- `job` joriy foydalanuvchiga tegishli bo'lishi kerak — boshqaning buyurtmasiga
  sharh qoldirib bo'lmaydi (`400`).
- `job.status` `completed` bo'lishi shart (`400`).
- `job.assigned_master` null bo'lmasligi kerak (`400`).
- Shu buyurtmaga allaqachon sharh qoldirilgan bo'lsa, serializer yoki DB
  constraint `400` qaytaradi.

## Javob

### `201 Created`

Javob `ReviewSerializer` formatida qaytadi (so'rov formatidan farqli — kengaytirilgan).

```json
{
  "id": 17,
  "author": {
    "id": 5,
    "full_name": "Aziza Karimova",
    "role": "client",
    "is_verified": true,
    "avatar": "http://localhost:8000/media/avatars/aziza.jpg",
    "city": {
      "id": 1,
      "name": "Toshkent",
      "slug": "toshkent",
      "latitude": 41.2995,
      "longitude": 69.2401
    }
  },
  "master": 3,
  "rating": 5,
  "text": "Juda yaxshi usta, vaqtida keldi va sifatli ish qildi.",
  "recommend": true,
  "created_at": "2024-11-20T14:32:00Z"
}
```

### Xato javoblari

| Kod | Sabab |
|---|---|
| `400` | `job` topilmadi, yoki boshqaning buyurtmasi, yoki yakunlanmagan, yoki usta biriktirilmagan, yoki bu buyurtmaga allaqachon sharh qoldirilgan |
| `401` | Autentifikatsiya talab qilinadi |
| `403` | Foydalanuvchi roli `client` emas |
| `429` | So'rovlar limiti oshib ketdi |

**400 xatolariga misollar:**

```json
{ "job": ["Bu buyurtmaga allaqachon sharh qoldirilgan."] }
{ "job": ["Faqat o'z buyurtmangizga sharh qoldira olasiz."] }
{ "job": ["Sharh faqat yakunlangan buyurtmaga qoldiriladi."] }
{ "job": ["Buyurtmaga usta biriktirilmagan."] }
```

## Misol

```bash
curl -X POST "http://localhost:8000/api/v1/reviews/" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "job": 12,
    "rating": 5,
    "text": "Juda yaxshi usta, vaqtida keldi va sifatli ish qildi.",
    "recommend": true
  }'
```
