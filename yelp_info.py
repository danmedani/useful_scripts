import csv
import requests
from urllib.parse import quote
import json
import os

auth = 'Bearer ' + os.environ['YELP_PUBLICAPI_TOKEN']

def getYelpInfo(yelp_bus_id):
	if len(yelp_bus_id) == 0:
		return None
	url = 'https://api.yelp.com/v3/businesses/' + quote(yelp_bus_id)
	headers = {
		'Authorization': auth,
		'Content-Type': 'application/json'
	}
	resp = requests.get(url, headers=headers)
	data = json.loads(resp.text)
	if data and 'error' not in data:
		return data['location']['zip_code'] + '___' + data['location']['state']

	return None

print(getYelpInfo('ZyfOt84HvbX4FsqGLOZqCw'))
print(getYelpInfo('ZyfOt84HvbX4FsqGLOZqCd'))
