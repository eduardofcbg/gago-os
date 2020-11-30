#!/bin/bash

stop() {
  echo "Received SIGINT or SIGTERM. Will shut down $DAEMON"
    
  pid=$(cat /var/run/sshd/sshd.pid)
  kill -SIGTERM "${pid}"
  wait "${pid}"
}

/scripts/setup_users.sh

echo "Starting sshd"
trap stop SIGINT SIGTERM

/usr/sbin/sshd -D -e & pid="$!"
echo "${pid}" > /var/run/sshd/sshd.pid
wait "${pid}" && sshd_exit_code=$?

/scripts/save_users.sh
exit $sshd_exit_code
