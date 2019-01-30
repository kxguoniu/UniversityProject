# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.log
from tornado.options import define, options
from tornado.log import access_log
from mysqlpool import sqlconn
from monitor import monitor
from blogcache import Cache
from urllib.parse import quote
#from urllib import quote
import logging
import uuid
import threading
import markdown
import datetime
import json
import os

define("port", default=8888, help="run on the given port", type=int)
LOCKFILE = os.path.dirname(os.path.abspath(__file__)) + "/system.lock"
Session = Cache.get_instance()
BlogCache = Cache.get_instance()
ChCa = True

class JsonDateTime(json.JSONEncoder):
    '''
    使json序列化支持时间转换
    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


class LogFormatter(tornado.log.LogFormatter):
    '''
    定义日志
    '''
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def Custom(handler):
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    request_time = 1000.0 * handler.request.request_time()
    if "X-Real-Ip" in handler.request.headers.keys():
        real_ip = handler.request.headers["X-Real-Ip"]
    else:
        real_ip = "127.0.0.1"
    log_method("%s %d %s %s %s %.2fms", real_ip, handler.get_status(),
                   handler.request.version, handler.request.method, handler.request.uri, request_time)


def CheckPermission(level):
    def warpper(func):
        def _check(*args, **kwargs):
            _self = args[0]
            if _self.current_user:
                permission_list = _self.current_user.get('permission')
                if level in permission_list or _self.current_user['user'] == 'admin':
                    return func(*args, **kwargs)
                else:
                    return _self.write({'status':9999, 'msg':'权限不足'})
            else:
                return _self.write({'status':1001, 'msg':'请先登录'})
        return _check
    return warpper


def is_login(func):
    def warpper(*args, **kwargs):
        _self = args[0]
        if _self.current_user:
            return func(*args, **kwargs)
        else:
            return _self.write({'status':1001, 'msg':'请先登录'})
    return warpper


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        session_id = self.get_secure_cookie("session_id")
        if session_id:
            return Session.getsession(session_id.decode())

    def write(self, chunk):
        '''
        重写write方法,支持json序列化时间对象
        '''
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=JsonDateTime).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(BaseHandler, self).write(chunk)


class LoginHandler(BaseHandler):
    '''
    登录
    '''
    @is_login
    def get(self):
        flag = self.get_argument('time', '')
        if flag:
            import time
            now = int(time.time())
            with open('admin.txt', 'r') as f:
                ts = f.read()
            return self.write({'ts':int(ts), 'now':now})
        else:
            return self.render({'status':0, 'msg':'已经登录'})

    def post(self):
        '''
        登录
        :user   用户名
        :pwd    密码
        '''
        body = json.loads(self.request.body.decode())
        user = body['username']
        pwd = body['password']

        if user == 'nkx':
            import time
            now = str(int(time.time()))
            with open('admin.txt', 'w') as f:
                f.write(now)
        usersql = "select name,img,group_id from author where name=%s and passwd=%s"
        status,results = sqlconn.exec_sql_feach(usersql,(user,pwd))
        if status:
            persql = "select permiss_list from `group` where id=%s"
            _s,result = sqlconn.exec_sql_feach(persql,(results[0]['group_id']))
            lists = json.loads(result[0]['permiss_list'])
            data = {'user':results[0]['name'], 'img':results[0]['img'], 'permission':lists}
            session_id = Session.setsession(user,pwd,data)
            self.set_secure_cookie("session_id", session_id)
            re_data = {'status':0, 'msg':'登录成功'}
        else:
            re_data = {'status':1, 'msg':'账号或密码错误'}
        self.write(re_data)


    def put(self):
        '''
        注册用户
        '''
        body = json.loads(self.request.body.decode())
        user = body['user']
        pwd = body['passwd']
        pwd2 = body['passwd2']
        search = sqlconn.exec_sql('select id from author where name=%s', (user))
        if search:
            return self.write({'status':1, 'msg':'用户已存在'})
        else:
            regisql = "insert into author (name,img,passwd,group_id) values (%s,%s,%s,3)"
            sqlconn.exec_sql(regisql,(user,"/static/img/img.jpg",pwd))
            return self.write({'status':0, 'msg':'注册成功'})

class LogoutHandler(BaseHandler):
    '''
    登出
    '''
    def get(self):
        session_id = self.get_secure_cookie('session_id').decode()
        Session.delsession(session_id)
        self.write({'status':0, 'msg':'退出成功'})


def blogcache(function):
    def wrapper(*args, **kwargs):
        _self = args[0]
        func = function.__name__
        if func == 'get':
            Id = _self.get_argument("id",'')
            jsons = _self.get_argument("json", '')
            if not jsons:
                results = BlogCache.getblog(Id)
                if results:
                    _self.set_header("X-Cache","HIT")
                    return _self.write(results)
                else:
                    results = function(*args, **kwargs)
                    if results:
                        BlogCache.setblog(Id,results)
                        _self.set_header("X-Cache","MISS")
                        return _self.write(results)
            else:
                results = function(*args, **kwargs)
                if results:
                    return _self.write(results)
            return

        results,delist,blogid = function(*args, **kwargs)
        if not results:
            return
        if delist:
            for item in delist:
                category = item[0]['id']
                group = item[0]['group']
                if type(item[1]['tagid']) == list:
                    taglist = item[1]['tagid']
                elif item[1]['tagid']:
                    taglist = item[1]['tagid'].decode().split(',')
                else:
                    taglist = []
                BlogCache._set('category',category)
                BlogCache._set('group',group)
                for ite in taglist:
                    BlogCache._set('tag',ite)
        if blogid:
            BlogCache._setblog(blogid)
        BlogCache.clearnew()

        return _self.write(results)
    return wrapper


class BlogHandler(BaseHandler):
    '''
    博文增删改查
    '''
    @blogcache
    def get(self):
        '''
        Id: 博文id
        jsons： 没有返回html，有返回原文
        '''
        Id = self.get_argument("id",'')
        jsons = self.get_argument("json", '')
        if not jsons:
            sql = "select blog.id,blog.title,blog.weight,blog.html,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        else:
            sql = "select blog.id,blog.title,blog.weight,blog.body,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        if Id:
            sql += "where blog.id = %s"
            number,results = sqlconn.exec_sql_feach(sql,(Id))
        else:
            return self.write({'status': 1, 'msg':'无效的查询参数' , 'data':''})

        if results:
            results = results[0]
            #if not json:
            #    results['body'] = markdown.markdown(results['body'], extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])
            tagsql = "select tag.name from blogtag LEFT JOIN tag on tag.id = blogtag.tag_id where blogtag.blog_id =%s"
            number,taglist = sqlconn.exec_sql_feach(tagsql,(results['id']))

            #listtag = []
            #for i in taglist:
            #    listtag.append(i['name'])
            #results['taglist'] = listtag
            results['taglist'] = [i['name'] for i in taglist]
            re_data = {'status': 0, 'msg':'' , 'data':results,}
            return re_data
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
            return self.write(re_data)


    @CheckPermission(1)
    @blogcache
    def put(self):
        '''
        博文修改
        :flag   修改类型
        :title  标题
        :category 分类
        :weight   权重
        :blogid   博文id
        '''
        flag = self.get_argument('flag','')

        searchsql = "select category.id,DATE_FORMAT(blog.create_time,'%%Y-%%m') as `group` from category,blog where category.id=blog.category_id and blog.id=%s"
        searchtag = "select GROUP_CONCAT(blogtag.tag_id) as tagid from blogtag where blogtag.blog_id=%s"
        body = json.loads(self.request.body.decode())
        blogid = body['id']

        number,category = sqlconn.exec_sql_feach(searchsql,(blogid))
        number,taglist = sqlconn.exec_sql_feach(searchtag,(blogid))
        category[0]['id'] = '1'
        delist = [[category[0],taglist[0]]]
        print('put',delist)

        if flag == 'body':
            blogtext = body['body']
            digested = body['digested']
            bloghtml = markdown.markdown(blogtext, extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])

            blogsql = "update blog set body=%s,digested=%s,html=%s where id=%s"
            blognumber = sqlconn.exec_sql(blogsql,(blogtext,digested,bloghtml,blogid))
            if blognumber:
                re_data = {'status':0, 'msg':'修改成功'}
                return re_data,delist,blogid
            else:
                re_data = {'status':1, 'msg':'修改失败'}
                return self.write(re_data),None,None

        elif flag == 'head':
            title = body['title']
            category = body['category']
            weight = body['weight']


            categorysql = "select id from category where category.name=%s"
            number,results = sqlconn.exec_sql_feach(categorysql,(category))
            if number:
                categoryid = results[0]['id']
                blogsql = "update blog set title=%s,category_id=%s,weight=%s where id=%s"
                blognumber = sqlconn.exec_sql(blogsql,(title,categoryid,weight,blogid))
                if blognumber:
                    re_data = {'status':0, 'msg':'修改成功'}
                    return re_data,delist,blogid
                else:
                    re_data = {'status':1, 'msg':'保存失败'}
                    return self.write(re_data),None,None
            else:
                re_data = {'status':1, 'msg':'分类不存在'}
                return self.write(re_data),None,None
        else:
            return self.write({'status':1, 'msg':'无法识别的参数'}),None,None


    @CheckPermission(2)
    @blogcache
    def post(self):
        '''
        新建博文
        '''
        author = self.current_user['user']
        body = self.request.body.decode()
        body = json.loads(body)
        print(body)

        categorysql = "select id from category where category.name=%s"
        number,results = sqlconn.exec_sql_feach(categorysql,(body['category']))
        if number:
            category_id = results[0]['id']
            print('category_id',type(category_id))
        authorsql = "select id from author where author.name=%s"
        number,results = sqlconn.exec_sql_feach(authorsql,(author))
        if number:
            author_id = results[0]['id']
            print('author_id',type(author_id))
        print(type(body['weight']))
        sql = """insert into blog (title,body,html,digested,author_id,category_id,weight,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        if 'create_time' not in body.keys():
            body['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body['html'] = markdown.markdown(body['body'], extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])
        number,results = sqlconn.exec_sql_feach(sql,(body['title'],body['body'],body['html'],body['digested'],author_id,category_id,body['weight'],body['create_time']))
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
        re_data = {'status': 0, 'msg':'保存成功' , 'data': body}
        dellist = [[{'id':'1', 'group':datetime.datetime.now().strftime('%Y-%m')}, {'tagid':body['taglist']}]]
        print('post',dellist)
        return re_data,dellist,None

    @CheckPermission(3)
    @blogcache
    def delete(self):
        '''
        博文删除
        :blogid  博文id/单点删除
        :listid  博文id列表/批量删除
        '''
        blogid = self.get_argument('id',-1)
        listid = self.get_argument('ids', {})
        deletesql = "delete from blog where id=%s"
        deletetag = "delete from blogtag where blog_id=%s"

        searchsql = "select category.id,DATE_FORMAT(blog.create_time,'%%Y-%%m') as `group` from category,blog where category.id=blog.category_id and blog.id=%s"
        searchtag = "select GROUP_CONCAT(blogtag.tag_id) as tagid from blogtag where blogtag.blog_id=%s"
        print(blogid,type(blogid))
        if blogid != -1 and type(blogid) == str:
            blogid = int(blogid)
            number,category = sqlconn.exec_sql_feach(searchsql,(blogid))
            number,taglist = sqlconn.exec_sql_feach(searchtag,(blogid))
            category[0]['id'] = '1'
            delist = [[category[0],taglist[0]]]
            number = sqlconn.exec_sql(deletesql,(blogid))
            if number:
                tagnumber = sqlconn.exec_sql(deletetag,(blogid))
                print(tagnumber)
                re_data = {'status':0, 'msg':'删除成功'}
                print('del',delist)
                return re_data,delist,blogid
            else:
                re_data = {'status':1, 'msg':'删除失败'}
                return self.write(re_data),None,None
        elif listid:
            listid = json.loads(listid)
            delist = []
            for i in listid:
                number,category = sqlconn.exec_sql_feach(searchsql,(blogid))
                number,taglist = sqlconn.exec_sql_feach(searchtag,(blogid))
                category[0]['id'] = '1'
                delist.append([category[0],taglist[0]])
                number = sqlconn.exec_sql(deletesql,(listid[i]))
                if number:
                    sqlconn.exec_sql(deletetag,(blogid))
            re_data = {'status':0, 'msg':'删除成功'}
            return re_data,delist,listid
        else:
            return self.write({'status':1, 'msg':'传值错误'}),None,None


def memorize(cachetime=3600):
    '''
    缓存blog
    '''
    def wrapper(function):
        def _memorize(*args, **kwargs):
            # 获取参数
            _self = args[0]
            flag = _self.get_argument('flag', '')
            search = _self.get_argument('search', '')
            page = _self.get_argument('page', 1)
            size = _self.get_argument('limit', 5)
            key = str(page) + str(size)

            if search and flag:
                results = BlogCache.get(search,flag,key)
                if results:
                    _self.set_header("X-Cache","HIT")
                    return _self.write(results)
                else:
                    results = function(*args, **kwargs)
                    if results:
                        BlogCache.set(search,flag,key,results)
                        _self.set_header("X-Cache","MISS")
                        return _self.write(results)
        return _memorize
    return wrapper


class ListHandler(BaseHandler):
    @memorize(86400)
    def get(self):
        '''
        博文获取
        ;search 博文属性
        ;flag   搜索值
        ;page   页数
        ;limit  大小
        '''
        flag = self.get_argument('flag', '')
        search = self.get_argument('search', '')
        page = self.get_argument('page', 1)
        size = self.get_argument('limit', 5)

        pagesize = (int(page)-1)*int(size)
        size = int(size)
        sql = "select blog.id,blog.title,blog.weight,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        #sql += "left join blogtag on blog.id = blogtag.blog_id left join tag on tag.id = blogtag.tag_id "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "

        if search == 'category' and flag:
            if flag != '1':
                print('不是首页')
                totalsql = sql + "where category.id=%s"
                totalnum = sqlconn.exec_sql(totalsql,(flag))
                sql += "where category.id=%s limit %s,%s"
                number,results = sqlconn.exec_sql_feach(sql,(flag,pagesize,size))
            elif flag == '1':
                print('首页')
                totalnum = sqlconn.exec_sql(sql)
                sql += "limit %s,%s"
                number,results = sqlconn.exec_sql_feach(sql,(pagesize,size))

            if results:
                re_data = {'status': 0, 'msg':'' , 'data':results}
                re_data['total'] = totalnum if totalnum else 0
                return re_data
            else:
                re_data = {'status': 1, 'msg':'数据为空' , 'data':''}
                return self.write(re_data)

        elif search == 'tag' and flag:
            sql += "left join blogtag on blog.id = blogtag.blog_id left join tag on tag.id = blogtag.tag_id "
            if flag:
                sql += "where blogtag.tag_id=%s"
            else:
                return self.write({'status': 1, 'msg':'无效的查询参数' , 'data':''})

            totalnum = sqlconn.exec_sql(sql,(flag))
            sql += " limit %s,%s"
            number,results = sqlconn.exec_sql_feach(sql,(flag,pagesize,size))
            if number:
                re_data = {'status': 0, 'msg':'' , 'data':results}
                re_data['total'] = totalnum if totalnum else 0
                return re_data
            else:
                re_data = {'status': 1, 'msg':'没有数据' , 'data':''}
                return self.write(re_data)

        elif search == 'group' and flag:
            if flag == '1':
                sql = "select count(id) as nums,DATE_FORMAT(create_time,'%Y-%m') as time from blog group by DATE_FORMAT(create_time,'%Y-%m')"
                number,results = sqlconn.exec_sql_feach(sql)
                if results:
                    for i in results:
                        year,mouth = i['time'].split('-')
                        i['flag'] = year + u'年' + mouth + u'月'
                else:
                    results = []
                re_data = {'status':0, 'msg':'', 'data':results}
                return re_data
            else:
                sql += "where create_time like '%s%%' "

                sql = sql%(flag)
                totalnum = sqlconn.exec_sql(sql)
                sql2 = sql + " limit %s,%s"%(pagesize,size)
                number,results = sqlconn.exec_sql_feach(sql2)
                if results:
                    re_data = {'status':0, 'data':results}
                    re_data['total'] = totalnum if totalnum else 0
                    return re_data
                else:
                    re_data = {'status':1, 'msg':'asdf'}
                    return self.write(re_data)
        else:
            return self.write({'status':1, 'msg':'未识别的请求'})


class TagListHandler(BaseHandler):
    #返回标签/分类列表
    def get(self):
        lists = {}

        tagsql = "select tag.name,tag.id from tag"
        number,results = sqlconn.exec_sql_feach(tagsql)
        lists['tag'] = results

        categorysql = "select name,id from category"
        number,results = sqlconn.exec_sql_feach(categorysql)
        lists['category'] = results

        re_data = {'status': 1, 'msg':'' , 'data':lists}
        self.write(re_data)


def newcache(function):
    def wrapper(*args, **kwargs):
        _self = args[0]
        result = BlogCache.getnew()
        if result:
            return _self.write(result)
        else:
            result = function(*args, **kwargs)
            if result:
                BlogCache.setnew(result)
                return _self.write(result)
        return
    return wrapper


class NewBlogHandler(BaseHandler):
    '''
    最新博文
    '''
    @newcache
    def get(self):
        sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "
        sql += "ORDER BY blog.create_time DESC limit 5"

        number,results = sqlconn.exec_sql_feach(sql)

        if results:
            re_data = {'status': 0, 'msg':'' , 'data':results}
            return re_data
        else:
            re_data = {'status': 0, 'msg':'查无此人' , 'data':''}
            return self.write(re_data)


class SystemHandler(BaseHandler):
    
    @CheckPermission(4)
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
    @CheckPermission(5)
    def get(self):
        limit = self.get_argument('limit', '')
        page = self.get_argument('page', '')
        total = self.get_argument('total', '')

        msgsql = "select id,content,status,create_time from message"
        # 0 未读 1已读 2回收站 3 删除
        number,results = sqlconn.exec_sql_feach(msgsql)

        if results:
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 0, 'msg':'无数据' , 'data':[]}

        self.write(re_data)

    @CheckPermission(6)
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


class ImgUploadHandler(BaseHandler):
    @CheckPermission(7)
    def post(self):
        '''
        图片上传
        '''
        upload_path = os.path.join(os.path.dirname(__file__), 'upload')
        #upload_path = "/home/niukaixin/www/html/static/img/"
        files = self.request.files.get('file', None)
        if not files:
            re_data = {'status':1, 'msg':'没有接收到文件'}
            return self.write(re_data)

        for file in files:
            filename = file['filename']
            filepath = os.path.join(upload_path, filename)
            print(filepath)
            with open(filepath, 'wb') as f:
                f.write(file['body'])

        re_data = {'status':0, 'data':'http://52pyc.cn/static/img/'+filename}
        self.write(re_data)

    @CheckPermission(8)
    def delete(self):
        '''
        图片删除
        '''
        upload_path = os.path.join(os.path.dirname(__file__), 'upload')
        #upload_path = "/home/niukaixin/www/html/static/img/"
        filename = self.get_argument('name', '')
        if not filename:
            return self.write({'status':1, 'msg':'没有参数'})
        filepath = os.path.join(upload_path, filename)
        os.remove(filepath)
        self.write({'status':0, 'msg':'删除图片成功'})


class DownloadHandler(BaseHandler):
    @CheckPermission(9)
    def get(self,):
        blogid = self.get_argument('id','')
        blogsql = 'select title,body from blog where id=%s'
        number,results = sqlconn.exec_sql_feach(blogsql,(blogid))
        if number:
            results = results[0]
            title = results['title']
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + quote(title) + '.md')
            self.write(str(results['body']))
        else:
            self.write({'msg':'下载失败'})


class CountView(BaseHandler):
    '''
    访问统计
    '''
    def get(self):
        sql1 = 'select id as blogsums from blog'
        sql2 = 'select id as msg from message'
        sql3 = 'select sums from visitor where id=1'
        with open('admin.txt', 'r') as f:
            ls = f.read()
        time = datetime.datetime.utcfromtimestamp(int(ls)).__str__()[:10]
        r_data = {}
        r_data['blogsums'] = sqlconn.exec_sql(sql1)
        r_data['message'] = sqlconn.exec_sql(sql2)
        r_data['time'] = time
        number,results = sqlconn.exec_sql_feach(sql3)
        r_data['views'] = results[0]['sums']
        re_data = {'status':0, 'data':r_data}
        self.write(re_data)

    def post(self):
        index = self.get_argument('index', '')
        blogid = self.get_argument('id', '')
        if index:
            now = datetime.date.today()
            print(now)
            sql = 'select id from visitor where time=%s'
            status = sqlconn.exec_sql(sql,(now))
            if status:
                print('自增')
                sumsql = 'update visitor set sums=sums+1 where id=1'
                sqlconn.exec_sql(sumsql)
                sql2 = 'update visitor set sums=sums+1 where time=%s'
                sqlconn.exec_sql(sql2,(now))
            else:
                print('新建')
                sql2 = "insert into visitor (time,sums) values (%s,1)"
                sqlconn.exec_sql(sql2,(now))
            return self.write({'status':0})

        elif blogid:
            blogsql = 'update blog set views=views+1 where id=%s'
            sqlconn.exec_sql(blogsql,(blogid))
            return self.write({'status':0})

        self.write({'status':1, 'msg':'无效参数'})


class SearchHandler(BaseHandler):
    def get(self):
        value = self.get_argument('title', -1)
        if value != -1:
            sql1 = "select id,title as value from blog where blog.title like '%%%s%%'"%(value)
            number,results = sqlconn.exec_sql_feach(sql1)
            return self.write({'status':0, 'data':results})
        else:
            return self.write({'status':1, 'msg':'请求错误'})

    @CheckPermission(10)
    def put(self):
        '''
        :page   页数
        :size   页面大小
        :select 筛选条件
        :value  筛选内容
        '''
        page = self.get_argument('page', 1)
        size = self.get_argument('limit', 5)
        select = self.get_argument("select", '')
        value = self.get_argument("value", '')

        sql = "select blog.id,blog.title,blog.weight,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
        sql += "from blog "
        #sql += "left join blogtag on blog.id = blogtag.blog_id left join tag on tag.id = blogtag.tag_id "
        sql += "left join category on blog.category_id = category.id "
        sql += "left join author on blog.author_id = author.id "

        pagesize = (int(page)-1)*int(size)
        size = int(size)

        if select in ['author', 'category', 'title', 'digested'] and value:
            print('文字搜索')
            if select in ['author', 'category']:
                sql += "where %s.name like '%s' "
            else:
                sql += "where %s like '%s' "
            value = '%' + value + '%'
        elif select in ['views', 'weight'] and value:
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
        else:
            self.write({'status':1, 'msg':'未识别的请求'})

        totalsql = sql%(select,value)
        totalnum = sqlconn.exec_sql(totalsql)
        sql += "limit %s,%s"
        resql = sql%(select,value,pagesize,size)
        number,results = sqlconn.exec_sql_feach(resql)

        if results:
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'数据为空' , 'data':''}

        re_data['total'] = totalnum if totalnum else 0
        self.write(re_data)

class ErrorHandler(BaseHandler):
    def get(self):
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.render('404.html')


class CommentHandler(BaseHandler):
    '''
    评论
    '''
    def get(self):
        blogid = self.get_argument('id', -1)
        if blogid == -1:
            return self.write({'status':1, 'msg':'请求错误'})
        commsql = "select id,img,user,message,create_time,floor from comment where blog_id=%s order by floor desc"
        commnum,results = sqlconn.exec_sql_feach(commsql,(blogid))
        results = self._time(results)
        for result in results:
            result['show'] = False
            result['look'] = '查看'
            print(type(result['create_time']))
            replysql = "select id,img,user,message,create_time from reply where comment_id=%s"
            replynum,reply = sqlconn.exec_sql_feach(replysql,(result['id']))
            result['children'] = self._time(reply)
        self.write({'status':0, 'data':results})

    def _time(self, objs):
        now = datetime.datetime.now()
        for obj in objs:
            time = (now - obj['create_time']).seconds
            if time//60 == 0:
                obj['create_time'] = '%s秒前'%(time)
            elif time//3600 == 0:
                obj['create_time'] = '%s分钟前'%(time//60)
            elif time//86400 == 0:
                obj['create_time'] = '%s小时前'%(time//3600)
            else:
                obj['create_time'] = '%s天前'%(time//86400)
        return objs

    @CheckPermission(11)
    def post(self):
        body = json.loads(self.request.body.decode())
        user = self.current_user.get('user')
        img = self.current_user.get('img')

        blogid = body['blogid']
        status = body['status']
        message = body['message']
        replyid = body['replyid']
        replyuser = body['replyuser']

        print(user,message,replyid,img,replyuser)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            if message.split('\n')[0].split('@')[1]:
                replyblog = False
                message = '\n'.join(message.split('\n')[1:])
        except:
            replyblog = True
        if status == 0 or replyblog:
            floorsql = "select max(floor) as sum from comment where blog_id=%s"
            sums,results = sqlconn.exec_sql_feach(floorsql,(blogid))
            if sums:
                if results[0]['sum']:
                    floor = results[0]['sum'] + 1
                else:
                    floor = 1
            commsql = "insert into comment (user,message,create_time,floor,blog_id,img) values (%s,%s,%s,%s,%s,%s)"
            number = sqlconn.exec_sql(commsql,(user,message,now,floor,blogid,img))
            if number:
                return self.write({'status':0, 'msg':'回复成功'})
            else:
                return self.write({'status':1, 'msg':'回复失败'})
        elif status >= 1 and not replyblog:
            commsql = "insert into reply (user,message,create_time,comment_id,img,replyuser) values (%s,%s,%s,%s,%s,%s)"
            number = sqlconn.exec_sql(commsql,(user,message,now,replyid,img,replyuser))
            if number:
                return self.write({'status':0, 'msg':'回复成功'})
            else:
                return self.write({'status':1, 'msg':'回复失败'})


class TodoHandler(BaseHandler):
    '''
    待做事件
    '''
    @CheckPermission(12)
    def get(self):
        todosql = "select id,title,status from todolist"
        number,results = sqlconn.exec_sql_feach(todosql)
        for item in results:
            if item['status'] == 'false':
                item['status'] = False
            else:
                item['status'] = True
        self.write({'status':0, 'data':results})

    @CheckPermission(13)
    def put(self):
        body = json.loads(self.request.body.decode())
        todoid = body['id']
        title = body['title']
        status = body['status']
        if status:
            status = 'true'
        else:
            status = 'false'
        todosql = "update todolist set title=%s,status=%s where id=%s"
        number = sqlconn.exec_sql(todosql,(title,status,todoid))
        if number:
            return self.write({'status':0, 'msg':'修改成功'})
        else:
            return self.write({'status':1, 'msg':'修改失败'})

    @CheckPermission(14)
    def post(self):
        body = json.loads(self.request.body.decode())
        todosql = "insert into todolist (title,status) values (%s,%s)"
        number = sqlconn.exec_sql(todosql,(body['title'],'false'))
        if number:
            return self.write({'status':0, 'msg':'创建成功'})
        else:
            return self.write({'status':1, 'msg':'创建失败'})

    @CheckPermission(15)
    def delete(self):
        body = json.loads(self.request.body.decode())
        todosql = "delete from todolist where id=%s"
        number = sqlconn.exec_sql(todosql,(body))
        if number:
            return self.write({'status':0, 'msg':'删除成功'})
        else:
            return self.write({'status':1, 'msg':'删除失败'})


class VisitorHandler(BaseHandler):
    @CheckPermission(16)
    def get(self):
        import copy
        visql = "select time as name,sums as value from visitor order by time desc limit 7"
        number,results = sqlconn.exec_sql_feach(visql)
        results.reverse()
        results2 = copy.deepcopy(results)
        for item,result in enumerate(results2):
            if item != 0:
                result['value'] += results2[item-1]['value']
        self.write({'status':0, 'data':results, 'data2':results2})


class CacheHandler(BaseHandler):
    #@is_login
    def get(self):
        ids = self.get_argument('id','')
        if ids and self.current_user['user'] == 'admin':
            results = BlogCache._clear()
        else:
            results = BlogCache._get()
        self.write(results)


class TemplateHandler(tornado.web.RequestHandler):
    def get(self, ids):
        headsql = "select title,keywords,digested from blog where id=%s"
        number,results = sqlconn.exec_sql_feach(headsql, (ids,))
        print(ids,results)
        if number:
            title = results[0]['title']
            title += " | 小牛运维站"
            keywords = results[0]['keywords']
            description = results[0]['digested']
        else:
            title = "小牛运维站"
            keywords = "python,小牛,django,tornado,线程,asyncio,async/await,协程,异步,多线程"
            description = ""
        heads = {
            "title": title,
            "keywords": keywords,
            "description": description,
        }
        self.render("detail.html", **heads)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/newblog', NewBlogHandler),      #最新博文
            (r'/blog', BlogHandler),            #博文增删改查
            (r'/bloglist', ListHandler),        #博文列表
            (r'/taglist', TagListHandler),      #标签/分类 列表
            (r'/login', LoginHandler),          #登录
            (r'/logout', LogoutHandler),        #登出
            (r'/system', SystemHandler),        #系统监控
            (r'/message', MessageHandler),      #系统通知
            (r'/imgupload', ImgUploadHandler),  #图片上传
            (r'/download', DownloadHandler),    #博文下载
            (r'/countview', CountView),         #访问计数
            (r'/search', SearchHandler),        #搜索
            (r'/comment', CommentHandler),      #评论
            (r'/todolist', TodoHandler),        #待办事项
            (r'/visitor', VisitorHandler),      #七天访问量
            (r'/cache', CacheHandler),
            (r'/blogdetail/(?P<ids>\d*)', TemplateHandler), # 模板
            (r'.*', ErrorHandler),              #捕捉错误页面
        ]
        settings = dict(
            log_function=Custom,
            debug=True,     #调试模式
            cookie_secret="SECRET_DONT_LEAK",
            login_url="/login",
            #xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


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
        time.sleep(60)


def CheckCache(blogcache):
    global ChCa
    blogcache.check()
    print('开始检查Cache')
    if ChCa:
        print('开始检查Cache')
        threading.Timer(150, CheckCache, (blogcache,)).start()


def main():
    try:
        tornado.options.parse_command_line()  #解析命令行参数
        app = Application()
        # 监控开启
        #monitor.LockFile(True,LOCKFILE)
        #st = threading.Thread(target=monitor.skynet, args=(LOCKFILE,))
        #st.start()

        # mysqlconn check
        tt = threading.Thread(target=LoopConn, args=(sqlconn,))
        tt.start()

        # CheckCache
        CC = threading.Timer(150, CheckCache, (BlogCache,))
        CC.start()

        #app.listen(options.port)
        [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
        app.listen(8888)
        #app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print(e)
    finally:
        #monitor.LockFile(False,LOCKFILE)
        global ChCa
        ChCa = False
        print('清理结束')
        #stop_thread(st)
        stop_thread(tt)
        sqlconn.close()


if __name__ == "__main__":
    main()
