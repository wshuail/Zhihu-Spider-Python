# !/usr/bin/env python
# -*- coding: utf-8 -*-


import ConfigParser
import requests
from time import time
from bs4 import BeautifulSoup
import sys
import math
import json
import chardet
import re

reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.session()


class Login(object):
    """ 
    Login in www.zhihu.com firstly

    """
    def __init__(self):
        """
        define some essential objects, and get cookies for login in Zhihu.
        param str email
        param str password
        param dic header
        param '_xsrf': an random value, essential part of the post data for login. included in the cookies, or could be accessed from the web page.
        """
        self.login_url = 'http://www.zhihu.com/login'

	    # Read the email and password recorded in the file 'config.ini'
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        self.email = config.get('info', 'email')
        self.password = config.get('info', 'password')     

        response = session.post(self.login_url)
        
        # Get the value of '_xsrf' used for login.
        self._xsrf = dict(response.cookies)['_xsrf']

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
        self.data = {
                'email': self.email,
                'password': self.password,
                '_xsrf': self._xsrf,  # get from the cookies
                'rememberme': 'y'
                }


    # Get the captcha
    def captcha(self):
        """
        Download the figure for captcha.
        """
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + str(int(time()*1000))
        captcha = session.get(captcha_url)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha.content)


    # Post the data
    def login(self):
        """
        Post the data for login.
        """
        response = session.post(self.login_url, data = self.data, headers = self.header)
        return response



    def main(self):
        """
        post the data and login in, return the result of this trival.
        """
        session.headers.update(self.header)
        response = self.login()  # May fail due to the captcha. If so, login in after processing the captcha.       
        # judge if login successfully
        json = response.json()
        code = json['r']
        if code == 0:
            print 'Login Successfully !!!'
        elif code == 1:  # It's most likely that there is the captcha.
            self.captcha()
            print 'We have to input the captcha.\
                    Please open the file captcha.gif.'
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


