.PHONY: help db-clear createsuperuser db-clear-local createsuperuser-local up down

help:
	@echo "Bajarilishi mumkin bo'lgan buyruqlar:"
	@echo "  make db-clear             - Ma'lumotlar bazasini tozalash (Docker orqali)"
	@echo "  make createsuperuser      - Superuser yaratish (Docker orqali)"
	@echo "  make db-clear-local       - Ma'lumotlar bazasini tozalash (Lokal muhitda)"
	@echo "  make createsuperuser-local- Superuser yaratish (Lokal muhitda)"
	@echo "  make up                   - Docker konteynerlarni ishga tushirish"
	@echo "  make down                 - Docker konteynerlarni to'xtatish"

# Docker yordamida (Asosiy)
db-clear:
	docker compose exec web python manage.py flush --no-input
	@echo "Ma'lumotlar bazasi tozalandi (Docker)."

createsuperuser:
	docker compose exec web python manage.py createsuperuser

# Lokal Python yordamida (Agar Dockersiz ishlayotgan bo'lsangiz)
db-clear-local:
	python manage.py flush --no-input
	@echo "Ma'lumotlar bazasi tozalandi (Lokal)."

createsuperuser-local:
	python manage.py createsuperuser

# Qulaylik uchun Docker buyruqlari
up:
	docker compose up -d

down:
	docker compose down
