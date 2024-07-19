`/proc` - info about computer and all running processes, ie. `/proc/1/cmdline`, `/proc/cpuinfo`
`/sys` - information about the hardware and kernel, ie. `/sys/fs/xfs/nvme0n1p1/stats/stats`

### uname
`-m` - architecture
`-r` - kernel version
`-a` - all info

### lsmod
`modinfo` get info about a module
`modprobe` load/unload kernel module
`modprobe -r` unload kernel module

## udev service
udev is a device manager
udev detects connected devices and passes info through D-Bus
the drive is attached at /dev that contains all handles

`lsblk` - lists all block devices

`/dev/cpu`
`/dev/dri` - video cards
`/dev/nvme0` `n1` `p1` nvme drive with partitions

`lspci` `-k` `-v` list pcie devices, it will query /dev and show pcie devices (with kernel info, verbose)
`lsusb` `-v` `-t` 
`lscpu`
`lsblk` `-f`


### dmesg
legacy

### journalctl
`-k` kernel messages

# init
- sysvinit
- upstart
- launchd - mac
- systemd


## sysvinit
`/sbin/init` 
`/etc/inittab/`
what runlevel
`<identified>:<runlevel>:<action>:<process>`

rc - run commands
`/etc/rc.d` - red hat
`/etc/init.d` - debian

`/etc/rc.d/rc.local` - run after target

isn't designed to detect changes in hardware

## upstart
async capability 

![[Pasted image 20240528155458.png]]


waiting -> starting -> running -> stopping -> killed -> post-stop -> wairing...

running -> respawning (10 times at 5 sec intervals)

# systemd
got rid of bash scripts
replcase some shell scripts with compiled c code
`/usr/lib/systemd/system` - don't edit those, could be replaced in update
`/etc/systemd/system` - for system administrators, take precedence
`/run/systemd/system`
`systemctl list-unit-files`

```
[Unit]
Description=Multi-User System
Documentation=man:systemd.special(7)
Requires=basic.target
  or Wants (won't prevent from starting)
Conflicts=rescue.service rescue.target
After=basic.target rescue.service rescue.target
  also Before
```
`man 5 systemd.unit`

`systemctl cat something.unit`
`systemctl cat httpd.service`

systemd creates symlink 
`/sbin/init -> ../lib/systemd/systemd`




`runlevel` - show runlevel, `N 5` - no previous run level
`telinit <runlevel>` or `init <runlevel>` change runlevel

`cat /etc/inittab` default runlevel

`reboot`

## change runlevel during boot
click any key to enter grub
`a` to modify

add `3` (or any other runlevel) to the end of the boot command

`telinit 0` - shutdown

## systemd
`multiuser.target` - multiuser similar to runlevel 3
`graphical.target` - graphical, similar to runlevel 5
`rescue.target` - basic system and file system mounts and provides a rescue shell
`basic.target` - used during the boot process before another target takes over
`sysinit.target` - system initalization 
`man 5` and `7`

`systemd cat graphical.target`

`systemctl list-unit-files -t target` show all targets

`systemctl list-units -t target` all active units

default is symlink
`systemctl get-default`

`systemctl set-default <target>`

### change current target
`systemctl isolate multi-user.target`
`systemctl <target>`
`systemctl poweroff`

# rebooting
`reboot`
`telinit 6`
`shutdown -r now`
`systemctl isolate reboot.target`

`wall` + Ctrl-d
# shutdown
`poweroff`
`telinit 0`
`shutdown -h 1 minute` (ctrl c to cancel)
`shutdown -c` cancels shutdown
`systemctl isolate poweroff.target`
`systemctl isolate shutdown.target`

## acpid
system events like power button, laptop lid etc
`/etc/acpi`

`/`
`/var`
`/home`
`/boot`
`/opt`

![[Pasted image 20240529125452.png]]

`mount`
`lsblk`
`fdisk -l /dev/sda` - info about disk
`swapon --summary` - info about SWAP

# lvm
`pvs` - physical volume setup, show volume setup
`vgs` - volume groups
`lvs` - show logical volumes

## legacy grub
bios
stage 1 - MBR -> boot.img
stage 1.5 - core.img - locate boot partition
stage 2 - grub.com or menu.lst, device.map
`grub-install /dev/sda`

`find /grub/stage`

`install` command, advanced
`setup (hd0)` easier, hd0 for mbr

# grub2
MBR - only 26 total partitions, 4 partitions with one extended to 23 partitions
partition limited to 2TB

