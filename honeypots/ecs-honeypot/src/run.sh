#!/bin/sh
/usr/bin/python3 /opt/monitor.py &
python3 -m http.server 80 --directory www &
/opt/ynetd -p 6000 "/opt/vuln $HPID"
