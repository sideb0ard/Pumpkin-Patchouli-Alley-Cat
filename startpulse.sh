#!/bin/sh

ps awux | grep [p]ulseaudio > /dev/null
OUT=$?
if [ $OUT -eq 0 ]; then
    echo "Pulse Running - NOOP"
else
    echo "Pulse Not running - starting now"
    /usr/bin/pulseaudio -D
fi
