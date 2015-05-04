# !/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import time
from bs4 import BeautifulSoup
import sys
import math
import json
import MySQLdb


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
            print 'OOPS! Please dno\'t to hesitate with me, and I will fix this bug asap.'
    else:
        print 'OOPS! Please dno\'t to hesitate with me, and I will fix this bug asap.'


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
    
    # Exclude unvalid url
    if response.status_code == 200:
        soup = BeautifulSoup(response.content)
    
    # store data in a dictionary
    dict = {}

    # Get the follower or the people answering the question who has the most funs. 
    answerer_most_funs = [0]  # Avoid empty list for max() function.
    follower_most_funs = [0]  # Avoid empty list for max() function.

    # Initilize some data
    total_follower_number_answerer = 0
    total_comment_number = 0
    total_upvote = 0
    total_follower_follower = 0
    follower_number = 0
 
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
    
    # xsrf is one part of the data
    _xsrf = soup.find('input', attrs = {'name': '_xsrf'})['value']
    # print 'The value of xsrf: ', _xsrf
    
    # Get the sampling time
    scrapy_time = time.strftime('%Y-%m-%d-%H')
    dict['time'] = scrapy_time

    # get the id of the question
    question_id = url[-8: ].encode('utf-8')
    dict['question_id'] = question_id
    # print 'The question id: ', question_id

    # Get the length of the title
    title = soup.find('title').string.replace('\n', '')
    dict['len_title'] = len(title)
    # print 'Title: ', title

    # Get the length of the  details
    detail = soup.find('div', id = 'zh-question-detail').get_text().replace('\n', '')
    len_detail = len(detail)
    dict['len_detail'] = len_detail
    # print 'The detail: ', detail

    # Get the number of visitor of this question.
    visitor_number = soup.find('meta', itemprop = 'visitsCount')['content']
    dict['visitor_num'] = int(visitor_number)
    # print 'How many people have visited this question? ', visitor_number

    # get the number of people who follow the relevant topic of the question
    topic_follower_number_doc = soup.find_all('div', class_ = 'zg-gray-normal')[2]
    topic_follower_number = topic_follower_number_doc.find_all('strong')[1].string
    dict['topic_follower_num'] = int(topic_follower_number)
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

        # The value of xsrf is one part of the post data for more information on this page.
        _xsrf = follower_soup.find('input', attrs = {'name': '_xsrf'})['value']
        
        # More than one page of followers would be considered.
        for i in xrange((follower_number - 1)/20 + 1):
            if i == 0:  # the first (<)20 followers.
                if follower_soup.find_all('div', class_ = 'details zg-gray') != None:
                    user_detail_docs = follower_soup.find_all('div', class_ = 'details zg-gray')
                    for user_detail_doc in user_detail_docs:
                        follower_doc = user_detail_doc.find('a').string
                        # print follower_doc.string
                        follower_number = int(filter(lambda x: x.isdigit(), follower_doc))
                        
                        # Put each value into the list for the follower with most funs.
                        follower_most_funs.append(follower_number)
                        # print follower_number

                        # Count the total funs of the followers.
                        total_follower_follower += follower_number
                    # print 'How many people are following the people who follows this question?', total_follower_follower
                else:
                    # print 'All followers are anonymous.'
                    follower_number = 0
                    follower_most_funs.append(follower_number)
                    total_follower_follower += follower_number

                # print 'How many people are following the people who follows this question?', total_follower_follower

            else:  # More than 20 people are following the question
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
                
                # Judge if post successfully
                # response_status = more_follower_response.json()['r']
                # print 'The status of response: ', response_status
                
                # Get the lists of more followers' information.
                follower_lists = more_follower_response.json()['msg'][1]
                # print follower_lists
                more_follower_soup = BeautifulSoup(follower_lists)
                
                # Avoid anonymous followers.
                if more_follower_soup.find_all('div', class_ = 'details zg-gray') != None:
                    user_detail_docs = more_follower_soup.find_all('div', class_ = 'details zg-gray')
                    for user_detail_doc in user_detail_docs:
                        follower_doc = user_detail_doc.find('a').string
                        # print follower_doc.string
                        follower_number = int(filter(lambda x: x.isdigit(), follower_doc))
                        
                        # Put each value into the list for the follower with most funs.
                        follower_most_funs.append(follower_number)
                        # print follower_number
                        
                        # Count total number the followers' funs
                        total_follower_follower += follower_number
                    # print 'How many people are following the people who follows this question?', total_follower_follower

                else:
                    # '(All) the followers are anonymous.'
                    # The number of their followers could not be figured out. 
                    follower_number = 0
                    # Put each value into the list for the follower with most funs.
                    follower_most_funs.append(follower_number)
                    # Count total number the followers' funs
                    total_follower_follower += follower_number
        
                # print 'How many people are following the people who follows this question?', total_follower_follower
        
        # Get the number of follower with most funs, and save it into the dictionary. 
        bigest_follower = max(follower_most_funs)
        dict['bigest_follower'] = int(bigest_follower)

        dict['follower_follower'] = total_follower_follower
    
    else:
        # No people is followring the question.
        follower_number = 0
        total_follower_follower += follower_number
        # print 'No people is following this question.'
        
        dict['follower_num'] = follower_number
        dict['bigest_follower'] = 0
        dict['follower_follower'] = total_follower_follower

   
    # Get the number of answer under this question.
    # Judge if there is answer under this question.
    if soup.find('h3', id = 'zh-question-answer-num') != None: 
        answer_number = int(soup.find('h3', id = 'zh-question-answer-num')['data-num'])
        # print 'How many answers are under this question: ', answer_number

        # Get the number of people who follow the user answering the question.
        # Judge if the number if answer is more than 50.
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
                        answerer_funs = people_soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                        answerer_funs = int(answerer_funs)
                        # print answerer funs 
                        # Put it into the dictionary for the people with most funs.
                        answerer_most_funs.append(answerer_funs)
                        # Get the total funs's number of the people ansering this question.
                        total_follower_number_answerer += answerer_funs
                    
                    else:  # The people answering this question are(is) anonymous.
                        answerer_funs = 0
                        answerer_most_funs.append(answerer_funs)
                        total_follower_number_answerer += answerer_funs
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

                except:  # The answer is forbiden.
                    comment_number = 0
                    total_comment_number += comment_number
                # print 'Number of total comments: ', total_comment_number

                # Get the total number of upvote
                try:
                    upvote_number_docs = soup.find_all('span', class_ = 'count')
                    for upvote_number_doc in upvote_number_docs:
                        upvote_number = int(upvote_number_doc.string)
                        total_upvote += upvote_number
                except:  # The annswer is forbiden.
                    upvote_number = 0
                    total_upvote += upvote_number
                # print 'How many people voted up for the answers: ', total_upvote

            # Or, The number of answers are beyond 50 and need post data.  
            else:
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
                # post_status = more_answer_response.json()['r']
                # print 'Post status: ', post_status
                # Get the list containing more answers.
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
                            answerer_funs = answerer_soup.find('div', class_ = 'zm-profile-side-following zg-clear').find_all('a')[1].strong.string
                            answerer_funs = int(answerer_funs)
                            # print answerer_funs
                            # Put into the dictionary for people wiith most funs 
                            answerer_most_funs.append(answerer_funs)
                            # Get the total number of funs of the peoples asswering this question.
                            total_follower_number_answerer += answerer_funs
                        
                        else:
                            # Anonymous user
                            answerer_funs = int(answerer_funs)
                            # print answerer_funs
                            answerer_most_funs.append(answerer_funs)
                            total_follower_number_answerer += answerer_funs
                    # print 'How many people are following the people who answer this question ?', total_follower_number_answerer
                    
                    # Get the number of comments under the answers.
                    try:
                        comment_docs = soup.find('a', class_ = ' meta-item toggle-comment')
                        comment_content = comment_docs.get_text()
                        comment_number = filter(lambda x: x.isdigit(), comment_content)
                        if comment_number != '':
                            total_comment_number += int(comment_number)
                        else:
                            comment_number = 0
                            total_comment_number += comment_number
                    
                    except:  # The answer is forbiden.
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
        
        # Get the number of funs for people with most followers
        bigest_answerer = max(answerer_most_funs)

    else:
        answer_number = 0
        bigest_answerer = 0
    
    dict['answer_num'] = answer_number
    dict['followers_answerer'] = total_follower_number_answerer
    dict['comment_num'] = total_comment_number
    dict['upvote_num'] = total_upvote
    dict['bigest_answerer'] = bigest_answerer
    # print 'How many people are following this question?', follower_number 
    # print 'How many visitor of this question?', visitor_number
    # print 'How many people are following the relavant topics?', topic_follower_number
    # print 'How many answers are under this question ?', answer_number 
    # print 'How many comments are under this question?', total_comment_number
    # print 'How many people voted up for the answers: ', total_upvote
    # print 'How many people are following the people who answer this question ?', total_follower_number_answerer
    
    return dict


