import os
import sys

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
import click
import ogr2ogr
import sqlite3

# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")

def getBoundingBox(name, path):
    """returns the bounding Box of supported Datatypes and standards in WGS84.

    supported data: Shapefile (.shp), GeoJson (.json/.geojson), GeoTIFF (.tif), netCDF (.nc), GeoPackage (.gpkg), alle ISO19xxx standardisiete Formate, CSV on the web
    
    @param path Path to the file
    @param name name of the file with extension
    @returns a boundingbox as an array in WGS84, formated like [minLong, minLat, maxLong, maxLat]
    """
    # connect name and path to file
    filepath = "%s\%s" % (path, name)
    # get file extension
    filename, file_extension = os.path.splitext(filepath)
    print(file_extension)

    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute("""   SELECT min_x, min_y, max_x, max_y, srs_id 
                    FROM gpkg_contents 
            """)
    # print(type(c.fetchone()))
    row = c.fetchone()
    bbox = [row[0], row[1], row[2], row[3]]
    print(bbox)

    refsys = row[4]

    # Input file details   
    minpoint = CRSTransform(row[0], row[1], refsys)
    maxpoint = CRSTransform(row[2], row[3], refsys)

    bbox = [minpoint[0], minpoint[1], maxpoint[0], maxpoint[1]]
    print(bbox)


def CRSTransform(Lat, Long, refsys):
    # Coordinate Reference System (CRS)
    SourceEPSG = refsys
    TargetEPSG = 4326

    source = osr.SpatialReference()
    source.ImportFromEPSG(SourceEPSG)

    target = osr.SpatialReference()
    target.ImportFromEPSG(TargetEPSG)

    transform = osr.CoordinateTransformation(source, target)
    point = ogr.CreateGeometryFromWkt("POINT (%s %s)" % (Lat, Long))
    point.Transform(transform)
    return [point.GetX(),point.GetY()]


# Main method
if __name__ == '__main__':
    getBoundingBox()