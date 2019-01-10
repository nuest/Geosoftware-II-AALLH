import generalSimilarity
import unittest

# author Lia Kirsch
# Testing generalSimilarity 
# 09.01.19

def test_similarTitle():
    total = generalSimilarity.similarTitle("1.txt","1.txt")
    assert total == 100

def test_similarTitle():
    total = generalSimilarity.similarTitle("1.txt","2.txt")
    assert total != 100

def test_similarTitle():
    total = generalSimilarity.similarTitle("abcd.txt","abef.txt")
    assert total == 50

def test_similarTitle():
    total = generalSimilarity.similarTitle("1.txt","2.txt")
    assert total == 0

def test_similarTitle():
    total = generalSimilarity.similarTitle("abcd.txt","aegf.txt")
    assert total == 25

def test_similarTitle():
    total = generalSimilarity.similarTitle("abcd.txt","abcf.txt")
    assert total == 75



def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.txt", "abef.txt")
    assert total == 100

def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.py", "abef.txt")
    assert total == 100


def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.js", "abef.txt")
    assert total == 0

def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.tif", "abcd.geotif")
    assert total == 100

def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.tiff", "abef.geotiff")
    assert total == 0

def test_sameDatatype():
    total = generalSimilarity.sameDatatype("abcd.docs", "abef.txt")
    assert total == 0