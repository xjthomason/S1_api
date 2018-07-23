import requests, datetime, time

import csv_reader, email_google

today = datetime.date.today()

#token_file = open("D:\VM_Share\S1_api\S1_token.txt", 'r')
token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = 'APIToken ' + token_file.read()
head = {'Authorization': myToken}

#API calls
applications = requests.get("https://avx.sentinelone.net/web/api/v1.6/application-inventory?limit=7500", headers=head)
#TODO run against a list of unapproved publishers/apps
agents = requests.get("https://avx.sentinelone.net/web/api/v1.6/agents?limit=7500", headers=head)
threats = requests.get("https://avx.sentinelone.net/web/api/v1.6/threats?limit=10", headers=head)
#TODO actions on threats
#TODO reports on threats that haven't been addressed
device_pull = "https://avx.sentinelone.net/web/api/v1.6/agents/"
#TODO run query on device id based on return from threat call


def app_inventory():
	
	#create an array of application data to filter publishers and applciation names
	apps = []
	list = []
	list = applications.json()
	
	cont = True
	
	while cont:
		try:
			opt = raw_input("""Enter '1' to pull entire application inventory\nEnter '2' to pull applications for specific host\nEnter '3' for list of applications without a publisher: """)
	
			if opt == '1':
				#entire application inventory
				print("\n\nCOMING SOON!\n")
				return
			elif opt == '2':
				#applications for specified host
				agent_list = []
				call = []
				call = agents.json()
				
				#pull agents to retrieve hostnames and user info
				hostname = raw_input("Enter hostname: ")
				if hostname != None:
					for x in range(0,7500):
						try:
							agent_list.append((u'{0}, {1}, {2}'.format(call[x]['network_information']['computer_name'],
																  call[x]['id'],
																  call[x]['last_logged_in_user_name']
																  )))
						except Exception, e:
							break
				else:
					print("No hostname entered...")
					continue
					
				for x in range(0,len(agent_list)):
					if hostname == agent_list[x].rsplit(',', 2)[0]:
						#print(agent_list[x].rsplit(',', 2)[1])
						S1_id = agent_list[x].rsplit(',', 2)[1].lstrip(' ')
						#print(device_pull+S1_id+"/applications")
						agent_apps = []
						agent_apps = requests.get(device_pull+S1_id+"/applications", headers=head).json()
						#print(agent_apps[0])
						agent_apps_list = []
						try:
							for x in range(0,len(agent_apps)):
								agent_apps_list.append((u'{0}, {1}, {2}, {3}, {4}, {5}'.format(agent_apps[x]['publisher'].replace(',',' '),
																								 agent_apps[x]['name'],
																								 agent_apps[x]['signed'],
																								 agent_apps[x]['installed_date'],
																								 agent_apps[x]['version'],
																								 agent_apps[x]['size']
																								 )))
						except Exception, e:
							print e
						time.sleep(5)
						filename = csv_reader.appCSV(agent_apps_list, 2, hostname)
						#print(agent_list[x])
					else:
						continue
				
			elif opt == '3':
					#applications with no publisher
				for x in list['applications']:
					try:
						if x['publisher'] == '':
							apps.append((u'{0}, {1}, {2}, {3}, {4}, {5}'.format(x['count'],
																	'NO PUBLISHER',
																	x['name'],
																	x['signed'],
																	x['version'],
																	x['size']
																	)))
					except:
						continue
			cont = False
						
		except Exception, e:
			print e
			cont = False
		
	
	if apps == []:
		print("File with host apps created!")
	elif opt == 3:
		filename = csv_reader.appCSV(apps, 1)
		print("File with no publishers created!")
	elif opt == 1:
		filename = csv_reader.appCSV(apps, 1)
		print("File with all apps created!")
	else:
		print("No file created!")
	#print(len(list['applications']))
	
		#email a copy to an address
	e = raw_input("Email a copy to someone (Y/N)?: ")
	if e == 'Y' or e == 'y':
		address = raw_input("Enter an email address: ")
		email_google.send_email(address, filename)
	elif e == 'N' or e == 'n':
		return
	else:
		return
	

def agents_inventory():
	
	try:
		d = int(input("Enter created date range(in days), leave blank if you want all assets: "))
	except:
		d = 0
	week_ago = unicode(today - datetime.timedelta(days=d))
	
	#create array of data pulled from S1 and email to interested parties
	agents_S1 = []
	list = []
	list = agents.json()
	
	if d == 0:
		for x in range(0,7500):
			try:
				agents_S1.append((u'{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}'.format(list[x]['network_information']['computer_name'],
															list[x]['software_information']['os_name'],
															list[x]['software_information']['os_revision'],
															list[x]['network_status'],
															list[x]['network_information']['domain'],
															list[x]['group_id'],
															list[x]['network_information']['interfaces'][0]['inet'][0],
															list[x]['last_logged_in_user_name'],
															list[x]['meta_data']['created_at'].split('T')[0]
															)))
			except Exception, e:
				break
	elif d > 0:
		for x in range(0,7500):
			try:
				if list[x]['meta_data']['created_at'] >= week_ago:
					agents_S1.append((u'{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}'.format(list[x]['network_information']['computer_name'],
																list[x]['software_information']['os_name'],
																list[x]['software_information']['os_revision'],
																list[x]['network_status'],
																list[x]['network_information']['domain'],
																list[x]['group_id'],
																list[x]['network_information']['interfaces'][0]['inet'][0],
																list[x]['last_logged_in_user_name'],
																list[x]['meta_data']['created_at'].split('T')[0]
																)))
				else:
					continue
			except Exception, e:
				break
	else:
		print("Invalid...")
	
	
	print("Creating .csv for all agents in this instance created %d days ago..." % d)
	filename = csv_reader.agentCSV(agents_S1)
	
	#email a copy to an address
	e = raw_input("Email a copy to someone (Y/N)?: ")
	if e == 'Y' or e == 'y':
		address = raw_input("Enter an email address: ")
		email_google.send_email(address, filename)
	elif e == 'N' or e == 'n':
		return
	else:
		return

def threats_pull():
	
	threat_list = []
	list = []
	list = threats.json()
	
	#list of all threats
	for x in range(0,1):
		try:
			asset = requests.get(device_pull+list[x]['agent'], headers=head).json()
			print(asset['network_information']['computer_name'])
			print("\n")
			print(list[x])
		except:
			continue
	
	raw_input("Press Enter to Continue...")
	
	return
