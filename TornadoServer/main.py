import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import uuid
import markdown
import pymysql
import json

define("port", default=8888, help="run on the given port", type=int)
DB = pymysql.Connection(host='*', database='blog', user='root', password='*', charset='utf8')

dict_session = {}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_id = self.get_secure_cookie("session_id")
        return dict_session.get(session_id.decode())


class BlogHandler(BaseHandler):
    def initialize(self):
        self.db = DB


    def get(self):
        flag = self.get_argument("flag",'')
        page = self.get_argument("page",'1')
        size = self.get_argument("size",'5')

        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select blog.*,category.name from blog,category where blog.category_id = category.id and category.name = %s"
        number = cursor.execute(sql,(flag))
        results = cursor.fetchall()
        cursor.close()

        self.write(json.dumps(results))


class LoginHandler(BaseHandler):
    def initialize(self):
        self.db = DB


    def get(self):
        self.render("login.html")


    def post(self):
        user = self.get_argument("user")
        pwd = self.get_argument("pwd")

        cursor = self.db.cursor()
        sql = "select user from user where user=%s and pwd=%s"
        number = cursor.execute(sql,(user,pwd))
        cursor.close()
        if not number:
            self.redirect("/login")
        
        session_id = str(uuid.uuid1())
        dict_session[session_id] = user
        self.set_secure_cookie("session_id", session_id)
        self.redirect("/")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class CateGoryHandler(BaseHandler):
    def initialize(self):
        self.db = DB

    def get(self):
        flag = self.get_argument("flag",'')
        page = self.get_argument("page",'1')
        size = self.get_argument("size",'5')
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested from blog left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
        if flag != '1':
            sql += "where category.id=%s"
            number = cursor.execute(sql,(flag))
        elif flag == '1':
            sql += "limit 10"
            number = cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class TagBlogHandler(BaseHandler):
    def initialize(self):
        self.db = DB


    def get(self):
        tag = self.get_argument("tag",'')
        if tag:
            sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
            sql += "from blogtag "
            sql += "left join blog on blog.id = blogtag.blog_id left join tag on tag.id = blogtag.tag_id "
            sql += "left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
            sql += "where blogtag.tag_id=%s"
        else:
            return self.finish({'status': 1, 'msg':'无效的查询参数' , 'data':''})
        
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        number = cursor.execute(sql,(tag))
        results = cursor.fetchall()
        cursor.close()
        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class TagListHandler(BaseHandler):
    def initialize(self):
        self.db = DB

    def get(self):
        sql = "select tag.name from tag"
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        number = cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        if results:
            re_data = {'status': 1, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class DetailHandler(BaseHandler):
    def initialize(self):
        self.db = DB

    def get(self):
        Id = self.get_argument("id",'')
        sql = "select blog.id,blog.title,blog.body,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        if Id:
            sql += "where blog.id = %s"
            cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            number = cursor.execute(sql,(Id))
            results = cursor.fetchall()
            cursor.close()
        else:
            return self.finish({'status': 1, 'msg':'无效的查询参数' , 'data':''})

        if results:
            results = results[0]
            results['create_time'] = str(results['create_time'])
            results['change_time'] = str(results['change_time'])
            results['body'] = markdown.markdown(results['body'], extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class NewBlogHandler(BaseHandler):
    def initialize(self):
        self.db = DB

    def get(self):
        sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        sql += "ORDER BY blog.create_time DESC limit 5"
        cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        number = cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 0, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),        #首页
            (r'/newblog', NewBlogHandler),      #最新博文
            (r'/category', CateGoryHandler),    #分类博文列表
            (r'/tagblog', TagBlogHandler),      #标签博文列表
            (r'/taglist', TagListHandler),      #标签列表
            (r'/detail', DetailHandler),        #博文详情
            (r'/login', LoginHandler),          #登录
            (r'/blog', BlogHandler),            #无
        ]
        settings = dict(
            debug=True,     #调试模式
            cookie_secret="SECRET_DONT_LEAK",
            login_url="/login",
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()  #解析命令行参数
    app = Application()
    #app.listen(options.port)
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()