import tornado.ioloop
import tornado.web
import csv
import json
import os
import codecs

CSV_PATH = 'comments.csv'

newFile = not os.path.exists(CSV_PATH)
if newFile:
    with open(CSV_PATH, 'wb') as f:
        # 在创建新文件的时候写入UTF-8 BOM
        f.write(codecs.BOM_UTF8)
        
f = open(CSV_PATH, 'a', newline='', encoding='utf-8')
wr = csv.writer(f)

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', '*')
    def get(self):
        self.write("Hello, world")
    def post(self):
        # 处理来自BrowerExtension的POST请求
        body = self.request.body.decode('utf-8')
        print(body)
        wr.writerows(json.loads(body))
        f.flush()


def make_app():
    return tornado.web.Application([
        (r"/api", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8710)
    try:
        print('Service started...')
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        f.close()
        print('Bye bye!')