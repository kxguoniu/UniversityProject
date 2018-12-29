# -*- coding: utf-8 -*-
import threading
from mysqlpool import sqlconn
from monitor import monitor
from blogcache import Cache

BlogCache = Cache.get_instance()

class MyThread(threading.Thread):
    def __init__(self, lookfile=None, looptime=600, cachetime=3600, montime=60):
        threading.Thread.__init__(self)
        self.Timer = threading.Timer
        self.loopcoon = None
        self.looptime = looptime
        self.check = None
        self.checktime = cachetime
        self.mon = None
        self.montime = montime
        self.lookfile = lookfile

    def cancel(self):
        self.loopcoon.cancel()
        self.check.cancel()
        self.mon.cancel()

    def LoopConn(self):
        result,number = sqlconn.check()
        if result:
            print('检测成功',number)
        else:
            print('检测失败',number)
        self.loopcoon = self.Timer(self.looptime, self.LoopConn)
        self.loopcoon.start()

    def CheckCache(self):
        global BlogCache
        BlogCache.check()
        self.check = self.Timer(self.checktime, self.CheckCache)
        self.check.start()

    def Monitor(self):
        monitor.skynet(LOOKFILE)
        self.mon = self.Timer(self.montime, self.Monitor)
        self.mon.start()

    def run(self):
        self.LoopConn()
        self.CheckCache()
        self.Monitor()
