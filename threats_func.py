import requests

#token_file = open("S1_token.txt", 'r')
token_file = open("D:\VM_Share\S1_api\S1_token.txt", 'r')
#token_file = open("C:\Users\Josh Thomason\Documents\Work\S1_token.txt", 'r')
myToken = 'APIToken ' + token_file.read()
head = {'Authorization': myToken}

threat_post = "https://avx.sentinelone.net/web/api/v1.6/threats/"

def resolve(id):
	
	try:
		#print(threat_post + id.lstrip(' ') + "/resolve")
		resolve_threat = requests.post(threat_post + id.lstrip(' ') + "/resolve", headers=head)
		#print(threat_post + id.lstrip(' ') + "/resolve")
	except Exception, e:
		print e
		return
	
	print("Threat resolved...")
	return
