'''
Created on 29.10.2018

@author: Henry Fock, Lia Kirsch
'''

import csv
import os
import sys
import json

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
from xml.etree import ElementTree as ET
from os import listdir
from os.path import isfile, join
from xml.dom.minidom import parse

import click
import netCDF4 as nc
import pandas as pd
import pygeoj
import shapefile
import xarray as xr
import ogr2ogr

# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")

def getBoundingBox(name, path):
    """
    returns the bounding Box of supported Datatypes and standards in WGS84.
    
    supported data: Shapefile (.shp), GeoJson (.json/.geojson), GeoTIFF (.tif), netCDF (.nc),
                    GeoPackage (.gpkg), alle ISO19xxx standardisiete Formate, CSV on the web
    
    @param path Path to the file
    @param name name of the file with extension
    @returns a boundingbox as an array in WGS84, formated like [minLong, minLat, maxLong, maxLat]
    """
    # connect name and path to file
    filepath = "%s\%s" % (path, name)
    # get file extension
    filename, file_extension = os.path.splitext(filepath)
    print(file_extension)
    #shapefile handelig
    if file_extension == ".shp":
        try:
            myshp = open(filepath, "rb")
            sf = shapefile.Reader(shp=myshp)
        # error
        except:
            click.echo("File not Found!")
            return None
        else: # if no error accured
            click.echo(sf.bbox)
            return sf.bbox

    # geojson handeling
    elif file_extension == ".json" or file_extension == ".geojson":
        try:
            myGeojson = pygeoj.load(filepath=filepath)
            click.echo(myGeojson.bbox)
            return myGeojson.bbox
        except ValueError: # if geojson is not a featureCollection
            myJson = open(filepath, "rb")
            myJson = json.load(myJson)

            # raw FeatureCollection
            myGeojson = {
                "type": "FeatureCollection",
                "features": []
            }

            myGeojson.get("features").append(myJson)
            myGeojson = pygeoj.load(data=myGeojson)
            click.echo(myGeojson.bbox)
            return myGeojson.bbox
        # errors
        except:
            click.echo("File not Found")
            return None

    elif file_extension == ".tif" or file_extension == ".tiff":
        # @see https://stackoverflow.com/questions/2922532/obtain-latitude-and-longitude-from-a-geotiff-file
        try:
            # get the existing coordinate system
            ds = gdal.Open(filepath)
            old_cs= osr.SpatialReference()
            old_cs.ImportFromWkt(ds.GetProjectionRef())

            # create the new coordinate system
            wgs84_wkt = """
            GEOGCS["WGS 84",
                DATUM["WGS_1984",
                    SPHEROID["WGS 84",6378137,298.257223563,
                        AUTHORITY["EPSG","7030"]],
                    AUTHORITY["EPSG","6326"]],
                PRIMEM["Greenwich",0,
                    AUTHORITY["EPSG","8901"]],
                UNIT["degree",0.01745329251994328,
                    AUTHORITY["EPSG","9122"]],
                AUTHORITY["EPSG","4326"]]"""
            new_cs = osr.SpatialReference()
            new_cs .ImportFromWkt(wgs84_wkt)

            # create a transform object to convert between coordinate systems
            transform = osr.CoordinateTransformation(old_cs,new_cs) 

            #get the point to transform, pixel (0,0) in this case
            width = ds.RasterXSize
            height = ds.RasterYSize
            gt = ds.GetGeoTransform()
            minx = gt[0]
            miny = gt[3] + width*gt[4] + height*gt[5] 
            maxx = gt[0] + width*gt[1] + height*gt[2]
            maxy = gt[3] 

            #get the coordinates in lat long
            latlongmin = transform.TransformPoint(minx,miny)
            latlongmax = transform.TransformPoint(maxx,maxy)
            bbox = [latlongmin[0], latlongmin[1], latlongmax[0], latlongmax[1]]
            click.echo(bbox)
            return bbox
        # errors
        except:
            click.echo("File not Found or TIFF is not GeoTIFF")

    # netCDF handeling
    elif file_extension == ".nc":
        try:
            # https://gis.stackexchange.com/questions/270165/gdal-to-acquire-netcdf-like-metadata-structure-in-python
            ds = xr.open_dataset(filepath)
            # transform coordinates section in a dictionary
            coordinates = ds.to_dict()['coords']
            # get the coordinates as a list
            lats = coordinates['latitude']['data']
            longs = coordinates['longitude']['data']

            # taking the smallest and highest coordinates from the lists
            bbox = [min(longs), min(lats), max(longs), max(lats)]
            click.echo(bbox)
            return bbox
        # errors
        except KeyError:
            click.echo("coordinate names may be spelled wrong: should be 'latitude'/'longitude")
            return None
        except:
            click.echo("File not found")
            return None

