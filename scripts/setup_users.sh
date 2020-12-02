#!/bin/bash

echo root:${PASS} | chpasswd

if [ -s /opt/etc/passwd ]
then
   /scripts/restore_users.sh
fi

cat /config/users.txt | while read user 
do
   useradd -s /bin/bash -m $user

   if [ $? -eq 0 ]
   then
      /scripts/reset_password.sh $user
   fi
done
