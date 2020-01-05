#
# A client for scissors video stream.
#
# The stream is provided as opencv compatible series of frames.
#
# author: aleksandar
#

import logging
import cv2

logger = logging.getLogger(__name__)

class ScissorsCamClient:
    def __init__(self, scissors):
        self.scissors = scissors
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture('tcp://' + self.scissors)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_frame_stream(self, cb):
        while True:
            frame = self.get_next_frame()

            if frame is None:
                logger.error('Video stream stopped')
                cb(None)
                break

    def get_next_frame(self):
        _, frame = self.cap.read()
        return frame
