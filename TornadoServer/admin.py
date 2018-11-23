# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.log
from tornado.options import define, options
from mysqlpool import sqlconn
import pymysql
import logging
import uuid
import threading
import markdown
import json
import os

ROOT = 'nkx'

define("port", default=8888, help="run on the given port", type=int)
LOCKFILE = os.path.dirname(os.path.abspath(__file__)) + "/system.lock"
dict_session = {}


class LogFormatter(tornado.log.LogFormatter):
    '''
    定义日志
    '''
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_id = self.get_secure_cookie("session_id")
        return dict_session.get(session_id.decode())


class BlogHandler(BaseHandler):

    def get(self):
        flag = self.get_argument("flag",'')
        page = self.get_argument("page",'1')
        size = self.get_argument("size",'5')
        
        sql = "select blog.*,category.name from blog,category where blog.category_id = category.id and category.name = %s"
        number,results = sqlconn.exec_sql_feach(sql,(flag))

        self.write(json.dumps(results))


class LoginHandler(BaseHandler):
    '''
    登录
    '''
    def get(self):
        self.render("login.html")

    def post(self):
        '''
        登录
        :user   用户名
        :pwd    密码
        '''
        body = json.loads(self.request.body)
        user = body['username']
        pwd = body['password']

        session_id = str(uuid.uuid1())
        dict_session[session_id] = user
        self.set_secure_cookie("session_id", session_id)
        re_data = {'status':0, 'msg':'登录成功'}
        self.write(re_data)


class LogoutHandler(BaseHandler):
    '''
    登出
    '''
    @tornado.web.authenticated
    def get(self):
        del dict_session[self.get_secure_cookie('session_id').decode()]
        self.write({'status':0, 'msg':'退出成功'})


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class CateGoryHandler(BaseHandler):
    '''
    分类博文列表
    '''
    #@tornado.web.authenticated
    def get(self):
        '''
        :flag   分类
        :page   页数
        :size   页面大小
        :total  博文总数量
        :select 筛选条件
        :value  筛选内容
        '''
        flag = self.get_argument("flag", '')
        page = self.get_argument("page", 1)
        size = self.get_argument("limit", 20)
        total = self.get_argument("total", 0)
        select = self.get_argument("select", '')
        value = self.get_argument("value", '')

        sql = "select blog.id,blog.title,blog.weight,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested from blog left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
        pagesize = (int(page)-1)*int(size)
        size = int(size)
        if not select:
            print('不搜索')
            totalnum = sqlconn.exec_sql(sql)
            if flag != '1':
                sql += "where category.id=%s limit %s,%s"
                number,results = sqlconn.exec_sql_feach(sql,(flag,pagesize,size))
            elif flag == '1':
                sql += "limit %s,%s"
                number,results = sqlconn.exec_sql_feach(sql,(pagesize,size))

            if results:
                for i in results:
                    i['create_time'] = str(i['create_time'])
                    i['change_time'] = str(i['change_time'])
                re_data = {'status': 0, 'msg':'' , 'data':results}
            else:
                re_data = {'status': 1, 'msg':'查无此人' , 'data':''}

            re_data['total'] = totalnum if totalnum else 0
            return self.write(re_data)
        elif select in ['author', 'category', 'title', 'digested']:
            print('文字搜索')
            if select in ['author', 'category']:
                sql += "where %s.name like '%s' "
            else:
                sql += "where %s like '%s' "
            value = '%' + value + '%'
        elif select in ['views', 'weight']:
            print('数字搜索')
            if value[0] == '@':
                value = value[1:]
                sql += "where %s<%s "
            elif value[-1] == '$':
                value = value[:-1]
                sql += "where %s>%s "
            else:
                sql += "where %s=%s "

            try:
                value = int(value)
            except:
                return self.write({'status':1, 'msg':'输入值不合法'})

        if flag != '1':
            sql += "and category.id=%s limit %s,%s"
            totalsql = sql + "and category.id=%s"
            totalnum = sqlconn.exec_sql(totalsql,(select,value,flag))
            number,results = sqlconn.exec_sql_feach(sql,(select,value,flag,pagesize,size))
        elif flag == '1':
            sql += "limit %s,%s"
            resql = sql%(select,value,pagesize,size)
            print(resql)
            totalnum = sqlconn.exec_sql(resql)
            number,results = sqlconn.exec_sql_feach(resql)

        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}

        re_data['total'] = totalnum if totalnum else 0
        self.write(re_data)

    @tornado.web.authenticated
    def post(self):
        '''
        博文修改
        :title  标题
        :category 标签
        :weight   权重
        :blogid   博文id
        '''
        user = self.current_user
        if user != 'nkx':
            return self.write({'status':1, 'msg':'WARRING!  权限不足'})
        body = json.loads(self.request.body)
        title = body['title']
        category = body['category']
        weight = body['weight']
        blogid = body['id']
 
        categorysql = "select id from category where category.name=%s"
        number,results = sqlconn.exec_sql_feach(categorysql,(category))
        if number:
            categoryid = cursor.fetchall()[0]['id']
            blogsql = "update blog set title=%s,category_id=%s,weight=%s where id=%s"
            blognumber = sqlconn.exec_sql(blogsql,(title,categoryid,weight,blogid))
            if blognumber:
                re_data = {'status':0, 'msg':'修改成功'}
            else:
                re_data = {'status':1, 'msg':'保存失败'}
        else:
            re_data = {'status':1, 'msg':'分类不存在'}
        self.write(re_data)

    @tornado.web.authenticated
    def delete(self):
        '''
        博文删除
        :blogid  博文id/单点删除
        :listid  博文id列表/批量删除
        '''
        if self.current_user != 'nkx':
            return self.write({'status':1, 'msg':'WARRING!  权限不足'})
        blogid = self.get_argument('id',-1)
        listid = self.get_argument('id', {})
        if blogid != -1 and type(blogid) == int:
            blogid = int(blogid)

            number = sqlconn.exec_sql(deletesql,(blogid))
            if number:
                re_data = {'status':0, 'msg':'删除成功'}
            else:
                re_data = {'status':1, 'msg':'删除失败'}
            return self.write(re_data)
        elif listid:
            listid = json.loads(listid)
            deletesql = "delete from blog where id=%s"
            for i in listid:
                print(i)
                number = sqlconn.exec_sql(deletesql,(listid[i]))
            re_data = {'status':0, 'msg':'删除成功'}
            return self.write(re_data)
        else:
            return self.write({'status':1, 'msg':'传值错误'})


