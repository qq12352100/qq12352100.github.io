# -*- coding: utf-8 -*-
# @Author: shizy@yisa.com
# @Date:   2020-03-26 17:57:27
# @Last Modified by:   szy
# @Last Modified time: 2020-03-26 22:51:42
# 取kafka数据上传FTP

from ftplib import FTP
from kafka import KafkaConsumer
import json
import yaml
import logging
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler
from daemon import Daemon
import threading
import requests
import sys
import os
import pickle
import time,timeit
import uuid
import base64
import Queue
from io import BytesIO
from pykafka import KafkaClient
from pykafka.common import OffsetType
import redis
import pylru

reload(sys)
sys.setdefaultencoding('utf-8')
class FTPUtils():
    def __init__(self,config):
        self.config = config
    #FTP初始化登陆方法
    def login(self):
        ftp = FTP()
        try:
            ftp.connect(self.config['host'],self.config['port'])
            ftp.login(self.config['username'],self.config['password'])
        except ftplib.all_errors:
            raise RuntimeError("ftp 连接失败!...")
        except KeyError as why:
            raise KeyError("缺少配置项! {}".format(str(why)))
        else:
            return ftp

class MyDaemon(Daemon):
    def format_msg(self,msg):
        try:
            row = {}
            img_data = ''
            if len(msg[7])<7 or msg[7]=='未识别' or msg[7]=='无' or msg[7]=='无车牌' or msg[7]=='车牌':
                row['license_plate'] = '无牌'
            else:
                row['license_plate'] = msg[7].strip()
                #row['license_plate'] = row['license_plate'].decode("gbk").encode('utf-8')
            row['unit_id'] = 2
            row['has_image'] = 1
            #诸城region         
            row['region_id'] = '371600'
            row["plate_type_id"]=int(msg[9])
            #卡口编号
            row['location_id'] = base64.b64encode (row['region_id']+":"+str(msg[4]))
           # print row['location_id']
            row['loc_id'] = row['region_id'] +":"+str(msg[4])
           # print row['loc_id']
            #设备编号
            #row['device_id'] = base64.b64encode(str(msg['SBBH']))
            #row['dev_id'] = str(msg['SBBH'])
            #数据库中没有设备编号
            row['device_id'] = 0
            row['dev_id'] = ''
            row['lane_id'] = msg[5]
            row['speed'] = int(msg[16])
            row['capture_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg[3] / 1000))
           # print row["capture_time"]
            #logging.info(row["capture_time"])
            row['direction_id'] = msg[6]
            #####################
            #add by sj
            img_server_id = str(msg[18])
            image_id_index = {"599":"http://172.25.98.100:6120","21":"http://172.16.1.201:8088", "573":"http://172.24.1.238:8088", "575":"http://172.24.1.233:8088", "236":"http://172.24.1.236:8088", "30":"http://172.24.1.231:8088", "574":"http://172.24.1.235:8088", "28":"http://172.23.0.41:8088", "29":"http://172.23.0.49:8088", "34":"http://172.27.2.3:8088", "36":"http://172.25.91.8:8009", "45":"http://172.22.4.112:8081", "47":"http://172.18.50.27:8081", "48":"http://172.18.50.28:8081", "96":"http://172.27.67.5:8088", "166":"http://172.18.1.37:9099", "170":"http://172.18.1.41:9099", "268":"http://172.27.131.229:8088", "476":"http://172.20.4.16:6001", "35":"http://172.27.128.252:8088", "41":"http://172.21.1.204:9000", "100":"http://172.27.131.228:8088", "295":"http://172.22.17.113:8081", "131":"http://172.25.91.132:8088", "177":"http://172.20.4.76:6001", "180":"http://172.25.91.127:8088", "183":"http://172.29.0.233:8088", "279":"http://172.24.1.238:8088", "471":"http://172.26.100.80:8088", "30":"http://172.24.1.231:8088", "31":"http://172.24.1.233:8200", "32":"http://172.20.4.73:6501", "99":"http://172.26.1.100:8009", "294":"http://172.22.17.112:8088", "185":"http://172.23.0.46:8009", "187":"http://172.26.100.62:8088", "296":"http://172.22.17.114:8081", "298":"http://172.22.17.116:8081", "299":"http://172.22.17.117:8081", "300":"http://172.22.17.122:8081", "302":"http://172.22.17.124:8081", "303":"http://172.22.17.125:8081", "304":"http://172.22.17.126:8081", "305":"http://172.22.17.80:8081", "306":"http://172.22.17.81:8081", "468":"http://172.26.100.81:8088", "33":"http://172.20.4.111:8088", "46":"http://172.22.4.14:8081", "49":"http://172.23.0.43:8088", "66":"http://172.27.131.2:8088", "297":"http://172.22.17.115:8081", "165":"http://172.18.1.29:9099", "167":"http://172.18.1.38:9099", "168":"http://172.18.1.39:9099", "169":"http://172.18.1.40:9099", "301":"http://172.22.17.123:8081", "237":"http://172.23.0.4:8088","681":"http://172.20.4.60:6120","564":"http://172.18.23.71:80","713":"http://172.24.1.188:6120"}
            #image_id_index = {"599":"http://172.25.98.100:6120","21":"http://172.16.1.201:8088", "573":"http://172.24.1.238:8088", "575":"http://172.24.1.233:8088", "236":"http://172.24.1.236:8088", "30":"http://172.24.1.231:8088", "574":"http://172.24.1.235:8088", "28":"http://172.23.0.41:8088", "34":"http://172.27.2.3:8088", "36":"http://172.25.91.8:8009", "45":"http://172.22.4.112:8081", "47":"http://172.18.50.27:8081", "48":"http://172.18.50.28:8081", "96":"http://172.27.67.5:8088", "166":"http://172.18.1.37:9099", "170":"http://172.18.1.41:9099", "268":"http://172.27.131.229:8088", "476":"http://172.20.4.16:6001", "35":"http://172.27.128.252:8088", "41":"http://172.21.1.204:9000", "100":"http://172.27.131.228:8088", "295":"http://172.22.17.113:8081", "131":"http://172.25.91.132:8088", "177":"http://172.20.4.76:6001", "180":"http://172.25.91.127:8088", "183":"http://172.29.0.233:8088", "279":"http://172.24.1.238:8088", "471":"http://172.26.100.80:8088", "30":"http://172.24.1.231:8088", "31":"http://172.24.1.233:8200", "32":"http://172.20.4.73:6501", "99":"http://172.26.1.100:8009", "294":"http://172.22.17.112:8088", "185":"http://172.23.0.46:8009", "187":"http://172.26.100.62:8200", "296":"http://172.22.17.114:8081", "298":"http://172.22.17.116:8081", "299":"http://172.22.17.117:8081", "300":"http://172.22.17.122:8081", "302":"http://172.22.17.124:8081", "303":"http://172.22.17.125:8081", "304":"http://172.22.17.126:8081", "305":"http://172.22.17.80:8081", "306":"http://172.22.17.81:8081", "468":"http://172.26.100.81:8089", "33":"http://172.20.4.111:8088", "46":"http://172.22.4.14:8081", "66":"http://172.27.131.2:8088", "297":"http://172.22.17.115:8081", "165":"http://172.18.1.29:9099", "167":"http://172.18.1.38:9099", "168":"http://172.18.1.39:9099", "169":"http://172.18.1.40:9099", "301":"http://172.22.17.123:8081","681":"http://172.20.4.60:6120","564":"http://172.18.23.71:80"}

            #####################
            if  image_id_index.has_key(img_server_id):
                row['image_url'] = image_id_index[img_server_id] + msg[20]
            else:
                #logging.info('%s not in image_id_index,%s',img_server_id,msg)
                return None
                #row['image_url'] = "http://172.16.1.201:8088/none/" + msg[20]
            '''
            if row['image_url']:
                try:
                    if row['image_url'].startswith('http'):
                        r = requests.get(row['image_url'],timeout=1)
                        img_data = r.content
                        logging.info('capture_time = %s  , image_url = %s', row['capture_time'],row['image_url'])
                        #logging.info(img_data)
                        #time.sleep(1000)
                    else:
                        if len(row['image_url']) > 0:
                            logging.error('无效图片地址：[%s]', row['image_url'])
                except Exception as e:
                    logging.error(e)
                
                if len(img_data) > 10:
                    row['img_data'] = base64.b64encode(img_data)
                    row['img_data'] = 'data:img/jpeg;base64,'+row['img_data']
                    #logging.info(row['img_data'])
                    #time.sleep(1000)
                else:
                    row['img_data'] = ''
           # print row['image_url'] 
            #if row['location_id'] in self.location_to_yisa_location:
            #    row['location_id'] = self.location_to_yisa_location[row['location_id']]
            #else:
            #    insert_id = self.execute_sql("INSERT INTO mon_location SET location_name = '',loc_id='%s',region_code='%s';" % (base64.b64decode(row['location_id']).encode("utf-8"),row['region_id']),"insert")
            #    if insert_id > 0:
            #        print insert_id,base64.b64decode(row['location_id']).encode("utf-8")
            #        r = requests.get('http://127.0.0.1:9002/?format=json&action=update_location_id')
            #        r = requests.get('http://127.0.0.1:9002/?format=json&action=make_location_dict_cache')
            #        self.load_cache()
            #        if row['location_id'] in self.location_to_yisa_location:
            #            row['location_id'] = self.location_to_yisa_location[row['location_id']]
            #print row['location_id']
            '''
            return row
            
        except Exception, e:
            logging.exception('格式化信息时错误: %s', str(e))
            print Exception,e
            return None
        except Exception, e:
            logging.exception('格式化信息时错误: %s', str(e))
            return None   

    def get_msg(self):
        #获取hik_kafka连接
        logging.warning('创建连接Kafka...')
        #topic='thirdUser_YISA'
        '''
        client = KafkaClient(hosts='172.16.1.250:9092,172.16.1.249:9092,172.16.1.251:9092')#这里连接多个客户端
        topic = client.topics['BAYONET_VEHICLEPASS'] #从zookeeper消费,zookeeper的默认端口为2181
        balanced_consumer = topic.get_balanced_consumer( 
        consumer_group='thirdUser_YISA_666',
        #auto_offset_reset=OffsetType.LATEST, 
        auto_commit_enable=True,# 设置为False的时候不需要添加consumer_group,直接连接topic即可取到消息
        #auto_commit_enable=False,# 设置为False的时候不需要添加consumer_group,直接连接topic即可取到消息
        #auto_offset_reset='latest',
        auto_offset_reset=OffsetType.LATEST, 
        zookeeper_connect='172.16.1.250:2181,172.16.1.251:2181,172.16.1.249:2181' #这里就是连接多个zk 
        ) 
        '''
        kafka_brokers = "172.16.1.250:9092,172.16.1.249:9092,172.16.1.251:9092"
        #consumer = KafkaConsumer('BAYONET_VEHICLEPASS',group_id='thirdUser_YISA_666888',bootstrap_servers=kafka_brokers, auto_offset_reset='latest')
        consumer = KafkaConsumer('BAYONET_VEHICLEPASS',group_id='thirdUser_YISA_666888',bootstrap_servers=kafka_brokers,metadata_max_age_ms=300000)
        #consumer = KafkaConsumer('BAYONET_VEHICLEPASS',group_id='thirdUser_YISA_666890',bootstrap_servers=kafka_brokers,max_poll_records=2147483646)
        recv_number = 0
        results = []
        start = timeit.default_timer()
        while 1:
            try:
                #for message in balanced_consumer:
                for message in consumer:
                    if message is not None: 
                        recv_number += 1
                        # 消息内容
                        offset = message.offset # kafka偏移量
                        if recv_number%5000==0:
                            logging.warning('offset:%d,recv:%d',offset,recv_number)   
                        # continue
                        row = json.loads(message.value[2:])['values']
                        #print row
                        self.MSG_QUEEN.put(row)
            except Exception, e:
                logging.exception('读取kafka时错误: %s', str(e))
                #print("1111111111111111111111111")
                time.sleep(10)

    def deal_msg(self):
        r = redis.StrictRedis(unix_socket_path=self.config['redis_mq']['unix_socket_path'],password=self.config['redis_mq']['password'])
        pipe = r.pipeline()
        cache = pylru.lrucache(50000)
        results = []
        start_ttt = timeit.default_timer()
        while True:
            try:
                result = self.MSG_QUEEN.get(timeout=5)
                if result:
                    msg = self.format_msg(result)
                    logging.info(msg)
                    if msg:
                        try:
                            if len(msg['image_url']) > 10:
                                if cache.get(msg['image_url']) is None:
                                    cache[msg['image_url']] = 1
                                else: #过滤重复数据
                                    pipe.incr(time.strftime('%Y%m%d',time.localtime(time.time()))+":HIK:ERR")
                                    cache[msg['image_url']] +=1
                                    logging.warning('重复数据[%s][%d]',msg['image_url'],cache[msg['image_url']])
                                    continue
                                pipe.incr(time.strftime('%Y%m%d',time.localtime(time.time()))+":HIK")
                                pipe.rpush(self.config['redis_mq']['queue_key_name'],json.dumps(msg))
                                if pipe.__len__()==1:
                                    start_ttt = timeit.default_timer()
                        except UnicodeDecodeError,ude:
                            logging.error('编码json时错误: %s',msg['license_plate'])
                else:
                    logging.info('self.MSG_QUEEN is null')
                    time.sleep(5)
                    continue

                if timeit.default_timer()-start_ttt > 1 or pipe.__len__()>100:
                    pipe.execute()

            except Exception as e:
                logging.info('处理数据失败：%s',str(e))

    def connect_ftp(self):
        #获取FTP连接
        if self.ftp is None:
            try:
                self.ftp = FTPUtils(self.config['FTP']).login()
            except KeyError as why:
                logging.error(str(why))
            except RuntimeError as why:
                logging.error(str(why))

    def run(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml') as config_file:
            self.config = yaml.safe_load(config_file)

        name = 'hik_sdk_to_ftp4' 
        logging.basicConfig(level=logging.INFO) 
        handler = RotatingFileHandler('/var/log/%s.log' % name, maxBytes=134217728, backupCount=7)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger('').addHandler(handler)
        logging.warning('启动 [%s]', name)

        self.threads = []
        self.MSG_QUEEN = Queue.Queue(0)
        #self.ftp = None
        #r = redis.StrictRedis(unix_socket_path=self.config['redis_mq']['unix_socket_path'],password=self.config['redis_mq']['password'])
        #self.pipe = r.pipeline()

        #self.connect_ftp()
        for x in xrange(0,9):
            GMT = threading.Thread(target=self.get_msg)
            self.threads.append(GMT)

        for x in xrange(0,32):
            t = threading.Thread(target=self.deal_msg)
            self.threads.append(t)
        for t in self.threads:
            t.start()
            time.sleep(1)
        try:
            for t in self.threads:
                t.join()
        except KeyboardInterrupt:
            logging.error('Ctrl+C,终止运行')
            sys.exit()


if __name__ == "__main__":
    daemon = MyDaemon('/var/run/hik_sdk_to_ftp4.pid')
    #daemon.run()
    #sys.exit(0)
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