class Monitor(object):
    dict = {}
    def __init__(self, url):
        self.url = url
        response = session.get(self.url)
        self.soup = BeautifulSoup(response.content)
        self.dict = {}
        self.list = []
        self.header = {
                'Host': 'www.zhihu.com',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Length': 133,
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
                }



        #def parse(self, url):
        #response = session.get(self.url)
        #soup = BeautifulSoup(response.content)
        # return soup

    # Get the (title of the) question
    def get_title(self):
        soup = self.soup
        title = soup.find('title').string.replace('\n', '')
        print 'Title: ', title
        self.dict['title'] = title
    
    # Get the detail of this question
    # Frozen contemporaly
    def get_detail(self):
        soup = self.soup
        detail = soup.find('div', id = 'zh-question-detail').text
        print 'Detail: ', detail

    # Get the data of the question
    def get_question_data(self):
        soup = self.soup
        total_follower_number_answerer = 0
        total_comment_number = 0
        total_upvote = 0
        _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
        # print 'The value of xsrf: ', _xsrf

        # Get the title
        title = soup.find('title').string.replace('\n', '')
        print 'Title: ', title

        # Get the details
        detail = soup.find('div', id = 'zh-question-detail').get_text().replace('\n', '')
        print 'The detail: ', detail

        # Get the number of the followers of the question
        try:
            follower_number = int(soup.find("div", class_ = "zg-gray-normal").a.strong.string)
            self.follower_number = follower_number
            self.dict['NumberFollower'] = follower_number
            print 'How many people following this question?', follower_number
        except:
            follower_number = 0
            self.follower_number = follower_number
            print 'No people is following this question.'
        
        # Get the number of visitor of this question.
        visitor_number = soup.find('meta', itemprop = 'visitsCount')['content']
        self.dict['visitor'] = visitor_number
        print 'How many people have visited this question? ', visitor_number


        # get the number of people who follow the relevant topic of the question
        topic_follower_number_doc = soup.find_all('div', class_ = 'zg-gray-normal')[2]
    	topic_follower_number = topic_follower_number_doc.find_all('strong')[1].string
        print 'How many people follow the relevant topics: ', topic_follower_number
        
        # Get the number of answer under this question.
        try:
            answer_number = int(soup.find('h3', id = 'zh-question-answer-num')['data-num'])
            # print 'How many answers are under this question: ', answer_number

            if answer_number:
                self.answer_number = answer_number
                for i in xrange((answer_number - 1)/50 + 1):
                    if i == 0:  # All answers are on this page.

                        # get the number of users followering the people who answered.
                        people_link_docs = soup.find_all('h3', class_ = 'zm-item-answer-author-wrap')
                        for people_link_doc in people_link_docs:
                            if people_link_doc.string != '匿名用户':
                                people_link_part = people_link_doc.find('a')['href']
                                people_link = 'http://www.zhihu.com' + people_link_part
                                print 'The people who answered this question: ', people_link
                                response = session.get(people_link)
                                soup = BeautifulSoup(response.content)
                                # Get the funs of this user.
                                funs = soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                                funs = int(funs)
                                # print funs
                                total_follower_number_answerer += funs
                            else:
                                None
                        print 'How many followers of this people?', total_follower_number_answerer

                        # Get the number of comments under the answers.
                        try:
                            comment_docs = soup.find_all('a', class_ = ' meta-item toggle-comment')
                            for comment_doc in comment_docs:
                                comment_content = comment_doc.get_text()
                                comment_number = filter(lambda x: x.isdigit(), comment_content)
                                if comment_number != '':
                                    comment_number = int(comment_number)
                                    total_comment_number += comment_number
                                else:
                                    comment_number = 0
                                    total_comment_number += comment_number
                        except:
                            print 'The answer is forbiden.'
                            comment_number = 0
                            total_comment_number += comment_number
                        print 'Number of total comments: ', total_comment_number

                        # Get the total number of upvote
                        try:
                            upvote_number_docs = soup.find_all('span', class_ = 'count')
                            for upvote_number_doc in upvote_number_docs:
                                upvote_number = int(upvote_number_doc.string)
                                total_upvote += upvote_number
                        except:
                            print 'The annswer is forbiden.'
                            upvote_number = 0
                            total_upvote += upvote_number
                        print 'How many people voted up for the answers: ', total_upvote

                    
                    # Or, The answers beyond 50 need post data.  
                    else:
                        print 'The answers are more than 50.'
                        post_url = 'http://www.zhihu.com/node/QuestionAnswerListV2'
                        offset = i*50
                        params = json.dumps({
                                'url_token': int(self.url[-8:]), 'pagesize': 50,
                                'offset': offset
                                })
                        post_data = {
                                'method': 'next',
                                'params': params,
                                '_xsrf': _xsrf
                                }
                        self.header['Referer'] = post_url
                        response = session.post(post_url, data = post_data, headers = self.header)
                        post_status = response.json()['r']
                        # print 'Post status: ', post_status
                        answer_list = response.json()['msg']
                        for j in xrange(min(50, answer_number - i*50)):
                            soup = BeautifulSoup(answer_list[j])
                            # Get the number of users who follows the people who answered.
                            people_link_docs = soup.find_all('h3', class_ = 'zm-item-answer-author-wrap')
                            if people_link_doc.string != '匿名用户':
                                people_link_part = people_link_doc.find('a')['href']
                                people_link = 'http://www.zhihu.com' + people_link_part
                                # print people_link
                                # Get the number of his (her) followers.
                                # soup = self.parse(people_link)
                                response = session.get(people_link)
                                people_soup = BeautifulSoup(response.content)
                                funs = people_soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                                funs = int(funs)
                                total_follower_number_answerer += funs
                            else:
                                None  # Anonymous user.

                            print 'How many people are following the people who answer this question ?', total_follower_number_answerer
                            # Get the number of comments under the answers.
                            comment_docs = soup.find('a', class_ = ' meta-item toggle-comment')
                            comment_content = comment_docs.get_text()
                            comment_number = filter(lambda x: x.isdigit(), comment_content)
                            if comment_number != '':
                                total_comment_number += int(comment_number)
                            else:
                                None
                            print 'Number of total comments: ', total_comment_number

                            # Get the total number of upvote
                            upvote_number_docs = soup.find('span', class_ = 'count')
                            upvote_number = int(upvote_number_doc.string)
                            total_upvote += upvote_number
                            print 'How many people voted up for the answers: ', total_upvote
            else:
                print 'There is no answer. But the error could not be figured out.'
            
            print 'How many people are following this question?', follower_number 
            print 'How many visitor of this question?', visitor_number
            print 'How many people are following the relavant topics?', topic_follower_number
            print 'How many answers are under this question ?', answer_number 
            print 'How many comments are under this question?', total_comment_number
            print 'How many people voted up for the answers: ', total_upvote
            print 'How many people are following the people who answer this question ?', total_follower_number_answerer

        except:
            question_url = soup.find('h3').find('a')['href']
            print question_url
        
    def get_funs_of_follower(self):
        soup = self.soup
        follower_number = self.follower_number
        _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
        # print 'The value of xsrf: ', _xsrf
        total_count = 0
        if follower_number == 0:
            None
        else:
            try:
                followers_link_part = soup.find('div', class_ = 'zh-question-followers-sidebar').div.find('a')['href']
                followers_link = 'http://www.zhihu.com' + followers_link_part
                print followers_link
                # soup = self.parse(followers_link)
                response = session.get(followers_link)
                soup = BeautifulSoup(response.content)
                for i in xrange((follower_number - 1)/20 + 1):
                    if i == 0:
                        funs = soup.find_all('div', class_ = 'details zg-gray')
                        for fun in funs:
                            fun_number = fun.find('a')
                            # print fun_number.string
                            fun_number = int(filter(lambda x: x.isdigit(), fun_number.string))
                            # print fun_number
                            total_count += fun_number
                        print 'How many people are following the people who follows this question?', total_count
                    else:
                        # print 'More than 20 people follow this question.'
                        post_link = followers_link
                        # print post_link
                        self.header['Referer'] = post_link
                        offset = i*20
                        post_data = {
                                'start': 0,
                                'offset': offset,
                                '_xsrf': _xsrf
                                }
                        response = session.post(post_link, data = post_data, headers = self.header)
                        response_status = response.json()['r']
                        # print 'The status of response: ', response_status
                        follower_lists = response.json()['msg'][1]
                        soup = BeautifulSoup(follower_lists)
                        funs = soup.find_all('div', class_ = 'details zg-gray')
                        for fun in funs:
                            fun_number = fun.find('a')
                            fun_number = int(filter(lambda x: x.isdigit(), fun_number.string))
                            # print fun_number
                            total_count += fun_number
                        print 'How many people are following the people who follows this question?', total_count

            except:
                followers_link = None

            print 'How many people are following the people who follows this question?', total_count
    
    def main(self):
        #self.get_title()
        #self.get_detail()
        self.get_question_data()
        self.get_funs_of_follower()


