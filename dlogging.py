import logging
import logging.handlers
import random
import time
import zmq
from zmq.log.handlers import PUBHandler

LOG_LEVELS = (logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR, logging.CRITICAL)
 
formatters = {
        logging.DEBUG: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.INFO: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.WARN: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.ERROR: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n"),
        logging.CRITICAL: logging.Formatter("%(filename)s:%(lineno)d | %(message)s\n")
        }

host="134.158.75.161"
port = 5558

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
pub.connect('tcp://%s:%i' % (host,port))
logger = logging.getLogger("clientapp1")
logger.setLevel(logging.INFO)
handler = PUBHandler(pub)
handler.formatters = formatters
logger.addHandler(handler)


if __name__=="__main__":
    logger = logging.getLogger()
    context = zmq.Context()
    socket_fd = context.socket(zmq.SUB)
    socket_fd.bind('tcp://%s:%i' % (host,port))
    socket_fd.setsockopt(zmq.SUBSCRIBE, "")
    filehandler = logging.handlers.TimedRotatingFileHandler('var/log', 'midnight',1)
    logger.setLevel(logging.DEBUG)
    filehandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    while True:
        topic, message = socket_fd.recv_multipart()
        pos = topic.find('.')
        level = topic
        if pos > 0: level = topic[:pos]
        if message.endswith('\n'): message = message[:-1]
        log_msg = getattr(logging, level.lower())
        if pos > 0: message = topic[pos+1:] + " | " + message
        log_msg(message)
