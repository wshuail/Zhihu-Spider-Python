####Zhihu-Monitor
<br/>
####Introduction  
This is a Python spider aiming to scrapy data on the question page of [Zhihu](http://www.zhihu.com/), a quora-like website popular in China.
The data can be used to analyze factors influencing the activities of the questions.
<br/>
Specifically, functions below can be achieved by this spider：
1. Login in.
2. Scrapy latest questions.
3. Scrapy the relative data of these questions at the time this spider is working:
- Length of the title.
- Length of details of the question  
- Number of visitor for this question.
- Number of followers for the relevant topics 
- Number of answers
- Total number of comments under the answers
- Total number of followers for people answering the question
- Largest number of followers for people ansering the question 
- Number of followers for this question
- Total number of followers for people following the question
- Largest number of followers for people following the question
4. Save the data into MySQL database.
5. Scrapy the data at different time for Time Series Analysis.
<br/>
Project [zhihu-python](https://github.com/egrcc/zhihu-python)by[egrcc](https://github.com/egrcc), and project [zhihu-py3](https://github.com/7sDream/zhihu-py3) by [7sDream](https://github.com/7sDream) was referred。
<br/>
####Requirement：  
-[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)  
-[requests](https://github.com/kennethreitz/requests)
-[MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)

requests and beautifulsoup4 can be installed by pip：

> pip install requests  
> pip install beautifulsoup4  

MySQLdb can be installed for Ubuntu by:

>apt-get install python-mysqldb
 
<br/>
Tested under Ubuntu 14.10 LTS + Python 2.7.4 + Beautifulsoup 4.2.1 + requests 2.6.0 + MySQL-python 1.2.3.
<br/>
####How to use 
1. Configure *config.ini* firstly with your email and password for login.

2. Configure line 546 in *Zhihu.py* for MySQL if necessary。

3. The main script is in *zhihu.py*, and the functions were conducted by *collector.py* and *monitor.py*. Collect question by *collector*, and the links of the questions will be saved into *question_pool.txt*. You can changed the number of questions to be collected (the default value is 10000).
Scrapy the data by *monitor*, and the data will be saved into MySQL。  
<br/>
####Potential Problems
1. Extraordinary Code. The type of default encode&decode of working platform may differ.
2. After the script is executed, 'Login Successfully !!!' means that you have login successfuly !!!
If it shows you that: 'Please open the file captcha.gif and enter the captcha.'. You should open the file captcha.gif (Downloaded antomatically by the script), enter the captacha. This solution was from project [zhihu-py3](https://github.com/7sDream/zhihu-py3) by [7sDream](https://github.com/7sDream).  
3. If you fail to login in, pleasure make sure that the file 'config.ini' was configured with correct email and password.
4. If the data can not be saved into MySQL, pleasure make sure that line 546 in Zhihu.py was configured correctly.
5. Don't hasitate to contact me if you fond bugs or other problems.

<br/>
####Next To Do
1. Test program.
2. Scrapy text of the questions and answers for NLP.
3. Optimize its efficient and functions.

<br/>
#### Contact With Me
Github: [Shauilong WANG](https://github.com/wangshuailong)
Email: oopswangsl@gmail.com

<br/>
#### NO Way But the Hard Way ####