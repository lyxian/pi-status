#!/bin/bash

if [ $# -eq 1 ]; then
    LOG_PATH=$1
    FILENAME=`basename $1 | cut -d '.' -f1`
    if [ -f $LOG_PATH ]; then
        NEW_PATH=`echo $LOG_PATH | sed "s/$FILENAME/$FILENAME-ytd/"`
        cp $LOG_PATH $NEW_PATH
        echo -ne "\nbackup completed on `date '+%Y-%m-%dT%H:%M:%S'`" >> $NEW_PATH
        rm $LOG_PATH
    fi
fi