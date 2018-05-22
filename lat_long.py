import csv
import requests
from urllib.parse import quote
import json

spots = []
with open('venues.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter='\t')
	for row in spamreader:
		spots.append({
			'id': row[0],
			'street': row[3],
			'city': row[4],
			'country': row[5]
			# ,'public_address': row[4]
		})		

def extractLatLng(result):
	return {
		'lat': result['geometry']['location']['lat'],
	 	'lng': result['geometry']['location']['lng']
 	}

def findRegion(components):
	for component in components:
		for type in component['types']:
			if type == 'administrative_area_level_1':
				return component['short_name']
	return ''

def findPostalCode(components):
	for component in components:
		for type in component['types']:
			if type == 'postal_code':
				return component['short_name']
	return ''

def extractPostalCodeAndRegion(result):
	return findPostalCode(result['address_components']) + '___' + findRegion(result['address_components'])
	# return {
	# 	'postalCode': findPostalCode(result['address_components']),
	#  	'region': findRegion(result['address_components'])
 # 	}

def getResult(address):
	# print('getting ' + address)
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + quote(address)
	resp = requests.get(url)
	data = json.loads(resp.text)
	# print(data)
	if len(data['results']) > 0:
		return data['results'][0]

	return None

for spot in spots:
	# latLng = getLatLng(spot['public_address'])
	# if not latLng:
	result = getResult(spot['street'] + ',' + spot['city'] + ',' + spot['country'])
	# print(result)

	if not result:
		print('no dice' + spot['id'])
		# spot['lat'] = None
	else:
		# spot['lat'] = latLng['lat']
		# spot['lng'] = latLng['lng']
		print(extractPostalCodeAndRegion(result))

# with open('out.csv', 'w') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for spot in spots:
#     	if spot['lat']:
#     		spamwriter.writerow([spot['id'], spot['lat'], spot['lng']])





