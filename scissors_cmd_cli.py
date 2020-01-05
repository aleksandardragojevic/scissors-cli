#
# Client for scissors. Allows sending commands.
#
# author: aleksandar
#

import logging
import socket

logger = logging.getLogger(__name__)

class ScissorsCmdClient:
    def __init__(self, scissors):
        self.scissors_text = scissors
        ip_port = scissors.split(':')
        self.scissors = (ip_port[0], int(ip_port[1]))
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.info('Created socket for sending commands')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def cmd_text(self, text):
        bytes_sent = self.sock.sendto(text.encode('utf-8'), self.scissors)
        logger.debug(
            '{0} <- "{1}" ({2} bytes)'.format(
                self.scissors_text,
                text,
                bytes_sent))


