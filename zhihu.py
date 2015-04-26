# !/usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import requests
from time import time
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ZhihuLogin(object):
    '''
    Login in www.zhihu.com firstly

    '''
    def __init__(self):
	'''
	define some essential objects, and get cookies for login in Zhihu.
	param str email
	param str password
	param dic header
	param '_xsrf': an random value, essential part of the post data for login. included in the cookies, or could be accessed from the web page.
	'''
	self.login_url = 'http://www.zhihu.com/login'

	# Read the email and password recorded in the file 'config.ini'
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	self.email = config.get('info', 'email')
	self.password = config.get('info', 'password')     
	self.email = email
        self.password = password

	# Create an instance of requests(module)
	self.session = requests.session()
	s = self.session.post(self.login_url)
	
	# Get the value of '_xsrf' used for login.
        self._xsrf = dict(s.cookies)['_xsrf']

	# The header. 
        self.header = {
		    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'Keep-Alive',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'www.zhihu.com',
                    'DNT': '1'
                    }

	# The post data
        self.data = {'email': self.email,
                    'password': self.password,
                    '_xsrf': self._xsrf,  # get from the cookies
                    'rememberme': 'y'}


    # Get the captcha
    def captcha(self):
	'''
	Download the figure for captcha.
	'''
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(int(time()*1000))
        captcha = self.session.get(captcha_url)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha.content)


    # Post the data
    def login(self):
	'''
	Post the data for login.
	'''
        response = self.session.post(self.login_url, data = self.data, headers = self.header)
        return response



    def main(self):
	'''
	post the data and login in, return the result of this trival.
	'''
	self.session.headers.update(self.header)
	response = self.login()  # May fail due to the captcha. If so, login in after processing the captcha.       
	# judge if login successfully
        json = response.json()
	code = json['r']
        if code == 0:
            print 'Login Successfully !!!'
        elif code == 1:  # It's most likely that there is the captcha.
            self.captcha()
            print 'We have to input the captcha.\nPlease open the file captcha.gif.\n'
            captcha = raw_input('Enter the characters on the figure here: ')
            captcha = str(captcha)
            self.data['captcha'] = captcha  # Add the values of the captcha in the form data.
            response = self.login()  # Try to login in again.
            json = response.json()
            code = json['r']  # Check if login in successfully the second time.
            if code == 1:
                print 'Login Failed !!!'
                for code, description in json.items():
                    print 'Here is the information about the failure login, %s: %s' %(code, description)
            elif code == 0:
                print 'Login Successfully!'
            else:
                print 'OOPS! Please dno\'t to hesitate with me, and I will fix this error asap.'
	else:
	    print 'OOPS! Please dno\'t to hesitate with me, and I will fix this error asap.'

ZhihuLogin().main()

