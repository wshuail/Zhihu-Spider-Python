#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Zhihu import collect
import json

def main():
    question_poll = collect()
    with open('question_poll.txt', 'w') as file:
        json.dump(question_poll, file)

if __name__ == '__main__':
    main()
    
