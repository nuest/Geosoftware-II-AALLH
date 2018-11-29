'''
Created on 30.10.2018

@author: hfock
'''
import os, sys

file_path = '../Python_Modules'
sys.path.append(file_path)

import click
import csv

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name without extension")
#@click.option('--type', prompt="File type ", help="File type")

def getBoundingBox(name, path):
    filepath = "%s\%s" % (path, name)
    try:
        csv_file = open("%s.txt" % (filepath), "rt")
    except :
        pass

    try:
        csv_file = open("%s.csv" % (filepath), "rt")
    except :
        pass

    try:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                click(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                click(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
    except:
        click("File not Found!")