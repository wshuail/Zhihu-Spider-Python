# !/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import time
from bs4 import BeautifulSoup
import sys
import json
import re
import os
import lxml

reload(sys)
sys.setdefaultencoding('utf-8')

class Zhihu(object):

    def __init__(self, session = None, soup = None):
        self.session = None
        self.soup = None
        self.login_url = 'http://www.zhihu.com/login/email'
        self.header = {'X-Requested-With': 'XMLHttpRequest',
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
        self.email = config.get('info', 'email')
        self.password = config.get('info', 'password')
        if self.email == '' or self.password == '':
            print 'Please configure the config.ini file firstly!'
            sys.exit(0)


    def login(self):
        """
        Login in www.zhihu.com firstly

        Args:
            None

        Returns:
            session login in.

        """

        # Get the value of '_xsrf' used for login.
        session = requests.session()
        response = session.get(self.login_url, headers = self.header)
        self.soup = BeautifulSoup(response.content)
        _xsrf = self.soup.find('input', attrs = {'name': '_xsrf'})['value']

        # The post data
        data = {
                'email': self.email,
                'password': self.password,
                '_xsrf': _xsrf,  # get from the cookies
                'rememberme': 'y'
                }

        session = requests.session()
        response = session.post(self.login_url, data = data, headers = self.header)
        print 'response: ', response.status_code

        # judge if login successfully
        json = response.json()
        print 'json: ', json['msg']
        code = json['r']
        if code == 0:
            print 'Login Successfully !!!'
        elif code == 1:  # It's most likely that there is the captcha.
            captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(int(time.time()*1000))
            captcha = session.get(captcha_url)
            with open('captcha.gif', 'wb') as f:
                f.write(captcha.content)

            print 'Please open the file captcha.gif and enter the captcha.'
            captcha = raw_input('Enter the characters on the figure here: ')
            captcha = str(captcha)
            data['captcha'] = captcha  # Add the values of the captcha in the form data.
            # Post data with captcha.
            response = session.post(self.login_url, data = data, headers = self.header)
            print 'response: ', response.status_code
            json = response.json()
            code = json['r']  # Check if login in successfully the second time.
            if code == 0:
                print 'Login Successfully !!!'
            elif code == 1:
                print 'Login Failed !!!'
                for code, description in json.items():
                    print 'Here is the information about the failure login, %s: %s' %(code, description)
                    sys.exit(0)
            else:
                print 'OOPS! Please don\'t hesitate to contact with me, and I will fix this bug asap.'
                sys.exit(0)
        else:
            print 'OOPS! Please don\'t hesitate to contact with me, and I will fix this bug asap.'
            sys.exit(0)

        self.session = session

        return self.session

    def parse(self, url):
        if self.session == None:
            self.session = self.login()

        response = self.session.get(url)
        if response.status_code == 200:
            try:
                self.soup = BeautifulSoup(response.content, 'lxml')
            except:
                self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            print 'Failed to open the url.'
        return self.soup

