# transmission-telegam-notify

![cover](http://file.sudo.host/rNWZ/Image%202018-05-06%20at%206.23.35%20PM.png)

## Overview
This little script will make notify when your transmission finish download or add new queue

## Dependency
- [transmissionrpc](https://bitbucket.org/blueluna/transmissionrpc/wiki/Home)

## Install

```shell
pip install transmissionrpc

#or download as zip
git clone https://github.com/tasi788/transmission-telegram-notify.git

#edit config.example.py and rename as config.py
#cp config.example.py config.py

#it's should work, i don't test on my device
sudo cat crontab >> /var/spool/cron/crontabs/"$USER"
service cron reload
```