class TagBlogHandler(BaseHandler):
    #返回标签对应的博文

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
        
        number,results = sqlconn.exec_sql_feach(sql,(tag))
        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class TagListHandler(BaseHandler):
    #返回标签列表
    @tornado.web.authenticated
    def get(self):
        tagsql = "select tag.name from tag"

        number,results = sqlconn.exec_sql_feach(tagsql)

        lists = {}
        lists['tag'] = results
        categorysql = "select name from category"
        number,results = sqlconn.exec_sql_feach(categorysql)

        lists['category'] = results


        if results:
            re_data = {'status': 1, 'msg':'' , 'data':lists}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class DetailHandler(BaseHandler):

    def get(self):
        Id = self.get_argument("id",'')
        sql = "select blog.id,blog.title,blog.weight,blog.body,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        if Id:
            sql += "where blog.id = %s"

            number,results = sqlconn.exec_sql_feach(sql,(Id))
        else:
            return self.finish({'status': 1, 'msg':'无效的查询参数' , 'data':''})

        if results:
            results = results[0]
            results['create_time'] = str(results['create_time'])
            results['change_time'] = str(results['change_time'])
            results['body'] = markdown.markdown(results['body'], extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])
            
            tagsql = "select tag.name from blogtag LEFT JOIN tag on tag.id = blogtag.tag_id where blogtag.blog_id =%s"
            number,taglist = sqlconn.exec_sql_feach(tagsql,(results['id']))
  
            listtag = []
            for i in taglist:
                listtag.append(i['name'])
            results['taglist'] = listtag
            re_data = {'status': 0, 'msg':'' , 'data':results,}
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class BlogSaveHandler(BaseHandler):

    def post(self):
        body = self.request.body
        body = json.loads(body)
        print(body)

        categorysql = "select id from category where category.name=%s"
        number,results = sqlconn.exec_sql_feach(categorysql,(body['category']))
        if number:
            category_id = results[0]['id']
            print('category_id',type(category_id))
        authorsql = "select id from author where author.name=%s"
        number,results = sqlconn.exec_sql_feach(authorsql,(body['author']))
        if number:
            author_id = results[0]['id']
            print('author_id',type(author_id))
        print(type(body['weight']))
        sql = """insert into blog (title,body,digested,author_id,category_id,weight) values (%s,%s,%s,%s,%s,%s)"""
        number,results = sqlconn.exec_sql_feach(sql,(body['title'],body['content'],body['content_short'],author_id,category_id,body['weight']))
        if number:
            number,blog_id = sqlconn.exec_sql_feach("""select id from blog where blog.title=%s""",(body['title']))
            blog_id = blog_id[0]['id']
            print('blog_id',blog_id)
            for tag in body['taglist']:
                tagsql = "select id from tag where tag.name=%s"
                number,tag_id = sqlconn.exec_sql_feach(tagsql,(tag))
                if number:
                    tag_id = tag_id[0]['id']
                    tagblogsql = """insert into blogtag (blog_id,tag_id) values (%s,%s)"""
                    number = sqlconn.exec_sql(tagblogsql,(blog_id,tag_id))
                else:
                    pass
        re_data = {'status': 0, 'msg':'查无此人' , 'data': body}
        self.write(re_data)


