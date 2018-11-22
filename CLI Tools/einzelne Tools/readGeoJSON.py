'''
Created on 29.10.2018

@author: hfock
'''

import os, sys

file_path = '../Python_Modules'
sys.path.append(file_path)

import click
import json
import pygeoj

@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name without extension")
#@click.option('--type', prompt="File type", help="file type: no abbreviation but the type in a word (i.e. shapefile, json/geojson")

def getBoundingBox(name, path):
    filepath = "%s\%s.json" % (path, name)
    try:
        myGeojson = pygeoj.load(filepath=filepath)
        click.echo(myGeojson.bbox)
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
    except:
        click.echo("File not Found")

def isFeatureCollection(geojson):
    return True if geojson.get("type") == "FeatureCollection" else False

if __name__ == '__main__':
    getBoundingBox()
