#!/bin/bash

set -e

exec 2>/dev/null

which nginx

systemctl is-active nginx --quiet && echo "nginx started"

cat /var/www/html/index.nginx-debian.html | grep -i amigos

ls /var/www/html/bem-vindos.html

cat /var/www/html/bem-vindos.html | grep -i site

ls /var/www/html/eu.html

cat /var/www/html/eu.html | grep -i sou

cat /var/www/html/index.nginx-debian.html | grep -E 'href="\/?bem-vindos.html"' | grep -i "Boas-vindas"

cat /var/www/html/index.nginx-debian.html | grep -E 'href="\/?eu.html"' | grep -i "Mais sobre mim"

cat /var/www/html/bem-vindos.html | grep -E 'href="\/"'

cat /var/www/html/eu.html | grep -E 'href="\/"'