GPT GUID Partition Table
128 partitions
up to ZB zettabyte range
needs UEFI

### UEFI
uefi bios
stage 1 - mbr boot.img
gpt header
partition entry array - list of partitions and ids and where they located
stage 1.5 - typically empty sectors core.img
ESP `/boot/efi` vfat or FAT32 - where boot images are located
stage 2 - `/boot/grub2` grubenv, themes

red hat - `grub2-<command>`
debian - `grub-<command>`

`grub2-editenv list` view default entry for the grub config file
`/etc/default/grub` modify grub options
`/etc/grub.d/`
`grub2-mkconfig` - it modifies `/boot/grub2/grub.cfg`

`update-grub`

### systemd 
add to linux in kernel `systemd.unit=rescue.target`

`(hd0,msdos1)` means MBR

`ls(hd0,1)/` lists drive

## manually boot
`set root=(hd0,1)`
`linux /boot/vmlinuz-<TAB to autocomplete> root=/dev/sda1`
`initrd /boot/initrd.img-<same as kernel>`
`boot`


# shared libraries
`/lib`
`/usr/lib` and `/usr/lib64`
`/usr/local/lib`
`/usr/share`

`.so` dynamic
`.a` statically linked

`ldd <bin>` check what libraries

`ldconfig` build cache listing of recently used libraries
`cat /etc/ld.so.conf`

`/etc/ld.so.conf.d/libc.conf`
...

`LD_LIBRARY_PATH` env variable with custom library path
`export LD_LIBRARY_PATH=/opt/java/jre/lib`

# apt - advanced package tool
reads `/etc/apt/sources.list`
uses `dpkg`
`apt-get update`
`apt-get upgrade`
`apt-get install <package>`
`apt autoremove`
`apt-get purge <package>` remove package and config

`apt-get dist-upgrade` upgrades everything

`apt-get download htop`

`apt-cache search apache`
`apt-cache show libapache2-mod-bw` info about package
`apt-cache showpkg <package>` more info about repo of package

# dpkg
`dpkg --info <file>` list info about .deb file
`dpkg --status <installed package>` info about package
`dpkg -l <package>` list packages with info

`dpkg -i <file>` install package
`dpkg -L <package>` list all files of package

`dpkg -r <package>` uninstall package
`dpkg -P <package>` remove and purge package config files

`dpkg -S <search string>` find config files

`dpkg-reconfigure` 
`dpkg-reconfigure console-setup` change console font etc

# yum
on red hat
`/etc/yum.conf`
`/etc/yum.repos.d/`

`yum update`
`yum upgrade`
`yum search <package>`

`yum list installed | less`

`yum clean all`
`yum install [-y] <package> `
`yum remove [-y] <package>`
`yum autoremove` remove unused packages
`yum whatprovides */<package>`
`yum reinstall <package>`

you need `yum-utils` to just download without installation
`yumdownloader <package>`


## other
### zypper
SUSE
`zypper repos`
`zypper install vim`

### dnf
fedora linux
same syntax as yum


# rpm
`/var/lib/rpm
`rpm --rebuilddb`
rpm **does not** handle dependencies

`rpm -qpi <file>` show info about package
`rpm -qpl <file>` show files within package
`rpm -qa | less` show installed packages
`rpm -i[v (verbose) h (hash)] <file>` install package
`rpm -Uvh <file>` update package

`rpm -e <package>` uninstalls (erases) installed package
`rpm -Va` verify all installed packages

S - size is different
M - mode is different
5 - hash (MD5) is different
L - 
U - user permission is different
G - group permission is different
T - modified time of the file is different
d - 
c - config file
g - ghost file (didn't come with package)

`rpm2cpio <file> | cpio -idmv` converts rpm to cpio
i extract
d same directory structure
m modified time the same
v verbose


# installing RPMs and managing dependencies
`rpm -ivh <file>`
if required dependencies
`yum [what]provides <dependency>[*]`
`yum install <dep>`


# virtualization

full virtualization - guest system is not aware that it is a virtual machine
paravirtualization - gues system is aware that it is a virtual machine, uses guest drivers - typically perform better

cloud-init
creates new SSH keys
sets the system's default locale
sets the system's host name
sets up mount points

# containers

isolated set of packages
machine containers - shares a kernel and file system with the host computer
application container - shares everything but the application files and library files that the application needs

examples
docker
nspawn (from systemd)
LXD
OpenShift

# shell
## bash
`env` show current envs
`echo $LOGNAME`
`set` shows env variables and functions
`set -x` show debugging
`set +x` disable debugging
`unset` unset env var
```bash
function name() {
	echo fun
}
```

`shopt` show current options for shell
`shopt -s histredit` toggle option
`export` export variable so that each shell created in this shell will have this var
`export FOO=bar`

`pwd` gets info from $PWD env variable
`which`
`type <command>` find if it's an alias or binary
`echo $PATH`
`"` weak quotes - expand variables
`'` strong quotes - doesn't

