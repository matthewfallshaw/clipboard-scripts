#!/bin/sh
PATH=/usr/local/bin:/opt/local/bin:$PATH

wongahta=$RANDOM
echo ${wongahta:0:4} | pbcopy
/usr/bin/env growlnotify -a Quicksilver -m "New pin in clipboard."
