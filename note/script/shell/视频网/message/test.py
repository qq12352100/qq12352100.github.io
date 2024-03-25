import os
import sys
import yaml
import pylru
import logging
import daemon
import multiprocessing
from daemon import Daemon
from logging.handlers import RotatingFileHandler

class Dispatcher(multiprocessing.Process):
    def __init__(self,config,cpu_count):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.config = config
    def run(self):
        for x in xrange(0,4):
            print (x)

class MyDaemon(Daemon):
    def run(self):
        config_file = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yaml')
        config = yaml.safe_load(config_file)
        config_file.close()

        name = 'testP'
        logging.basicConfig(level=logging.DEBUG)
        handler = RotatingFileHandler('/var/log/%s.log' % name, maxBytes=134217728, backupCount=7)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.warning('启动 [%s]', name)  
        logging.warning('主线程 Pid [%d]', os.getpid())
        self.cache = pylru.lrucache(5000) 
        process = []
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
    daemon = MyDaemon('/var/run/test.pid')
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
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
