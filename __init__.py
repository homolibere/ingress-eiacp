__author__ = 'homolibere'
__version__ = '0.1 beta'

import sys
import time
import platform
import http_work
import logging

from daemon import Daemon

class ingress_daemon(Daemon):
    def run(self):
        chat_th = http_work.chat_thread()
        chat_th.start()
        score_th = http_work.score_thread()
        score_th.start()

if __name__ == "__main__":
    if sys.platform.find('linux') > -1:
        daemon = ingress_daemon('/tmp/daemon-example.pid')
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
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        chat_th = http_work.chat_thread()
        chat_th.start()
        score_th = http_work.score_thread()
        score_th.start()
        while 1:
            time.sleep(1)