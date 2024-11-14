#!/bin/bash

oldVersion='V0.1, 2024-11-14'
newVersion='V0.2, 2024-11-14'

listOfFiles=(
   a11y-slides-math-template.html
   readme.md
)

for indvfile in "${listOfFiles[@]}"
do
   set -x
   sed -i.bak "s/$oldVersion/$newVersion/g" $indvfile
   codespell.exe -w $indvfile
   set +x
done
exit