class Collector(object):

    def __init__(self):
        self.initial_url = 'http://www.zhihu.com/log/questions'
        response = session.get(self.initial_url)
        self.soup = BeautifulSoup(response.content)
        self._xsrf = self.soup.find('input', attrs = {'name': '_xsrf'})['value']
        self.header = {
                'Host': 'www.zhihu.com',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Length': 64,
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
                }

    def main(self):
        soup = self.soup
        question_poll = []
        while len(question_poll) < 30:
            question_docs = soup.find_all('h2', class_ = 'zm-item-title')
            for question_doc in question_docs:
                question_link_part = question_doc.find('a')['href']
                question_link = 'http://www.zhihu.com' + question_link_part
                print question_link
                question_poll.append(question_link)

            start_value_doc = soup.find_all('div', class_ = 'zm-item')[19]['id']
            start_value = str(start_value_doc[-9:])
            # print start_value
            question_number = len(question_poll)
            self.header['Referer'] = self.initial_url
            post_data = {
                    'start': start_value,
                    'offset': question_number,
                    '_xsrf': self._xsrf
                    }
            response = session.post(self.initial_url, data = post_data, headers = self.header)
            response_status = response.json()['r']
            # print response_status

            question_list = response.json()['msg'][1]
            soup = BeautifulSoup(question_list)

Login().main()
# Monitor().main()
Collector().main()
