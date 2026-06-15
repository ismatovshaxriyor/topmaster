# TopMaster — AWS EC2 ga deploy qilish

Bu qo'llanma loyihani **bitta AWS EC2** serveriga joylashtirish, **topmaster.ismatov.uz**
domenini HTTPS bilan ulash va **GitHub Actions CI/CD**ni sozlashni qadam-baqadam
ko'rsatadi.

## Arxitektura

Hammasi bitta EC2'da Docker Compose orqali ishlaydi:

```
Internet ──▶ Nginx (:80/:443, Let's Encrypt TLS)
                 ├─ /                → web (gunicorn+uvicorn, Django ASGI)  ──▶ Postgres
                 │                                                          ──▶ Redis (Channels/Celery/cache)
                 ├─ /ws/...          → web (WebSocket)
                 └─ /topmaster-media/→ MinIO (fayllar)
             celery_worker, celery_beat ──▶ Redis + Postgres
             certbot (sertifikatni avtomatik yangilaydi)
```

Faqat **80** va **443** portlari tashqariga ochiq. Postgres/Redis/MinIO faqat
ichki Docker tarmog'ida.

---

## 0. Talablar

- AWS akkaunt (EC2 + Elastic IP).
- `ismatov.uz` domenining DNS boshqaruviga kirish (A yozuvi qo'shish uchun).
- Mahalliy kompyuterda SSH va `git`.
- Kod GitHub'da (pastdagi "CI/CD" bo'limiga qarang).

---

## 1. EC2 instance yaratish

AWS Console → EC2 → **Launch instance**:

| Sozlama | Tavsiya |
|---|---|
| Name | `topmaster-prod` |
| AMI | **Ubuntu Server 24.04 LTS** (x86_64) |
| Instance type | **t3.medium** (4 GB) tavsiya · `t3.small` (2 GB) minimum |
| Key pair | yangi yarating (`topmaster-key.pem`) yoki mavjudini tanlang |
| Storage | **30 GB gp3** |
| Region | Foydalanuvchilarga yaqin: `me-central-1` (BAA) yoki `eu-central-1` (Frankfurt) |

> Postgres + Redis + MinIO + Django + Celery + Nginx bitta serverda — shuning uchun
> 2 GB juda kam, 4 GB qulayroq.

---

## 2. Security group (xavfsizlik guruhi)

Instance'ning security group'iga **inbound** qoidalar:

| Tur | Port | Manba | Izoh |
|---|---|---|---|
| SSH | 22 | **Mening IP'im** (My IP) | faqat o'zingiz; `0.0.0.0/0` qo'ymang |
| HTTP | 80 | `0.0.0.0/0` | TLS sertifikat + redirect |
| HTTPS | 443 | `0.0.0.0/0` | asosiy trafik |

Postgres/Redis/MinIO portlarini **ochmang** — ular ichki tarmoqda.

---

## 3. Elastic IP (o'zgarmas IP)

EC2 → **Elastic IPs** → Allocate → instance'ga **Associate** qiling. Bu IP domen
uchun ishlatiladi va instance qayta ishga tushganda o'zgarmaydi. Masalan: `203.0.113.45`.

---

## 4. DNS — topmaster.ismatov.uz

`ismatov.uz` DNS boshqaruvida (Cloudflare / Route 53 / registrator panelida) **A yozuvi**:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `topmaster` | `<Elastic IP>` | 300 |

Tekshirish (bir necha daqiqadan keyin):

```bash
dig +short topmaster.ismatov.uz   # Elastic IP'ni qaytarishi kerak
```

