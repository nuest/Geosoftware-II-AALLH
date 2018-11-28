import os
import sys

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr

def spatialOverlap(bboxA, bboxB):
    allPoints = 15
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

    reachedPoints = intersectArea*15/largerArea

    print(reachedPoints)
    return reachedPoints
    

def generateGeometryFromBbox(bbox):
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
        }""" % (bbox[0],bbox[1], bbox[0], bbox[3], bbox[2], bbox[3], bbox[1], bbox[2], bbox[0], bbox[1]))
    return boxA

    

# bbox1 = [26.982421875, 45.06867131826392, 27.113914489746094, 45.16945179362033]
# bbox2 = [26.982421875, 45.06867131826392, 27.113914489746094, 45.16945179362033]
# overlap(bbox1, bbox2)