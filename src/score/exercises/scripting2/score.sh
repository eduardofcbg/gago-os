#!/bin/bash

workdir=$1
solveddir="/src/score/exercises/scripting2/solved"

score=$(cmp <(${workdir}/scripting1) <(${solveddir}/scripting1) && bash ${solveddir}/scripting1 | wc -l || awk '{print $NF-1}')

cmp -s ${workdir}/jogos_nintendo ${solveddir}/jogos_nintendo && score=$((score+1))

cmp -s ${workdir}/jogos_open_world ${solveddir}/jogos_open_world && score=$((score+1))

cmp -s ${workdir}/jogos_shadow ${solveddir}/jogos_shadow && score=$((score+1)) 

echo $score
