import os
import sys
import functools
import math


def sameDatatype(file1, file2):
    filename1, file_extension1 = os.path.splitext(file1)
    filename2, file_extension2 = os.path.splitext(file2)

    same1, same2 = 0,0
    same1 = file_extension1.find(file_extension2) # 2 in 1
    same2 = file_extension2.find(file_extension1) # 1 in 2

    return 100 if same1>=0 or same2>=0 else 0

# def sameAuthor(file1, file2):
#     author1 = ""
#     author2 = ""

#     return 100 if author1.lower() == author2.lower() else 0

def similarTitle(file1, file2):
    filename1, file_extension1 = os.path.splitext(file1)
    filename2, file_extension2 = os.path.splitext(file2)

    countList = 0
    if len(filename1) >= len(filename2):
        # searches for same caracters in both strings
        charList = []
        for i in filename2:
            if i not in charList:
                charList.append(i)
                countList += filename1.count(i)
        percent = 0
        if len(filename1) != 0:
            percent = countList*100/len(filename1)
            percent = math.floor(percent*100)/100
        return percent
    else:
        charList = []
        for i in filename1:
            if i not in charList:
                charList.append(i)
                countList += filename2.count(i)
        percent = 0
        if len(filename2) != 0:
            percent = countList*100/len(filename2)
            percent = math.floor(percent*100)/100
        return percent

print(similarTitle("FeatureCollection.json","geoTiffTest.tif"))