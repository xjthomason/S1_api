import csv, datetime

import groups

today = datetime.date.today()

def appCSV(list, mode, hostname=None):
	
	if mode == 1:
		with open('Sentinel_One_Apps_%s.csv' % today, 'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = ['# installed','Publisher','Name',
															'Signed','Version','Size'])
			writer.writeheader()
			for i in list:
				count = i.split(',')[0]
				publisher = i.split(',')[1]
				name = i.split(',')[2]
				signed = i.split(',')[3]
				version = i.split(',')[4]
				size = i.split(',')[5]
				
				writer.writerow({'# installed': count.encode('utf-8'), 
								 'Publisher': publisher.encode('utf-8'), 
								 'Name': name.encode('utf-8'), 
								 'Signed': signed.encode('utf-8'),
								 'Version': version.encode('utf-8'),
								 'Size': size.encode('utf-8')})
		filename = 'Sentinel_One_Apps_%s.csv' % today
		return filename
	elif mode == 2:
		with open('Sentinel_One_Apps_%s.csv' % hostname, 'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = ['Publisher','Name','Signed',
															'Installed Date','Version','Size'])
			writer.writeheader()
			for i in list:
				publisher = i.split(',')[0]
				name = i.split(',')[1]
				signed = i.split(',')[2]
				installed_date = i.split(',')[3]
				version = i.split(',')[4]
				size = i.split(',')[5]
				
				writer.writerow({'Publisher': publisher.encode('utf-8'), 
								 'Name': name.encode('utf-8'), 
								 'Signed': signed.encode('utf-8'),
								 'Installed Date': installed_date.encode('utf-8'),
								 'Version': version.encode('utf-8'),
								 'Size': size.encode('utf-8')})
				
		filename = 'Sentinel_One_Apps_%s.csv' % hostname
		return filename
	else:
		print("Invalid Mode...")
	
	return
	
def agentCSV(list):
	
	with open('Sentinel_One_Update_%s.csv' % today, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = ['Asset Name', 'OS Name', 'OS Version', 'Network Status', 'Domain', 
													   'Group', 'IP Address', 'Last User', 'Created Date'])
		writer.writeheader()
		for i in list:
			computer_name = i.split(',')[0]
			os_name = i.split(',')[1]
			os_version = i.split(',')[2]
			network_status = i.split(',')[3]
			group_id = i.split(',')[5].lstrip(' ')
			domain = i.split(',')[4].lstrip(' ')
			IP = i.split(',')[6]
			last_user = i.split(',')[7]
			created = i.split(',')[8]
			group = groups.S1_group(group_id)
			
			if group == 'Default group':
				writer.writerow({'Asset Name': computer_name, 
							 'OS Name': os_name,
							 'OS Version': os_version,
							 'Network Status': network_status,
							 'Group': group,
							 'Domain': domain, 
							 'IP Address': IP,
							 'Last User': last_user, 
							 'Created Date': created})
			
	
	filename = 'Sentinel_One_Update_%s.csv' % today
	return filename

def threatCSV(list):
	
	with open('Sentinel_One_Threats_Suspicious.csv', 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = ['Name', 'Threat ID', 'Status','Last User','Threat Name', 
													   'Hash', 'Created'
													  ])
		writer.writeheader()
		for i in list:
			computer_name = i.split(',')[0]
			threat_id = i.split(',')[1]
			status = i.split(',')[2]
			username = i.split(',')[3]
			threat_name = i.split(',')[4]
			threat_hash = i.split(',')[5]
			created = i.split(',')[6]
			
			writer.writerow({'Name': computer_name.encode('utf-8'),
							 'Threat ID': threat_id.encode('utf-8'),
							 'Status': status.encode('utf-8'),
							 'Last User': username.encode('utf-8'),
							 'Threat Name': threat_name.encode('utf-8'),
							 'Hash': threat_hash.encode('utf-8'),
							 'Created': created.encode('utf-8')})
