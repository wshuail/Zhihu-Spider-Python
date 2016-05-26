####Zhihu-Spider-Python
<br/>
####简介
该项目能够抓取[知乎](http://www.zhihu.com/)相关信息，包括问题，答案和用户信息等。相当于一个用Python2构建的非官方API。


参阅了[egrcc](https://github.com/egrcc)的[zhihu-python](https://github.com/egrcc/zhihu-python)，和[7sDream](https://github.com/7sDream)的[zhihu-py3](https://github.com/7sDream/zhihu-py3)两个项目。

<br/>
####依赖：
-[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)  
-[requests](https://github.com/kennethreitz/requests)

requests和beautifulsoup4可以使用pip来安装：

> pip install requests  
> pip install beautifulsoup4

<br/>
在 Ubuntu 14.10 LTS 和 OS X10.11 环境下通过测试。  
Windows下未测试，很可能会遇到编码问题。

<br/>  
#### 如何使用
注意，本项目并不提供一个"一篮子"程序，而只是提供一系列可调用的函数，需要爬取大量信息时，您需要自己写程序调用，然后运行。

<br/>
#### 例子
简单概括，就是用链接构建对象，然后用方法获取数据。 
目前支持问题（Question），回答（Answer），用户（User）三类对象。
 
例如获取一个问题下的数据:

```
from zhihu.question import Question

url = 'https://www.zhihu.com/question/40989110'
q = Question(question_url)

title = q.title()
topics = q.topics()
detail = q.detail()
...

```
  


  
<br/>
#### 联系我
Email: oopswangsl@gmail.com

<br/>
#### No Way But the Hard Way ####
