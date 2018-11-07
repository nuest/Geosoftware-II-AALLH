'''
Created on 29.10.2018

@author: hfock
'''

import os, sys

file_path = '../Python_Modules'
sys.path.append(file_path)

import click
import shapefile
import pygeoj
from netCDF4 import Dataset
from osgeo import gdal
from osgeo import ogr
import pandas as pd
import csv

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")

def getBoundingBox(name, path):
    filepath = "%s\%s" % (path, name)
    filename, file_extension = os.path.splitext(filepath)
    print(file_extension)
    #shapefile handelig
    if file_extension == ".shp" or file_extension == ".dbf":
        try:
            myshp = open(filepath, "rb")
            sf = shapefile.Reader(shp=myshp)
        except:
            click.echo("File not Found!")
            return None
        else:
            click.echo(sf.bbox)
            return sf.bbox

    elif file_extension == ".json" or file_extension == ".geojson":
        try:
            myGeojson = pygeoj.load(filepath=filepath)
            click.echo(myGeojson.bbox)
            return myGeojson.bbox
        except ValueError:
            myJson = open(filepath, "rb")
            myJson = json.load(myJson)

            myGeojson = {
                "type": "FeatureCollection",
                "features": []
            }

            myGeojson.get("features").append(myJson)
            myGeojson = pygeoj.load(data=myGeojson)
            click.echo(myGeojson.bbox)
            return myGeojson.bbox
        except:
            click.echo("File not Found")
            return None

    elif file_extension == ".tif":
        try:
            gtif = gdal.Open(filepath)
            print (gtif.GetMetadata())
        except:
            click.echo("File not Found")

    elif file_extension == ".nc":
        rootgrp = Dataset(filepath, "w", format="NETCDF4")
        print (rootgrp.data_model)
        rootgrp.close()

    elif file_extension == ".gpkg":
        sql = "SELECT ST_IsEmpty() FROM %s as file" % filepath
        test = gdal.Dataset.ExecuteSQL(sql)
        print(test)

    elif file_extension == ".csv" or file_extension == ".txt":
        #@see https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
        try:
            csvfile = open(filepath)
            head = csv.reader(csvfile, delimiter=' ', quotechar='|')
            print(next(head))

            ###############################
            # search for coordinat colums #
            ###############################

            df = pd.read_csv(filepath, header=0)

            # doesn't work. should return latitudes and longitudes as a List
            # latitudes = df.lon.tolist()
            # longitudes = df.lat.tolist()

            # calculate BBOX x=lat y=lon
            bbox = [max(latitudes), max(longitudes), min(latitudes), min(longitudes)]

            click.echo(bbox)
            return bbox
        except:
            click.echo("File Error: ")
            return None

    
    else:
        click.echo("type %s not yet supported" % file_extension)
        return None

if __name__ == '__main__':
    getBoundingBox()
