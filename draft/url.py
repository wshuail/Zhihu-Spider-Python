# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from collections import deque
import re


class Url(object):
    
    def __init__(self, url):
        self.url = url
	self.queue = deque()
	self.visited = set()
        self.session = requests.session()

    
    def parse(self, url):
        url = self.url
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content)
	return soup

    def extractUrl(self):

        self.queue.append(self.url)
            

        cnt = 0
        print len(self.queue)

        while len(self.queue) > 0:
            url = self.queue.popleft()
            self.visited |= {url}

            soup = self.parse(url)
            print len(self.queue)


            cnt += 1
            urls = soup.find_all(text = re.compile("href"))
	    print urls
            print len(urls)
            for url in urls:
#                try:
                part_url = url['href']
                if part_url and part_url[0:20] == 'http://www.zhihu.com':
                    print part_url
                elif part_url and part_url[0:10] == '/question':
                    full_url = 'http://www.zhihu.com/' + part_url[0:18]
                    print full_url
                elif part_url and part_url[0:7] == '/people':
                    full_url = 'http://www.zhihu.com/' + part_url
                    print full_url
                elif part_url and part_url[0:6] == '/topic':
                    full_url = 'http://www.zhihu.com' + part_url
                    print full_url
                else:
                    pass

Url('http://www.zhihu.com/topic/19553309').extractUrl()
