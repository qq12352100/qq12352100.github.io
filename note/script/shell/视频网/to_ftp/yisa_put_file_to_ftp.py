#!/usr/bin/python
#-*- coding: utf-8 -*-
#########################################################################
# File Name: yisa_put_file_to_ftp.py
# Author: name
# Mail: name@yisa.com
# Created Time: 2020-11-25 15:30:45
# Edit Time: 2020-11-25 15:30:45
# Description: 数据处理脚本
# Version: 1.0.0
#########################################################################
import zipfile
import StringIO

import uuid
from datetime import datetime,date
import os,sys,time,timeit,random
import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler
import multiprocessing,threading
import redis,Queue
import yaml,json
import math
import requests
import contextlib
from urllib2 import urlopen
import xxhash
from daemon import Daemon
import random
import re

reload(sys)
sys.setdefaultencoding('utf-8')
filterIP= {'ip'}
def redis_connect(redis_config):
    if 'database' not in redis_config:
        redis_config['database'] = 0
    if 'password' not in redis_config:
        redis_config['password'] = ''
    if ('host' not in redis_config or str(redis_config['host']) == '127.0.0.1') and 'unix_socket_path' in redis_config:
        redis_connect = redis.StrictRedis(unix_socket_path=redis_config['unix_socket_path'], password=redis_config['password'], db=redis_config['database'])
    else:
        redis_connect = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'], password=redis_config['password'], db=redis_config['database'])
    return redis_connect

class InMemoryZip(object):
    def __init__(self):
        self.in_memory_zip = StringIO.StringIO()
    def append(self, filename_in_zip, file_contents):
        zf = zipfile.ZipFile(self.in_memory_zip, "a")
        zf.writestr(filename_in_zip, file_contents)
        for zfile in zf.filelist:
            zfile.create_system = 0      
        return self
    def read(self):
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()
    def writetofile(self, filename):
        f = file(filename, "w")
        f.write(self.read())
        f.close()
    def extract(self,filename):
        zip_files = zipfile.ZipFile(filename,mode='r')
        files = []
        for i in zip_files.filelist:
            files.append((i.filename, zip_files.read(i.filename)))
        zip_files.close()
        return files

