#!/bin/sh

run_type_d="unit_integration"
test_dir_d="./server"
report_dir_d="./reports/tests"

usage() {
    echo "Usage: $0 [-h | --help] [run_type] [test_dir] [report_dir]"
    echo "Defaults: run_type = $run_type_d, test_dir = $test_dir_d, report_dir = $report_dir_d"
}

if [ "-h" = "$1" ] || [ "--help" = "$1" ];then
    usage
    exit 0
fi

run_type="${1:-$run_type_d}"
test_dir="${2:-$test_dir_d}"
report_dir="${3:-$report_dir_d}"

current_time=$(date +"%m-%d-%Y %H.%M.%S")
filename="$run_type-$current_time.txt"

if [ ! -d "$test_dir" ];then
    ( echo "Error: test_dir '$test_dir' does not exist"
    usage ) >&2
    exit 1
fi

if [ ! -d "$report_dir" ];then
    echo "report_dir '$report_dir' does not exist, creating it now"
    if ! mkdir -p "$report_dir";then
        echo "Error: Failed to create report directory, aborting" >&2
        exit 1
    fi
fi

python -m pytest -v "$test_dir/$1" 2>&1 | tee "$report_dir/$filename"