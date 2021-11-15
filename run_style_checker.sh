#!/bin/bash

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
filename="pylint-$current_time.txt"

echo "Running pylint for server source files..."
pylint ./server | tee ./reports/style_bug_checker/$filename
