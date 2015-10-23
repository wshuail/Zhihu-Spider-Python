# !/usr/bin/env python2
# -*- coding: utf-8 -*-

from zhihu import Question
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


question_url = 'http://www.zhihu.com/question/28530832'
s = Question(question_url)

if __name__ == '__main__':
    # test function get_title 
    print 'Get the title of the Question.\n'
    print s.get_title()
    print '\n'

    print 'Get the detail of the Question if it has.\n'
    print s.get_detail()
    print '\n'
