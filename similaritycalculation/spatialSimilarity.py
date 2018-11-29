import os
import sys
from math import *

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr

def spatialOverlap(bboxA, bboxB):
    boxA = generateGeometryFromBbox(bboxA)
    boxB = generateGeometryFromBbox(bboxB)

    print(boxA)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    print(areaA)

    largerArea = areaA if areaA >= areaB else areaB

    intersection = boxA.Intersection(boxB)
    intersectGeometry = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())

    intersectArea = intersectGeometry.GetArea()

    print(intersectArea)

    reachedPercent = intersectArea*100/largerArea

    print(reachedPercent)
    return reachedPercent


# similar scale fehlt
def similarArea(bboxA, bboxB):
    boxA = generateGeometryFromBbox(bboxA)
    boxB = generateGeometryFromBbox(bboxB)

    print(boxA)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    print(areaA)
    print(areaB)

    reachedPercent = 0
    if areaA >= areaB:
        reachedPercent = areaB*100/areaA
    else:
        reachedPercent = areaA*100/areaB

    print(reachedPercent)
    return reachedPercent


# funktioniert noch nicht
def spatialDistance(bboxA, bboxB):
    centerA = center_geolocation(((bboxA[0],bboxA[1]),(bboxA[2], bboxA[3])))
    centerB = center_geolocation(((bboxB[0],bboxB[1]),(bboxB[2], bboxB[3])))

    print(centerA)
    print(centerB)

    wkt = "LINESTRING (%f %f, %f %f)" % (centerA[0], centerA[1], centerB[0], centerB[1])
    centerLine = ogr.CreateGeometryFromWkt(wkt)

    distance = centerLine.Length()
    print(distance)




def center_geolocation(geolocations):
    """
    Provide a relatively accurate center lat, lon returned as a list pair, given
    a list of list pairs.
    @see: https://stackoverflow.com/questions/34549767/how-to-calculate-the-center-of-the-bounding-box
    ex: in: geolocations = ((lat1,lon1), (lat2,lon2))
        out: (center_lat, center_lon)
    """
    x = 0
    y = 0
    z = 0

    for lat, lon in geolocations:
        lat = float(lat)
        lon = float(lon)
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / len(geolocations))
    y = float(y / len(geolocations))
    z = float(z / len(geolocations))

    return (atan2(y, x), atan2(z, sqrt(x * x + y * y)))


def generateGeometryFromBbox(bbox):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(2927)

    boxA = ogr.CreateGeometryFromJson("""{
            "type":"Polygon",
            "coordinates":[
                [
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ]
                ]
            ]
        }""" % (bbox[0],bbox[1], bbox[0], bbox[3], bbox[2], bbox[3], bbox[2], bbox[1], bbox[0], bbox[1]))

    
    transform = osr.CoordinateTransformation(source, target)
    boxA.Transform(transform)

    return boxA


bbox1 = [13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134]
bbox2 = [17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686]
similarArea(bbox1, bbox2)

# wkt = "POLYGON ((1162440.5712740074 672081.4332727483, 1162440.5712740074 647105.5431482664, 1195279.2416228633 647105.5431482664, 1195279.2416228633 672081.4332727483, 1162440.5712740074 672081.4332727483))"
# poly = ogr.CreateGeometryFromWkt(wkt)
# print ("Area = %d" % poly.GetArea())