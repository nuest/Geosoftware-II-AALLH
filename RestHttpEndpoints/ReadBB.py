'''
@author: Aysel Tandik, Anika Graupner
'''

import os, sys

file_path = '../CLI Tools'
sys.path.append(file_path)

import getBoundingBox as bbox

# Data to serve with our API
BB = {
    "Ausgabe": {
        "BoundingBox": bbox.getBoundingBox('shapeTest.shp', 'C:\Users\celeb\Desktop\Uni\Geoinformatik_5Semester\Geosoft2\Gruppenarbeit\Geosoftware-II-AALLH\testdataF')
    }
}


# Create a handler for our read (GET) BoundingBox
def read():
    """
    This function responds to a request for /api/BB
    with the complete lists of Boundingboxes

    :return:        sorted list of bb
    """
    # Create the list of Boundingboxes from our data
    return [BB[key] for key in sorted(BB.keys())]