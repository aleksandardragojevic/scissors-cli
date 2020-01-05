#
# Scissors console video client.
#
# author: aleksandar
#

import os
import logging
import logging.config
import cv2
import time

#
# Logger.
#
LoggerConfigFileName = 'scissors-cam-log.conf'
if os.path.exists(LoggerConfigFileName):
    logging.config.fileConfig(fname=LoggerConfigFileName, disable_existing_loggers=True)
else:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)

import argparse
import scissors_cam_cli

#
# Arguments
#
def parse_args():
    parser = argparse.ArgumentParser(description='Scissors console camera client')
    
    parser.add_argument(
        '--scissors',
        help='IP address and port of the scissors',
        default='scissors.local:13367')

    return parser.parse_args()

def log_args(args):
    logger.info(
        'Using arguments:\n'
        '  scissors: {0}\n'.format(
            args.scissors))

#
# Entry
#
def main():
    logger.info('Starting camera client')
    logger.info('Press Ctrl+C to stop')

    args = parse_args()
    log_args(args)

    try:
        with scissors_cam_cli.ScissorsCamClient(args.scissors) as cli:
            while True:
                frame = cli.get_next_frame()

                if frame is None:
                    logger.error("Video stream stopped")
                    break

                cv2.imshow('scissors', frame)
                cv2.waitKey(15)
    except KeyboardInterrupt:
        logger.info("Exiting...")

main()
