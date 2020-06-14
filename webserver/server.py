# -*- coding: utf-8 -*-
# server.py
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server

# 导入我们自己编写的application函数:
from run_web_server import app as application

# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8001, application)
print("Serving HTTP on port 8001...")

# 开始监听HTTP请求:
httpd.serve_forever()
