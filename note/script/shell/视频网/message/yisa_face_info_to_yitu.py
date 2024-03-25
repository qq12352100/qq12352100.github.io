#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import json
import yaml
import time
import Queue
import pylru
import redis
import timeit
import pickle
import random
import base64
import xxhash
import MySQLdb
import logging
import binascii
import requests
import datetime
import threading
import multiprocessing
from datetime import date
from daemon import Daemon
from datetime import datetime
from confluent_kafka import Consumer
from confluent_kafka import Producer
from confluent_kafka import KafkaError
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
reload(sys)
sys.setdefaultencoding('utf-8')


def redis_connect(redis_config):
    if 'database' not in redis_config:
        redis_config['database'] = 0
    if 'password' not in redis_config:
        redis_config['password'] = ''
    if ('host' not in redis_config or str(redis_config['host']) == '127.0.0.1') and 'unix_socket_path' in redis_config:
        redis_connect = redis.StrictRedis(unix_socket_path=redis_config['unix_socket_path'], 
                                        password=redis_config['password'], 
                                        db=redis_config['database'])
    else:
        redis_connect = redis.StrictRedis(host=redis_config['host'], 
                                        port=redis_config['port'], 
                                        password=redis_config['password'], 
                                        db=redis_config['database'])
    return redis_connect

