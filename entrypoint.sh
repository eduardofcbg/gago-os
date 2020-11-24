#!/bin/bash

/scripts/setup_users.sh

stop() {
  echo "Received SIGINT or SIGTERM. Will shut down $DAEMON"
  
  /scripts/save_users.sh
  
  pid=$(cat /var/run/sshd/sshd.pid)
  kill -SIGTERM "${pid}"
  wait "${pid}"
}

echo "Starting sshd"
trap stop SIGINT SIGTERM

/usr/sbin/sshd -D -e & pid="$!"
echo "${pid}" > /var/run/sshd/sshd.pid
wait "${pid}" && exit $?

