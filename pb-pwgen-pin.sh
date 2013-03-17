#!/bin/sh
PATH=/usr/local/bin:/opt/local/bin:$PATH

wongahta=`expr $RANDOM + 1000`
echo -n ${wongahta:0:4} | pbcopy
unset wongahta
/usr/bin/env growlnotify -a Quicksilver -m "New pin in clipboard."
