#!/bin/sh
PATH=/usr/local/bin:/opt/local/bin:$PATH

if [ $(pbpaste | wc -l) -gt 1 ]; then
  pbpaste | sort -if | pbcopy;
else
  pbpaste | tr , "\n" | sed 's/^ //' | sort -if | paste -s -d, - | pbcopy
fi
/usr/bin/env growlnotify -a Quicksilver -t "Sorted" -m "`pbpaste`"
