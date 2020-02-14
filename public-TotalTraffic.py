import requests
import json
import csv
import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)

def total_traffic(domain):
	api_key = '' #insert you key
	# Start date or month (format: YYYY-MM-DD or YYYY-MM)
	start_date = '2019-01'
	# End date or month (format: YYYY-MM-DD or YYYY-MM)
	end_date = '2020-01'
	# Country filter, as a 2-letter ISO country code, or "world" for worldwide.
	# To see the country filters you have access to, please refer to the Check Capabilities endpoint.
	country = 'world'
	# Set the granularity for the returned values. Can be 'daily', 'weekly' or 'monthly'.
	granularity = 'monthly'

	url = "https://api.similarweb.com/v1/website/"+domain+"/total-traffic-and-engagement/visits?api_key="+api_key+"&start_date="+start_date+"&end_date="+end_date+"&country="+country+"&granularity="+granularity+"&main_domain_only=false&format=json"

	payload = {}
	headers= {}

	response = requests.request("GET", url, headers=headers, data = payload)
	return response.json()

DOMAINS = []
with open('domains.txt', 'r') as domains_file:
	for domfile in domains_file:
		domfile = domfile.replace('\n','')

		DOMAINS.append(domfile)

with open('employee_file.csv', mode='w') as employee_file:
	employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# write header with the correct date range
	visits = total_traffic('geeksforgeeks.org')['visits']
	row_data = []
	row_data.append('domains')
	for v in visits:
		row_data.append(v['date'])
	employee_writer.writerow(row_data)

	# write data
	domains_list_len = len(DOMAINS)
	counter = 0
	for domain in DOMAINS:
		counter +=1

		json_data = total_traffic(domain)
		status = json_data['meta']['status']

		
		
		if status == 'Success':
			visits = json_data['visits']

			row_data = []
			row_data.append(domain)

			for v in visits:
				row_data.append(v['visits'])

			employee_writer.writerow(row_data)
			print('[',counter,' / ',domains_list_len,'] # ', Back.GREEN+status,' # ', domain) #counter
		else:
			row_data = []
			row_data.append(domain)
			row_data.append(status)
			employee_writer.writerow(row_data)
			print('[',counter,' / ',domains_list_len,'] # ', Back.RED+status,' # ', domain) #counter
