# author: Aysel Tandik
# Testing timeSimilarity
# 09.01.2018

import timeSimilarity
import unittest

def test_timeLength():
    result = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result == 0

def test_timeOverlap():
    result = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result == 0.54

def test_similarInterval():
    result = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result == 0.0

def test_Similartime():
    result1 = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    result2 = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    result3 = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    assert result1 == 100
    assert result2 == 100
    assert result3 == 100

def test_NotSimilartime():
    result1 = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['1957/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 123])
    result2 = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['2000/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 123])
    result3 = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], ['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 0])
    assert result1 == 0
    assert result2 == 0
    assert result3 == 0
