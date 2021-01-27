#!/bin/bash

exec 2>&1

workdir=$1

cd $workdir

ls ficheiro* > /dev/null

printf "ficheiro%d\n" {1..100} | sort | diff -q - <(ls -1 ficheiro*)

concat_files=$(printf 'conteudo do meu ficheiro %d\n' {1..100} | sort)

echo "$concat_files" | diff -bBq - <(cat ficheiro*)

ls tudo_junto > /dev/null

echo "$concat_files" | diff -bBq - <(cat tudo_junto | sort)

ls tudo_guardado.zip > /dev/null

unzip -cq tudo_guardado.zip | diff -bBq - <(echo "$concat_files")
