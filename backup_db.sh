#!/bin/bash
IMAGE=2b4b84e2cf3b
TIMESTAMP=$(date +%Y%m%d)
WORKDIR='/home/splitgal4_org'
BKUPPATH='/home/chenyenjung/splitgal4_org/backup'

sudo docker exec ${IMAGE} bash -c 'python manage.py dumpdata --indent 2 | gzip > bkup.json.gz'
sudo docker cp ${IMAGE}:${WORKDIR}/bkup.json.gz ${BKUPPATH}/${TIMESTAMP}.json.gz
sudo docker exec ${IMAGE} bash -c 'rm bkup.json.gz'