class Dispatcher(multiprocessing.Process):
    def __init__(self,config,cpu_count):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.config = config#配置文件
        self.thread_num = int(math.ceil(float(config['worker']['thread_num'])/cpu_count))#计算出每个进程开启的线程数
        self.threads = []#处理图像的线程数组
        self.try_times = 2#重试次数
        self.queen_max_size = 500#消息队列最大数量
        self.message_queen = Queue.Queue(0)#消息队列
        self.result_queen = Queue.Queue(0)#结果队列
        self.sreq = requests.Session()#利用会话减少网络连接开销
        self.sreq.keep_alive = False  # 关闭多余连接
        a = requests.adapters.HTTPAdapter(pool_connections = 1000, pool_maxsize = 1000,max_retries=3)
        self.sreq.mount('http://', a)
        self.start_time = datetime.now()
        self.end_time = datetime.now() 
        
    def run(self):
        logging.info('%s pid %d', self.name,os.getpid())
        # self.redis_num = redis_connect(self.config['redis_quick'])

        # 每个进程开启1个读数据线程
        GMT = threading.Thread(target=self.get_message)
        self.threads.append(GMT)
        # 每个进程开启1个保存数据线程
        t = threading.Thread(target=self.save_result_to_ftp)
        self.threads.append(t)
        
        for x in xrange(0, self.thread_num):
            t = threading.Thread(target=self.processing,name = self.name+'>processing-'+str(x))
            self.threads.append(t)
            
        for t in self.threads:
            t.start()
            time.sleep(1)
            
        for t in self.threads:
            t.join()

    def get_message(self):#从redis抽取数据
        redis_mq = redis_connect(self.config['redis_mq'])
        pipe = redis_mq.pipeline()
        while 1:
            self.end_time = datetime.now()
            #logging.info((self.end_time - self.start_time).seconds)
            if (self.end_time - self.start_time).seconds > 6000:  #脚本运行超过100分钟
                #logging.info('ZZZZZZZZZZZZZZZZZZZZZZZZ')
                time.sleep(1200) #睡眠20分钟
                self.start_time = datetime.now()
            if self.queen_max_size > self.message_queen.qsize():
                try:
                    for x in xrange(10):
                        pipe.rpop((self.config['redis_mq']['queue_key_name']))
                    messages = pipe.execute()
                    #logging.info(messages)
                except Exception,e:
                    logging.exception('从redis抽取数据时错误: %s', str(e))
                else:
                    for msg in messages:
                        if msg:
                            # row = json.loads(msg)
                            # self.redis_num.incr(str(row['capture_time'].replace('-','').replace(' ','')[:10])+":from_mq")
                            self.message_queen.put({'message':msg,'try_times':0})
                        else:
                            time.sleep(0.05)
            else:
                #print 'message_queen is full'
                time.sleep(1)
                
    def save_result_to_ftp(self): #将数据放打包成zip文件放到本地
        count = 0
        history = {}
        imz = InMemoryZip()
        while 1:
            try:
                result = self.result_queen.get(timeout=5)
                try:
                    if result:
                        if result['uuid'] in history:
                            continue
                        history[result['uuid']] = 1
                        imz.append(result['uuid']+'.jpg',result['img_data'])
                        del result['img_data']
                        imz.append(result['uuid']+'.json',json.dumps(result))
                        count+=1
                        if count > 8:
                            try:
                                #打包上传
                                try:
                                    str_time = time.strftime("%Y%m%d%H%M%S",time.localtime(int(time.time())))
                                    str_uid = str(uuid.uuid1()).replace("-","")
                                    remotepath = "/ftpdata/yisa_car/Vehicle_{}_{}.zip".format(str_time,str_uid)
                                    imz.writetofile(remotepath)
                                    count = 0
                                    imz = InMemoryZip()
                                    history = {}
                                    #logging.info('222222222222222222222222222222222222')
                                except Exception as e:
                                    logging.error('数据打包失败：%s',str(e))
                                    continue
                                #logging.info('上传成功')
                            except Exception as e:
                                logging.info('保存数据到FTP时错误: %s',str(e))
                    else:
                        logging.info('result_queen is null sleep.....')
                        time.sleep(5)
                        continue
                except Exception as e:
                    logging.exception('保存数据到FTP时错误: %s', str(e))
                    logging.info(result)
                    self.result_queen.put(result)
                    time.sleep(0.1)
            except Queue.Empty:
                time.sleep(0.01)
                continue

    def processing(self):#把图片下载并包成json
        thread = threading.current_thread()
        logging.warning('线程ID [%s]', thread.getName())
        redis_mq = redis_connect(self.config['redis_mq'])
        pipe = redis_mq.pipeline()
        global filterIP 
        while 1:
            try:
                message_info = self.message_queen.get(timeout=10)
                message = message_info['message']
                try_times = message_info['try_times']+1
                try:
                    json_msg = json.loads(message)
                except Exception, e:
                    logging.exception('转json对象时错误: %s %s', str(e), message)
                else:
                    image_url = json_msg['image_url']
                    #惠民网络速度慢影响数据处理 酌情处理一部分晚处理惠民数据尝试加快处理图片速度
                    if str(re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{1,5}", image_url)) in filterIP :
                        continue
                    img_data = ''
                    try:
                        down_time1 = time.time()
                        if image_url.startswith('http'):
                            r = self.sreq.get(image_url, timeout=3)
                            img_data = r.content
                        elif image_url.startswith('ftp'):  
                            with contextlib.closing(urlopen(image_url, None, 10)) as r:
                                img_data = r.read()
                        elif image_url.startswith('/data'):
                            file_obj=open(image_url) 
                            img_data = file_obj.read()
                            file_obj.close()
                        else:
                            if len(image_url)>0:
                                logging.error('无效的图片地址: [%s]', image_url)
                        down_time2 = time.time()
                        down_loss_time = down_time2 - down_time1
                        #logging.info("下载图片耗时: {:.2f}, url: {}".format(down_loss_time, image_url))
                        if down_loss_time > 3:
                            logging.warning("下载图片耗时较长: {:.2f}, url: {}".format(down_loss_time, image_url))
                    except Exception, e:                        
                        if try_times < self.try_times:
                            self.message_queen.put({'message':message,'try_times':try_times})#将消息退回队列
                            continue
                        filterIP.add(str(re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{1,5}", image_url)))
                        logging.warning(filterIP)
                        logging.warning('下载图片时错误: [%s] %s', image_url,str(e))
                        pipe.incr(time.strftime('%Y%m%d',time.localtime(time.time()))+":downpic_error")
                    result = json_msg
                    result['uuid'] = xxhash.xxh64(image_url).hexdigest()
                    result['img_data'] = img_data
                    img_len = len(img_data)
                    if img_len>50 and img_len<100000000:
                        while self.queen_max_size < self.result_queen.qsize():
                            time.sleep(1)
                            logging.warning('结果队列已满1: [%s]', thread.getName())
                        self.result_queen.put(result)  # 放入保存数据队列
                        continue
                    else:
                        #logging.info('图片长度不够过滤该数据,len= %d,url = %s',img_len,result['image_url'])
                        continue
            except Queue.Empty:
                #print 'message_queen is empty'
                continue                                
            except Exception,e:
                logging.exception('分析过车数据时错误: %s', str(e))

class MyDaemon(Daemon):
    def run(self):
        config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
        config = yaml.safe_load(config_file)
        config_file.close()
        name = 'yisa_put_file_to_ftp'
        logging.basicConfig(level=logging.INFO)
        handler = RotatingFileHandler('/var/log/%s.log' % name, maxBytes=134217728, backupCount=7)
        formatter = logging.Formatter('%(asctime)s - %(lineno)d- %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        #-------------------同步输出到控制台-------------------
        # console = logging.StreamHandler()
        # console.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # console.setFormatter(formatter)
        # logging.getLogger().addHandler(console)
        #-------------------------------------------------------
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.ERROR)            
        logging.warning('启动 [%s]', name)  
        logging.warning('主线程 Pid [%d]', os.getpid())
        
        process = []
        cpu_count = multiprocessing.cpu_count()
        cpu_count = min(config['worker']['max_process'],cpu_count)
        
        logging.warning('CPU线程数 [%d]', cpu_count)
        for x in xrange(0, cpu_count):
            process.append(Dispatcher(config,cpu_count))
        for p in process:    
            p.start()  
        try:    
            for p in process:    
                p.join()          
        except KeyboardInterrupt:
            for p in process:    
                p.terminate()
            logging.warning('Ctrl+C,终止运行')
        #=================本机测试代码用======================

if __name__ == "__main__":
    daemon = MyDaemon('/var/run/yisa_put_file_to_ftp.pid')
    #daemon.run()
    #sys.exit(1)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
