#!/usr/bin/env bash

BASE_DIR=$(dirname $(readlink -f $0))
cd $BASE_DIR

python src/run.py