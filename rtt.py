# coding=utf-8
# 
# Convert files from InteractiveBrokers to the below format:
# 
# 1. Bloomberg upload trade file.
# 2. Geneva reconciliation file.
#

import requests
from datetime import datetime
from time import sleep
from itertools import count
from functools import partial
from network_rtt.utility import getURL
from utils.iter import numElements
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
		logger.error('timeout,{0},{1}'.format(timeBefore, requestNo))
	
	except:
		logger.error('error,{0},{1}'.format(timeBefore, requestNo))
	


def delayedRTT(delaySeconds, url, timeout, requestNo):
	"""
	[Integer] delaySeconds, ...

	It sleeps for delaySeconds, then call measureRTT() with the given
	parameters.
	"""
	sleep(delaySeconds)
	measureRTT(url, timeout, requestNo)




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

	# Simply creating the map() object won't do anything yet. We need to 
	# consume it to make things happen. Therefore the numElement call.
	numElements(map(partial(delayedRTT, 5, getURL(), 1), range(1,1000)))