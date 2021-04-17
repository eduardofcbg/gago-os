#!/bin/bash

cp -p /opt/etc/{passwd,group,shadow,gshadow} /etc/

cat /config/users.txt | while read user
do
   mkdir -p /home/$user
done

echo "Users restored"
