# -*- coding: utf-8 -*-
from mysqlpool import sqlconn
import pymysql
import time
import os

class Monitor:

    def LockFile(self, val, lockpath):
        if val and not os.path.isfile(lockpath):
            #os.mknod(lockpath)
            with open(lockpath, 'w') as f:
                f.close()
        elif not val and os.path.isfile(lockpath):
            os.remove(lockpath)

    def skynet(self, lockpath):
        print(lockpath)
        status = True
        netstatus = False
        lastin = 0
        lastout = 0
        db = pymysql.Connection(host='123.206.95.123', database='blog', user='root', password='Nkx.29083X', charset='utf8')
        sql = """insert into skynet (min1,min5,min15,uscpu,sycpu,total,used,free,netin,netout,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
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

                create_time = time.strftime('%Y-%m-%d %H:%M:%S')
                number = cursor.execute(sql,(min1,min5,min15,uscpu,sycpu,total,used,free,netin,netout,create_time))
                print('开启')
                time.sleep(60)
            else:
                print('关闭')
                status = False
        print('监控结束')

monitor = Monitor()