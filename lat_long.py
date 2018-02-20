import csv
import requests
from urllib.parse import quote
import json

spots = []
with open('query_result.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		spots.append({
			'id': row[0],
			'street': row[1],
			'city': row[2],
			'country': row[3],
			'public_address': row[4]
		})		

def getLatLng(address):
	print('getting ' + address)
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + quote(spot['public_address'])
	resp = requests.get(url)
	data = json.loads(resp.text)
	if len(data['results']) > 0:
		return {
			'lat': data['results'][0]['geometry']['location']['lat'],
		 	'lng': data['results'][0]['geometry']['location']['lng']
	 	}
	
	return None

for spot in spots:
	latLng = getLatLng(spot['public_address'])
	if not latLng:
		latLng = getLatLng(spot['street'] + ',' + spot['city'] + ',' + spot['country'])

	if not latLng:
		print('no dice' + spot['id'])
		spot['lat'] = None
	else:
		spot['lat'] = latLng['lat']
		spot['lng'] = latLng['lng']

with open('out.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for spot in spots:
    	if spot['lat']:
    		spamwriter.writerow([spot['id'], spot['lat'], spot['lng']])





