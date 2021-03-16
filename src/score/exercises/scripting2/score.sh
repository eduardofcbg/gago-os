#!/bin/bash

exec 2> /dev/null

workdir=$1
solveddir="/src/score/exercises/scripting2/solved"

if cmp -s -- <(${workdir}/scripting2) <(${solveddir}/scripting2); then
  # Identical output
  score=$(bash ${solveddir}/scripting2 | wc -l)
elif [[ -x ${workdir}/scripting2 ]]; then
  # Different output
  score=$(./com.py <(${workdir}/scripting2) <(${solveddir}/scripting2) | wc -l)
else
  # Script does not exist or not exacutable
  score=0
fi


cmp -s ${workdir}/jogos_nintendo ${solveddir}/jogos_nintendo && score=$((score+1))

cmp -s ${workdir}/jogos_open_world ${solveddir}/jogos_open_world && score=$((score+1))

cmp -s ${workdir}/jogos_shadow ${solveddir}/jogos_shadow && score=$((score+1)) 

echo $score
