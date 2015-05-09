# !/usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import requests
from time import time
from bs4 import BeautifulSoup
import sys
import math
from lxml import etree, html


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


class GetContent(object):
    dict = {}
    def __init__(self, url):
        self.url = url
	self.session = requests.session()
        response = self.session.get(self.url)
        self.soup = BeautifulSoup(response.content)
        self.dict = {}
        self.list = []


    def parse(self, url):
	response = self.session.get(self.url)
	soup = BeautifulSoup(response.content)
	return soup

    # Get the (title of the) question
    def getTitle(self):
        soup = self.soup
        title = soup.find('title').string.replace('\n', '')
        print 'Title: ', title
        self.dict['title'] = title
    
    # Get the detail of this question
    # Frozen contemporaly
    def getDetail(self):
        soup = self.soup
        detail = soup.find('div', id = 'zh-question-detail').a.get_text()
        print 'Detail: ', detail
    
    
    # Get the number of the followers of the question
    def getNumberFollower(self):
        soup = self.soup
        try:
	    follower = int(soup.find("div", class_ = "zg-gray-normal").a.strong.string)
            self.dict['NumberFollower'] = follower
	    return follower
            print 'How many people following this question?', follower
	except:
	    follower = 0
	    print 'No people is following this question.'
        
    
    # Get the number of the ansmers for this question
    def getNumberAnswer(self):
        soup = self.soup
        try:
	    number_answer = int(soup.find('h3', id = "zh-question-answer-num")["data-num"])
            self.dict['answer'] = number_answer
	    return number_answer
            print 'How many answers are under this question: ', number_answer
	except:
	    number_answer = 0
	    print 'There is no answer under this question now.'


    # Get the number of all the upvotes for all the answers
    def getNumberUpvote(self):
        soup = self.soup
        number_up_vote = soup.find_all('span', class_ = 'count')
  	up_vote = 0
	for i in range(0, len(number_up_vote)):
#     	    print number_up_vote[i].string
#	    print type(number_up_vote[i].string)
#	    print type(int(number_up_vote[i].string))
	    up_vote += int(number_up_vote[i].string)
	self.dict['upvote'] = up_vote
        print 'How many people voted up for the answers: ', up_vote


    # Get the number of all the comment under this questiion
    def getNumberComment(self):
        soup = self.soup
	# find comments under each answer.
        comment = soup.find_all('a', class_ = ' meta-item toggle-comment')
	total_comment_number = 0
	for i in range(0, len(comment)):
	    commentContent = comment[i].get_text()
	    # Try to extract number in the string. If failed the number of the comments is 0.
	    try:
		commentNumber = int(filter(lambda x: x.isdigit(), commentContent))
		total_comment_number += commentNumber
	    except:
		commentNumber = 0
		total_comment_number += 0
	print 'How many comments under this question: ', total_comment_number

    
    # Get the topic of the question.
    # Frozen temporarily
    def getTopic(self):
        soup = self.soup
        topic = soup.find_all('a', class_ = 'zm-item-tag')
        for i in topic:
            print 'Topic: ', i.contents[0]
    
    

    # Get the number of the visitor of the question
    def getNumberVisitor(self):
        soup = self.soup
        number_visitor = soup.find('meta', itemprop = 'visitsCount')['content']
        self.dict['visitor'] = number_visitor
        print 'How many people have visited this question? ', number_visitor


    # get the number of people who follow the relevant topic of the question
    def getTopicFollower(self):
        soup = self.soup
        number_of_relevant_topic_follower_doc = soup.find_all('div', class_ = 'zg-gray-normal')[2]
	print len(number_of_relevant_topic_follower_doc)
	for i in number_of_relevant_topic_follower_doc:
	    print i
	number_of_relevant_topic_follower = number_of_relevant_topic_follower_doc.find('strong').string
	print 'Number of people who follows relevant topics: ', number_of_relevant_topic_follower


    # Frozen
    def getFunsAnswerer(self):
	soup = self.soup
	number_answer = self.getNumberAnswer()
	if number_answer == 0:
	    user_url = None
	elif number_answer > 0:
	    for i in range(0, number_answer):
	        try:
		    answer = soup.find_all('h3', class_ = 'zm-item-answer-author-wrap')[i].find('a')['href']
		    user_url = 'http://www.zhihu.com' + answer
#                   print 'The people who answered this question: ', user_url
                except:
                    None

    # Frozen
    def getFunsFollower(self):
	soup = self.soup
	try:
	    followers_link_part = soup.find('div', class_ = 'zh-question-followers-sidebar').div.find('a')['href']
	    followers_link = 'http://www.zhihu.com' + followers_link_part
	    print followers_link
	except:
	    followers_link = None

    
    def main(self):
	print 'type of url: ', type(self.url)
        self.getTitle()
        self.getNumberFollower()
        self.getNumberAnswer()
        self.getNumberUpvote()
        self.getNumberComment()
        self.getNumberVisitor()
        self.getTopicFollower()
#       self.getFunsAnswerer()    
#	self.getFunsFollower()


	


ZhihuLogin().main()
GetContent('http://www.zhihu.com/question/29702276').main()
