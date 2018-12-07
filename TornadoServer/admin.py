# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.log
from tornado.options import define, options
from tornado.log import access_log
from mysqlpool import sqlconn
from monitor import monitor
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
dict_session = {}


class JsonDateTime(json.JSONEncoder):
    '''
    使json序列化支持时间转换
    '''
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
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


class BaseHandler(tornado.web.RequestHandler):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

        

    def get_current_user(self):
        session_id = self.get_secure_cookie("session_id")
        if session_id:
            return dict_session.get(session_id.decode())

    def write(self, chunk):
        '''
        重写write方法,支持json序列化时间对象
        '''
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=JsonDateTime).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super().write(chunk)


class BlogHandler(BaseHandler):

    def get(self):
        flag = self.get_argument("flag",'')
        page = self.get_argument("page",'1')
        size = self.get_argument("size",'5')
        
        sql = "select blog.*,category.name from blog,category where blog.category_id = category.id and category.name = %s"
        number,results = sqlconn.exec_sql_feach(sql,(flag))

        self.write(results)


class LoginHandler(BaseHandler):
    '''
    登录
    '''
    def get(self):
        a = self.xsrf_token
        print(a)
        flag = self.get_argument('time', '')
        if flag:
            import time
            now = int(time.time())
            with open('admin.txt', 'r') as f:
                ts = f.read()
            return self.write({"ts":int(ts), "now":now})
        else:
            return self.render("login.html")

    def post(self):
        '''
        登录
        :user   用户名
        :pwd    密码
        '''
        body = json.loads(self.request.body)
        user = body['username']
        pwd = body['password']
        
        if user == 'nkx':
            import time
            now = str(int(time.time()))
            with open('admin.txt', 'w') as f:
                f.write(now)
        usersql = "select name,img from author where name=%s and passwd=%s"
        status,results = sqlconn.exec_sql_feach(usersql,(user,pwd))
        if status:
            results = results[0]
            session_id = str(uuid.uuid1())
            dict_session[session_id] = {'user':results['name'], 'img':results['img']}
            self.set_secure_cookie("session_id", session_id)
            re_data = {'status':0, 'msg':'登录成功'}
        else:
            re_data = {'status':1, 'msg':'账号或密码错误'}
        self.write(re_data)


    def put(self):
        '''
        注册用户
        '''
        body = json.loads(self.request.body)
        user = body['user']
        pwd = body['passwd']
        pwd2 = body['passwd2']
        search = sqlconn.exec_sql('select id from author where name=%s', (user))
        if search:
            return self.write({'status':1, 'msg':'用户已存在'})
        else:
            regisql = "insert into author (name,img,passwd) values (%s,%s,%s)"
            sqlconn.exec_sql(regisql,(user,"/static/img/img.jpg",pwd))
            return self.write({'status':0, 'msg':'注册成功'})


class LogoutHandler(BaseHandler):
    '''
    登出
    '''
    #@tornado.web.authenticated
    def get(self):
        del dict_session[self.get_secure_cookie('session_id').decode()]
        self.write({'status':0, 'msg':'退出成功'})


class MainHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html")


