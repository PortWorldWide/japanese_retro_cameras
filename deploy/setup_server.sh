#!/bin/bash
# Скрипт первичной настройки на Ubuntu 22.04/24.04 VPS.
# Запуск: sudo bash deploy/setup_server.sh

set -e

PROJECT_DIR="/var/www/japanese_retro_cameras"
DOMAIN="${1:-your-domain.ru}"

echo "=== Установка системных пакетов ==="
apt update
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx

echo "=== Создание директории проекта ==="
mkdir -p "$PROJECT_DIR"
chown -R $SUDO_USER:$SUDO_USER "$PROJECT_DIR" 2>/dev/null || true

echo ""
echo "Дальше выполните вручную:"
echo ""
echo "1. Загрузите файлы проекта в $PROJECT_DIR (без папки venv)"
echo "2. cd $PROJECT_DIR"
echo "3. python3 -m venv venv && source venv/bin/activate"
echo "4. pip install -r requirements.txt"
echo "5. cp .env.example .env  # и отредактируйте .env"
echo "6. python manage.py migrate"
echo "7. python manage.py collectstatic --noinput"
echo "8. python manage.py init_site  # данные, фото и admin из переменных окружения"
echo ""
echo "10. sudo cp deploy/gunicorn.service.example /etc/systemd/system/retro_cameras.service"
echo "    sudo sed -i 's|/var/www/japanese_retro_cameras|$PROJECT_DIR|g' /etc/systemd/system/retro_cameras.service"
echo "11. sudo systemctl enable retro_cameras && sudo systemctl start retro_cameras"
echo "12. sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/retro_cameras"
echo "    sudo sed -i 's|your-domain.ru|$DOMAIN|g' /etc/nginx/sites-available/retro_cameras"
echo "    sudo sed -i 's|/var/www/japanese_retro_cameras|$PROJECT_DIR|g' /etc/nginx/sites-available/retro_cameras"
echo "    sudo ln -sf /etc/nginx/sites-available/retro_cameras /etc/nginx/sites-enabled/"
echo "    sudo nginx -t && sudo systemctl reload nginx"
echo "13. sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "Админ-панель: https://$DOMAIN/admin/"
