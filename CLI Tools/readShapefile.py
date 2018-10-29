'''
Created on 27.10.2018

@author: hfock
'''
import os, sys

file_path = '../Python_Modules'
sys.path.append(file_path)

import shapefile
import click

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name ", help="File name")
#@click.option('--type', prompt="File type ", help="File type")

def getBoundingBox(path, name):
    filepath = "%s\%s" % (path, name)
    print(filepath)
    try:
        myshp = open("%s.shp" % (filepath), "rb")
        sf = shapefile.Reader(shp=myshp)
    except :
        pass

    try:
        mydbf = open("%s.dbf" % filepath, "rb")
        sf = shapefile.Reader(dbf=mydbf)
    except :
        pass

    try:
        click.echo(sf.bbox)
    except:
        click.echo("File not Found: Try to check the spelling!")

    

if __name__ == '__main__':
    getBoundingBox()