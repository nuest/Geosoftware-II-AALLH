# author: Anika Graupner 
# source: https://stackoverflow.com/questions/40140412/post-xml-file-with-requests/40140503
import requests

# Set the name of the XML file.
xml_file = "Transaction-delete.xml"

headers = {'Content-Type':'text/xml'}

# Open the XML file.
with open(xml_file) as xml:
    # Give the object representing the XML file to requests.post.
    r = requests.post('http://localhost:8000/csw', data=xml)

print (r.content);






