import csv
import os
import sys
import json
import functools
import math
import sqlite3
import time as timeMod
import tempfile

# add local modules folder
file_path = os.path.join('..', 'Python_Modules')
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
import click
import netCDF4 as nc
import pandas as pd
import pygeoj
import shapefile
import xarray as xr
import ogr2ogr
from DateTime import DateTime
from datetime import date


# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")
@click.option('--clear','-c', default=False, is_flag=True, help='Clear screen before showing results')
def main(path, name, clear):
    res = getTimeExtent(name, path)
    if clear:
        click.clear()
    if res[0] is not None:
        click.echo(res[0])
    else:
        click.echo(res[1])

def getTimeExtent(name, path):
    """
    returns the bounding Box of supported Datatypes and standards in WGS84.
    
    supported data: Shapefile (.shp), GeoJson (.json/.geojson), netCDF (.nc),
                    all ISO19xxx standardisiete Formate, CSV on the web
    
    @param path Path to the file
    @param name name of the file with extension
    @returns a boundingbox as an array in WGS84, formated like [minLong, minLat, maxLong, maxLat]
    """
    # connect name and path to file
    filepath = os.path.join(path, name)
    # get file extension
    filename, file_extension = os.path.splitext(filepath)

    #################################################################

    def netCDFCase(filepath):
        try:
            # https://gis.stackexchange.com/questions/270165/gdal-to-acquire-netcdf-like-metadata-structure-in-python
            ds = xr.open_dataset(filepath)
            # transform coordinates section in a dictionary
            time = ds.to_dict()['coords']['time']['data']
            isoTimeSeq = list(map(DateTime,(list(map(str, time)))))
            isoTimeSeq.sort()
            avgInt = 0
            if len(isoTimeSeq) > 1:
                interval = []

                for i in range(len(isoTimeSeq)-1):
                    interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                
                avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
                # avgInt = math.floor(avgInt*1000)/1000
                # print(avgInt)
            
            return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt],None)

            
        # errors
        except KeyError:
            return (None, "'time' may be spelled wrong: should be 'time")
        except:
            return (None, "File Error!")

    def CSVCase(filepath):
        # column name should be either date, time or timestamp
        # @see https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
        try: # finding the correct collums for latitude and longitude
            csvfile = open(filepath)
            head = csv.reader(csvfile, delimiter=' ', quotechar='|')
            # get the headline and convert, if possible, ';' to ',' 
            # and seperate each word devided by a ',' into an array 
            header = next(head)[0].replace(";", ",").split(",")
            time = None
            # searching for valid names for latitude and longitude
            for t in header:
                if t == "date":
                   time = "date"
                if t == "time":
                    time = "time"
                if t == "timestamp":
                    time = "timestamp"
            csvfile.close()

            csvfile = open(filepath)
            correctCSV = csvfile.read()
            correctCSV = correctCSV.replace(";", ",")
            csvfile.close()

            # if there is no valid name or coordinates, an exception is thrown an cought with an errormassage
            if(time is None):
                raise ValueError("pleas rename timestamp to: date/time/timestamp")

            
        # errors
        except ValueError as e:
            return (None, e)
        except:
            return (None, "File Error!")
        
        # if no error accured
        else:
            try:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    curDir = os.getcwd()
                    os.chdir(tmpdirname)
                    newFile = open("newCSV.csv","w+")
                    newFile.write(correctCSV)
                    newFile.close()
                    df = pd.read_csv(os.path.join(tmpdirname, "newCSV.csv"), header=0)
                    os.chdir(curDir)

                # get time from found columns
                timestamp = df[time].tolist()

                isoTimeSeq = list(map(DateTime,(list(map(str, timestamp)))))
                isoTimeSeq.sort()
                avgInt = 0
                if len(isoTimeSeq) > 1:
                    interval = []

                for i in range(len(isoTimeSeq)-1):
                    interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                
                avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
            
                return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt], None)

            # errors
            except:
                return (None, "File Error: File not found or check if your csv file is valid to 'csv on the web'")

    def geojsonCase(filepath):
        try:
            ds = open(filepath)
            jsonDict = json.load(ds)
            isoTimeSeq = []
            if jsonDict["type"] == "FeatureCollection":
                prop = ""
                if "time" in jsonDict["features"][0]:
                    prop = "time"
                elif "date" in jsonDict["features"][0]:
                    prop = "date"
                else:
                    return (None, "no time data available")

                timeext = []
                for feature in jsonDict["features"]:
                    timeext.append(feature["properties"][prop])
                isoTimeSeq = list(map(DateTime, timeext))

                isoTimeSeq.sort()
                avgInt = 0
                if len(isoTimeSeq) > 1:
                    interval = []

                for i in range(len(isoTimeSeq)-1):
                    interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                
                avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
            
                return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt], None)
            else:
                prop = ""
                if "time" in jsonDict:
                    prop = "time"
                elif "date" in jsonDict:
                    prop = "date"
                else:
                    return (None, "no time data available")

                timeext = jsonDict["properties"]["time"]
                timeext = DateTime(timeext)
                return ([timeext, timeext, 0], None)
        except:
            return (None, "File Error!")
        finally:
            ds.close()

    def geoPackageCase(filepath):
        try:
            conn = sqlite3.connect(filepath)
            c = conn.cursor()
            c.execute("""   SELECT last_change 
                            FROM gpkg_contents 
                    """)
            row = c.fetchone()
            row = list(map(DateTime, row))
            # print(row)
            return ([str(row[0]), str(row[0]), 0], None)
        except:
            return (None, "File Error!")
        finally:
            try:
                conn.close()
            except:
                pass

#################################################################

    # netCDF handeling
    if file_extension == ".nc":
        return netCDFCase(filepath)

    # csv handeling
    elif file_extension in (".csv", ".txt"):
        return CSVCase(filepath)

    # json handeling
    elif file_extension in (".json", ".geojson"):
        return geojsonCase(filepath)

    # geopackage handeling
    elif file_extension == ".gpkg":
        return geoPackageCase(filepath)
    
    # unsupported files handeling
    else:
        return (None, "Filetype %s not yet supported" % file_extension)

# Main method
if __name__ == '__main__':
    main()
