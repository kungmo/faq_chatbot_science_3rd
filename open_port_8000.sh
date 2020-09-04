#!/bin/sh
#!/bin/bash

sudo iptables -I INPUT 5 -i ens3 -p tcp --dport 8000 -m state --state NEW,ESTABLISHED -j ACCEPT
