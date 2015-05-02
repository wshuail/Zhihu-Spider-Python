#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Zhihu import collect
import json

# Number of questions need to be collected.
n = 10000 

def main():
    # Collect questions by collect() function.
    question_poll = collect(n)
    # Write them into the json file. 
    with open('question_poll.txt', 'w') as file:
        json.dump(question_poll, file)

if __name__ == '__main__':
    main()
    
