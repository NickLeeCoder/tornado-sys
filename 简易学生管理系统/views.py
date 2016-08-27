import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from db import get_db_session
from settings import debug_settings
from models import Student, Admin


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def initialize(self):
        self.session = get_db_session(debug_settings)


class IndexHandler(BaseHandler):
    """
    首页
    如果登陆过  直接显示学生信息列表
    否则显示登陆页面
    """
    @tornado.web.authenticated
    def get(self):
        return self.redirect('/students')


class LoginHandler(BaseHandler):
    """
    登录页面
    """
    def get(self):
        self.render('reglogin.html')

    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        if username=='' or password=='':
            return self.render('error.html', result='用户名或者密码不能为空')

        res = self.session.query(Admin).filter(Admin.admin_name==username).all()
        print('这是啥', res)

        if len(res) == 0:
            self.render('error.html', result='用户不存在')
            return
        elif len(res) == 1:
            if res[0].password != password:
            # 密码错误
                self.render('error.html', result='密码错误')
                return

        # 登录成功  设置coodies
        self.set_secure_cookie('user', self.get_argument('username'))
        self.redirect('/students')


class RegisterHandler(BaseHandler):
    """
    注册页面
    """
    def get(self):
        self.render('reglogin.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        res = self.session.query(Admin).filter(Admin.admin_name==username).all()
        if not res:
            print('没有注册过,可以注册')
            admin = Admin(username, password)
            self.session.add(admin)
            self.session.commit()
        else:
            self.render('error.html', result='用户名已存在,请更换用户名后重新注册!!!!')

        print('post 注册页面', username, password)
        self.set_secure_cookie('user', self.get_argument('username'))
        self.redirect('/students')



class LogoutHandler(BaseHandler):
    """
    登出页面
    """
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class EditHandler(BaseHandler):
    """
    编辑学生信息
    """
    def get(self):
        id = self.get_argument('id')
        stu = self.session.query(Student).filter(Student.id==id).one()
        self.render('edit.html', id=stu.id, username=stu.username, age=stu.age, height=stu.height)

class DeleteHandler(BaseHandler):
    """
    删除学生信息
    """
    def get(self, *args, **kwargs):
        id = self.get_argument('id')
        self.session.query(Student).filter(Student.id==id).delete()
        self.session.commit()
        self.redirect('/students')


class AddHandler(BaseHandler):
    """
    添加新的学生
    """
    def get(self, *args, **kwargs):
        self.render('add.html')

    def post(self):
        username = self.get_argument('username')
        age = self.get_argument('age')
        height = self.get_argument('height')
        grade = self.get_argument('grade')
        # x
        stu = Student(username, age, height, grade)
        self.session.add(stu)
        self.session.commit()
        self.redirect('/students')


class SaveHandler(BaseHandler):
    """
    保存编辑后的信息
    """
    def post(self):
        id = self.get_argument('id')
        username = self.get_argument('username')
        height = self.get_argument('height')
        self.session.query(Student).filter(Student.id==id).\
            update({'username': username,
                   'height': height})
        self.session.commit()
        self.redirect('/students')


class StudentsHandler(BaseHandler):
    """
    学生信息列表
    """
    @tornado.web.authenticated
    def get(self):
        stus = self.session.query(Student).order_by(Student.id).limit(10)
        self.render('students.html', stus=stus, current_page=1)

    def post(self):
        page = self.get_argument('page')
        page = int(page)
        per_page = self.get_argument('per_page')
        print('来自ajax 的请求', page, per_page)
        stus = self.session.query(Student).order_by(Student.id).offset(per_page*page).limit(per_page)
        json_s = []
        for m in stus:
            json_s.append(m.json_str())
            print('我是啥',m.json_str())


        a = json.dumps(json_s,ensure_ascii=False)
        print(a)
        # return a

        return json.dumps(['haha','fff'])

        # u = Student('ss',12,21,3)
        # print('我的类型', type(u))
        # print(json_s)
        # return json.dumps(json_s, ensure_ascii=False)








