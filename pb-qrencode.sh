#!/bin/sh
# Generate and display QR-code from clipboard
# Mac only

/usr/bin/pbpaste | /usr/local/bin/qrencode -o /tmp/qr.png
qlmanage -p 2>/dev/null /tmp/qr.png
