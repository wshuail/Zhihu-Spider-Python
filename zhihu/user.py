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

from question import Question

reload(sys)
sys.setdefaultencoding('utf-8')

session = None

class User(Question):

    def __init__(self, url):
        self.url = url
        self.soup = None
        self.profile_url = self.url + '/about'
        self.url_suffix = re.match(r'.+/people/(.+)', self.url).group(1) 
        self.ask_url = self.url + '/asks'
        self.answer_url = self.url + '/answers'
        self.post_url = self.url + '/posts'
        self.collection_url = self.url + '/collections'
        self.edit_url = self.url + '/logs'
        self.ask_num = None
        self.answer_num = None
        self.post_num = None
        self.collection_num = None
        self.edit_num = None

    def signature(self):
        if self.soup == None:
            self.soup = self.parse(self.url)

        signature = self.soup.find('div', {'class': 'zm-profile-header-main'}).find('span', {'class': 'bio'})['title']
        return signature

    def bussiness_domain(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        bussiness_domain = self.soup.find('span', {'class': 'business item'})['title']
        return bussiness_domain

    def gender(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        gender_profile = self.soup.find('div', {'class': 'zm-profile-header-info'}).find('span', {'class': 'item gender'}).find('i')['class']
        if gender_profile[1] == 'icon-profile-male':
            gender = 'M'
        elif gender_profile[1] == 'icon-profile-female':
            gender = 'F'
        else:
            gender = 'unknown'

        return gender
    
    def location(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        location = self.soup.find('span', {'class': 'location'})['title']
        return location

    def company(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        company = self.soup.find('span', {'class': 'employment'})['title']
        return company

    def positon(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        position = self.soup.find('span', {'class': 'position'})['title']
        return position

    def education(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        education = self.soup.find('span', {'class': 'education'})['title']
        return education

    def education_extra(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        education_extra = self.soup.find('span', {'class': 'education-extra'})['title']
        return education_extra

    def following_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        docs = self.soup.find('div', {'class': 'zu-main-sidebar'}).find_all('strong')
        following_num = docs[0].string
        follower_num = docs[1].string

        return following_num, follower_num

    def agree_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        agree_num = self.soup.find('span', {'class': 'zm-profile-header-user-agree'}).strong.string
        return agree_num
        
    def thank_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        thank_num = self.soup.find('span', {'class': 'zm-profile-header-user-thanks'}).strong.string
        return thank_num

    def user_visitor_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        docs = self.soup.find('div', {'class': 'zu-main-sidebar'}).find_all('div', {'class': 'zm-profile-side-section'})
        user_visitor_num = docs[len(user_visitor_num_docs) - 1].find('div', {'class': 'zm-side-section-inner'}).strong.string
        return user_visitor_num

    def ask_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        ask_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(r'/people/.+/asks')}).find('span', {'class': 'num'}).string)
        self.ask_num = ask_num
        return ask_num

    def answer_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        answer_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(r'/people/.+/answers')}).find('span', {'class': 'num'}).string)
        self.answer_num = answer_num
        return answer_num

    def post_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        post_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(r'/people/.+/posts')}).find('span', {'class': 'num'}).string)
        self.post_num = post_num
        return post_num

    def collection_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        collection_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(r'/people/.+/collections')}).find('span', {'class': 'num'}).string)
        self.collection_num = collection_num
        return collection_num

    def edit_num(self):
        if self.soup == None:
            self.soup = self.parse(self.url)
        edit_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(r'/people/.+/logs')}).find('span', {'class': 'num'}).string)
        self.edit_num = edit_num
        return edit_num

    def user_ask(self):
        if self.ask_num == None:
            self.ask_num = self.ask_num()
        ask_link_list = []
        if self.ask_num > 0:
            for i in range(1, int(self.ask_num/20) + 2):
                ask_url = self.ask_url + '?page=' + str(i)
                ask_soup = self.parse(self.ask_url)
                docs = ask_soup.find_all('h2')
                for doc in docs:
                    ask_link = 'https://www.zhihu.com' + str(doc.find('a', {'class': 'question_link'})['href'])
                    ask_link_list.append(ask_link)
        return ask_link_list

    def user_answer(self):
        if self.answer_num == None:
            self.answer_num = self.answer_num()
        answer_link_list = []
        if self.answer_num > 0:
            for i in range(1, int(self.answer_num/20) + 2):
                answer_url = self.answer_url + '?page=' + str(i)
                soup = self.parse(self.answer_url)
                docs = soup.find_all('h2')
                for doc in docs:
                    link = 'https://www.zhihu.com' + str(user_answer_doc.find('a', {'class': 'question_link'})['href'])
                    answer_link_list.append(link)
        return answer_link_list

