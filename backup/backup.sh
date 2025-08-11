#!/bin/bash
# backup/backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="spider"
DB_USER="spider"
CONTAINER="spider-osint-db-1"

mkdir -p $BACKUP_DIR

docker exec -t $CONTAINER pg_dump -U $DB_USER -d $DB_NAME | gzip > "$BACKUP_DIR/spider_$DATE.sql.gz"

# Удаляем бэкапы старше 7 дней
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "✅ Бэкап создан: spider_$DATE.sql.gz"