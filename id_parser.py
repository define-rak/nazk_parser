# coding=utf-8

import requests
import json
import csv

def get_json(page):

	return json.loads(requests.get(u'https://public-api.nazk.gov.ua/v1/declaration/?page=' + str(page), verify=False).text)

csvfile_1 = open('declaration_ids_full.csv', 'wb')
writer_1 = csv.writer(csvfile_1, dialect = 'excel')

csvfile_2 = open('declaration_ids_advanced.csv', 'wb')
writer_2 = csv.writer(csvfile_2, dialect = 'excel')

flag = True

for i in xrange(1, 400):
	print i
	page = get_json(i)

	if 'error' in page.keys():
		break

	for item in page['items']:
		writer_1.writerow([item['id']])
		writer_2.writerow([item['id'], item['firstname'].encode('utf-8'), item['lastname'].encode('utf-8'), item['placeOfWork'].encode('utf-8'), item['position'].encode('utf-8'), item['linkPDF']])
		#print item['id']