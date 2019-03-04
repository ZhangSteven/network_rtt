# coding=utf-8
# 

import unittest2
from network_rtt.analysis import readLine, infoLine, httpStatus200, \
                                correctResponse, interval, histogram, \
                                analyzeFile
from network_rtt.utility import getCurrentDirectory
from utils.iter import numElements
from functools import partial
from toolz.functoolz import compose
from datetime import datetime, timedelta
from os.path import join



class TestAnalysis(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAnalysis, self).__init__(*args, **kwargs)


    def testInfoLine(self):
        inputFile = join(getCurrentDirectory(), 'test', 'samplelog.log')
        self.assertEqual(10, numElements(filter(infoLine, readLine(inputFile))))



    def testhttpStatus200(self):
        inputFile = join(getCurrentDirectory(), 'test', 'samplelog.log')
        self.assertEqual(9, numElements(filter(httpStatus200 \
                                               , filter(infoLine \
                                                        , readLine(inputFile)))))



    def testCorrectResponse(self):
        inputFile = join(getCurrentDirectory(), 'test', 'samplelog.log')
        self.assertEqual(8
                        , numElements(filter(correctResponse \
                                            , filter(httpStatus200 \
                                                    , filter(infoLine \
                                                            , readLine(inputFile))))))



    def testInterval(self):
        inputFile = join(getCurrentDirectory(), 'test', 'samplelog.log')
        starttime = datetime.strptime('2019-03-03 11:30:00', '%Y-%m-%d %H:%M:%S')
        interval_1130 = partial(interval \
                                , starttime
                                , starttime + timedelta(minutes=30))
        n = compose(numElements \
                    , partial(filter, interval_1130) \
                    , partial(filter, correctResponse) \
                    , partial(filter, httpStatus200) \
                    , partial(filter, infoLine) \
                    , readLine)(inputFile)

        self.assertEqual(n, 3)



    def testHistogram(self):
        timeSlots = [datetime.strptime('2019-03-03 11:00:00', '%Y-%m-%d %H:%M:%S') \
                    , datetime.strptime('2019-03-03 11:30:00', '%Y-%m-%d %H:%M:%S')
                    , datetime.strptime('2019-03-03 12:00:00', '%Y-%m-%d %H:%M:%S')
                    , datetime.strptime('2019-03-03 12:30:00', '%Y-%m-%d %H:%M:%S')]

        lines = ['INFO 2019-03-03 11:29:04,531 rtt | 200,2019-03-03 11:29:04.511230,1,0.02,response 1' \
                , 'INFO 2019-03-03 11:55:32,110 rtt | 200,2019-03-03 11:55:32.086230,4,0.024,response 4' \
                , 'INFO 2019-03-03 11:59:31,816 rtt | 200,2019-03-03 11:59:31.802230,4,0.014,response 4' \
                ]
        self.assertEqual([1, 2, 0], list(histogram(timeSlots, lines)))



    def testAnalyzeFile(self):
        inputFile = join(getCurrentDirectory(), 'test', 'samplelog.log')
        timeSlots = [datetime.strptime('2019-03-03 11:00:00', '%Y-%m-%d %H:%M:%S') \
                    , datetime.strptime('2019-03-03 11:30:00', '%Y-%m-%d %H:%M:%S')
                    , datetime.strptime('2019-03-03 12:00:00', '%Y-%m-%d %H:%M:%S')
                    , datetime.strptime('2019-03-03 12:30:00', '%Y-%m-%d %H:%M:%S')]

        self.assertEqual([2, 3, 3], list(analyzeFile(timeSlots, inputFile)))