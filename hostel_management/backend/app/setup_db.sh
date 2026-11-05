#!/usr/bin/env bash
# Run once as root:  sudo bash setup_db.sh
set -e

APP_DIR="/home/neeraj/Documents/hostel_management/backend/app"
DB_USER="hostel"
DB_PASS="hostelapp_9f3k2m"
DB_NAME="hostel_db"

mariadb <<SQL
DROP USER IF EXISTS 'hostel@localhost';
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
ALTER USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL

TABLES=$(mariadb -N -B -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME' AND table_name='users';")
if [ "$TABLES" = "0" ]; then
    mariadb < "$APP_DIR/schema.sql"
    echo "Loaded schema.sql"
else
    echo "Tables already exist, skipped schema.sql"
fi

echo "Database user '$DB_USER' is ready."