class Dispatcher(multiprocessing.Process):
    def __init__(self,config,cpu_count):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        #self.thread_num = int(math.ceil(float(config['worker']['thread_num'])/cpu_count))#计算出每个进程开启的线程数
        self.config = config
        self.threads = []  # 处理图像的线程数组
        self.queen_size = 5000  # 消息队列最大数量
        self.message_queen = Queue.Queue(0)  # 消息队列
        self.face_queen = Queue.Queue(0)  # 结果队列
        self.sreq = requests.Session()  # 利用会话减少网络连接开销
        a = requests.adapters.HTTPAdapter(pool_connections = 1000, pool_maxsize = 1000,max_retries=3)
        self.sreq.mount('http://', a)   
        # 前端点位loc_id与yisa点位location_id对应关系
        self.location_dict = {"loc_id":"location_id"}
    
    def run(self):
        self.redis_counter = redis_connect(self.config['redis_counter'])
        for x in xrange(0,4):
            GMT = threading.Thread(target=self.get_message_face)  # , args=(10,)
            self.threads.append(GMT)  # 每个进程开启1个读数据线程

        for x in xrange(0, 256):
            t = threading.Thread(target=self.push_info)#, args=(10,)
            self.threads.append(t)#每个进程开启2个保存人脸数据线程


        for t in self.threads:
            t.start()
            time.sleep(1)
            
        for t in self.threads:
            t.join()

    def get_message_face(self):
        consumer_conf = {
            'bootstrap.servers': ','.join(self.config['kafka']['host']),
            'group.id': 'face_yisa_20200823',
            'enable.auto.commit': 'true',
            'default.topic.config': {
                'auto.offset.reset': 'largest'
            }
        }
        # 实例化消费者
        consumer = Consumer(consumer_conf)
        def print_assignment(consumer, partitions):
            logging.info("Assignment: {}".format(partitions))
        def print_revoke(consumer, partitions):
            logging.info("Revoke: {}".format(partitions))
        consumer.subscribe([self.config['kafka']["face_topic"]],
                    on_assign=print_assignment,
                    on_revoke=print_revoke)
        number_unassigned = 0
        number_pull = 0
        while 1:
            try:
                message = consumer.poll(timeout=5.0)
                if message is None:
                    time.sleep(0.01)
                    if not consumer.assignment():
                        number_unassigned += 1
                        if number_unassigned % 100 == 0:
                            logging.warning("Partition is not assignment. 请检查进程数量是否大于partition个数或kafka leader状态是否正常. ")
                    continue
                partition = message.partition()
                offset = message.offset()
                #logging.info('偏移量:{}'.format(str(offset)))
                value = message.value()
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        pass
                    else:
                        logging.error("kafka consumer error! {}".format(message.error()))
                    continue
                number_pull += 1
                if value:
                    messages = []
                    row = json.loads(value)
                    if isinstance(row, dict):
                        messages = [row]
                    else:
                        messages = row
                    for msg in messages:
                        self.message_queen.put(msg)
            except Queue.Empty:
                continue
            except Exception as e:
                logging.exception('读取kafka时错误: {}'.format(str(e)))
                time.sleep(1)

    def push_info(self):

        def __get_image_base64__(img_url):
            image_base64 = ''
            try:
                r = requests.get(img_url, timeout=5)
                img_data = r.content
                image_base64 = base64.b64encode(img_data)
            except Exception as e:
                logging.exception('请求图片内容错误: {}, {}'.format(str(e), img_url))
                return None
            return image_base64

        while 1:
            try:
                if self.message_queen.qsize() > 0:
                    try:
                        face_message = self.message_queen.get(timeout=3)
                        capture_time = int(face_message['capture_time'])
                        private_data = json.loads(face_message['item_params']['video_params']['private_data'])
                        loc_id = private_data['LOC_ID']
                        yitu_loc_id = {"1":"75", "2":"76", "3":"77", "4":"78", "5":"79", "6":"80", "7":"81", "9":"82", "10":"95", "11":"84", "12":"85", "13":"86", "14":"87", "15":"102", "16":"103", "17":"104", "18":"105", "19":"106", "20":"107", "21":"108", "22":"109", "23":"110", "24":"111", "25":"112", "26":"113", "27":"114", "28":"115", "29":"116", "30":"117", "31":"118", "32":"88", "33":"89", "34":"90", "35":"92", "36":"93", "37":"94", "63":"119", "8122881675101184":"96", "7941668883858432":"97", "7941668890149888":"98", "7941668898014208":"99", "7943081859154944":"100"}
                        face_big_url = face_message['image_url']
                        # 拼接小图地址
                        face_smail_url = '{}?&x={}&y={}&width={}&height={}'.format(face_message['image_url'],
                                                                                  face_message['objects'][0]['detection']['x'],
                                                                                  face_message['objects'][0]['detection']['y'],
                                                                                  face_message['objects'][0]['detection']['w'],
                                                                                  face_message['objects'][0]['detection']['h'])
                        logging.info('face_smail_url: {}'.format(face_smail_url))
                        logging.info('face_big_url: {}'.format(face_big_url))
                        # 下载小图和大图图片内容，转成base64字符串
                        face_smail_img = __get_image_base64__(face_smail_url)
                        face_big_img = __get_image_base64__(face_big_url)
                        #logging.info(face_big_img)
                        if face_smail_img and face_big_img:
                            task = []
                            ddd = {}
                            payload = {'face_image_content_base64': face_smail_img,
                                       'picture_image_content_base64': face_big_img,
                                       'camera_id': int(yitu_loc_id[str(loc_id)]),
                                       'timestamp': capture_time
                                       }
                            task.append(payload)
                            ddd = {"tasks": task}
                            pddd = json.dumps(ddd)
                            #payload = json.dumps(task)
                            #logging.info((ddd))
                            #yt_api = 'http://172.27.130.98:21100/face/v1/face_image_flow'
                            #yt_api = 'http://172.27.130.98:21100/face/v1/face_image_flow/batch'
                            yt_api = 'http://172.16.1.131:21100/face/v1/face_image_flow/batch'
                            with open('./111.txt','wb') as ff:
                                ff.write(pddd)
                            ff.close()
                            try:
                                #logging.info(type(payload))
                                re = requests.post(yt_api, data=pddd)
                                rtn = json.loads(re.text)
                                logging.info(rtn)
                                if rtn['rtn']>=0:
                                    logging.info("推送数据到依图接口...依图接收正常.")
                                else:
                                    logging.info("推送数据到依图接口...依图接收异常...状态描述: {}".format(rtn['message']))
                                self.redis_counter.incr(time.strftime("%Y%m%d", time.localtime(time.time())) + ":ToYitu")
                            except Exception as e:
                                logging.exception('请求依图雅典娜任性图片导入接口, 错误: {}'.format(str(e)))
                                continue
                    except Queue.Empty:
                        continue
                    except Exception as e:
                        logging.exception('推送数据到依图接口失败：%s',e)
                #else:
                #    time.sleep(0.1)
            except Queue.Empty:
                continue
            except Exception,e:
                logging.exception("push error"+str(e))
                
                
class MyDaemon(Daemon):
    def run(self):
        config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
        config = yaml.safe_load(config_file)
        config_file.close()
        
        name = 'yisa_face_info_to_yitu'
        logging.basicConfig(level=logging.DEBUG)
        handler = RotatingFileHandler('/var/log/%s.log' % name, maxBytes=134217728, backupCount=7)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.ERROR)            
        logging.warning('启动 [%s]', name)  
        logging.warning('主线程 Pid [%d]', os.getpid())
        self.cache = pylru.lrucache(5000) 
        process = []
        #cpu_count = multiprocessing.cpu_count()
        #cpu_count = min(config['worker']['max_process'],cpu_count)
        cpu_count = 4
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


if __name__ == "__main__":
    daemon = MyDaemon('/var/run/yisa_face_info_to_yitu.pid')
    daemon.run()
    sys.exit(0)
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



