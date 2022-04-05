# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from my_framework.main import Framework
from urls import routes, fronts

app = Framework(routes, fronts)

with make_server('', 8000, app) as httpd:
    print("Server started on port 8000...")
    httpd.serve_forever()   # Respond to requests until the process is killed


