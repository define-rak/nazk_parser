# coding=utf-8

import requests
import json
from collections import OrderedDict

def get_json(id_):
	return json.loads(requests.get(u'https://public-api.nazk.gov.ua/v1/declaration/' + id_, verify=False).text)


def str_to_float(str):
	return float(str.replace(',', '.'))


f = open('declaration_ids.txt', 'r')

declarations = []

for line in f.readlines():
	if line.strip() == '':
		break

	declaration = get_json(line.strip())

	processed_declaration = OrderedDict()

	processed_declaration[u'id'] = declaration[u'id']
	processed_declaration[u'created_date'] = declaration[u'created_date']
	processed_declaration[u'lastmodified_date'] = declaration[u'lastmodified_date']
	processed_declaration[u'declarationType'] = declaration[u'data'][u'step_0'][u'declarationType']
	processed_declaration[u'declarationYear1'] = declaration[u'data'][u'step_0'][u'declarationYear1']
	processed_declaration[u'lastname'] = declaration[u'data'][u'step_1'][u'lastname'].encode('utf-8')
	processed_declaration[u'firstname'] = declaration[u'data'][u'step_1'][u'firstname'].encode('utf-8')
	processed_declaration[u'middlename'] = declaration[u'data'][u'step_1'][u'middlename'].encode('utf-8')
	processed_declaration[u'workPost'] = declaration[u'data'][u'step_1'][u'workPost'].encode('utf-8')
	processed_declaration[u'workPlace'] = declaration[u'data'][u'step_1'][u'workPlace'].encode('utf-8')
	processed_declaration[u'responsiblePosition'] = declaration[u'data'][u'step_1'][u'responsiblePosition'].encode('utf-8')
	processed_declaration[u'postCategory'] = declaration[u'data'][u'step_1'][u'postCategory'].encode('utf-8')
	processed_declaration[u'corruptionAffected'] = declaration[u'data'][u'step_1'][u'corruptionAffected'].encode('utf-8')

	processed_declaration[u'land'] = OrderedDict()
	processed_declaration[u'land']['no_info'] = 0.0
	processed_declaration[u'land']['until_2014'] = 0.0
	processed_declaration[u'land']['in_2014'] = 0.0
	processed_declaration[u'land']['in_2015'] = 0.0
	processed_declaration[u'land']['all'] = 0.0

	processed_declaration[u'houses'] = OrderedDict()
	processed_declaration[u'houses']['no_info'] = 0.0
	processed_declaration[u'houses']['until_2014'] = 0.0
	processed_declaration[u'houses']['in_2014'] = 0.0
	processed_declaration[u'houses']['in_2015'] = 0.0
	processed_declaration[u'houses']['all'] = 0.0

	processed_declaration[u'appartments'] = OrderedDict()
	processed_declaration[u'appartments']['no_info'] = 0.0
	processed_declaration[u'appartments']['until_2014'] = 0.0
	processed_declaration[u'appartments']['in_2014'] = 0.0
	processed_declaration[u'appartments']['in_2015'] = 0.0
	processed_declaration[u'appartments']['all'] = 0.0

	processed_declaration[u'other_land'] = OrderedDict()
	processed_declaration[u'other_land']['no_info'] = 0.0
	processed_declaration[u'other_land']['until_2014'] = 0.0
	processed_declaration[u'other_land']['in_2014'] = 0.0
	processed_declaration[u'other_land']['in_2015'] = 0.0
	processed_declaration[u'other_land']['all'] = 0.0

	if isinstance(declaration[u'data'][u'step_3'], list):
		declaration[u'data'][u'step_3'] = {}

	for property in declaration[u'data'][u'step_3'].items():

		percentage = 0.0

		for owner in property[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		date = ''

		if property[1][u'owningDate'] == '':
			date = 'no_info'
		elif int(property[1][u'owningDate'].split('.')[2]) < 2014:
			date = 'until_2014'
		elif int(property[1][u'owningDate'].split('.')[2]) == 2014:
			date = 'in_2014'
		elif int(property[1][u'owningDate'].split('.')[2]) == 2015:
			date = 'in_2015'


		if property[1][u'objectType'] == u'Земельна ділянка':
			processed_declaration[u'land'][date] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
			processed_declaration[u'land']['all'] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
		elif property[1][u'objectType'] == u'Житловий будинок':
			processed_declaration[u'houses'][date] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
			processed_declaration[u'houses']['all'] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
		elif property[1][u'objectType'] == u'Квартира':
			processed_declaration[u'appartments'][date] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
			processed_declaration[u'appartments']['all'] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
		else:
			processed_declaration[u'other_land'][date] += str_to_float(property[1][u'totalArea']) * percentage / 100.0
			processed_declaration[u'other_land']['all'] += str_to_float(property[1][u'totalArea']) * percentage / 100.0


	processed_declaration[u'personalty'] = OrderedDict()
	processed_declaration[u'personalty']['no_info'] = 0.0
	processed_declaration[u'personalty']['until_2014'] = 0.0
	processed_declaration[u'personalty']['in_2014'] = 0.0
	processed_declaration[u'personalty']['in_2015'] = 0.0
	processed_declaration[u'personalty']['all'] = 0.0

	if isinstance(declaration[u'data'][u'step_5'], list):
		declaration[u'data'][u'step_5'] = {}

	for personalty in declaration[u'data'][u'step_5'].items():

		percentage = 0.0

		for owner in personalty[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		date = ''

		if personalty[1][u'dateUse'] == '':
			date = 'no_info'
		elif int(personalty[1][u'dateUse'].split('.')[2]) < 2014:
			date = 'until_2014'
		elif int(personalty[1][u'dateUse'].split('.')[2]) == 2014:
			date = 'in_2014'
		elif int(personalty[1][u'dateUse'].split('.')[2]) == 2015:
			date = 'in_2015'


		cost = 0.0

		if personalty[1][u'costDateUse'] == '':
			cost = 120000.0
		elif str_to_float(personalty[1][u'costDateUse']) < 120000.0:
			cost = 120000.0
		else:
			cost = str_to_float(personalty[1][u'costDateUse'])
		
		processed_declaration[u'personalty'][date] += cost * percentage / 100.0
		processed_declaration[u'personalty']['all'] += cost * percentage / 100.0


	processed_declaration[u'transport'] = OrderedDict()
	processed_declaration[u'transport']['no_info'] = 0.0
	processed_declaration[u'transport']['until_2014'] = 0.0
	processed_declaration[u'transport']['in_2014'] = 0.0
	processed_declaration[u'transport']['in_2015'] = 0.0
	processed_declaration[u'transport']['all'] = 0.0
	processed_declaration[u'transport_amount_cars'] = 0

	if isinstance(declaration[u'data'][u'step_6'], list):
		declaration[u'data'][u'step_6'] = {}

	for transport in declaration[u'data'][u'step_6'].items():

		percentage = 0.0

		for owner in transport[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		date = ''

		if transport[1][u'owningDate'] == '':
			date = 'no_info'
		elif int(transport[1][u'owningDate'].split('.')[2]) < 2014:
			date = 'until_2014'
		elif int(transport[1][u'owningDate'].split('.')[2]) == 2014:
			date = 'in_2014'
		elif int(transport[1][u'owningDate'].split('.')[2]) == 2015:
			date = 'in_2015'


		cost = 0.0

		if transport[1][u'costDate'] == '':
			cost = 120000.0
		else:
			cost = str_to_float(transport[1][u'costDate'])
		
		processed_declaration[u'transport'][date] += cost * percentage / 100.0
		processed_declaration[u'transport']['all'] += cost * percentage / 100.0

		if transport[1][u'objectType'] == u'Автомобіль легковий':
			processed_declaration[u'transport_amount_cars'] += 1


	processed_declaration[u'securities'] = OrderedDict()
	processed_declaration[u'securities']['no_info'] = 0.0
	processed_declaration[u'securities']['until_2014'] = 0.0
	processed_declaration[u'securities']['in_2014'] = 0.0
	processed_declaration[u'securities']['in_2015'] = 0.0
	processed_declaration[u'securities']['all'] = 0.0

	if isinstance(declaration[u'data'][u'step_7'], list):
		declaration[u'data'][u'step_7'] = {}

	for securities in declaration[u'data'][u'step_7'].items():

		percentage = 0.0

		for owner in securities[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		date = ''

		if securities[1][u'owningDate'] == '':
			date = 'no_info'
		elif int(securities[1][u'owningDate'].split('.')[2]) < 2014:
			date = 'until_2014'
		elif int(securities[1][u'owningDate'].split('.')[2]) == 2014:
			date = 'in_2014'
		elif int(securities[1][u'owningDate'].split('.')[2]) == 2015:
			date = 'in_2015'


		cost = 0.0

		if securities[1][u'cost'] == '':
			cost = 0
		else:
			cost = str_to_float(securities[1][u'cost'])
		
		processed_declaration[u'securities'][date] += cost * percentage / 100.0
		processed_declaration[u'securities']['all'] += cost * percentage / 100.0


	processed_declaration[u'corporate'] = 0.0

	if isinstance(declaration[u'data'][u'step_8'], list):
		declaration[u'data'][u'step_8'] = {}

	for corporate in declaration[u'data'][u'step_8'].items():

		percentage = 0.0

		for owner in corporate[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0

		cost = 0.0

		if corporate[1][u'cost'] == '':
			cost = 0
		else:
			cost = str_to_float(corporate[1][u'cost'])
		
		processed_declaration[u'corporate'] += cost * percentage / 100.0


	if isinstance(declaration[u'data'][u'step_9'], list):
		declaration[u'data'][u'step_9'] = {}
	processed_declaration[u'corporate_amount'] = len(declaration[u'data'][u'step_9'].items()) / 2


	processed_declaration[u'income'] = OrderedDict()
	processed_declaration[u'income']['salary'] = 0.0
	processed_declaration[u'income']['persents'] = 0.0
	processed_declaration[u'income']['other'] = 0.0
	processed_declaration[u'income']['all'] = 0.0

	if isinstance(declaration[u'data'][u'step_11'], list):
		declaration[u'data'][u'step_11'] = {}

	for income in declaration[u'data'][u'step_11'].items():

		percentage = 0.0

		for owner in income[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		income_type = ''

		if income[1][u'objectType'].split(' ')[:2] == [u'Заробітна', u'плата']:
			income_type = 'salary'
		elif income[1][u'objectType'].split(' ')[0] == u'Подарунок':
			income_type = 'persents'
		else:
			income_type = 'other'


		cost = 0.0

		if income[1][u'sizeIncome'] == '':
			cost = 0
		else:
			cost = str_to_float(income[1][u'sizeIncome'])
		
		processed_declaration[u'income'][income_type] += cost * percentage / 100.0
		processed_declaration[u'income'][u'all'] += cost * percentage / 100.0


	currencies_list = ['UAH', 'USD', 'EUR', 'RUB', 'GBP']
	currencies = {'UAH': 1.0, 'USD': 25.0, 'EUR': 28.0, 'RUB': 0.4, 'GBP': 31.0}

	processed_declaration[u'money'] = OrderedDict()
	processed_declaration[u'money']['bank'] = 0.0
	processed_declaration[u'money']['cash'] = 0.0
	processed_declaration[u'money']['other'] = 0.0
	processed_declaration[u'money']['all'] = 0.0

	if isinstance(declaration[u'data'][u'step_12'], list):
		declaration[u'data'][u'step_12'] = {}


	for money in declaration[u'data'][u'step_12'].items():

		percentage = 0.0

		for owner in money[1][u'rights'].items():
			if owner[1][u'ownershipType'] != u'Оренда':
				if owner[1][u'percent-ownership'] == '':
					percentage += 100.0
				else:
					percentage += str_to_float(owner[1][u'percent-ownership'])

		if percentage > 100.0:
			percentage = 100.0


		income_type = ''

		if money[1][u'objectType'] == u'Кошти, розміщені на банківських рахунках':
			money_type = 'bank'
		elif money[1][u'objectType'] == u'Готівкові кошти':
			money_type = 'cash'
		else:
			money_type = 'other'


		cost = 0.0

		if money[1][u'sizeAssets'] == '':
			cost = 0
		else:
			cost = str_to_float(money[1][u'sizeAssets'])

		currency = 0
		if money[1][u'assetsCurrency'] in currencies_list:
			currency = currencies[money[1][u'assetsCurrency']]
		else:
			currency = 1.0
		
		processed_declaration[u'money'][money_type] += cost * currency * percentage / 100.0
		processed_declaration[u'money'][u'all'] += cost * currency * percentage / 100.0

	declarations.append(processed_declaration)
	# print json.dumps(processed_declaration, indent=4)


title = []

for key_1 in declarations[0].keys():
	if isinstance(processed_declaration[key_1], dict):
		for key_2 in processed_declaration[key_1].keys():
			title.append(key_1 + '/' + key_2)
	else:
		title.append(key_1)

import csv

csvfile = open('declarations.csv', 'wb')
writer = csv.writer(csvfile, dialect = 'excel')
writer.writerow(title)



for declaration in declarations:
	row = []
	for key_1 in declaration.keys():
		if isinstance(declaration[key_1], dict):
			for key_2 in declaration[key_1].keys():
				row.append(declaration[key_1][key_2])
		else:
			row.append(declaration[key_1])

	writer.writerow(row)

csvfile.close()










