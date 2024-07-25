#!/bin/bash

usage() {
  echo "Usage: $0 -o <operation> -n <numbers> [-d]"
  echo "  -o <operation>: one of +, -, *, %"
  echo "  -n <numbers>: sequence of numbers"
  echo "  -d: debug flag (optional)"
  exit 1
}

while getopts ":o:n:d" opt; do
  case $opt in
    o) operation=$OPTARG ;;
    n) numbers=($OPTARG) ;;
    d) debug=1 ;;
    \?) usage ;;
  esac
done

# Check if the operation is valid
case $operation in
  "+" | "-" | "*" | "%") ;;
  *) usage ;;
esac

# Check if the numbers are provided
if [ -z "$numbers" ]; then
  usage
fi

result=0
case $operation in
  "+") for num in "${numbers[@]}"; do ((result += num)); done ;;
  "-") for num in "${numbers[@]}"; do ((result -= num)); done ;;
  "*") result=1; for num in "${numbers[@]}"; do ((result *= num)); done ;;
  "%") result=${numbers[0]}; for ((i=1; i<${#numbers[@]}; i++)); do ((result %= ${numbers[i]})); done ;;
esac

echo "Result: $result"

if [ -n "$debug" ]; then
  echo "User: $(whoami)"
  echo "Script: $0"
  echo "Operation: $operation"
  echo "Numbers: ${numbers[*]}"
fi