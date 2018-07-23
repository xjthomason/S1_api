import requests, sys, json, datetime

#token_file = open("D:\VM_Share\S1_api\S1_token.txt", 'r')
token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = 'APIToken ' + token_file.read()
head = {'Authorization': myToken}

group_call = "https://avx.sentinelone.net/web/api/v1.6/groups/"

def S1_group(id):
	
	groups_pull = requests.get(group_call + id, headers=head)
	list = []
	list = groups_pull.json()
	
	return list['name']
