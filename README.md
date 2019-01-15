# Geosoftware II Project of the Group "A²HL²", WWU <!-- omit in toc -->

[Aysel Tandik](https://github.com/atlanta11950), [Anika Graupner](https://github.com/Anika2), [Henry Fock](https://github.com/HenFo), [Lia Kirsch](https://github.com/cherry13579), [Lukas Jahnich](https://github.com/lukasjah)

**Project order:** This project will close the gap between geospatial data formats and repositories respectively geospatial metadata catalogues and similarity measurements. Project groups will extend an existing Free and Open Source Software (FOSS) project with the functionality to retrieve and view similar records. This comprises both the API and UI, namely providing an HTTP endpoint to retrieve an ordered list of records based on a provided record and displaying/linking similar records in a detail view of a record respectively.

## Table of Contents <!-- omit in toc -->
- [Instructions to start pycsw](#instructions-to-start-pycsw)
  - [Test our additional features:](#test-our-additional-features)
- [Using the CLI-Tools](#using-the-cli-tools)
    - [Option 1](#option-1)
    - [Option 2](#option-2)
  - [Examples](#examples)

## Instructions to start pycsw

- install docker: [https://docs.docker.com/install/](https://docs.docker.com/install/)
- clone our repository to your computer
- make sure, docker is running
- open Windows PowerShell (or Docker Toolbox) on your computer and navigate into the pycsw folder: 

```bat
cd .../pycsw
```

- add the following in PowerShell (just completely copy and paste)

```docker
docker run --name pycsw-dev --volume ${PWD}/pycsw:/usr/lib/python3.5/site-packages/pycsw --volume ${PWD}/docs:/home/pycsw/docs --volume ${PWD}/VERSION.txt:/home/pycsw/VERSION.txt --volume ${PWD}/LICENSE.txt:/home/pycsw/LICENSE.txt --volume ${PWD}/COMMITTERS.txt:/home/pycsw/COMMITTERS.txt --volume ${PWD}/CONTRIBUTING.rst:/home/pycsw/CONTRIBUTING.rst --volume ${PWD}/pycsw/plugins:/home/pycsw/pycsw/plugins --volume ${PWD}/our.cfg:/etc/pycsw/pycsw.cfg --volume ${PWD}/db-data:/db-data/ --publish 8000:8000 geopython/pycsw --reload
```

- sometimes you could get an input/output error, if so, simply restart Docker and try again
- go to localhost:8000 in your browser, when you see a xml tree, everething went fine
- to remove the container, add the following in powerShell (necessary if the container should be restarted with the above command):

```shell
docker rm -f pycsw-dev
```

### Test our additional features:

- we added two own functions for the api in pycsw/pycsw/ogc/csw/csw2.py (for code review):
	- `def getsimilarrecords(self)`
	- `def getsimilaritybbox(self, raw=False)`

In your Browser, test our new requests by adding the following endpoints:

- http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=24
- http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=24,6
- http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=24,6&outputformat=application/xml
- http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarityBBox&idone=24&idtwo=4
- http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarityBBox&idone=24&idtwo=4&outputformat=application/xml
  
## Using the CLI-Tools

#### Option 1

- clone Repository
- install Python and pip
- navigate in Folder `$ cd Geosoftware-II-AALLH`
- run `$ pip install -r requirements.txt`
- if [GDAL](https://www.gdal.org/) won't install with pip, try a different Method
  - in my case (Windows) it worked using gdal from [this site](http://www.xavierdupre.fr/enseignement/setup/index_modules_list.html)
  - `$ pip install <path to .whl>`
- download ogr2ogr from [this](http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/ogr2ogr.py) site and add the python file to `python/Lib/site-packages`

 Open the commandline and navigate to the CLI Tools folder in our project folder `$ cd CLI Tools` and type `$ python masterExtract.py --help` to show the options you can chose from.

#### Option 2
If pip is installed:
- `$ pip install geodataExtent`
- If GDAL won't install, try method above
- download ogr2ogr as described above

type `$ extract-extent --help`

```bat
Options:
  --path TEXT  Path to Folder containing Geofiles
  -c, --clear  Clear screen before showing results
  -t, --time   execute time extraction for one file
  -s, --space  execute boundingbox extraction for one file
  -h, --hull   execute convex-hull extraction for one file
  --help       Show this message and exit.
```
Those are **only** options, you do not have to use them. However, if you do not choos any of the execution flags `(-t / -s / -h)`, the folderextraction will be triggered and gives you the spatial and temporal extent of each of your Geofiles within the chosen folder in addition to the full spatial and temporal extent of the folder.

You are not limeted to choose only one option but all of them at once except for `--help`.

If you do not use `--path`, the path will be prompted. That means it is a shortcut only.

### Examples

```
$ python masterExtract.py -t -s -h  'OR' extract-extent -t -s -h
Pleas enter path to Folder: <path>
Pleas enter filename: <filename>

Timeextent:
['1935/01/01 00:00:00 GMT+0', '2014/01/01 00:00:00 GMT+0', 365.253164556962]


Spatialextent:
[-179.5, -89.5, 179.5, 89.5]


Spatialextent as Convex Hull:
[(-179.5, -89.5), (-179.5, 89.5), (179.5, 89.5), (179.5, -89.5)]
```

The Timeextent starts with the beginning and ends with the end date as ISO8601 standard. the last number is the average intervall in which measurements have been taken.

The spatial extent is shown as a boundingbox. `[minX/minLong, minY/minLat, maxX/maxLong, maxY/maxLat]`

For more percission the `-h / --hull` flag gives you the spatial exnent as a convex hull. That means from all the points of a dataset the outer most points are beeing calculated and returned in correct order.

#### Folderextraction <!-- omit in toc -->

If you want to extract your hole folder, the `-c / --clear` flag is recommended because a long list of processing outputs is generated before the final output appears.
```
$ python masterExtract.py -c --path "<folder path>"
$ extract-extent -c --path "<folder path>"
```


