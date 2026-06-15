# Auth & Accounts — Bo'lim indeksi

Bazaviy yo'l: `/api/v1/auth/`

Bu bo'lim autentifikatsiya, foydalanuvchi profili, sozlamalar, parol boshqaruvi va push qurilma tokenlarini qamrab oladi.

## Endpointlar

| Fayl | Method | Yo'l | Qisqa tavsif |
|---|---|---|---|
| [register.md](register.md) | `POST` | `register/` | Yangi hisob yaratish (+ emailga tasdiqlash kodi) |
| [verify-email.md](verify-email.md) | `POST` | `verify-email/` | 6 xonali kod bilan emailni tasdiqlash (+ auto-login) |
| [verify-email-resend.md](verify-email-resend.md) | `POST` | `verify-email/resend/` | Tasdiqlash kodini qayta yuborish |
| [login.md](login.md) | `POST` | `login/` | Tizimga kirish; `access` + `refresh` + `user` |
| [token-refresh.md](token-refresh.md) | `POST` | `token/refresh/` | Refresh token orqali yangi access olish |
| [logout.md](logout.md) | `POST` | `logout/` | Refresh tokenni blacklist qilish |
| [me.md](me.md) | `GET` `PATCH` | `me/` | O'z profil ma'lumotlarini o'qish/yangilash |
| [settings.md](settings.md) | `GET` `PATCH` | `settings/` | Bildirishnoma va interfeys sozlamalari |
| [password-change.md](password-change.md) | `POST` | `password/change/` | Joriy parolni o'zgartirish |
| [password-reset.md](password-reset.md) | `POST` | `password/reset/` | Parol tiklash kodini (6 xonali) email orqali yuborish |
| [password-reset-confirm.md](password-reset-confirm.md) | `POST` | `password/reset/confirm/` | email + kod bilan yangi parol o'rnatish |
| [devices.md](devices.md) | `GET` `POST` `PUT` `PATCH` `DELETE` | `devices/` | FCM qurilma tokenlarini boshqarish |

## Umumiy auth oqimi

```
1. POST /register/        → hisob yaratiladi (UserSummary) + emailga 6 xonali kod
2. POST /verify-email/    → email+kod → email_verified=True + access/refresh (auto-login)
   (ixtiyoriy: /verify-email/resend/ — kodni qayta yuborish)
3. POST /login/           → access + refresh tokenlar + UserSummary
4. Har so'rovda           → Authorization: Bearer <access>
5. access muddati o'tsa  → POST /token/refresh/ (refresh token bilan)
6. Chiqishda             → POST /logout/ (refresh tokenni blacklist)
```

> Eslatma: email tasdiqlanmagan bo'lsa ham login ishlaydi (`email_verified` `/me`'da ko'rinadi).

## Parol tiklash oqimi

```
1. POST /password/reset/          → emailga 6 xonali kod yuboriladi (15 daqiqa)
2. POST /password/reset/confirm/  → email + code + new_password
   → muvaffaqiyatda barcha mavjud refresh tokenlar bekor qilinadi
```

## Throttle sozlamalari

| Scope | Rate | Qo'llaniladi |
|---|---|---|
| `anon` | 60/min | Global anonim so'rovlar |
| `user` | 1000/min | Global autentifikatsiya qilingan so'rovlar |
| `login` | 10/min | `POST /login/` |
| `register` | 5/min | `POST /register/` |
| `password_reset` | 5/min | `POST /password/reset/` va `POST /password/reset/confirm/` |
| `email_verify` | 15/min | `POST /verify-email/` va `POST /verify-email/resend/` |

## JWT sozlamalari

| Parametr | Qiymat |
|---|---|
| `access` token muddati | 60 daqiqa (sozlanadi: `JWT_ACCESS_MINUTES`) |
| `refresh` token muddati | 14 kun (sozlanadi: `JWT_REFRESH_DAYS`) |
| Rotatsiya | Yoqilgan (`ROTATE_REFRESH_TOKENS=True`) |
| Blacklist | Yoqilgan (`BLACKLIST_AFTER_ROTATION=True`) |