def collect(x):

    """
    Collect questions for monitoring.i

    Args:
        Number of question need to be collected.

    Returns: 
        A json format file containing all the links of the questions.
    """

    initial_url = 'http://www.zhihu.com/log/questions'
    
    global session
    if session == None:
        login()
    response = session.get(initial_url)
    soup = BeautifulSoup(response.content)
    # The value of _xsrf is essential for post data to get more questions.
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
    while len(question_poll) < x:
        question_docs = soup.find_all('h2', class_ = 'zm-item-title')
        for question_doc in question_docs:
            question_link_part = question_doc.find('a')['href']
            question_link = 'http://www.zhihu.com' + question_link_part
            # print question_link
            # Put the link into the question poll to be stored into the json file.
            question_poll.append(question_link)
        
        # The start value is part of parameter to post to get more qestion. 
        start_value_doc = soup.find_all('div', class_ = 'zm-item')[19]['id']
        start_value = str(start_value_doc[-9: ])
        # print start_value
        
        # 'offset' is another part of post data, equaling with the number of questions collected.
        question_number = len(question_poll)
        header['Referer'] = initial_url
        post_data = {
                'start': start_value,
                'offset': question_number,
                '_xsrf': _xsrf
                }
        response = session.post(initial_url, data = post_data, headers = header)
        # response_status = response.json()['r']
        # print response_status

        # Get the list containing more question links.
        question_list = response.json()['msg'][1]
        soup = BeautifulSoup(question_list)
        
        print 'Questions collected: ', len(question_poll)
    return question_poll

