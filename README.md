####Zhihu-Monitor
<br/>
####简介  
这是一个能够抓取[知乎](http://www.zhihu.com/)问题页面相关数据的Python爬虫。
目的是分析影响一个问题诞生后，影响其活跃度的相关因素。
  
Here is the [README](https://github.com/wangshuailong/Zhihu-Monitor-Python/blob/master/README_English.md) file in English.
  
<br/>
具体来说，该爬虫可以实现：  
1. 登陆知乎。  
2. 抓取知乎上最新提出的问题。    
3. 抓取这些问题的相关数据。  
4. 将数据存入MySQL数据库。    
5. 通过分时段抓取，就可以获得每个问题各项数据在时间序列上变化曲线。    

目标数据包括     
- 标题长度  
- 问题描述长度    
- 页面访问人数  
- 相关话题关注人数    
- 回答数    
- 评论数    
- 回答者粉丝总数  
- 被关注最多回答者粉丝数    
- 问题关注人数  
- 关注该问题者粉丝总数  
- 被关注最多的关注者粉丝数     
 
<br/>
 
参阅了[egrcc](https://github.com/egrcc)的[zhihu-python](https://github.com/egrcc/zhihu-python)，和[7sDream](https://github.com/7sDream)的[zhihu-py3](https://github.com/7sDream/zhihu-py3)两个项目。

<br/>
####依赖：  
-[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)   
-[requests](https://github.com/kennethreitz/requests)   
-[MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)

requests和beautifulsoup4可以使用pip来安装：

> pip install requests  
> pip install beautifulsoup4  

Ubuntu下MySQLdb可通过如下方式安装
>apt-get install python-mysqldb

其他平台请自行查阅。  
<br/>
在 Ubuntu 14.10 LTS + Python 2.7.4 + Beautifulsoup 4.2.1 + requests 2.6.0 + MySQL-python 1.2.3
环境下测试通过。

<br/>
####如何使用  
1. 首先配置config.ini文件，写上自己的知乎登录邮箱和密码。
2. 如果需要使用MySQL，还需要在Zhihu.py文件546行配置连接MySQL的命令，因为不同平台和个人设置差异较大~~我懒得弄~~，该问题未做深入研究。
3. 程序主体都在zhihu.py里，通过collector.py和monitor.py执行。collector负责收集问题，可以手动修改问题数量（默认为10000个）。问题会被写入question_pool.txt的自动生成文件中。monitor可以读取问题，抓取相关数据，并将其存入MySQL。  
<br/>  

####可能出现的情况
1. 编码异常，因为编码方式在不同平台间有所差异~~是个比较坑爹的问题~~！！
2. 运行之后如果显示'Login Successfully !!!'就表示登录成功了。一切正常！
如果出现'Please open the file captcha.gif and enter the captcha.'表示需要填写验证码，打开文件夹下captcha.gif文件（此为程序自动下载），输入验证码，回车就搞定了。这个处理参考了[7sDream](https://github.com/7sDream)的[zhihu-py3](https://github.com/7sDream/zhihu-py3)项目。  
3. 如果无法登录，请确保您在'config.ini'上配置了正确的登陆邮箱和密码。否则请联系我，联系方式见下。
4. 数据无法存入MySQL，请修改Zhihu.py文件546行配置连接MySQL的命令。
5. 如果运行过程中出现其他BUG，也欢迎~~联系我~~**拍砖**。

<br/>
####下一步
1. 加入test程序。给这个爬虫单写一个测试文件比较具有挑战性呀~~很麻烦的~~！！
2. 加入文本内容抓取，进行文本分析。文本分析很重要~~坑爹我还没学呀~~!
3. 优化程序，包括效率和抓取内容。~~这爬虫是作者三个月编程生涯第一个迷你项目我会到处乱说吗~~

<br/>
#### 联系我
Github: [Shauilong WANG](https://github.com/wangshuailong)       
Email: oopswangsl@gmail.com

<br/>
#### NO Way But the Hard Way ####