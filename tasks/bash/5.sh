#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 -i <input file> -o <output file> [options]"
    echo "Options:"
    echo "  -v           : Swap lowercase characters with uppercase and vice versa"
    echo "  -s A_WORD B_WORD : Substitute A_WORD with B_WORD in text (case sensitive)"
    echo "  -r           : Reverse text lines"
    echo "  -l           : Convert all text to lowercase"
    echo "  -u           : Convert all text to uppercase"
    exit 1
}

# Parse command line arguments
while getopts ":i:o:vs:rul" opt; do
    case $opt in
        i) input_file=$OPTARG ;;
        o) output_file=$OPTARG ;;
        v) swap_case=true ;;
        s) shift; words=($OPTARG); shift ;;
        r) reverse_lines=true ;;
        l) to_lowercase=true ;;
        u) to_uppercase=true ;;
        *) usage ;;
    esac
done

if [ ! -z "$words" ]; then
    a_word=${words[0]}
    b_word=${words[1]}
fi

# Check if input and output files are provided
if [ -z "$input_file" ] || [ -z "$output_file" ]; then
    usage
fi

# Check if at least one operation is specified
if [ -z "$swap_case" ] && [ -z "$a_word" ] && [ -z "$reverse_lines" ] && [ -z "$to_lowercase" ] && [ -z "$to_uppercase" ]; then
    usage
fi

# Process the input file based on specified options
process_text() {
    local text="$1"
    
    if [ "$swap_case" = true ]; then
        text=$(echo "$text" | tr 'a-zA-Z' 'A-Za-z')
    fi

    if [ ! -z "$a_word" ] && [ ! -z "$b_word" ]; then
        text=$(echo "$text" | sed "s/$a_word/$b_word/g")
    fi

    if [ "$reverse_lines" = true ]; then
        text=$(echo "$text" | awk '{ lines[NR] = $0 } END { for (i = NR; i > 0; i--) print lines[i] }')
    fi

    if [ "$to_lowercase" = true ]; then
        text=$(echo "$text" | tr '[:upper:]' '[:lower:]')
    fi

    if [ "$to_uppercase" = true ]; then
        text=$(echo "$text" | tr '[:lower:]' '[:upper:]')
    fi

    echo "$text"
}

# Read input file, process text, and write to output file
input_text=$(<"$input_file")
output_text=$(process_text "$input_text")
echo "$output_text" > "$output_file"

echo "Processing complete. Output written to $output_file"