#!/bin/bash
TIMESTAMP=$(date +%Y%m%d)
BKUPPATH='/home/chenyenjung/splitgal4_org/backup'
SITEPATH='/home/chenyenjung/splitgal4_org/splitgal4.org/'

cd ${SITEPATH}
sudo docker compose exec web python manage.py dumpdata --indent 2 | gzip > ${BKUPPATH}/${TIMESTAMP}.json.gz
# Also backup the actual sqlite file (belt and suspenders)
cp db.sqlite3 ${BKUPPATH}/db_${TIMESTAMP}.sqlite3
