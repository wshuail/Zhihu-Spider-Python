# !/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
import requests
import time
from bs4 import BeautifulSoup
import sys
import math
import json
import re
from random import randint
from chardet import detect
import functools
import lxml

from zhihu import login
from zhihu import session

reload(sys)
sys.setdefaultencoding('utf-8')

class Question(object):

    def __init__(self, url):
        self.url = url
        self.soup = None
        self.answer_number = None

    def parse(self, url):
        global session
        if session == None:
            session = login()

        response = session.get(url)
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, 'lxml')
            except:
                soup = BeautifulSoup(response.content, 'html.parser')
        self.soup = soup
        return soup


    def title(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        title = self.soup.find('title').string.replace('\n', '').replace(' - 知乎', '')
        return title

    def topics(self):
        topics = []
        if self.soup is None:
            self.soup = self.parse(self.url)
        docs = self.soup.find_all('a', class_ = 'zm-item-tag')
        if docs != None:
            for doc in docs:
                topic = doc.get_text()
                topics.append(topic)
        return topics

    def detail(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        detail = self.soup.find('div', id = 'zh-question-detail').get_text()
        #.find('div', class_ = 'zm-editable-content').get_text()
        if detail != None:
            return detail
        else:
            return None

    def visitor_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        #visitor_number_doc = self.soup.find('meta', itemprop = 'visitsCount')
        visitor_number = self.soup.find('meta', {'itemprop': 'visitsCount'})['content']
        if visitor_number is None:
            visitor_number = 0
        return visitor_number

    def follower_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('div', class_ = 'zh-question-followers-sidebar').find('div')
        if len(list(doc.children)) == 1:
            follower_number = 0
        # elif len(list(doc.children)) == 3:
        else:
            follower_number = doc.a.strong.string
        return follower_number

    def topic_follower_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find_all('div', class_ = 'zg-gray-normal')[2]
        topic_follower_num = doc.find_all('strong')[1].string
        if topic_follower_num is None:
            topic_follower_num = 0
        return topic_follower_num

    def answer_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('h3', id = 'zh-question-answer-num')
        if doc != None:
            answer_num = doc['data-num']
        else:
            answer_num = 0
        # print 'answer_num: ', answer_num
        self.answer_number = answer_num
        return answer_num

    def answer_links(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        answer_links = []
        docs = self.soup.find_all('span', class_ = 'answer-date-link-wrap')
        for doc in docs:
            answer_link = 'https://www.zhihu.com' + doc.find('a')['href']
            answer_links.append(answer_link)
        return answer_links

    def answer(self):
        links = self.answer_links()
        if len(links) > 0:
            for link in links:
                soup = self.parse(link)
                answer = soup.find('div', class_ = 'zm-editable-content clearfix').get_text()
        return answer