> Cloudflare ishlatsangiz, sertifikat olish paytida **proxy (to'q sariq bulut)ni
> o'chirib** (DNS only, kulrang) qo'ying; cert olingach yoqsangiz bo'ladi.

---

## 5. Serverga ulanish + Docker o'rnatish

```bash
chmod 400 topmaster-key.pem
ssh -i topmaster-key.pem ubuntu@<Elastic IP>
```

Server ichida:

```bash
# Docker + Compose plugin
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
# Guruh o'zgarishi kuchga kirishi uchun qaytadan kiring:
exit
ssh -i topmaster-key.pem ubuntu@<Elastic IP>

docker --version && docker compose version   # tekshirish
```

---

## 6. Repozitoriyni klonlash + .env

```bash
sudo mkdir -p /opt/topmaster && sudo chown ubuntu:ubuntu /opt/topmaster
git clone <SIZNING_GITHUB_REPO_URL> /opt/topmaster
cd /opt/topmaster

cp .env.prod.example .env
# SECRET_KEY yarating:
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
nano .env   # SECRET_KEY, POSTGRES_PASSWORD, MINIO_ROOT_PASSWORD ni to'ldiring
```

`.env`'da kamida shularni o'zgartiring:
- `SECRET_KEY` — yuqorida yaratilgan satr
- `POSTGRES_PASSWORD` — kuchli parol
- `MINIO_ROOT_PASSWORD` — kuchli parol
- `ALLOWED_HOSTS=topmaster.ismatov.uz` (allaqachon shunday)

> `.env` hech qachon git'ga tushmaydi (`.gitignore`da).

---

## 7. Birinchi deploy (TLS'siz, ilovani ko'tarish)

Avval nginx/certbot'siz qolgan hammasini ko'taramiz:

```bash
cd /opt/topmaster
docker compose -f docker-compose.prod.yml up -d --build \
  db redis minio minio-init web celery_worker celery_beat
```

Web "healthy" bo'lguncha kuting (migratsiya + collectstatic + seed avtomatik ishlaydi):

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f web   # Ctrl+C bilan chiqing
```

---

## 8. HTTPS sertifikat (Let's Encrypt)

DNS allaqachon serverga ishora qilayotganiga ishonch hosil qiling (4-qadam), keyin:

```bash
chmod +x deploy/init-letsencrypt.sh scripts/*.sh
LETSENCRYPT_EMAIL=siz@example.com ./deploy/init-letsencrypt.sh
```

Skript: vaqtinchalik sertifikat yaratadi → Nginx'ni ishga tushiradi → haqiqiy
Let's Encrypt sertifikatini oladi → Nginx'ni qayta yuklaydi.

> Avval sinab ko'rish uchun (rate-limit'ga tushmaslik): `STAGING=1 LETSENCRYPT_EMAIL=... ./deploy/init-letsencrypt.sh`, so'ng `STAGING`'siz qayta ishga tushiring.

Endi butun stack'ni (certbot yangilovchisi bilan) ko'taring:

```bash
docker compose -f docker-compose.prod.yml up -d
```

Sertifikat **avtomatik yangilanadi** (certbot har 12 soatda tekshiradi, nginx har 6 soatda reload qiladi).

---

## 9. Tekshirish + superuser

```bash
curl -s https://topmaster.ismatov.uz/health/        # {"status":"ok",...}
# Brauzerda: https://topmaster.ismatov.uz/api/docs/  (Swagger)
#            https://topmaster.ismatov.uz/admin/     (admin panel)

# Admin foydalanuvchi:
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# (ixtiyoriy) demo ma'lumotlar:
docker compose -f docker-compose.prod.yml exec web python manage.py seed_demo
```

---

## 10. CI/CD — har push'da avtomatik deploy

Workflow: `.github/workflows/deploy.yml` — `main`'ga push bo'lganda testlar o'tadi,
so'ng EC2'ga SSH orqali `scripts/deploy.sh` ishlaydi (`git pull` + rebuild).

### 10.1. Deploy uchun SSH kalit yarating (mahalliy kompyuterda)

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f topmaster_deploy_key -N ""
# Ikki fayl: topmaster_deploy_key (private), topmaster_deploy_key.pub (public)
```

Public kalitni serverga qo'shing:

```bash
ssh-copy-id -i topmaster_deploy_key.pub ubuntu@<Elastic IP>
# yoki qo'lda: public kalitni serverdagi ~/.ssh/authorized_keys ga qo'shing
```

### 10.2. GitHub Secrets

GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret nomi | Qiymat |
|---|---|
| `EC2_HOST` | `<Elastic IP>` yoki `topmaster.ismatov.uz` |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | **private** kalit (`topmaster_deploy_key`) to'liq matni |
| `EC2_SSH_PORT` | `22` (ixtiyoriy) |

### 10.3. Ishlatish

`main` branch'ga push qiling → Actions test o'tkazadi → muvaffaqiyatli bo'lsa
serverda `git pull` + rebuild + healthcheck avtomatik bajariladi.

> Server `git pull` qila olishi uchun repo public bo'lishi yoki serverda repoga
> o'qish huquqi (deploy key / HTTPS token) bo'lishi kerak. Private repo bo'lsa:
> serverda alohida read-only **deploy key** sozlang (GitHub repo → Settings → Deploy keys).

---

## Operatsiyalar (kundalik)

```bash
cd /opt/topmaster

# Loglar
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml logs -f nginx

# Qayta ishga tushirish
docker compose -f docker-compose.prod.yml restart web

# Holat
docker compose -f docker-compose.prod.yml ps

# Qo'lda deploy (CI'siz)
./scripts/deploy.sh

# DB zaxira nusxasi (backup)
docker compose -f docker-compose.prod.yml exec -T db \
  pg_dump -U topmaster topmaster | gzip > backup_$(date +%F).sql.gz

# DB tiklash
gunzip -c backup_YYYY-MM-DD.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T db psql -U topmaster -d topmaster
```

> **Tavsiya:** `pg_dump` backup'ini cron orqali kunlik bajaring va S3/boshqa joyga nusxalang.

---

## Xavfsizlik eslatmalari

- `.env` faqat serverda; kuchli, takrorlanmas parollar.
- SSH 22 faqat o'z IP'ingizdan; parol bilan emas, kalit bilan kiring.
- MinIO konsoli (9001) tashqariga ochiq emas — kerak bo'lsa SSH tunnel:
  `ssh -i key.pem -L 9001:localhost:9001 ubuntu@<IP>` so'ng `http://localhost:9001`.
- Tizimni yangilab turing: `sudo apt update && sudo apt upgrade -y`.
- `DEBUG=False` (prod settings allaqachon shunday).

---

## Troubleshooting

| Muammo | Yechim |
|---|---|
| `init-letsencrypt.sh` xato beradi | DNS hali tarqalmagan bo'lishi mumkin (`dig +short topmaster.ismatov.uz`); 80-port ochiqligini tekshiring; avval `STAGING=1` bilan sinang |
| Nginx ishlamayapti (`no such file ... fullchain.pem`) | 8-qadam (init-letsencrypt) bajarilmagan — sertifikat yo'q |
| 502 Bad Gateway | `web` healthy emas: `docker compose -f docker-compose.prod.yml logs web` |
| Rasm/fayl ko'rinmayapti | `.env`'da `MINIO_PUBLIC_DOMAIN=topmaster.ismatov.uz/topmaster-media` to'g'riligini, bucket "download" public ekanligini tekshiring (`minio-init` log) |
| WebSocket ulanmayapti | `wss://topmaster.ismatov.uz/ws/...?token=<access>` ishlating (http emas, wss) |
| Migratsiya ishlamadi | `docker compose -f docker-compose.prod.yml exec web python manage.py migrate` |
