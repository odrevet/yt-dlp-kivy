#!/bin/bash

source utils/config.sh

rm $BIN/*
bash utils/build.sh
bash utils/sign.sh
bash utils/install.sh