`history`
`!<number>` reference command in the history
`cat ~/.bash_history`
`echo $HISTFILESIZE`

`man <command>`
![[Pasted image 20240607103906.png]]

`man -k <keyword ie. touch>` search for keyword
`appropos touch` same thing

`man 4 synamtics` show 4th section


# text files
`cat` concatenate
`cat <file1> <file2>`
`less` read longer files in read only mode
`head` by default display first 10 lines
`head -15 <file>` 15 lines
`tail`

`sudo tail -f /var/log/secure` show login log

`^c`

`zcat` display contents of compressed file (gz)
`bzcat` same but bz2
`xzcat` same but xz

`nl` number line - count lines
`nl -b a <file>` - also count empty lines
`wc` word count
`<number of lines> <number of words> <byte count>`
`wc -w` just count words
`wc -l` just count lines
`wc -c` just count bytes
`od <file>` octal dump
`<byte offset> <octal representation>`
`od -c <file>` octal data in character format
`od -a` ascii format

#### crypto checking
`<algo>sum`
`md5sum <file>`
`md5sum -c test.md5`
`sha256sum`
`sha512sum`

#### text manipulation
`sort <file>` sort file
`sort -n` considers number as a whole
`sort -t "," -k2 <file>` sort csv sorted by 2nd column
`uniq` delete grouped duplicate lines
`uniq -c <file>` show stats
`uniq --group` show groups
`sort -u` only show unique values, ignores gruping
`tr` translate (or swap) characters in file for another character
`cat <file> | tr ',' ':'` replace
`cat <file> | tr -c ','` delete
`cat <file> | tr 'A-Z' 'a-z'` replaces all upper to lower
`cat <file> | tr 'A-Z' 'a-z' | tr ',' ':'` replaces all upper to lower and commas
`cut -d ',' -f 3 <file>` get only 3rd column
`cut -d ',' -f 2,3 <file>` get 2nd and 3rd column
`cat <file> | tr ',' '\t' | cut -f 2,3` change , in to tabs, then cut out only 2nd and 3rd column
`paste <file1> <file2>` paste second file2 to the right of file1
`paste -d ',' list.csv stats.txt`
`paste -d ',' -s list.csv stats.txt`

`sed` stream editor
`sed 's/<text to replace>/<replace with>/' <file>`
`sed 's/././g'` in some version it could only replace the first - 'g' to counter it as in globally
`sed -i ...` in place replacement

`split <file>` split file into files with 1000 lines
`split -b 100 <file>` break down file into 100 bytes files
`split -d` numeric suffix 
`--verbose`
`split -n2` two files

## basic file management
`ls`
`ls -dl <directory>`
`ls -lR <dir>` recursive

`touch` create blank files or change file's timestamp

`cp <file> <new file>` copy
`cp -R <dir> <new dir>`
`cp -i <file> <new file>` will prompt if file exists (default depends on distro)
`cp -f` does not prompt

`rm` remove
`-i` interactive
`-f` force
`-r` recursive delete, works with folders

`mv <old_file> <new file>` move or just change name

`file` determine file's type

### working with dir
`ls`
`cd`
`cd -` change to last dir
`$PWD` current
`$OLDPWD` last

absolute path - starts with `/`
relative path - relative to current location

`mkdir`
`mkdir -p <dir>/<subdir>` create dir and subdir
`mkdir -p Projects{ancient,classical,medival}`
`rmdir` delete only empty dir
`rm -r <dir>` delete dir and files

`$PATH`

`dd if=boot.img of=/dev/sdc` write img to device
`dd if=/dev/xcda of=/tmp/mbr.img bs=512 count=1` backup mbr
`dd if=/dev/urandom of=file bs=1024 count=10` random 10 mb file
`ls -h` human readable

`tar` tar archive, tarball
`tar -cf <new file>.tar <file or dir>`
`tar -tf <file>` list files
`tar -xf <file>` extract files
`rm -rf *` remove all
`tar -czf <new file.tgz or .tar.gz> <file or dir>` compress with gzip
`tar -cjf x.tar.bz2 ...` bzip2
`tar -CJf x.tar.xz ...` xz compression

