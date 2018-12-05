import os
import sys
from math import *
import time as timeMod

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
from DateTime import DateTime
from datetime import date


def timeLength(timeA, timeB):
    startA = DateTime(timeA[0])
    endA = DateTime(timeA[1])

    startB = DateTime(timeB[0])
    endB = DateTime(timeB[1])

    lengthA = endA - startA
    lengthB = endB - startB

    if lengthA>= lengthB:
        lengthPercentage = lengthB/lengthA
        lengthPercentage = floor(lengthPercentage/100)*100
        print(lengthPercentage)
        return lengthPercentage
    else:
        lengthPercentage = lengthA/lengthB
        lengthPercentage = floor(lengthPercentage/100)*100
        print(lengthPercentage)
        return lengthPercentage

def timeOverlap(timeA, timeB):
    overlap = abs(DateTime(timeA[1]) - DateTime(timeB[0]))

    timeLengthA = DateTime(timeA[1]) - DateTime(timeA[0])
    timeLengthB = DateTime(timeB[1]) - DateTime(timeB[0])

    if timeLengthA >= timeLengthB:
        overlapPercentage = overlap/timeLengthA
        overlapPercentage = floor(overlapPercentage*100)/100
        print(overlapPercentage)
        return overlapPercentage
    else:
        overlapPercentage = overlap/timeLengthB
        overlapPercentage = floor(overlapPercentage*100)/100
        print(overlapPercentage)
        return overlapPercentage

def similarInterval(timeA, timeB):
    if timeA[2]>= timeB[2]:
        intervalPercentage = timeB[2]/timeA[2]
        intervalPercentage = floor(intervalPercentage*100)/100
        print(intervalPercentage)
        return intervalPercentage
    else:
        intervalPercentage = timeA[2]/timeB[2]
        intervalPercentage = floor(intervalPercentage*100)/100
        print(intervalPercentage)
        return intervalPercentage

