#!/bin/bash

exec 2>/dev/null

user=$1
workdir=$2
solveddir="/src/score/exercises/scripting2/solved"

[ -x ${workdir}/scripting2 ] && score=$(/src/score/exercises/scripting2/com.py <(${workdir}/scripting2) <(${solveddir}/scripting2) | wc -l) || score=0

cmp -s ${workdir}/jogos_nintendo ${solveddir}/jogos_nintendo && score=$((score+1))

cmp -s ${workdir}/jogos_open_world ${solveddir}/jogos_open_world && score=$((score+1))

cmp -s ${workdir}/jogos_shadow ${solveddir}/jogos_shadow && score=$((score+1)) 

chown $user jogos_nintendo
chown $user jogos_open_world
chown $user jogos_shadow

echo $score

