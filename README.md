####Zhihu-Monitor
<br/>
####介绍  
最近在学习Python，就从爬虫入手吧。由于太菜，暂时只实现了登录，后面的还没有完善，所以先不放上来了。  
参阅了[egrcc](https://github.com/egrcc)的[zhihu-python](https://github.com/egrcc/zhihu-python)，和[7sDream](https://github.com/7sDream)的[zhihu-py3](https://github.com/7sDream/zhihu-py3)两个项目。他们的项目功能已经都比较完善了。但作为菜鸟嘛，多造轮子总归是没错的。

<br/>
####依赖：  
-[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)  
-[requests](https://github.com/kennethreitz/requests)

可以使用pip来安装：

> pip install requests  
> pip install beautifulsoup4

在 Ubuntu 14.10 LTS + Python 2.7.4 + Beautifulsoup 4.2.1 + requests 2.6.0 环境下测试通过，其他环境未测试。

<br/>
####使用  
首先配置config.ini文件，写上自己的登录邮箱和密码。
然后运行zhihu.py就可以了。  
显示'Login Successfully !!!'就是登录成功了。  
也有可能需要填写验证码，它会自动下载一个图片，打开图片，输入验证码，回车就搞定了。  
暂时别的事情还不能做，你可以在此基础上学习修改。
当然，也欢迎拍砖啦！！
