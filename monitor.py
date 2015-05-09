#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Zhihu import monitor
from Zhihu import save_mysql
import json

def main():

    # Showing the questions left to be monitor
    question = []
    visited = set()
    error = 0

    # Read the questions from file stored by collector (function)
    with open('question_poll.txt') as file:
        for line in file:
            question.append(json.loads(line))

    # Gather the information of these questions by monitor (function), and save them into MySQL by save_mysql (function)
    for url in question[0]:
        try:
            dict = monitor(url)
            save_mysql(dict)
            visited |= {url}
            print 'Questions remaining: ', len(question[0]) - len(visited)
        except:
            error += 1
            print 'OOPS! %d errors happened!' % error
            continue

    print 'Number of errors happened: %d', %error

if __name__ == '__main__':
    main()
