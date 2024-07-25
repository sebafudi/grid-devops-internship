#!/bin/bash

usage() {
    echo "Usage: $0 -s <shift> -i <input file> -o <output file>"
    exit 1
}

while getopts ":s:i:o:" opt; do
    case $opt in
        s) shift_value=$OPTARG ;;
        i) input_file=$OPTARG ;;
        o) output_file=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if all parameters are provided
if [ -z "$shift_value" ] || [ -z "$input_file" ] || [ -z "$output_file" ]; then
    usage
fi

# Ensure shift value is a number
if ! [[ "$shift_value" =~ ^-?[0-9]+$ ]]; then
    echo "Error: Shift value must be an integer."
    exit 1
fi

caesar_encrypt() {
    local char=$1
    local shift=$2

    if [[ $char =~ [A-Za-z] ]]; then
        local offset
        if [[ $char =~ [A-Z] ]]; then
            offset=65
        else
            offset=97
        fi
        printf \\$(printf "%03o" $(( ( $(printf '%d' "'$char") - $offset + $shift + 26 ) % 26 + $offset )))
    else
        printf "%s" "$char"
    fi
}

while IFS= read -r -n1 char; do
    caesar_encrypt "$char" "$shift_value"
done < "$input_file" > "$output_file"

echo "Encryption complete. Output written to $output_file"