import os
import tornado
from settings import debug_settings
from tornado import web, httpserver, ioloop
from db import init_database
from tornado.options import define, options
from views import (
    IndexHandler,
    LoginHandler,
    RegisterHandler,
    LogoutHandler,
    StudentsHandler,
    EditHandler,
    SaveHandler,
    AddHandler,
    DeleteHandler
)

define('port', default=debug_settings['BIND_PORT'], help='run on the given port', type=int)


if __name__ == '__main__':

    print('server run at port:', options.port)

    if debug_settings['DROP']:
        init_database()
        debug_settings['DROP'] = False

    # 各种handles 视图函数映射
    handlers = [
        (r'/', IndexHandler),
        (r'/login', LoginHandler),
        (r'/register', RegisterHandler),
        (r'/logout', LogoutHandler),
        (r'/students', StudentsHandler),
        (r'/edit', EditHandler),
        (r'/save', SaveHandler),
        (r'/add', AddHandler),
        (r'/delete', DeleteHandler),

        ]

    # 设置模板  静态文件路径
    settings = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'login_url': '/login',
        'cookie_secret': 'dsadsafdsferfsfcsdfd'
        }

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=handlers, debug=True, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()