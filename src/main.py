import os
import time
from utils.auth import catch_rabbits
from utils.watch import logger
from utils.scrape import process_message


queue_name = 'launch_crawler'


def check_queue(queue_name):
    logger.info(f'Checking Que for URLs: {queue_name}')
    catch_rabbits(queue_name, process_message)


if __name__ == "__main__":
    check_queue(queue_name)
