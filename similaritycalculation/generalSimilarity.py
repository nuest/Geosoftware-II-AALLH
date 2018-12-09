import os
import sys

def sameDatatype(file1, file2):
    filename1, file_extension1 = os.path.splitext(file1)
    filename2, file_extension2 = os.path.splitext(file2)

    same1, same2 = 0,0
    same1 = file_extension1.find(file_extension2) # 2 in 1
    same2 = file_extension2.find(file_extension1) # 1 in 2

    return 100 if same1>=0 or same2>=0 else 0