# !/usr/bin/env python2
# -*- coding: utf-8 -*-

from question import Question
from zhihu import Zhihu

from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Answer(Zhihu):

    def __init__(self, url):
        Zhihu.__init__(self)
        self.url = url
        self.vote_number = None

    def vote_num(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        vote_num = self.soup.find('span', class_ = 'count').string
        self.vote_number = vote_num
        return vote_num

    def voter(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        if self.vote_number is None:
            self.vote_number = self.vote_num()
        voter_aid_list = []
        voter_aid_doc = self.soup.find('div', 'zm-item-answer  zm-item-expanded')
        voter_aid = voter_aid_doc['data-aid']

        voter_info_list = []

        vote_link_prefix = 'https://www.zhihu.com/answer/' + str(voter_aid) + '/voters_profile?&offset='
        for i in range(0, int(int(self.vote_number)/10 + 1)):
            vote_link = vote_link_prefix + str(i * 10)
            vote_response = self.session.get(vote_link)
            vote_json = vote_response.json()
            vote_payload = vote_json['payload']
            for vote_payload_item in vote_payload:
                voter_dict = {}
                vote_payload_soup = BeautifulSoup(vote_payload_item)
                voter_info = vote_payload_soup.find('a', {'target': "_blank", 'class': 'zg-link'})
                if voter_info:
                    voter_dict['nickname'] = voter_info.get('title')
                    voter_dict['link'] = voter_info.get('href')
                else:
                    anonymous = vote_payload_soup.find('img', {'title': True, 'class': "zm-item-img-avatar"})
                    voter_dict['nickname'] = anonymous.get('title')
                voter_info_list.append(voter_dict)

        # for voter_info in voter_info_list:
        #     for key, value in voter_info.items():
        #         print key, value

        # print 'len: ', len(voter_info_list)

        return voter_info_list

    def author(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        author_info = {}
        doc = self.soup.find('div', {'class': 'answer-head'}).find('a', {'class': 'author-link'})
        if doc != None:
            name = doc.string
            author_info['nickname'] = name
            link = 'https://www.zhihu.com/' + str(doc['href'])
            author_info['link'] = link
        elif self.soup.find('div', {'class': 'answer-head'}).find('span', {'class': 'name'}).string == u'匿名用户':
            author_info['nickname'] = u'匿名用户'

        return author_info

    def answer(self):
        if self.soup is None:
            self.soup = self.parse(self.url)
        docs = self.soup.find_all('div', {'class': 'zm-editable-content'})
        answer = docs[1].get_text()
        return answer

    def create_time(self):
        if self.soup is None:
            self.soup = self.parse(self.url)

        edit_date = self.soup.find('a', {'class': 'answer-date-link'}).string
        return edit_date

