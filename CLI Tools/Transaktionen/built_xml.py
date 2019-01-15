# xml for the update by record property transaction
# @author: Anika Graupner 

import time
import requests

updatexml = """<?xml version="1.0" encoding="UTF-8"?>
<csw:Transaction xmlns:ogc="http://www.opengis.net/ogc" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ows="http://www.opengis.net/ows" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd" service="CSW" version="2.0.2">
  <csw:Update>
	<csw:RecordProperty>
      <csw:Name>apiso:Modified</csw:Name>
      <csw:Value>%(actual_date)s</csw:Value>
    </csw:RecordProperty>
    <csw:RecordProperty>
      <csw:Name>apiso:BoundingBox</csw:Name>
      <csw:Value>%(bbox)s</csw:Value>
    </csw:RecordProperty>
	<csw:RecordProperty>
      <csw:Name>apiso:TempExtent_begin</csw:Name>
      <csw:Value>%(date_begin)s</csw:Value>
    </csw:RecordProperty>
	<csw:RecordProperty>
      <csw:Name>apiso:TempExtent_end</csw:Name>
      <csw:Value>%(date_end)s</csw:Value>
    </csw:RecordProperty>
	<csw:RecordProperty>
      <csw:Name>apiso:Format</csw:Name>
      <csw:Value>%(file_format)s</csw:Value>
    </csw:RecordProperty>
    <csw:Constraint version="1.1.0">
      <ogc:Filter>
        <ogc:PropertyIsEqualTo>
          <ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
          <ogc:Literal>%(id)s</ogc:Literal>
        </ogc:PropertyIsEqualTo>
      </ogc:Filter>
    </csw:Constraint>
  </csw:Update>
</csw:Transaction>
"""

#print(updatexml)

date = time.strftime("%Y-%m-%d")

#print(date)

boundingbox = 'POLYGON((-180.00 -90.00, -180.00 90.00, 180.00 90.00, 180.00 -90.00, -180.00 -90.00))' #((minx, miny, minx, maxy, maxx, maxy, maxx, miny, minx, miny))'
datebegin = '2019-01-04'
dateend = '2019-01-08'
fileformat = 'testformat'
identifier = 25 #wird in die Kommandozeile mit eingegeben 
data = {'actual_date':date , 'bbox':boundingbox, 'date_begin':datebegin, 'date_end':dateend, 'file_format':fileformat, 'id':identifier}
xml = updatexml%data
print(xml)

# send xml to server 
r = requests.post('http://localhost:8000/csw', data=xml)

print (r.content)