def save_mysql(dict):
    '''
    Save the data into MySQL

    Args:
        Data on question from function monitor().

    Returns:
        Data in MySQL
    '''
    # Connect with the MySQLdb module.
    db = MySQLdb.connect(host = 'localhost', user = 'root', db = 'zhihu')
    cursor = db.cursor()

    # Code for create the tables in MySQL
#    mysql> CREATE TABLE zhihu_data (
#        -> id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
#        -> len_title SMALLINT UNSIGNED,
#        -> answer_num SMALLINT UNSIGNED,
#        -> follower_num MEDIUMINT UNSIGNED,
#        -> len_detail SMALLINT UNSIGNED,
#        -> follower_follower MEDIUMINT UNSIGNED,
#        -> bigest_answerer MEDIUMINT UNSIGNED,
#        -> upvote_num SMALLINT UNSIGNED,
#        -> visitor_num MEDIUMINT UNSIGNED,
#        -> followers_answerer MEDIUMINT UNSIGNED,
#        -> time DATETIME,
#        -> topic_follower_num MEDIUMINT UNSIGNED,
#        -> comment_num SMALLINT UNSIGNED,
#        -> bigest_follower MEDIUMINT UNSIGNED,
#        -> question_id VARCHAR(12)
#        -> );

    # MySQL code for inserting data into MySQL
    sql = "INSERT INTO zhihu_data(len_title, answer_num, follower_num, len_detail, follower_follower, bigest_answerer, upvote_num, visitor_num, followers_answerer, time, topic_follower_num, comment_num, bigest_follower, question_id) VALUES ('%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%s', '%d', '%d', '%d', '%s')" % (dict['len_title'], dict['answer_num'], dict['follower_num'], dict['len_detail'], dict['follower_follower'], dict['bigest_answerer'], dict['upvote_num'], dict['visitor_num'], dict['followers_answerer'], dict['time'], dict['topic_follower_num'], dict['comment_num'], dict['bigest_follower'], dict['question_id'])
    
    # Try to excute.
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

