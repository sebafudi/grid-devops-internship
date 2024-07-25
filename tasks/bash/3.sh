#!/bin/bash

for num in $(seq 1 100); do
    str=""
    if [ (($num % 3)) -eq 0 ]; then
        str+="Fizz"
    elif [ (($num % 5 )) -eq 0 ]; then
        str+="Buzz"
    else
        str=$num
    fi
    echo $str
done