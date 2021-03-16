#!/bin/bash

workdir=$1
solveddir="/src/score/exercises/scripting2/solved"

./${workdir}/scripting1 | cmp - ${solveddir}/out | awk '{print $NF-1}'

cmp -s ${workdir}/jogos_nintendo ${solveddir}/jogos_nintendo && echo 1

cmp -s ${workdir}/jogos_open_world ${solveddir}/jogos_open_world && echo 1

cmp -s ${workdir}/jogos_shadow ${solveddir}/jogos_shadow && echo 1

