#
# Scissors console statistics client.
#
# author: aleksandar
#

import os
import logging
import logging.config

#
# Logger.
#
LoggerConfigFileName = 'scissors-stats-log.conf'
if os.path.exists(LoggerConfigFileName):
    logging.config.fileConfig(fname=LoggerConfigFileName, disable_existing_loggers=True)
else:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)

import argparse
import scissors_stats_cli

#
# Arguments
#
def parse_args():
    parser = argparse.ArgumentParser(description='Scissors console stats client')
    
    parser.add_argument(
        '--scissors',
        help='IP address and port of the scissors',
        default='scissors.local:13369')

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
    logger.info('Starting stats client')
    logger.info('Press Ctrl+C to stop')

    args = parse_args()
    log_args(args)

    try:
        with scissors_stats_cli.ScissorsStatsClient(args.scissors) as cli:
            cli.subscribe()

            while True:
                msg = cli.get_stats_msg_if_any(0.2)

                if msg is not None:
                    print(msg)
        logger.info('Done')
    except KeyboardInterrupt:
        logger.info("Exiting...")

main()
