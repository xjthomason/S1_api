import smartsheet, requests, groups, json, datetime

today = datetime.date.today()
week_ago = unicode(today - datetime.timedelta(days=7))

# Tokens
#token_file = open("Smart_token.txt", 'r')
token_file = open("D:\VM_Share\S1_api\Smart_token.txt", 'r')
#token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = token_file.read()#'Bearer ' + token_file.read()
head = {'Authorization': myToken}

update_request_message = "Hello,\n\nPlease update the sheet for the ongoing Sentinel One project.\n\nThanks,\n\nJoshua Thomason"

# API URL for Sentinel One Milestones Sheet
smart_url = "https://api.smartsheet.com/2.0/sheets/4408105728534404"

# Sheet IDs
S1_sheet_id = 4408105728534404

# Column IDs; one for agent count update and the other for checking update request statuses
actual_column_id = 5399751895082884
upd_column_id = 8172835916015492
total_column_id = 3697320274487172
comments_column_id = 7178495420852100

# DICTS AND LISTS
row_ids = {
		  ('ETHER', 'WORKGROUP'): 8607108786612100,
		  ('AVXEUR','Coleraine', 'Frimley'): 7199733903058820,
		  'GV': 'test',
		  'Workgroup': 'workgroup',
		  'Jerusalem': 8325633809901444,
		  'Betzdorf': 8463072763373444,
		  'Penang': 7055697879820164,
		  'St. Apollinaire': 8181597786662788,
		  'Lanskroun': 7618647833241476,
		  'S&C': 8347603171600260
		  }
groups_to_ignore = [
				   'Default group',
				   'SQL Servers',
				   'CDC Server'
				   ]
email_upd_dict = {
			'nathan.wilder@avx.com': 4103509159241604,
			'james.taggert@avx.com': 2696134275688324,
			'andreas.kielmann@avx.com': 3959473136002948,
			'Mandy.Guenzel@abelektronik.com ': 3844003544229764
			 }
email_send_dict = {
			'nathan.wilder@avx.com': 8607108786612100,
			'james.taggert@avx.com': 7199733903058820,
			'Mandy.Guenzel@abelektronik.com': 8347603171600260,
			'mandy.guenzel@avx.com': 8347603171600260,
			'joshua.thomason@avx.com': 7612545496311684
			 }

# Smartsheet init
ss_client = smartsheet.Smartsheet(myToken)

def ss_cell_update(input, column_id, site_row_id):
	
	# New Row and Cell Value
	new_cell = ss_client.models.Cell()
	new_cell.column_id = column_id
	new_row = ss_client.models.Row()
	
	try:
		
		new_cell.value = str(input)
		new_cell.strict = False
		
		new_row.id = site_row_id
		new_row.cells.append(new_cell)
		
		updated_row = ss_client.Sheets.update_rows(
			S1_sheet_id,
			[new_row])
		#print("Ethertronics updated!")
	
	except Exception, e:
		
		print(e)
		
	return

def update(list):
	global column_id
	global smart_url
	
	col_agent_count = 0
	eth_agent_count = 0
	gv_agent_count = 0
	SAC_agent_count = 0
	unk_agents = []
	
	try:
		# ingest S1 data and parse it to send to SmartSheet
		for S1_asset in list:
			
			asset = S1_asset.split(',')[0].lstrip(' ')
			domain = S1_asset.split(',')[1].lstrip(' ')
			group = S1_asset.split(',')[2].lstrip(' ')
		
			if group in groups_to_ignore:
				if 'ETHER' in domain or 'WORKGROUP' in domain:
					#print("Here in Ethertronics...")
					eth_agent_count += 1
				elif 'AVXEUR' in domain:
					col_agent_count += 1
				elif 'GV' in domain:
					gv_agent_count += 1
				elif 'GLOBAL' in domain:
					SAC_agent_count +=1
				else:
					unk_agents.append((u'{0}, {1}, {2}'.format(asset,
															   domain,
															   group)))
			else:
				if 'Coleraine' in group or 'Frimley' in group:
					#print("Here in Coleraine...")
					col_agent_count += 1
				elif 'Timisoara' in group:
					SAC_agent_count += 1
				elif 'Ethertronics' in group:
					eth_agent_count += 1
				else:
					unk_agents.append((u'{0}, {1}, {2}'.format(asset,
															   domain,
															   group)))
	except Exception, e:
		print(e)
	
	# Ethertronics
	try:
		ss_cell_update(eth_agent_count, actual_column_id, 8607108786612100)
		print("Ethertronics updated!")
	except Exception, e:
		print(e)
	
	# Coleraine
	try:
		ss_cell_update(col_agent_count, actual_column_id, 7199733903058820)
		print("Coleraine updated!")
	except Exception, e:
		print(e)
	
	# S&C
	try:
		ss_cell_update(SAC_agent_count, actual_column_id, 8347603171600260)
		print("S&C updated!")
	except Exception, e:
		print(e)		
	
	#print(eth_agent_count)
	#print(col_agent_count)
	#print(gv_agent_count)
	#print(SAC_agent_count)
	#print(unk_agents)
	
	#sheet_response = requests.get(smart_url, headers=head)
	#print(sheet_response.json())
	#try:
		#for x in range(0,100):
			#for y in range(0,30):
				#try:
					##print(sheet_response.json()['rows'][x]['cells'][y]['columnId'])
					#if column_id == int(sheet_response.json()['rows'][x]['cells'][y]['columnId']):
						#print(sheet_response.json()['rows'][x]['cells'][y]['displayValue'])
					#else:
						#continue
				#except:
					#continue		
	#except Exception, e:
		#print(e)
		#print("done")
	raw_input("press enter to continue..")
	return

def delete_requests(request_id):
	
	ss_client.Sheets.delete_update_request(S1_sheet_id, request_id)
	
def send_ss_update_request(email):
	global update_request_message
	
	update_request_payload = {"sendTo": [
			{"email": email}
			],
			"subject": "SentinelOne Update",
			"message": update_request_message,
			"ccMe": True,
			"rowIds": [email_send_dict[email]],
			"columnIds": [3697320274487172, 7178495420852100],
			"includeAttachments": False,
			"includeDiscussions": False
			}
	
	try:
		email_ss_send = requests.post(smart_url + "/updaterequests",
									headers=head,
									data=json.dumps(update_request_payload))
	except Exception, e:
		print(e)
		
def update_requests():
	global week_ago
	
	#TODO if pending and over 7 days old | send new update request
	response = ss_client.Sheets.list_sent_update_requests(S1_sheet_id)
	json_resp = json.loads(str(response))

	for x in range(0, 50):
		try:
			upd_reqs = json_resp['data'][x]
			if upd_reqs['status'] == 'PENDING':
				if upd_reqs['sentAt'] <= week_ago:
					#print("Delete this %s request" % upd_reqs['updateRequestId'])
					delete_requests(upd_reqs['updateRequestId'])
					send_ss_update_request(upd_reqs['sentTo']['email'])
					ss_cell_update('Y', upd_column_id, email_upd_dict[upd_reqs['sentTo']['email']])
				else:
					ss_cell_update('Y', upd_column_id, email_upd_dict[upd_reqs['sentTo']['email']])
			elif upd_reqs['status'] == 'COMPLETED':
				ss_cell_update('N', upd_column_id, email_upd_dict[upd_reqs['sentTo']['email']])
			else:
				continue
		except:
			continue
	
#update_requests()

#send_ss_update_request('joshua.thomason@avx.com', 'Test')

#update()
