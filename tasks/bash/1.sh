#!/bin/bash

function fib () {
    re='^[0-9]+$'
    if ! [[ $1 =~ $re ]] ; then
        echo "error: Not a positive number" >&2; exit 1
    fi
    NUMBER="$1"
    if [ "$NUMBER" -eq "0" ]; then
        echo 0
    elif [ "$NUMBER" -eq "1" ]; then
        echo 1
    else
        echo $(($(fib $(($NUMBER - 1))) + $(fib $(($NUMBER - 2)))))
    fi
}

fib "$1"