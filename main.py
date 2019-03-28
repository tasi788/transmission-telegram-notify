#!/bin/python3
__author__ = '@DingChen_Tsai'
__website__ = 'https://tdccc.com.tw'


#import requests

import config
import os
import math
import json
import random
import logging
import transmissionrpc
from termcolor import *
from urllib import request, parse


def initlogger(logname, level='info'):
    logger = logging.getLogger(logname)
    if level == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] {levelname} %(name)s %(message)s'.format(
        levelname='%(levelname)s'), datefmt='%Y/%m/%d %I:%M:%S %p')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def run():
    log = initlogger('transmission-notify', 'debug')
    log.info('Init...')

    def notify(text):
        url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
            token=config.telegram.token)
        for uid in config.telegram.uid:
            data = {
                'chat_id': uid,
                'text': text,
                'parse_mode': 'html'
            }
            parse_data = parse.urlencode(data).encode()
            req = request.Request(url, data=parse_data)
            resp = request.urlopen(req)

    def convert_size(size_bytes):
        if size_bytes == 0:
            return '0B'
        size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        # return '%s %s' % (s, size_name[i])
        return '{size} {size_name}'.format(size=s, size_name=size_name[i])

    tc = transmissionrpc.Client(
        address=config.transmission.url,
        user=config.transmission.user,
        password=config.transmission.passwd)
    log.info('Logined')
    # touch notify_list if does'nt exist
    if os.path.isfile('notify_list') is not True:
        with open('notify_list', 'w') as f:
            f.write('[]')
            f.close()
            notify_list = []
    else:
        notify_list = open('notify_list', 'r').read()
        notify_list = notify_list.split('\n')

    for torrent in tc.get_torrents():
        hash = torrent.hashString
        progress = torrent.progress
        name = torrent.name
        add = torrent.date_added
        fin = torrent.date_done
        cost = (fin-add).seconds
        size = torrent.totalSize
        path = torrent.downloadDir
        '''預覽
		#下載完成

		<b>{name}</b>
		📅 04/05 23:34 - 05/05 01:39
		🕔 2 hours, 4 minutes, 33 seconds
		Size: 11.2 GB

		📂 /data/download/bt/
		'''
        if hash in notify_list and progress == 100.0:

            formatter = '''
			#下載完成 {face}

			<b>{name}</b>

			📅 {add.month}月/{add.day}日 {add.hour}:{add.minute} - {fin.month}月/{fin.day}日 {fin.hour}:{fin.minute}
			🕔 {cost_h} hours, {cost_mins} mins
			💾 {size}

			📂 {path}
			'''.format(
                name=name,
                add=add,
                fin=fin,
                cost_h=cost//3600,
                cost_mins=(cost//60) % 60,
                size=convert_size(size),
                path=path,
                face=random.choice(config.face.emoticon))
            notify(formatter)
            with open('notify_list', 'w') as w:
                notify_list_str = ''
                notify_list.remove(hash)
                for x in notify_list:
                    notify_list_str += x
                w.write(notify_list_str)
                w.close()

        if hash not in notify_list and progress != 100.0:
            formatter = '''
			#新增下載任務 {face}

			<b>{name}</b>

			💾 {size}
			📂 {path}
			'''.format(
                name=name,
                size=convert_size(size),
                path=path,
                face=random.choice(config.face.emoticon))
            notify_list.append(hash)
            with open('notify_list', 'w') as w:
                notify_list_str = ''
                for x in notify_list:
                    notify_list_str += x+'\n'
                w.write(notify_list_str)
                w.close()
            notify(formatter)
