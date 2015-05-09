#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Zhihu import monitor
import json
import time

current_time = time.strftime('%Y%m%d%H%M')
file_name = str(current_time + '.txt')

def main():
    question = []
    data = []
    visited = set()
   
    with open('question_poll.txt') as file:
        for line in file:
            question.append(json.loads(line))

    for url in question[0]:
        try:
            print 'Questions remaining: ', len(question[0]) - len(visited)
            dict = monitor(url)
            data.append(dict)
            visited |= {url}

        except:
            continue
    
    with open(file_name, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    main()
