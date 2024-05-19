#!/bin/bash

echo -e "\n`date`"

[ -d .venv ] && . .venv/bin/activate

if [[ ! `env | grep SECRET_` ]]; then
    set -a
    [ -f .env ] && source .env && echo '.env loaded'
    set +a
fi

# check arch >>> uname -a | grep 'WSL' = wsl

if [[ `uname -a | grep 'WSL'` ]]; then
# windows/wsl (need to trim \r EOL from win)
physical=`cmd.exe /c netsh wlan show interfaces | grep Physical | sed 's/.*: \(.*\)/\1/' | tr a-z A-Z | sed 's/.$//'`
address=`cmd.exe /c netsh interface ip show address "Wi-Fi" | grep "IP A" | sed 's/.*: *\(.*\)/\1/' | sed 's/.$//'`
else
# linux
physical=`/usr/sbin/ifconfig -a wlan0 | grep 'ether ' | sed 's/.*ether \([^ ]*\) .*/\1/' | tr a-z A-Z`
    if [[ `/usr/sbin/ifconfig -a eth0 | grep 'inet '` ]]; then
    address=`/usr/sbin/ifconfig -a eth0 | grep 'inet ' | sed 's/.*inet \([^ ]*\) .*/\1/'`
    else
    address=`/usr/sbin/ifconfig -a wlan0 | grep 'inet ' | sed 's/.*inet \([^ ]*\) .*/\1/'`
    fi
fi
runningSince=`uptime -p | cut -d ' ' -f2- | tr -d ' '`

uid=`hostname`_${physical}_${address}_${runningSince}

python main.py $uid `date '+%Y-%m-%dT%H:%M:%S'`