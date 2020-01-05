#
# Stats client for scissors.
#
# author: aleksandar
#

import logging
import socket
import select

logger = logging.getLogger(__name__)

class ScissorsStatsClient:
    def __init__(self, scissors):
        self.scissors_text = scissors
        ip_port = scissors.split(':')
        self.scissors = (ip_port[0], int(ip_port[1]))
        self.sock = None
        self.subscribed = False

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.info('Created socket for sending commands')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.subscribed:
            self.subscribed = False
            self.unsubscribe()

        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def subscribe(self):
        self.sock.sendto('subscribe'.encode('utf-8'), self.scissors)
        logger.debug('Sent subscibe to {0}'.format(self.scissors_text))
        self.subscribed = True
    
    def unsubscribe(self):
         self.sock.sendto('unsubscribe'.encode('utf-8'), self.scissors)
         logger.debug('Sent unsubscibe to {0}'.format(self.scissors_text))

    def get_socket(self):
        return self.sock

    def get_stats_msg(self):
        msg, _ = self.sock.recvfrom(1000)
        return msg.decode('utf-8')

    def get_stats_msg_if_any(self, timeout = 0):
        ready_list, _, _ = select.select([self.sock], [], [], timeout)

        if len(ready_list) == 0:
            return None
        
        return self.get_stats_msg()

