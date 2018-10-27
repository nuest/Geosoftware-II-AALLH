'''
Created on 27.10.2018

@author: hfock
'''
import shapefile
import click

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name ", help="File name")
#@click.option('--type', prompt="File type ", help="File type")

def getBoundingBox(path, name):
    filepath = "%s\%s" % (path, name)
    try:
        myshp = open("%s.shp" % (filepath), "rb")
        sf = shapefile.Reader(shp=myshp)
    except:
        mydbf = open("%s.dbf" % filepath, "rb")
        sf = shapefile.Reader(dbf=mydbf)
        
    click.echo(sf.bbox)

if __name__ == '__main__':
    getBoundingBox()