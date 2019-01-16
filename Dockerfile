FROM geopython/pycsw

USER root

RUN apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/main/ \
    --allow-untrusted \
    libcrypto1.1 \
    && apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
    --allow-untrusted \
    gdal \
    gdal-dev

RUN pip3 install gdal

USER pycsw

# BUILD:
# docker build --tag aallh-pycsw .
#
# RUN:
# daniel@gin-nuest:~/Documents/2018_Geosoftware-II/code/Geosoftware-II-AALLH/$ docker run --rm -it --entrypoint /bin/sh aallh-pycsw
#
#~ $ gdalinfo --version
#GDAL 2.4.0, released 2018/12/14
#~ $ python3
#Python 3.5.2 (default, Dec 20 2016, 17:58:45)
#[GCC 5.3.0] on linux
#Type "help", "copyright", "credits" or "license" for more information.
#>>> import gdal
#>>> gdal.gdalconst
#<module 'osgeo.gdalconst' from '/usr/lib/python3.5/site-packages/osgeo/gdalconst.py'>
#>>> gdal.VersionInfo()
#'2040000'
#