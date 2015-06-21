import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888")
    def put(self):
        sincro = open("sincroniza","w")
        sincro.write("1")
        sincro.close()
        self.write("Hello, world")



    def post(self):
        archivo = open("secuencia.json","w")
        archivo.write(self.request.body)
        archivo.close()

class MainHandler2(tornado.web.StaticFileHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888")


if __name__ == "__main__":
    current_path = '.'
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/(.*)$', MainHandler2, {'path': current_path}),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
