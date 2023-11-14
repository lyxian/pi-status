#!/bin/bash

# check arch >>> uname -a | grep 'WSL' = wsl

if [[ `uname -a | grep 'WSL'` ]]; then
# windows/wsl (need to trim \r EOL from win)
physical=`cmd.exe /c netsh wlan show interfaces | grep Physical | sed 's/.*: \(.*\)/\1/' | tr a-z A-Z | sed 's/.$//'`
address=`cmd.exe /c netsh interface ip show address "Wi-Fi" | grep "IP A" | sed 's/.*: *\(.*\)/\1/' | sed 's/.$//'`
else
# linux
physical=`ifconfig -a wlan0 | grep 'ether ' | sed 's/.*ether \([^ ]*\) .*/\1/' | tr a-z A-Z`
address=`ifconfig -a wlan0 | grep 'inet ' | sed 's/.*inet \([^ ]*\) .*/\1/'`
fi

uid=`hostname`_${physical}_${address}

python tmp.py $uid `date '+%Y-%m-%dT%H:%M:%S'`