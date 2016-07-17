#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import sys

login_url = 'http://www.zhihu.com/login/email'
header = {'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Host': 'www.zhihu.com',
    'Referer':'http://www.zhihu.com/'
    }
# Read the email and password recorded in the file 'config.ini'
config = ConfigParser.ConfigParser()
# if os.path.isfile(../config.ini) == False:
config.read('../config.ini')
email = config.get('info', 'email')
password = config.get('info', 'password')
if email == '' or password == '':
    print 'Please configure the config.ini file firstly!'
    sys.exit(0)
