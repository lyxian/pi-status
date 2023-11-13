#!/bin/bash

# check arch >>> uname -a | grep 'WSL' = wsl

if [[ `uname -a | grep 'WSL'` ]]; then
# windows/wsl
uid=`hostname`_`cmd.exe /c netsh wlan show interfaces | grep Physical | sed 's/.*: \(.*\)/\1/' | tr a-z A-Z`_`cmd.exe /c netsh interface ip show address "Wi-Fi" | grep "IP A" | sed 's/.*: *\(.*\)/\1/'`
else
# linux
uid=`hostname`_`ifconfig -a wlan0 | grep 'ether ' | sed 's/.*ether \([^ ]*\) .*/\1/' | tr a-z A-Z`_ifconfig -a wlan0 | grep 'inet ' | sed 's/.*inet \([^ ]*\) .*/\1/'
fi

python tmp.py $uid `date '+%Y-%m-%dT%H:%M:%S%Z'`