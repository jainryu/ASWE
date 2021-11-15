#!/bin/sh

run_type_d = "all"
test_dir_d = "../unittest"
report_dir_d = "../test_reports"

usage() {
    echo "Usage: $0 [-h | --help] [run_type] [test_dir] [report_dir]"
    echo "Defaults: run_type = $run_type_d, test_dir = $test_dir_d, report_dir = $report_dir_d"
}

run_type="${1:-$run_type_d}"
test_dir="${2:-$test_dir_d}"
report_dir="${3:-$report_dir_d}"

current_time="$(date --utc "+%FT%TZ")"
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