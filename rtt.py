# coding=utf-8
# 
# Convert files from InteractiveBrokers to the below format:
# 
# 1. Bloomberg upload trade file.
# 2. Geneva reconciliation file.
#

from network_rtt.utility import getURL
import logging
logger = logging.getLogger(__name__)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	print(getURL())