# !/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
import sys
import re
from random import randint
import lxml

from zhihu import Zhihu

reload(sys)
sys.setdefaultencoding('utf-8')

class Question(Zhihu):

    def __init__(self, url, session = None, soup = None):
        Zhihu.__init__(self, session, soup)
        self.url = url
        self.answer_number = None

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