##########################################################################################################
    # handeling geoPackage (not working)
    # elif file_extension == ".gpkg":
    #     # @see http://cite.opengeospatial.org/pub/cite/files/edu/geopackage/text/advanced.html
    #     ds = ogr.Open(filepath)
    #     lyr = ds.GetLayerByName("gpkg_geometry_columns")
    #     print(lyr)

    #     # sql = "SELECT ST_IsEmpty() FROM %s as file" % filepath
    #     # test = gdal.Dataset.ExecuteSQL(sql)
    #     # print(test)
#########################################################################################################


    # csv or csv formated textfile handeling (csv on the web)
    elif file_extension == ".csv" or file_extension == ".txt":
        # @see https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
        try: # finding the correct collums for latitude and longitude
            csvfile = open(filepath)
            head = csv.reader(csvfile, delimiter=' ', quotechar='|')
            # get the headline an convert, if possible, ';' to ',' 
            # and seperate each word devided by a ',' into an array 
            header = next(head)[0].replace(";", ",").split(",")
            lng=None 
            lat=None
            # searching for valid names for latitude and longitude
            for t in header:
                if t == "longitude":
                    lng = "longitude"
                if t == "latitude":
                    lat = "latitude"
                if t == "lon":
                    lng = "lon"
                if t == "lng":
                    lng = "lng"
                if t == "lat":
                    lat = "lat"

            # if there is no valid name or coordinates, an exception is thrown an cought with an errormassage
            if(lat == None or lng == None):
                raise ValueError()
        # errors
        except ValueError:
            click.echo("pleas rename latitude an longitude: latitude/lat, longitude/lon/lng")
            return None
        except:
            click.echo("file not found")
            return None
        
        # if no error accured
        else:
            try:
                df = pd.read_csv(filepath, header=0)
                # get all coordinates from found collums
                latitudes = df[lng].tolist()
                longitudes = df[lat].tolist()
                
                # taking the smallest and highest coordinates from the lists
                bbox = [min(longitudes), min(latitudes), max(longitudes), max(latitudes)]
                click.echo(bbox)
                return bbox

            # in case the words are separated by a ';' insted of a comma
            except AttributeError:
                try:
                    # tell the reader that the seperator is a ';'
                    df = pd.read_csv(filepath, header=0, sep=';')
                    # get all coordinates from found collums
                    latitudes = df[lng].tolist()
                    longitudes = df[lat].tolist()
                    
                    # taking the smallest and highest coordinates from the lists
                    bbox = [min(longitudes), min(latitudes), max(longitudes), max(latitudes)]
                    click.echo(bbox)
                    return bbox
                # the csv is not valid
                except AttributeError:
                    click.echo("Pleas seperate your data with either ',' or ';'!" )
                    return None
            # errors
            except:
                click.echo("File Error: File not found or check if your csv file is valid to 'csv on the web'")
                return None

    # gml handeling
    elif file_extension == ".gml" or file_extension == ".xml":
        try:
            # @see https://gis.stackexchange.com/questions/39080/using-ogr2ogr-to-convert-gml-to-shapefile-in-python
            # convert the gml file to a GeoJSON file
            ogr2ogr.main(["","-f", "GeoJSON", "output.json", filepath])
            # srcDS = gdal.OpenEx(filepath)
            # ds = gdal.VectorTranslate('output.json', srcDS, format='GeoJSON')

            # get boundingbox from generated GeoJSON file
            myGeojson = pygeoj.load(filepath="output.json")
            click.echo(myGeojson.bbox)
            # delete generated GeoJSON file
            os.remove("output.json")
            return myGeojson.bbox
        # errors
        except:
            click.echo("file not found or your gml/xml/kml data is not valid")
            return None

    # if the extension has not been implemented yet or won't be supported
    else:
        click.echo("type %s not yet supported" % file_extension)
        return None


# Main method
if __name__ == '__main__':
    getBoundingBox()