`gzip <file>` zip file
`gunzip <file>` unzip file

`xz <file>`
`unxz <file>`

`zcat` tar.gz
`bzcat` tar.bz2
`xzcat` tar.xz

### finding files
`find`
`find . -name <filename>`
`-ctime 1` changed in last 24 hours 
`-atime -2` access time 48 hours
`-newer <file>` newer than this file
`-empty` all empty dirs and files
`-type f` files
`-exec rm -f {} \;` remove files while find
`find ~ -name "*.tar.*" -exec cp -v {} ~/test \;` copy all tars to `~/test`

### globbing
glob - global command
`*` zero or more chars
`?` any single char
`ls [Pp]*.csv` upper or lower case p
`[0-9]` numer range
`[^abc]` matches all except
`{one,two,three}` will expand to `one two three`

## standard output/input
redirect output
`>` or `>>`

`wc test.sh
`wc < test.sh` redirect standard input from file
`cat /etc/passwd | less`

stdin 0
stdout 1

## standard error
file handle 2

`script.sh 2> error.log` error to file
`script.sh 2>&1 | less` error and output to less

`echo "foo" > bar.txt` overwrite
`echo "fooo" >> bar.txt` append
`cat < bar.txt`

`ls -d /usr/share/doc/lib[Xx]* | tee lib-docs.txt`
`tee <file>` could be used as logs in between
`sort -r` sort in reverse
## xargs

`find test/ -empty | xargs rm -f`

`-l` only filename
`grep -l "junk" test/file_* | xargs -I {} mv {} test/bak/`
`find ~ -name "*.sh" | xargs ls -la > scripts.txt`

`ps -eH` show processes

process table

`ps -u <username>`

`-e` every process from all users
`-H --forest` hierarchy of processes
`-f` full format (arguments)
it gets info from /proc

`top`
`uptime`
`free` ram and swap
`free -m` in megabytes
`free -g` in gigabytes

`pgrep httpd` grep processes, default only pids
`pgrep -a httpd` with full name
`pgrep -u <username>` show user's processes

# signals

`man 7 signal`
`/Standard signals`

SIGHUP 1 hangup detected
SIGKILL 9 kill
SIGTERM 15 nicely close

`grep httpd`
`kill <pid>`
`kill -l` list kill signals
`kill -9 <pid>` force kill
`pkill <name>` kill with name instead of pid

`killall <name>`
`killall -s 9 httpd`
`watch` run command in a loop

### screen
`screen
`ctrl + a, d` detach
`screen -r` reattach
`screen -r <id>` attach to screen
`screen -ls` list screens

### tmux
`tmux`
`ctrl + b, d` detach
`tmux ls` list sessions
`tmux attach-session -t <number>`

`nohup ping www.google.com &`
`jobs` see running jobs
`fg <number>` bring to foreground
`ctrl z` send to background, stop
`bg %1` run the command again

# nice level- priority
0 default
19 lowest
-20 highest

`ps -o pid,nice.cmd,user`
`nice -n 5 <command>` run command with level 5
`renice -n -1 <PID>` change permission (-1 from current)

`top`
`u` search for user
`r` renice, provide pid

# regex
`grep`
`.` any single character
`^` beginning of line
`$` end of the line
`[abc]` any char
`-i` case insensitive
`[Aa]` both cases
`[^abc]` other characters
`*` match 0 or more
`man 7 regex`

`cat asswd | sed -n '/nologin$/p` just display
`cat passwd | sed '/nologin$/d > filtered.txt` delete and put output into file

`egrep` 
`grep -E` same thing 

`egrep 'bash$' passwd`
`egrep -c ...` count
`egrep '^rpc|nologin$` begins with rpc or ends with nologin

`grep -F` search strings
`fgrep`
`fgrep -f <file with search strings> <file>`

# vim
`i` insert mode
`ESC` go back to command mode
`hjkl` move cursor
`v` visual mode
`y` yank copy
`p` put, paste
`u` undo
`:w <name>` save
`SHIFT + G` beginning of the last line
`dw` delete word
`gg` move to beginning of the first line
`SHIFT + I` append at the end
`SHIFT + D` delete to the right

# MBR
`lsblk`

`fdisk /dev/sda`
`m` help
`p` show partitions
`n` new partition
fs id's
`83` linux fs ext2
`82` swap linux
`8e` lvm

