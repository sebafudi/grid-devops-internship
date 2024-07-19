`.bash_profile` runs on login
`.bashrc` runs on new terminal creation
`.bash_history` history of commands
`export HISTCONTROL=$HISTCONTROL:ignorespace`
use ` ` (space) before the command so that `.bash_history` won't capture it

`.bash_logout` run on clean logout


`env` show all env variables
`#!/bin/bash` shabang - create a new shell insted of making changes to current one
 
`"$VAR"` show variable
`` `date` `` execute command

`#` comment in bash

## command substitution
`` `find /home -user user` `` example
`alias TODAY="date"`
`alias UFILES="find /home -user user"`

`` A=`TODAY` ``
`echo "Today is $A"`

`shopt -s expand_aliases` expand aliases so that they work in shell script

## errors
`$?` show last status
`set -e` end script on error

## arithmetic expressions
`expr 2 + 2`
be sure to place the spaces, otherwise you'll get `2+2`
`expr 10 \* 8` you need to escape `*`
`expr \( 2 + 2 \) \* 4` force the order

## envs
`printenv` show global envs
`env` show envs (?)
`set` show local envs


`'$VAR'` will show `$VAR`
`"$VAR"` will show value
`` `date` `` will execute the command even if surrounded by parenthesis

## redirect to null
`ls -lah >> /dev/null`

## read input
`read VAR_NAME`

## shell expansion
`echo sh{ot,ort,oot}` -> `shot short shoot
`echo ~` home dir
`echo ~+` pwd
`echo ~-` last dir
`echo "$[ 2 * 2 ]"` will result in 4

## types
integeres
`declare` set type, get type
`declare -p MYVAR` get type
`declare -i NEWVAR=10` declare variables as integers

`declare +i NEWVAR` cancel the integer declaration
`declare -r VARIABLE="..."` read only variable
can't do `+r` on readonly to cancel this
`readonly MYVAR="..."` another way to set readonly

## arrays
`MYARRAY=("First" Second" "Third")`
`echo $MYARRAY` -> `First`
`echo ${MYARRAY[0]}` -> `First`
`echo ${MYARRAY[1]}` -> `Second`
`echo ${MYARRAY[*]}` -> `First Second Third`
`MYARRAY[3]="Fourth"` 
space delimiter

```bash
for INDEX in $(SERVERLIST[@]); do
	echo "Server: ${SERVERLIST[COUNT]}"
	COUNT="`expr $COUNT + 1`"
done
```

## variables as arguments from cli
```bash
echo "$1"
echo "$2"
```
`script.sh one two`

## ifs
```bash
if [ $GUESS -eq 3 ]
	then
		echo "You Guessed the Correct Number!"
fi
```

```bash
FILENAME="mytext.txt"
echo "if file exists $FILENAME"
if [ -a $FILENAME ]
	then
		echo "file $FILENAME exists"
fi
```

## negative test
```bash
if [ ! -a $FILENAME ]
	then
		echo "file $FILENAME does not exist"
fi
```

## more than one expression
```bash
FILENAME=$1
if [ -f $FILENAME ] && [ -r $FILENAME ]
	then
		echo "$FILENAME exists and is readable"
fi
```

## if/then/else
```bash
if [ "$VALUE" -eq "1" ] 2>/dev/null || [ "$VALUE" -eq 2 ] 2>/dev/null || [ "$VALUE" -eq 3 ] 2>/dev/null; then
	echo "correct"
else
	echo "incorrect"
fi
```

```bash
if [ "$VALUE" -eq "1" ] 2>/dev/null; then
	echo "number 1"
elif [ "$VALUE" -eq "2" ] 2>/dev/null; then
	echo "number 2"
elif [ "$VALUE" -eq "3" ] 2>/dev/null; then
	echo "number 3"
else
	echo "incorrect"
fi
```

## for loops
```bash
SHELLSCRIPTS=`ls *.sh`
echo "all shellscripts $SHELLSCRIPTS"
```

```bash
SHELLSCRIPTS=`ls *.sh`

for SCRIPT in "$SHELLSCRIPTS"; do
	DISPLAY="`cat $SCRIPT`"
	echo "$SCRIPT contains $DISPLAY"
done
```

## case
```bash
read MENUCHOICE
case $MENUCHOICE in
	1)
		echo "first"
		;;
	2)
		echo "second"
		;;
	3)
		echo "third";;
	*)
		echo "incorrect";;
```
`;;` both in the same line or next is fine

## while loop
```bash
COUNT=1
while [ $COUNT -le $DISPLAYNUMBER ]
do
	echo "Hello world - $COUNT"
	COUNT="`expr $COUNT + 1`"
done
```

## execution operators
`||` or
`&&` and
`rm something 2> /dev/null` doesn't show error
`rm something 2> /dev/nul && echo "File existst and was removed" || echo "File does not exist and cannot be deleted"`

```bash
if [ "$VALUE" -eq "1" ] || [ "$VALUE" -eq "3" ] || [ "$VALUE" -eq "5" ]; then
	echo "You entered the ODD value of $VALUE"
else
	echo "You entered another value of $VALUE"
fi
```

## reading file
```bash
# file reading (non-binary) and display one line at a time

echo "Enter a filename to read: "
read FILE

while read -r SUPERHERO; do
	echo "Superhero Name: $SUPERHERO"
done < "$FILE"
```

## file descriptors and handles
0, 1, 2 - reserved
```bash
echo "Enter a file name to read: "
read FILE

exec 5<>$FILE # open the file descriptor

while read -r SUPERHERO; do
	echo "Superhero Name: $SUPERHERO"
done <&5

echo "File Was Read On: `date`" >&5

exec 5>&- # close the file descriptor
```

`<` read only
`>` write only
`<>` read and write

## IFS - internal field separator, delimiting
```bash
FILE="file.txt"
DELIM=";"

IFS="$DELIM" # set the delimiter

while read -r CPU MEMORY DISK; do
	echo "CPU: $CPU"
	echo "Memory: $MEMORY"
	echo "Disk: $DISK"
done <"$FILE"
```

