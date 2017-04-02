import logging
import logging.handlers
import random
import time
import zmq
from zmq.log.handlers import PUBHandler
import socket

LOG_LEVELS = (logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL)
 
formatters = {
        logging.DEBUG: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.INFO: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.WARN: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.ERROR: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.CRITICAL: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n")
        }

host="127.0.0.1"
#host="134.158.75.161"
port = 5556

class LoggerClass(object):
    logger=None

    def connect(self):
        ctx = zmq.Context()
        pub = ctx.socket(zmq.PUB)
        pub.bind('tcp://%s:%i' % (host,port))

        self.logger = logging.getLogger("clientapp1")
        self.logger.setLevel(logging.DEBUG)
        handler = PUBHandler(pub)
        handler.formatters = formatters
        self.logger.addHandler(handler)
        time.sleep(1.)
    
#
#    for i in range(10):
#        logger.log(logging.INFO,socket.gethostname()+" | test")
#        time.sleep(1)

Logger=LoggerClass()

def log(level,message,**aa):
    tags=" ".join(["{%s:%s}"%(repr(a),repr(b)) for a,b in aa.items()])
    return Logger.logger.log(level,socket.gethostname()+" | "+message+" "+tags)

if __name__=="__main__":
    print "get"
    logger = logging.getLogger()

    context = zmq.Context()
    socket_fd = context.socket(zmq.SUB)
    socket_fd.connect('tcp://%s:%i' % (host,port))
    socket_fd.setsockopt(zmq.SUBSCRIBE, "")

    print "socket",socket_fd,'tcp://%s:%i' % (host,port)

    filehandler = logging.handlers.TimedRotatingFileHandler('var/log/dlog.log', 'midnight',1)
    logger.setLevel(logging.DEBUG)
    filehandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    while True:
        m=socket_fd.recv_multipart()
        topic,message=m
        print m
        pos = topic.find('.')
        level = topic
        if pos > 0: level = topic[:pos]
        if message.endswith('\n'): message = message[:-1]
        log_msg = getattr(logging, level.lower())
        if pos > 0: message = topic[pos+1:] + " | " + message
        log_msg(message)
else:
    Logger.connect()
