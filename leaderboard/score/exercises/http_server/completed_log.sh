#!/bin/bash

set -e

exec 2>/dev/null

which nginx

systemctl is-active nginx --quiet && echo "nginx started"

cat /var/www/html/index.nginx-debian.html | grep -i amigos | head -1

ls /var/www/html/bem-vindos.html

cat /var/www/html/bem-vindos.html | grep -i site | head -1

ls /var/www/html/eu.html

cat /var/www/html/eu.html | grep -i sou | head -1

cat /var/www/html/index.nginx-debian.html | grep -E 'href="\/?bem-vindos.html"' | grep -i "Boas-vindas" | head -1

cat /var/www/html/index.nginx-debian.html | grep -E 'href="\/?eu.html"' | grep -i "Mais sobre mim" | head -1

cat /var/www/html/bem-vindos.html | grep -E 'href="\/"' | head -1

cat /var/www/html/eu.html | grep -E 'href="\/"' | head -1
