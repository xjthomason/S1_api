import requests, datetime, time, json

import csv_reader, smartsheet_api

today = datetime.date.today()

#token_file = open("S1_token.txt", 'r')
token_file = open("D:\VM_Share\S1_api\S1_token.txt", 'r')
#token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = 'APIToken ' + token_file.read()
head = {'Authorization': myToken}

#API calls
applications = requests.get("https://avx.sentinelone.net/web/api/v1.6/application-inventory?limit=7500", headers=head)
#TODO run against a list of unapproved publishers/apps
agents = requests.get("https://avx.sentinelone.net/web/api/v1.6/agents?limit=7500", headers=head)
threats = requests.get("https://avx.sentinelone.net/web/api/v1.6/threats?limit=5000", headers=head)
#TODO actions on threats
#TODO reports on threats that haven't been addressed
device_pull = "https://avx.sentinelone.net/web/api/v1.6/agents/"
#TODO run query on device id based on return from threat call
	

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
	
	for x in range(0,7500):
		try:
			if list[x]['meta_data']['created_at'] >= week_ago:
				agents_S1.append((u'{0}, {1}, {2}'.format(list[x]['network_information']['computer_name'],
													 list[x]['network_information']['domain'],
													 list[x]['group_id']
													)))
			else:
				continue
		except Exception, e:
			break
	
	#for at in agents_S1:
		#group_id = at.split(',')[1]
		
	#print("Creating .csv for all agents in this instance created %d days ago..." % d)
	#filename = ''#csv_reader.agentCSV(agents_S1)
	
	##email a copy to an address
	#e = raw_input("Email a copy to someone (Y/N)?: ")
	#if e == 'Y' or e == 'y':
		#address = raw_input("Enter an email address: ")
		##email_google.send_email(address, filename)
	#elif e == 'N' or e == 'n':
		#print('Okay...')
	#else:
		#return
	print(len(agents_S1))
	sm = raw_input("Update Smartsheet (Y/N)?: ")
	if sm == 'Y' or sm == 'y':
		smartsheet_api.update(agents_S1)
	elif sm == 'N' or sm == 'n':
		print('Okay...')
	else:
		return
	time.sleep(10)
