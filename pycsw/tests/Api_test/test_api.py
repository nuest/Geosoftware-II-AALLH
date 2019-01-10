# author: Aysel Tandik
# Testing the API
# 19.12.2018

import unittest
import datetime
import requests
from requests import get

class TestApi():
    test_url = 'http://192.168.99.100:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=24'
    test_urlBB = 'http://192.168.99.100:8000/?service=CSW&version=2.0.2&request=GetSimilarityBBox&idone=2&idtwo=24'
    test_urlSimi = 'http://192.168.99.100:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=24&similar=1'
    test_failedUrl = 'http://192.168.99.100:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id='
    
    # Test--> if the schema has a json structure
    def get_response(self, test_url=test_url, format='json'):
        if format == 'json':
            response = get(test_url)
            response = get(self.test_urlBB)

        return response.json

    def test_json_response(self):
        print('Get json Response')
        assert self.get_response(format='json') != ''

    # Test--> if the statuscode is 200
    def test_status_response(self, test_url = test_url):
        print('Get Statuscode')
        response = requests.get(self.test_url)
        assert response.status_code == 200

        response = requests.get(self.test_urlBB)
        assert response.status_code == 200

    # Test--> The Timeresponse from the Url's doesnt take longer then 200ms
    def test_time_response_Similarrecords(self):
        r = requests.get(self.test_url, timeout=6)
        r.raise_for_status()
        responseTime = str(round(r.elapsed.total_seconds(),2))
        assert responseTime < '200'
    
    def test_time_response_SimilarBBox(self):
       r = requests.get(self.test_urlBB, timeout=6)
       r.raise_for_status()
       responseTime = str(round(r.elapsed.total_seconds(),2))
       assert responseTime < '200'

    def test_failedUrl(self):
        
	   
	   
	   
	   #umgebungsvariable erstellen für die IP
	   #performance test pytesting - wegen 200ms 
	   #similar n testen - negative zahlen, buchstaben
	   #
	   