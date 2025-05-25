#!/usr/bin/env python3
import logging

logger = logging.getLogger(__name__)


def do_something():
    logger.info('Doing something')


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')
    do_something()
    logger.info('Finished')


if __name__ == '__main__':
    main()
