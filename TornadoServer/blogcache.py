# -*- coding: utf-8 -*-
import hashlib
import time

class Cache():
    __instance = None
    def __init__(self):
        self.data = {}
        self.timeout = {}
        self.blog = {}
        self.session = {}
        self.new = {}

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = Cache(*args, **kwargs)
            return cls.__instance

    # 文章分组
    def get(self,search,flag,key):
        try:
            result = self.data[search][flag][key]
        except:
            return None
        else:
            keys = (search+flag+key).encode(encoding='utf-8')
            hashkey = hashlib.sha1(keys).hexdigest()
            now = int(time.time())
            self.timeout[hashkey]['time'] = now
            return result

    def set(self,search,flag,key,cache):
        if self.data.get(search):
            if self.data[search].get(flag):
                self.data[search][flag][key] = cache
            else:
                self.data[search][flag] = {key:cache}
        else:
            self.data[search] = {flag:{key:cache}}
        keys = (search+flag+key).encode(encoding='utf-8')
        hashkey = hashlib.sha1(keys).hexdigest()
        now = int(time.time())
        self.timeout[hashkey] = {'time':now, 'frist':now, 'data':[search,flag,key]}

    def _set(self,search,flag):
        if self.data.get(search) and self.data[search].get(flag):
            del self.data[search][flag]


    # 文章详情
    def getblog(self,id):
        id = str(id)
        if id in self.blog:
            now = int(time.time())
            self.blog['time'] = now
            return self.blog[id]['data']
        else:
            return None

    def setblog(self,id,data):
        now = int(time.time())
        id = str(id)
        self.blog[id] = {'time':now, 'frist':now, 'data':data}

    def _setblog(self,id):
        if id in self.blog:
            del self.blog[id]

    # session
    def getsession(self,session_id):
        result = self.session.get(session_id)
        if result:
            now = int(time.time())
            if now - result['time'] > 300:
                return None
            else:
                self.session[session_id]['time'] = now
                return result['data']
        else:
            return None

    def setsession(self,user,pwd,data):
        keys = (user+pwd).encode(encoding='utf-8')
        hashkey = hashlib.sha1(keys).hexdigest()
        now = int(time.time())
        self.session[hashkey] = {'data':data, 'time':now}
        return hashkey

    def checksession(self):
        now = int(time.time())
        for item in self.session:
            if now - self.session[item]['time'] > 600:
                del self.session[item]

    def delsession(self,session_id):
        if session_id in self.session:
            del self.session[session_id]
            return True
        else:
            return False

    # 最新文章
    def getnew(self):
        result = self.new.get('new')
        if result:
            now = int(time.time())
            if now - result['time'] > 86400:
                return None
            else:
                return result['data']
        else:
            return None

    def setnew(self,data):
        now = int(time.time())
        self.new['new'] = {'data':data, 'time':now}

    def clearnew(self):
        self.new = {}


    # 检查有效性
    def check(self):
        now = int(time.time())
        for item in self.timeout:
            if now - self.timeout[item]['time'] > 3600:
                x,y,z = self.timeout[item]['data']
                del self.data[x][y][z]
                del self.timeout[item]
        for item in self.blog:
            if now - self.blog[item]['time'] > 3600:
                del self.blog[item]

    def _get(self):
        data = {}
        blog = {}
        timeout = {}
        session = {}
        for item in self.data:
            data[item] = {}
            for item2 in self.data[item]:
                data[item][item2] = []
                for item3 in self.data[item][item2]:
                    data[item][item2].append(item3)
        now = int(time.time())
        for item in self.timeout:
            timeout[item] = {'time':(now - self.timeout[item]['time'])/60.0, 'frist':(now - self.timeout[item]['frist'])/60.0}
        for item in self.blog:
            blog[item] = {'time':(now - self.blog[item]['time'])/60.0, 'frist':(now - self.blog[item]['frist'])/60.0}
        for item in self.session:
            session[item] = {'time':(now - self.session[item]['time'])/60.0,'data':self.session[item]['data']}
        
        return {'data':data, 'timeout':timeout, 'blog':blog, 'session':session, 'new':self.new}