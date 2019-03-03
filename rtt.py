# coding=utf-8
# 
# Convert files from InteractiveBrokers to the below format:
# 
# 1. Bloomberg upload trade file.
# 2. Geneva reconciliation file.
#

import requests
from datetime import datetime
from network_rtt.utility import getURL
import logging
logger = logging.getLogger(__name__)



def measureRTT(url, timeout, requestNo):
	"""
	[String] url, [Integer] timeout (time out period in seconds), 
	[Integer] requestNo 
		=> no return value

	Send a request to url appended by an integer, wait for response and measure
	the round trip time (RTT) for this request, log the time to send the request
	and the RTT. If a time out or other error occurs, then log an error.
	"""
	timeBefore = datetime.now()
	try:
		r = requests.get(url + str(requestNo), timeout=timeout)
		rtt = (datetime.now() - timeBefore).total_seconds()
		logger.info('{0},{1},{2},{3},{4}' \
			.format(r.status_code, timeBefore, requestNo, rtt, r.text))

	except requests.exceptions.Timeout:
		logger.info('timeout,{0},{1}'.format(timeBefore, requestNo))
	
	except:
		logger.info('error,{0},{1}'.format(timeBefore, requestNo))
	




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	# As we use the requests module, by default they log messages with DEBUG
	# level, which is not desired in this case. So we manually set them to
	# warning level.
	# 
	# from: https://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library
	logging.getLogger('requests').setLevel(logging.WARNING)
	logging.getLogger('urllib3').setLevel(logging.WARNING)

	measureRTT(getURL(), 2, 1)