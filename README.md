一、后端环境搭建步骤如下（如果想在本地运行后端代码）：

1、安装mysql或者mariadb并启动mysql数据库,
2、修改settings文件，配置数据库
3、安装python-pip
4、pip install -r requirements.txt -i https://pypi.doubanio.com/simple
5、安装阿里云的mns安装教程参考如下连接：
  https://help.aliyun.com/document_detail/32305.html?spm=5176.product27412.6.658.w8j2lg

6、同步数据库
  python manager.py makemigrations
  python manager.py migrate

7、启动：
  python manager.py runserver 0.0.0.0:8000


二、前端环境搭建（一）（前端全部是静态文件，代码均在项目根目录下的static文件夹内，可自行搭建，以下是用
node.js搭建前端服务器）

1、安装node.js(自行百度)
2、npm install http-server -g
3、http-server [path] (path为静态文件根目录)

二、前端环境搭建（二）（前端全部是静态文件，代码均在项目根目录下的static文件夹内，可自行搭建，以下是用
node.js搭建前端服务器）
如果本地安装了python环境， 可在项目根目录下直接运行python -m SimpleHTTPServer（该服务占用8000端口）