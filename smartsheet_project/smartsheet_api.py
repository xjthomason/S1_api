import smartsheet, requests, groups

token_file = open("Smart_token.txt", 'r')
#token_file = open("D:\VM_Share\S1_api\Smart_token.txt", 'r')
#token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = token_file.read()#'Bearer ' + token_file.read()
head = {'Authorization': myToken}

smart_url = "https://api.smartsheet.com/2.0/sheets/4408105728534404"
group_url = "https://api.sentinelone.com/web/api/v1.6/agents/count-by-filters"
column_id = 5399751895082884
row_ids = {
		  'ETHER': 8607108786612100,
		  ('AVXEUR','Coleraine', 'Frimley'): 7199733903058820,
		  'GV': 'test',
		  'Workgroup': 'workgroup',
		  'Jerusalem': 8325633809901444,
		  'Betzdorf': 8463072763373444,
		  'Penang': 7055697879820164,
		  'St. Apollinaire': 8181597786662788,
		  'Lanskroun': 7618647833241476,
		  'Timisoara': 4419062017091460
		  }
groups_to_ignore = [
				   'Default group',
				   'Greenville (Servers)',
				   'CDC Sever'
				   ]

ss_client = smartsheet.Smartsheet(myToken)

def ss_cell_update(counts, site_row_id):
	
	# New Row and Cell Value
	new_cell = ss_client.models.Cell()
	new_cell.column_id = column_id
	new_row = ss_client.models.Row()
	
	try:
		
		new_cell.value = str(counts)
		new_cell.strict = False
		
		new_row.id = site_row_id
		new_row.cells.append(new_cell)
		
		updated_row = ss_client.Sheets.update_rows(
			4408105728534404,
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
			group_id = S1_asset.split(',')[2].lstrip(' ')
			group = groups.S1_group(group_id)		
		
			if group in groups_to_ignore:
				if 'ETHER' in domain:
					#print("Here in Ethertronics...")
					eth_agent_count += 1
				elif 'AVXEUR' in domain:
					col_agent_count += 1
				elif 'GV' in domain:
					gv_agent_count += 1
				else:
					unk_agents.append((u'{0}, {1}, {2}'.format(asset,
															   domain,
															   group)))
				#try:
					#ss_row_id = next(v for k, v in row_ids.items() if domain in k)
				#except:
					#continue
			else:
				if 'Coleraine' in group or 'Frimley' in group:
					#print("Here in Coleraine...")
					col_agent_count += 1
				elif 'Timisoara' in group:
					SAC_agent_count += 1
				else:
					unk_agents.append((u'{0}, {1}, {2}'.format(asset,
															   domain,
															   group)))
				#try:
					#ss_row_id = next(v for k, v in row_ids.items() if group in k)
				#except:
					#continue
	except Exception, e:
		print(e)
	
	# Ethertronics
	try:
		ss_cell_update(eth_agent_count, 8607108786612100)
		print("Ethertronics updated!")
	except Exception, e:
		print(e)
	
	# Coleraine
	try:
		ss_cell_update(col_agent_count, 7199733903058820)
		print("Coleraine updated!")
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
	
	return

#update()
