
#!/bin/bash

set -uo pipefail

# Load ssshtest
if [ ! -s ssshtest ]; then
    curl -fsSL -o ssshtest \
        https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
fi

. ssshtest

# File paths
SCATTER="src/scatter.py"
CO2="test/data/test_Agrofood_co2_emission.csv"
GDP="test/data/test_IMF_GDP.csv"

# Temporary output directory
OUTPUT_DIR="$(mktemp -d)"
trap 'rm -rf "$OUTPUT_DIR"' EXIT

# Test 1: Finland plot
file_name="$OUTPUT_DIR/finland.png"

run test_finland_plot \
    python "$SCATTER" \
    --co2_file "$CO2" \
    --gdp_file "$GDP" \
    --country "Finland" \
    --output_file "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"


# Test 2: Madagascar plot
file_name="$OUTPUT_DIR/madagascar.png"

run test_madagascar_plot \
    python "$SCATTER" \
    --co2_file "$CO2" \
    --gdp_file "$GDP" \
    --country "Madagascar" \
    --output_file "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"


# Test 3: USA plot
file_name="$OUTPUT_DIR/usa.png"

run test_usa_plot \
    python "$SCATTER" \
    --co2_file "$CO2" \
    --gdp_file "$GDP" \
    --country "United States of America" \
    --output_file "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"


# Test 4: Missing CO2 file
run test_missing_file \
    python "$SCATTER" \
    --co2_file "does_not_exist.csv" \
    --gdp_file "$GDP" \
    --country "Finland" \
    --output_file "$OUTPUT_DIR/missing.png"

assert_exit_code 1


# Test 5: Missing required argument
run test_missing_argument \
    python "$SCATTER" \
    --co2_file "$CO2" \
    --gdp_file "$GDP" \
    --country "Finland"

assert_exit_code 2
