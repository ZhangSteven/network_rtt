# coding=utf-8
# 

import unittest2
from network_rtt.analysis import readLine, infoLine, httpStatus200, \
                                correctResponse
from network_rtt.utility import getCurrentDirectory
from utils.iter import numElements
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