class NewBlogHandler(BaseHandler):

    def get(self):
        sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        sql += "ORDER BY blog.create_time DESC limit 5"

        number,results = sqlconn.exec_sql_feach(sql)

        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
                i['change_time'] = str(i['change_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 0, 'msg':'查无此人' , 'data':''}
        self.write(re_data)


class SystemHandler(BaseHandler):

    def get(self):
        """
        systemsql = "select GROUP_CONCAT(min1) as min1, GROUP_CONCAT(min5) as min5, GROUP_CONCAT(min15) as min15, "
        systemsql += "GROUP_CONCAT(uscpu) as uscpu, GROUP_CONCAT(sycpu) as sycpu, GROUP_CONCAT(total) as total, GROUP_CONCAT(used) as used, "
        systemsql += "GROUP_CONCAT(free) as free, GROUP_CONCAT(netin) as netin, GROUP_CONCAT(netout) as netout, GROUP_CONCAT(create_time) as create_time "
        systemsql += "from skynet order by skynet.create_time DESC limit 60"
        """
        sort = self.get_argument('sort', 'true')
        limits = self.get_argument('limit', 60)
        limits = int(limits)

        if sort == 'true':
            systemsql = "select * from skynet order by skynet.create_time desc limit %s"
        else:
            systemsql = "select * from skynet order by skynet.create_time limit %s"
        systemsql = "select * from skynet order by skynet.create_time desc limit %s"

        number,results = sqlconn.exec_sql_feach(systemsql,(limits))

        r_data = {}

        function = lambda x: [x['min1'],x['min5'],x['min15'],x['uscpu'],x['sycpu'],x['total'],x['used'],x['free'],x['netin'],-x['netout'],str(x['create_time'])[11:16]]
        min1,min5,min15,uscpu,sycpu,total,used,free,netin,netout,create_time = zip(*map(function,results))
        r_data['load'] = {'min1':min1, 'min5':min5, 'min15':min15}
        r_data['cpu'] = {'uscpu':uscpu, 'sycpu':sycpu}
        r_data['memory'] = {'total':total, 'used':used, 'free':free}
        r_data['net'] = {'netin':netin, 'netout':netout}
        r_data['create_time'] = create_time
        re_data = {'status':0, 'msg':'', 'data':r_data}
        self.write(re_data)


class MessageHandler(BaseHandler):
    '''
    系统通知
    '''
    def get(self):
        limit = self.get_argument('limit', '')
        page = self.get_argument('page', '')
        total = self.get_argument('total', '')

        msgsql = "select id,content,status,create_time from message"
        number,results = sqlconn.exec_sql_feach(msgsql)

        if results:
            for i in results:
                i['create_time'] = str(i['create_time'])
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 0, 'msg':'无数据' , 'data':[]}

        self.write(re_data)

    def post(self):
        msgid = self.get_argument('msgid','')
        status = self.get_argument('status', '')

        msgsql = "update message set status=%s where id=%s"
        number = sqlconn.exec_sql(msgsql,(status,msgid))
        if number:
            re_data = {'status':0, 'msg':'操作成功'}
        else:
            re_data = {'status':1, 'msg':'操作失败'}
        self.write(re_data)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),        #首页
            (r'/newblog', NewBlogHandler),      #最新博文
            (r'/category', CateGoryHandler),    #分类博文列表
            (r'/blogsave', BlogSaveHandler),    #保存博文
            (r'/tagblog', TagBlogHandler),      #标签博文列表
            (r'/taglist', TagListHandler),      #标签/分类 列表
            (r'/detail', DetailHandler),        #博文详情
            (r'/login', LoginHandler),          #登录
            (r'/logout', LogoutHandler),        #登出
            (r'/blog', BlogHandler),            #无
            (r'/system', SystemHandler),        #系统监控
            (r'/message', MessageHandler),      #系统通知
        ]
        settings = dict(
            debug=True,     #调试模式
            cookie_secret="SECRET_DONT_LEAK",
            login_url="/login",
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    try:
        tornado.options.parse_command_line()  #解析命令行参数
        app = Application()
        # 监控开启
        #LockFile(True)
        #st = threading.Thread(target=skynet, args=(LOCKFILE,))
        #st.start()
        
        # mysqlconn check
        tt = threading.Thread(target=LoopConn, args=(sqlconn,))
        tt.start()
        #app.listen(options.port)
        [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
        app.listen(80)
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print(e)
    finally:
        LockFile(False)
        print('清理结束')
        #stop_thread(st)
        stop_thread(tt)
        sqlconn.close()


def _async_raise(tid, exctype):
    import ctypes
    import inspect
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    if res == 1:
        print('清理线程OK')
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def LoopConn(val):
    import time
    while True:
        result,number = val.check()
        if result:
            print('检测成功',number)
        else:
            print('检测失败',number)
        time.sleep(600)

def LockFile(val, lockpath=LOCKFILE):
    if val and not os.path.isfile(lockpath):
        #os.mknod(lockpath)
        with open(lockpath, 'w') as f:
            f.close()
    elif not val and os.path.isfile(lockpath):
        os.remove(lockpath)


def skynet(lockpath):
    print(lockpath)
    status = True
    netstatus = False
    lastin = 0
    lastout = 0
    db = pymysql.Connection(host='123.206.95.123', database='blog', user='root', password='Nkx.29083X', charset='utf8')
    sql = """insert into skynet (min1,min5,min15,uscpu,sycpu,total,used,free,netin,netout,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    import time
    import datetime
    while status:
        if os.path.isfile(lockpath):
            try:
                loads = os.popen('uptime').read()
                loads = loads.split()
                min1 = float(loads[-3].split(',')[0])
                min5 = float(loads[-2].split(',')[0])
                min15 = float(loads[-1].split(',')[0])
            except:
                min1 = min5 = min15 = 0
            finally:
                if min15 > 1:
                    print('WARING!!!')

            try:
                cpus = os.popen("top -b -n 1 |grep Cpu").read()
                cpus = cpus.split()
                uscpu = float(cpus[1].split('%')[0])
                sycpu = float(cpus[2].split('%')[0])
            except:
                uscpu = sycpu = 0
            finally:
                if uscpu + sycpu > 90:
                    print('WARING!!!')

            try:
                memory = os.popen("free -m | grep Mem").read()
                memory = memory.split()
                total = int(memory[1])
                used = int(memory[2])
                free = int(memory[3])
            except:
                total = 1
                used = free = 0
            finally:
                if used / total > 0.9:
                    print('WARING!!!')

            try:
                net = os.popen("cat /proc/net/dev | grep eth").read()
                net = net.split()
                if netstatus:
                    netin = int(net[2]) - lastin
                    netout = int(net[10]) - lastout
                else:
                    netin = netout = 0
                    netstatus = True
                lastin = int(net[2])
                lastout = int(net[10])
            except:
                netin = netout = 0

            create_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            number = cursor.execute(sql,(min1,min5,min15,uscpu,sycpu,total,used,free,netin,netout,create_time))
            print('开启')
            time.sleep(60)
        else:
            print('关闭')
            status = False
    print('监控结束')

if __name__ == "__main__":
    main()