class CateGoryHandler(BaseHandler):
    '''
    博文增删改查
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
        select = self.get_argument("select", '')
        value = self.get_argument("value", '')

        sql = "select blog.id,blog.title,blog.weight,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested from blog left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
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
            print('不搜索')
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
            else:
                re_data = {'status': 1, 'msg':'数据为空' , 'data':''}

            re_data['total'] = totalnum if totalnum else 0
            return self.write(re_data)

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

    #@tornado.web.authenticated
    def put(self):
        '''
        博文修改
        :flag   修改类型
        :title  标题
        :category 标签
        :weight   权重
        :blogid   博文id
        '''
        if self.current_user['user'] != 'nkx':
            return self.write({'status':1, 'msg':'WARRING!  权限不足'})
        flag = self.get_argument('flag','')
        if flag == 'body':
            body = json.loads(self.request.body)
            blogid = body['id']
            blogtext = body['body']
            digested = body['digested']
            bloghtml = markdown.markdown(blogtext, extensions=['markdown.extensions.extra','markdown.extensions.toc','markdown.extensions.codehilite'])

            blogsql = "update blog set body=%s,digested=%s,html=%s where id=%s"
            blognumber = sqlconn.exec_sql(blogsql,(blogtext,digested,bloghtml,blogid))
            if blognumber:
                re_data = {'status':0, 'msg':'修改成功'}
            else:
                re_data = {'status':1, 'msg':'修改失败'}
            return self.write(re_data)

        elif flag == 'head':
            body = json.loads(self.request.body)
            title = body['title']
            category = body['category']
            weight = body['weight']
            blogid = body['id']
     
            categorysql = "select id from category where category.name=%s"
            number,results = sqlconn.exec_sql_feach(categorysql,(category))
            if number:
                categoryid = results[0]['id']
                blogsql = "update blog set title=%s,category_id=%s,weight=%s where id=%s"
                blognumber = sqlconn.exec_sql(blogsql,(title,categoryid,weight,blogid))
                if blognumber:
                    re_data = {'status':0, 'msg':'修改成功'}
                else:
                    re_data = {'status':1, 'msg':'保存失败'}
            else:
                re_data = {'status':1, 'msg':'分类不存在'}
            return self.write(re_data)
        else:
            return self.write({'status':1, 'msg':'无法识别的参数'})     

    #@tornado.web.authenticated
    def post(self):
        '''
        新建博文
        '''
        if self.current_user['user'] != 'nkx':
            return self.write({'status':1, 'msg':'WARRING!  权限不足'})

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
        re_data = {'status': 0, 'msg':'查无此人' , 'data': body}
        self.write(re_data)

    #@tornado.web.authenticated
    def delete(self):
        '''
        博文删除
        :blogid  博文id/单点删除
        :listid  博文id列表/批量删除
        '''
        if self.current_user['user'] != 'nkx':
            return self.write({'status':1, 'msg':'WARRING!  权限不足'})
        blogid = self.get_argument('id',-1)
        listid = self.get_argument('id', {})
        deletesql = "delete from blog where id=%s"
        deletetag = "delete from blogtag where blog_id=%s"
        print(blogid,type(blogid))
        if blogid != -1 and type(blogid) == str:
            blogid = int(blogid)
            number = sqlconn.exec_sql(deletesql,(blogid))
            if number:
                tagnumber = sqlconn.exec_sql(deletetag,(blogid))
                print(tagnumber)
                re_data = {'status':0, 'msg':'删除成功'}
            else:
                re_data = {'status':1, 'msg':'删除失败'}
            return self.write(re_data)
        elif listid:
            listid = json.loads(listid)
            for i in listid:
                number = sqlconn.exec_sql(deletesql,(listid[i]))
                if number:
                    sqlconn.exec_sql(deletetag,(blogid))
            re_data = {'status':0, 'msg':'删除成功'}
            return self.write(re_data)
        else:
            return self.write({'status':1, 'msg':'传值错误'})


class TagBlogHandler(BaseHandler):
    #返回标签对应的博文

    def get(self):
        tag = self.get_argument("flag",'')
        page = self.get_argument("page", 1)
        size = self.get_argument("limit", 5)

        pagesize = (int(page)-1)*int(size)
        size = int(size)
        if tag:
            sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
            sql += "from blog "
            sql += "left join blogtag on blog.id = blogtag.blog_id left join tag on tag.id = blogtag.tag_id "
            sql += "left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
            sql += "where blogtag.tag_id=%s"
        else:
            return self.finish({'status': 1, 'msg':'无效的查询参数' , 'data':''})
        
        totalnum = sqlconn.exec_sql(sql,(tag))
        sql += " limit %s,%s"
        number,results = sqlconn.exec_sql_feach(sql,(tag,pagesize,size))
        if number:
            re_data = {'status': 0, 'msg':'' , 'data':results}
        else:
            re_data = {'status': 1, 'msg':'没有数据' , 'data':''}
        re_data['total'] = totalnum if totalnum else 0
        self.write(re_data)


class TagListHandler(BaseHandler):
    #返回标签/分类列表
    #@tornado.web.authenticated
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


class DetailHandler(BaseHandler):
    '''
    博文详情
    '''
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
            return self.finish({'status': 1, 'msg':'无效的查询参数' , 'data':''})

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
        else:
            re_data = {'status': 1, 'msg':'查无此人' , 'data':''}
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


class TimeGroupHandler(BaseHandler):
    '''
    时间分组展示
    '''
    def get(self):
        '''
        flag 没有返回分组，有返回分组内博文
        '''
        flag = self.get_argument('flag', '')
        page = self.get_argument("page", 1)
        size = self.get_argument("limit", 5)

        pagesize = (int(page)-1)*int(size)
        size = int(size)
        if not flag:
            sql = "select count(id) as nums,DATE_FORMAT(create_time,'%Y-%m') as time from blog group by DATE_FORMAT(create_time,'%Y-%m')"
            number,results = sqlconn.exec_sql_feach(sql)
            if results:
                for i in results:
                    year,mouth = i['time'].split('-')
                    i['flag'] = year + u'年' + mouth + u'月'
            else:
                results = []
            re_data = {'status':0, 'msg':'', 'data':results}
            return self.write(re_data)
        else:
            sql = "select blog.id,blog.title,author.name as author,category.name as category,blog.create_time,blog.change_time,blog.views,blog.digested "
            sql += "from blog "
            sql += "left join category on blog.category_id = category.id left join author on blog.author_id = author.id "
            sql += "where create_time like '%s%%' "

            sql = sql%(flag)
            totalnum = sqlconn.exec_sql(sql)
            sql2 = sql + " limit %s,%s"%(pagesize,size)
            number,results = sqlconn.exec_sql_feach(sql2)
            if results:
                re_data = {'status':0, 'data':results}
            else:
                re_data = {'status':1, 'msg':'asdf'}
            re_data['total'] = totalnum if totalnum else 0
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
        # 0 未读 1已读 2回收站 3 删除
        number,results = sqlconn.exec_sql_feach(msgsql)

        if results:
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


class ImgUploadHandler(BaseHandler):
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

        re_data = {'status':0, 'data':'http://123.206.95.123:8080/static/img/'+filename}
        self.write(re_data)

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

    #@tornado.web.authenticated
    def post(self):
        body = json.loads(self.request.body)
        user = self.current_user['user']
        img = self.current_user['img']
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
        if status >= 1 and not replyblog:
            commsql = "insert into reply (user,message,create_time,comment_id,img,replyuser) values (%s,%s,%s,%s,%s,%s)"
            number = sqlconn.exec_sql(commsql,(user,message,now,replyid,img,replyuser))
            if number:
                return self.write({'status':0, 'msg':'回复成功'})
            else:
                return self.write({'status':1, 'msg':'回复失败'})


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),        #首页
            (r'/newblog', NewBlogHandler),      #最新博文
            (r'/category', CateGoryHandler),    #博文增删改查
            (r'/tagblog', TagBlogHandler),      #标签博文列表
            (r'/taglist', TagListHandler),      #标签/分类 列表
            (r'/detail', DetailHandler),        #博文详情
            (r'/login', LoginHandler),          #登录
            (r'/logout', LogoutHandler),        #登出
            (r'/blog', BlogHandler),            #无
            (r'/system', SystemHandler),        #系统监控
            (r'/message', MessageHandler),      #系统通知
            (r'/timegroup', TimeGroupHandler),  #时间分组
            (r'/imgupload', ImgUploadHandler),  #图片上传
            (r'/download', DownloadHandler),    #博文下载
            (r'/countview', CountView),         #访问计数
            (r'/search', SearchHandler),        #搜索
            (r'/comment', CommentHandler),      #评论
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
        time.sleep(600)


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
        #app.listen(options.port)
        [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
        app.listen(80)
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print(e)
    finally:
        #monitor.LockFile(False,LOCKFILE)
        print('清理结束')
        #stop_thread(st)
        stop_thread(tt)
        sqlconn.close()


if __name__ == "__main__":
    main()