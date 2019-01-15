from math import floor

from DateTime import DateTime

def timeLength(timeA, timeB):
    startA = DateTime(timeA[0])
    endA = DateTime(timeA[1])

    startB = DateTime(timeB[0])
    endB = DateTime(timeB[1])

    if startA > endA or startB > endB:
        raise AttributeError("start value is higher than end value")

    lengthA = endA - startA
    lengthB = endB - startB

    if lengthA == lengthB:
        return 100
    else:
        if lengthA > lengthB:
            lengthPercentage = lengthB/lengthA
            lengthPercentage = floor(lengthPercentage/100)*100
            return lengthPercentage
        else:
            lengthPercentage = lengthA/lengthB
            lengthPercentage = floor(lengthPercentage/100)*100
            return lengthPercentage

def timeOverlap(timeA, timeB):
    if DateTime(timeA[0]) == DateTime(timeB[0]) and DateTime(timeA[1]) == DateTime(timeB[1]):
        # timeA and timeB are equal
        return 100

    # start A below start B
    if DateTime(timeA[0]) <= DateTime(timeB[0]):
        if DateTime(timeA[1]) <= DateTime(timeB[0]):
            # no overlap, because end A below or on start B
            return 0
        else: # overlap
            overlap = DateTime(timeA[1]) - DateTime(timeB[0])

    else: # start B below start A
        if DateTime(timeB[1]) <= DateTime(timeA[0]):
            # no overlap, because end B below or on start A
            return 0
        else: # overlap
            overlap = DateTime(timeB[1]) - DateTime(timeA[0])
        
    timeLengthA = DateTime(timeA[1]) - DateTime(timeA[0])
    timeLengthB = DateTime(timeB[1]) - DateTime(timeB[0])

    # prevent division by zero by giving a single moment a duration of arround a second
    if timeLengthA == 0:
        timeLengthA = 0.00001
    if timeLengthB == 0:
        timeLengthB = 0.00001

    if timeLengthA > timeLengthB:
        overlapPercentage = overlap/timeLengthA
        overlapPercentage = floor(overlapPercentage*100)/100
        return overlapPercentage
    else:
        overlapPercentage = overlap/timeLengthB
        overlapPercentage = floor(overlapPercentage*100)/100
        return overlapPercentage

def similarInterval(timeA, timeB):
    if timeA[2] == timeB[2]:
        return 100
    else:
        if timeA[2] > timeB[2]:
            intervalPercentage = timeB[2]/timeA[2]
            intervalPercentage = floor(intervalPercentage*100)/100
            return intervalPercentage
        else:
            intervalPercentage = timeA[2]/timeB[2]
            intervalPercentage = floor(intervalPercentage*100)/100
            return intervalPercentage

# print(timeOverlap(['1935/01/01 00:00:00 GMT+0', '2014/01/01 00:00:00 GMT+0', 365.253164556962], ['2013/01/01 00:00:00 GMT+0', '2018/03/28 12:43:14.034000 GMT+0', 0]))

# print(DateTime('1935/01/01 00:00:10 GMT+0') - DateTime('1935/01/01 00:00:00 GMT+0'))
