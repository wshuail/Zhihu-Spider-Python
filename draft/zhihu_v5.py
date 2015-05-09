# !/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import time
from bs4 import BeautifulSoup
import sys
import math
import json

reload(sys)
sys.setdefaultencoding('utf-8')

session = None


def login():
    """ 
    Login in www.zhihu.com firstly

    define some essential objects, and get cookies for login in Zhihu.
    param str email
    param str password
    param dic header
    param '_xsrf': an random value, essential part of the post data for login. included in the cookies, or could be accessed from the web page.
    """

    login_url = 'http://www.zhihu.com/login'

    # Read the email and password recorded in the file 'config.ini'
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    email = config.get('info', 'email')
    password = config.get('info', 'password')     

    global session
    session = requests.session()
    response = session.post(login_url)

    # Get the value of '_xsrf' used for login.
    _xsrf = dict(response.cookies)['_xsrf']

    # The header. 
    header = {
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
    data = {
            'email': email,
            'password': password,
            '_xsrf': _xsrf,  # get from the cookies
            'rememberme': 'y'
            }


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


        
        
        print 'We have to input the captcha.\n Please open the file captcha.gif.'
        captcha = raw_input('Enter the characters on the figure here: ')
        captcha = str(captcha)
        data['captcha'] = captcha  # Add the values of the captcha in the form data.
        response = session.post(login_url, data = data, headers = header)
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


def monitor(url):
    """
    Get the data about the question

    Args: 
        (A list contains) the link(s) of the question

    Returns: A dict mapping items and its value
        Title: the title of the question
        Detail length: the length of the detail description
        Answer number: the number of the answers
        Follower number: the number of the followers of the question
        Visitor number: the total number of the people who visited this question
        Topic followers: The total number of the people who followed the relavant topic 
        Vote number: the total number of the upvotes of all answers
        Comment number: the total number of the comments under all answers
        Follower of answerers: the total number of the followers of people who answer the question
        follower of follower: the total number of the followers of the people who answer the question

    """
    global session
    if session == None:
        login()
    # session = requests.session()
    response = session.get(url)
    soup = BeautifulSoup(response.content)
    dict = {}
    list = []
    header = {
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

    total_follower_number_answerer = 0
    total_comment_number = 0
    total_upvote = 0
    total_follower_follower = 0
    follower_number = 0
    
    _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
    # print 'The value of xsrf: ', _xsrf
    
    scrapy_time = time.strftime('%m-%d-%Y')
    dict['time'] = scrapy_time

    # get the id of the question
    id = url[-8: ]
    dict['id'] = id
    # print 'The id: ', id

    # Get the title
    title = soup.find('title').string.replace('\n', '')
    dict['len_title'] = len(title)
    # print 'Title: ', title

    # Get the details
    detail = soup.find('div', id = 'zh-question-detail').get_text().replace('\n', '')
    len_detail = len(detail)
    dict['len_detail'] = len_detail
    # print 'The detail: ', detail

    # Get the number of visitor of this question.
    visitor_number = soup.find('meta', itemprop = 'visitsCount')['content']
    dict['visitor_num'] = visitor_number
    # print 'How many people have visited this question? ', visitor_number

    # get the number of people who follow the relevant topic of the question
    topic_follower_number_doc = soup.find_all('div', class_ = 'zg-gray-normal')[2]
    topic_follower_number = topic_follower_number_doc.find_all('strong')[1].string
    dict['topic_follower_num'] = topic_follower_number
    # print 'How many people follow the relevant topics: ', topic_follower_number
    


    # Get the number of the followers of the question
    if soup.find('div', class_ = 'zh-question-followers-sidebar').get_text() != '还没有人关注该问题':
        follower_number = int(soup.find("div", class_ = "zg-gray-normal").a.strong.string)
        # print 'How many people following this question?', follower_number
        dict['follower_num'] = follower_number

        # Get the number of people who follow the people following the question
        followers_link_part = soup.find('div', class_ = 'zh-question-followers-sidebar').div.find('a')['href']
        followers_link = 'http://www.zhihu.com' + followers_link_part
        # print followers_link

        follower_response = session.get(followers_link)
        follower_soup = BeautifulSoup(follower_response.content)
        _xsrf = follower_soup.find('input', attrs = {'name': '_xsrf'})['value']
        
        for i in xrange((follower_number - 1)/20 + 1):
            if i == 0:
                if follower_soup.find_all('div', class_ = 'details zg-gray') != None:
                    user_detail_docs = follower_soup.find_all('div', class_ = 'details zg-gray')
                    for user_detail_doc in user_detail_docs:
                        follower_doc = user_detail_doc.find('a').string
                        # print follower_doc.string
                        follower_number = int(filter(lambda x: x.isdigit(), follower_doc))
                        # print follower_number
                        total_follower_follower += follower_number
                    # print 'How many people are following the people who follows this question?', total_follower_follower
                else:
                    # print 'All followers are anonymous.'
                    follower_number = 0
                    total_follower_follower += follower_number

                # print 'How many people are following the people who follows this question?', total_follower_follower

            else:
                # print 'More than 20 people follow this question.'
                post_link = followers_link
                # print post_link
                header['Referer'] = post_link
                offset = i*20
                post_data = {
                        'start': 0,
                        'offset': offset,
                        '_xsrf': _xsrf
                        }
                more_follower_response = session.post(post_link, data = post_data, headers = header)
                response_status = more_follower_response.json()['r']
                # print 'The status of response: ', response_status
                follower_lists = more_follower_response.json()['msg'][1]
                # print follower_lists
                more_follower_soup = BeautifulSoup(follower_lists)
                if more_follower_soup.find_all('div', class_ = 'details zg-gray') != None:
                    user_detail_docs = more_follower_soup.find_all('div', class_ = 'details zg-gray')
                    for user_detail_doc in user_detail_docs:
                        follower_doc = user_detail_doc.find('a').string
                        # print follower_doc.string
                        follower_number = int(filter(lambda x: x.isdigit(), follower_doc))
                        # print follower_number
                        total_follower_follower += follower_number
                    # print 'How many people are following the people who follows this question?', total_follower_follower

                else:
                    # print 'All followers are anonymous.'
                    follower_number = int(response.json()['msg'][0])
                    total_follower_follower += follower_number
        
                # print 'How many people are following the people who follows this question?', total_follower_follower

        dict['follower_follower'] = total_follower_follower
    
    else:
        follower_number = 0
        total_follower_follower += follower_number
        # print 'No people is following this question.'
        
        dict['follower_num'] = follower_number
        dict['follower_follower'] = total_follower_follower

   
    # Get the number of answer under this question.
    if soup.find('h3', id = 'zh-question-answer-num') != None: 
        answer_number = int(soup.find('h3', id = 'zh-question-answer-num')['data-num'])
        # print 'How many answers are under this question: ', answer_number

        # Get the number of people who follow the user answering the question.
        for i in xrange((answer_number - 1)/50 + 1):
            if i == 0:  # All answers are on this page.

                # get the number of users followering the people who answered.
                people_link_docs = soup.find_all('h3', class_ = 'zm-item-answer-author-wrap')
                for people_link_doc in people_link_docs:
                    if people_link_doc.string != '匿名用户':
                        people_link_part = people_link_doc.find('a')['href']
                        people_link = 'http://www.zhihu.com' + people_link_part
                        # print 'The people who answered this question: ', people_link
                        
                        people_response = session.get(people_link)
                        people_soup = BeautifulSoup(people_response.content)
                        # Get the funs of this user.
                        funs = people_soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                        funs = int(funs)
                        # print funs
                        total_follower_number_answerer += funs
                    else:
                        funs = 0
                # print 'How many followers of this people?', total_follower_number_answerer
                
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
                    # print 'The answer is forbiden.'
                    comment_number = 0
                    total_comment_number += comment_number
                # print 'Number of total comments: ', total_comment_number

                # Get the total number of upvote
                try:
                    upvote_number_docs = soup.find_all('span', class_ = 'count')
                    for upvote_number_doc in upvote_number_docs:
                        upvote_number = int(upvote_number_doc.string)
                        total_upvote += upvote_number
                except:
                    # print 'The annswer is forbiden.'
                    upvote_number = 0
                    total_upvote += upvote_number
                # print 'How many people voted up for the answers: ', total_upvote

            # Or, The answers beyond 50 need post data.  
            else:
                # print 'The answers are more than 50.'
                post_url = 'http://www.zhihu.com/node/QuestionAnswerListV2'
                offset = i*50
                params = json.dumps({
                        'url_token': int(url[-8: ]), 'pagesize': 50,
                        'offset': offset
                        })
                post_data = {
                        'method': 'next',
                        'params': params,
                        '_xsrf': _xsrf
                        }
                header['Referer'] = post_url
                more_answer_response = session.post(post_url, data = post_data, headers = header)
                post_status = more_answer_response.json()['r']
                # print 'Post status: ', post_status
                answer_list = more_answer_response.json()['msg']
                
                for j in xrange(min(50, answer_number - i*50)):
                    more_answer_soup = BeautifulSoup(answer_list[j])
                    # Get the number of users who follows the people who answered.
                    people_link_docs = more_answer_soup.find_all('h3', class_ = 'zm-item-answer-author-wrap')
                    for people_link_doc in people_link_docs:
                        if people_link_doc.string != '匿名用户':
                            people_link_part = people_link_doc.find('a')['href']
                            people_link = 'http://www.zhihu.com' + people_link_part
                            # print people_link
                            
                            # Get the number of his (her) followers.
                            answerer_response = session.get(people_link)
                            answerer_soup = BeautifulSoup(answerer_response.content)
                            funs = answerer_soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                            funs = int(funs)
                            # print funs
                            total_follower_number_answerer += funs
                        else:
                            None  # Anonymous user.
                    # print 'How many people are following the people who answer this question ?', total_follower_number_answerer
                    # Get the number of comments under the answers.
                    try:
                        comment_docs = soup.find('a', class_ = ' meta-item toggle-comment')
                        comment_content = comment_docs.get_text()
                        comment_number = filter(lambda x: x.isdigit(), comment_content)
                        if comment_number != '':
                            total_comment_number += int(comment_number)
                        else:
                            None
                    except:
                        # print 'The answer is forbiden.'
                        comment_number = 0
                        total_comment_number += comment_number
                    # print 'Number of total comments: ', total_comment_number

                    # Get the total number of upvote
                    try:
                        upvote_number_docs = soup.find('span', class_ = 'count')
                        upvote_number = int(upvote_number_doc.string)
                        total_upvote += upvote_number
                    except:
                        upvote_number = 0
                        total_upvote  += upvote_number
                    # print 'How many people voted up for the answers: ', total_upvote
    
    else:
        answer_number = 0
    
    dict['answer_num'] = answer_number
    dict['followers_answerer'] = total_follower_number_answerer
    dict['comment_num'] = total_comment_number
    dict['upvote_num'] = total_upvote
    
    # print 'How many people are following this question?', follower_number 
    # print 'How many visitor of this question?', visitor_number
    # print 'How many people are following the relavant topics?', topic_follower_number
    # print 'How many answers are under this question ?', answer_number 
    # print 'How many comments are under this question?', total_comment_number
    # print 'How many people voted up for the answers: ', total_upvote
    # print 'How many people are following the people who answer this question ?', total_follower_number_answerer
    
    return dict

def collect():

    """
    Collect questions for monitoring.
    """

    initial_url = 'http://www.zhihu.com/log/questions'
    
    global session
    if session == None:
        login()
    response = session.get(initial_url)
    soup = BeautifulSoup(response.content)
    _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
    header = {
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

    question_poll = []
    while len(question_poll) < 30:
        question_docs = soup.find_all('h2', class_ = 'zm-item-title')
        for question_doc in question_docs:
            question_link_part = question_doc.find('a')['href']
            question_link = 'http://www.zhihu.com' + question_link_part
            # print question_link
            question_poll.append(question_link)

        start_value_doc = soup.find_all('div', class_ = 'zm-item')[19]['id']
        start_value = str(start_value_doc[-9: ])
        
        # print start_value
        question_number = len(question_poll)
        header['Referer'] = initial_url
        post_data = {
                'start': start_value,
                'offset': question_number,
                '_xsrf': _xsrf
                }
        response = session.post(initial_url, data = post_data, headers = header)
        response_status = response.json()['r']
        # print response_status

        question_list = response.json()['msg'][1]
        soup = BeautifulSoup(question_list)
        
        return question_poll


# monitor('http://www.zhihu.com/question/29990577')
