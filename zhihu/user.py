# !/usr/bin/env python2
# -*- coding: utf-8 -*-

from question import Question
from zhihu import Zhihu

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class User(Zhihu):

    def __init__(self, url):
        Zhihu.__init__(self)
        self.url = url
        self.profile_url = self.url + '/about'
        self.url_suffix = re.match(r'.+/people/(.+)', self.url).group(1)
        self.ask_url = self.url + '/asks'
        self.answer_url = self.url + '/answers'
        self.post_url = self.url + '/posts'
        self.collection_url = self.url + '/collections'
        self.edit_url = self.url + '/logs'
        self.ask_number = None
        self.answer_number = None
        self.post_number = None
        self.collection_number = None
        self.edit_number = None


    def user_name(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        name = self.soup.find_all('span', {'class': 'name'})[1].string
        return name

    def weibo(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('a', {'class': 'zm-profile-header-user-weibo'})
        if doc is not None:
            weibo = doc['href']
            return weibo

    def profile(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('div', {'class': 'body'}).find('img', {'class': 'Avatar'})
        if doc is not None:
            profile_link = doc['src'][0: len(doc['src']) - 5] + 'r.jpg'
        return profile_link

    def signature(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'bio'})
        if doc is not None:
            signature = doc['title']
        else:
            signature = None
        return signature

    def bussiness_domain(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find(
            'span', {'class': 'business'})
        if doc is not None:
            bussiness_domain = doc['title']
        else:
            bussiness_domain = None
        return bussiness_domain

    def gender(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'gender'})
        if doc is not None:
            if doc.find('i')['class'][1] == 'icon-profile-male':
                gender = 'M'
            #elif gender_profile[1] == 'icon-profile-female':
            else:
                gender = 'F'
        else:
            gender = 'unknown'
        return gender

    def location(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'location'})
        if doc is not None:
            location = doc['title']
        else:
            location = None
        return location

    def company(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'employment'})
        if doc is not None:
            company = doc['title']
        else:
            company = None
        return company

    def positon(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'position'})
        if doc is not None:
            position = doc['title']
        else:
            position = None
        return position

    def education(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'education'})
        if doc is not None:
            education = doc['title']
        else:
            education = None
        return education

    def education_extra(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        doc = self.soup.find('span', {'class': 'education-extra'})
        if doc is not None:
            education_extra = doc['title']
        else:
            education_extra = None
        return education_extra

    def following_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        docs = self.soup.find(
            'div', {'class': 'zu-main-sidebar'}).find_all('strong')
        following_num = docs[0].string
        follower_num = docs[1].string

        return following_num, follower_num

    def agree_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        agree_num = self.soup.find(
            'span', {'class': 'zm-profile-header-user-agree'}).strong.string
        return agree_num

    def thank_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        thank_num = self.soup.find(
            'span', {'class': 'zm-profile-header-user-thanks'}).strong.string
        return thank_num

    def user_visitor_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        docs = self.soup.find('div', {
                              'class': 'zu-main-sidebar'}).find_all('div', {'class': 'zm-profile-side-section'})
        user_visitor_num = docs[
            len(docs) - 1].find('div', {'class': 'zm-side-section-inner'}).strong.string
        return user_visitor_num

    def ask_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        ask_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(
            r'/people/.+/asks')}).find('span', {'class': 'num'}).string)
        self.ask_number = ask_num
        return ask_num

    def answer_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        answer_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(
            r'/people/.+/answers')}).find('span', {'class': 'num'}).string)
        self.answer_number = answer_num
        return answer_num

    def post_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        post_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(
            r'/people/.+/posts')}).find('span', {'class': 'num'}).string)
        self.post_number = post_num
        return post_num

    def collection_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        collection_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(
            r'/people/.+/collections')}).find('span', {'class': 'num'}).string)
        self.collection_number = collection_num
        return collection_num

    def edit_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        edit_num = int(self.soup.find('a', {'class': 'item', 'href': re.compile(
            r'/people/.+/logs')}).find('span', {'class': 'num'}).string)
        self.edit_number = edit_num
        return edit_num

    def user_ask(self):
        if self.ask_number is None:
            self.ask_number = self.ask_num()
        ask_link_list = []
        if self.ask_number > 0:
            for i in range(1, int(int(self.ask_number)/20) + 2):
                ask_url = self.ask_url + '?page=' + str(i)
                ask_soup = self.parse(ask_url)
                docs = ask_soup.find_all('h2')
                for doc in docs:
                    ask_link = 'https://www.zhihu.com' + \
                        str(doc.find('a', {'class': 'question_link'})['href'])
                    ask_link_list.append(ask_link)
        return ask_link_list

    def user_answer(self):
        if self.answer_number is None:
            self.answer_number = self.answer_num()
        answer_link_list = []
        if self.answer_number > 0:
            for i in range(1, int(int(self.answer_number)/20) + 2):
                answer_url = self.answer_url + '?page=' + str(i)
                soup = self.parse(answer_url)
                docs = soup.find_all('h2')
                for doc in docs:
                    link = 'https://www.zhihu.com' + \
                        str(doc.find('a', {'class': 'question_link'})['href'])
                    answer_link_list.append(link)
        return answer_link_list
