#
# Sending scissors commands driven from console.
#
# author: aleksandar
#

import os
import logging
import logging.config

#
# Logger.
#
LoggerConfigFileName = 'scissors-cmd-log.conf'
if os.path.exists(LoggerConfigFileName):
    logging.config.fileConfig(fname=LoggerConfigFileName, disable_existing_loggers=True)
else:
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)

import argparse
import scissors_cmd_cli

#
# Arguments
#
def parse_args():
    parser = argparse.ArgumentParser(description='Scissors console command client')
    
    parser.add_argument(
        '--scissors',
        help='IP address and port of the scissors',
        default='scissors.local:13368')
    parser.add_argument(
        'cmd',
        nargs='+',
        help='Command to send')

    return parser.parse_args()

def log_args(args):
    logger.info(
        'Using arguments:\n'
        '  scissors: {0}\n'
        '  cmd: {1}'.format(
            args.scissors,
            ' '.join(args.cmd)))

#
# Entry
#
def main():
    args = parse_args()
    log_args(args)

    try:
        with scissors_cmd_cli.ScissorsCmdClient(args.scissors) as cli:
            cli.cmd_text(' '.join(args.cmd))
        logger.info('Done')
    except KeyboardInterrupt:
        logger.info("Interrupted from keyboard. Exiting...")

main()
