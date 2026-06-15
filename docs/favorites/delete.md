# Saqlangan ustani o'chirish

`DELETE /api/v1/favorites/{id}/`

| | |
|---|---|
| **Bo'lim** | Favorites |
| **Autentifikatsiya** | Bearer JWT |
| **Ruxsat** | IsAuthenticated; egasi (faqat o'z yozuvi) |
| **Sahifalash** | Yo'q |
| **Throttle** | yo'q |

## Tavsif

Autentifikatsiya qilingan foydalanuvchining saqlangan ustalar ro'yxatidan bitta yozuvni o'chiradi. `id` parametri `SavedMaster` yozuvining identifikatori — ustaning `id`si emas. Foydalanuvchi faqat o'ziga tegishli yozuvni o'chira oladi: boshqa foydalanuvchining yozuviga murojaat qilsa `404` qaytariladi (queryset foydalanuvchi bo'yicha filtrlanadi).

## So'rov

### Path parametrlari

| Parametr | Tur | Tavsif |
|---|---|---|
| `id` | integer | O'chiriladigan `SavedMaster` yozuvining identifikatori |

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
| `404` | Berilgan `id` topilmadi yoki foydalanuvchiga tegishli emas |

## Misol

```bash
curl -X DELETE "http://localhost:8000/api/v1/favorites/14/" \
  -H "Authorization: Bearer $ACCESS"
```
