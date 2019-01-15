import math


def sameDatatype(fileEnding1, fileEnding2):
    print(fileEnding1, fileEnding2)
    same1, same2 = -1,-1
    same1 = fileEnding1.find(fileEnding2.replace(".", "")) # 2 in 1
    same2 = fileEnding2.find(fileEnding1.replace(".", "")) # 1 in 2
    print(same1, same2)

    return 100 if same1>=0 or same2>=0 else 0

def similarAuthor(author1, author2):
    return 100 if author1 == author2 else 0

def similarTitle(title1, title2):
    countList = 0
    if len(title1) >= len(title2):
        # searches for same caracters in both strings
        charList = []
        for i in title2:
            if i not in charList:
                charList.append(i)
                countList += title1.count(i)
        percent = 0
        if len(title1) != 0:
            percent = countList*100/len(title1)
            percent = math.floor(percent*100)/100
        return percent
    else:
        charList = []
        for i in title1:
            if i not in charList:
                charList.append(i)
                countList += title2.count(i)
        percent = 0
        if len(title2) != 0:
            percent = countList*100/len(title2)
            percent = math.floor(percent*100)/100
        return percent

print(sameDatatype(".tif",".geotif"))