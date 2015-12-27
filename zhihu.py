# !/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import time
from bs4 import BeautifulSoup
import sys
from sys import exit
import math
import json
import MySQLdb
from random import randint
from chardet import detect

reload(sys)
sys.setdefaultencoding('utf-8')

session = None


def login():
    """ 
    Login in www.zhihu.com firstly

    Args:
        None

    Returns:
        session login in.

    """

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
    config.read('config.ini')
    email = config.get('info', 'email')
    password = config.get('info', 'password')     
    if email == '' or password == '':
        print 'Please configure the config.ini file firstly!'
        exit(0)

    global session

    # Get the value of '_xsrf' used for login.
    session = requests.session()
    response = session.get(login_url, headers = header)
    soup = BeautifulSoup(response.content)
    _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']

    # The post data
    data = {
            'email': email,
            'password': password,
            '_xsrf': _xsrf,  # get from the cookies
            'rememberme': 'y'
            }

    session = requests.session()
    response = session.post(login_url, data = data, headers = header)

    # judge if login successfully
    json = response.json()
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
        response = session.post(login_url, data = data, headers = header)
        json = response.json()
        code = json['r']  # Check if login in successfully the second time.
        if code == 0:
            print 'Login Successfully !!!'
        elif code == 1:
            print 'Login Failed !!!'
            for code, description in json.items():
                print 'Here is the information about the failure login, %s: %s' %(code, description)
        else:
            print 'OOPS! Please don\'t to hesitate with me, and I will fix this bug asap.'
    else:
        print 'OOPS! Please don\'t to hesitate with me, and I will fix this bug asap.'

class Question(object):

    def __init__(self, url):
        self.url = url
        self.soup = None

    def parse(self, url):
        global session
        if session == None:
            login()

        response = session.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content)
        self.soup = soup
        return self.soup


    def get_title(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        title = self.soup.find('title').string.replace('\n', '')
        return title

    def get_detail(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        detail = self.soup.find('div', id = 'zh-question-detail').find('div', class_ = 'zm-editable-content').get_text() 
        if detail:
            return detail
        else:
            return None

    def get_visitor_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        visitor_number = self.soup.find('meta', itemprop = 'visitsCount')['content']
        if visitor_number:
            return visitor_number
        else:
            visitor_number = 0
            return visitor_number

    def get_topic_follower_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        topic_follower_number_doc = self.soup.find_all('div', class_ = 'zg-gray-normal')[2]
        topic_follower_number = topic_follower_number_doc.find_all('strong')[1].string
        if topic_follower_number:
            return topic_follower_number
        else:
            topic_follower_number = 0
            return topic_follower_number