`w` write
`fdisk -l /dev/sda`

`parted`
`help`
`p` print partition table
`mklabel msdos` set mbr
`mkpart` make partition
`quit`

# GPT
`gdisk` gpt port of fdisk
`8300`, `0x83` all the same, ext2

`parted`
`mklabel gpt`

# swap
swapfile is less efficient than swap partition
`8200` for swap partition in `gdisk`

`mkswap -L SWAP /dev/sda2`
`swapon -a` turn on all swap
`swapon -U <uuid>`
`swapon -L SWAP`
`free -m`
`swapoff`

`/etc/fstab`
`<physical location> <mount point> <fs type> <mode> <dumping> <fs checking order>`
`LABEL=SWAP swap swap defaults 0 0`
`swapoff -L SWAP`
`swapon -a` read `/etc/fstab`

# fs
ext2 is non-jorunaling

journaling
ext3
ext4
xfs

#### btrfs
uses CoW Copy on Write
uses subvolumes
snapshots

### FAT
fat
vfat virtual file allocation table
efi needs to be fat
exfat

### creating fs
`mkfs -t ext4`
`mkfs.ext4 -L <label> /dev/sda1`
`lsblk -f` show file system
`blkid /dev/sda1` show uuid, fs and label
`mkfs.xfs -L OPT /dev/vdb1`

## disk usage
`ls -lh`
`df -h` disk free
`df -h /`
`df -h /dev/xvda1`
`df --total -h`

`du` disk usage
`du -h` human readable
`du -sh` summary
`du -sh /tmp`
`du -hd 1` max depth

`inode`
`df -i`
`ls -i`
`du --inodes`

#### maintaining a filesystem
`lsblk -f`
`fsck -r LABEL=<label>`
`umount <dev/label/mount point>`
`e2fsck` ext2,3,4 
`e2fsck -f <dev>`
`e2sck -p <dev>`
`mke2fs` make new ext fs (mkfs uses this)

`/etc/mke2fs.conf` config for mke2fs
`mke2fs -t ext4 -L <label> <dev>`
`tune2fs` tune ext fs
`tune2fs -l <dev>` info
Errors behavior: continue - default
Check interval: 0
`tune2fs -i 3w` check every 3 weeks, changes next check after
`mount /dev/sdb1 /srv/extra`
if kernel found any broken files, it will move it to lost+found
`xfs_repair /dev/vdb1` 7 phases
`xfs_fsr /opt`
`xfs_db` debug
`frag` check fragmentation

# mounting
`/etc/fstab`
`/etc/mtab` -> `/proc/mounts` - mount
`mount /dev/vdb1 /opt`
`umount <dev>`
`mount -L OPT -t xfs -o rw,noexec /opt`
`/etc/fstab`
`LABEL=OPT /opt xfs rw,exec,suid,auto 1 2`
`mount -a`
`mount -t xfs` show all xfs
`/media` cdrom, usb etc
`mount /dev/sr0 /media`
`mount /root/isnall.iso [-t iso9660] -o ro,loop /media`

# permissions
owner group other
`chmod`
`o-r` remove read from other
`-R` recursively
`600` rw for owner only

`chown`
`owner:group` (can use `.` too)

`chgrp <group> <file>` change group too
normal user can't change the owner of the file, only root

### adcanved permissions
 `s` in ls set uid bit
 `chmod 4764 <file>` set uid bit 
 `chmod u+s`, `u-s`

sgid


`groups` show groups
`id` show groups too

`chmod -R 2770` set sgid

### sticky bit
`chmod 1777 <file>` set sticky bit
only allows the owner to delete it

![[Pasted image 20240614124442.png]]

## umask
default
`777` for dir
`666` for files

`umask 0002` for user
`umask 0022` for root

`/etc/bashrc` set global umask
`/home/[user]/.bashrc` set user umask

# links
`ln -s <source> <new link>` create symbolic link

# FHS - filesystem hierarchy standard

`bin` binaries
`boot` booting
`dev` devices
`etc` configuration 
`home` home folder
`lib` `lib64` shared libraries
`media` mouted usb, cd drives
`mnt` mounted hard drives
`opt` applications not in bin
`proc` info about running system
`root` home of root
`sbin` system admin tools
`srv` web servers
`sys` info about hardware system
`tmp` temporary
`usr` 
`var` vary in size, logs etc

# finding things
other than `find`
`locate`
`updatedb`
`locate updatedb.conf`
`/etc/updatedb.conf`

`whereis` show binaries for command and man files

