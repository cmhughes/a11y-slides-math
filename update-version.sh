#!/bin/bash

oldVersion='V0.4, 2024-11-19'
newVersion='V0.5, 2024-11-24'

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
