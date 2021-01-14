#!/bin/sh

cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
echo "Europe/Moscow" > /etc/timezone

cd /app
python3 main.py
