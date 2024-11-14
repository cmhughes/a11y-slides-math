#!/bin/bash

oldVersion='2024-11-14 v0.1'
newVersion='2024-MM-DD v0.X'

cd ../
sed -i.bak "s/$oldVersion/$newVersion/g" *
sed -i.bak "s/$oldVersion/$newVersion/g" docs/*
exit
