import requests
from bs4 import BeautifulSoup

#use VT API to pull results from search using hash pulled from SentinelOne
def VT_fetch(hash):
	
	r = requests.get("https://www.virustotal.com/latest-scan/" + hash)#, allow_redirects=False)

	#for resp in r.history:
	#print(resp.url)
	try:
		#print(r.text.encode('utf-8'))
		html = r.text.encode('utf-8')#
		parsed_html = BeautifulSoup(html, "lxml")
		encoded_parsed_html = parsed_html.encode('utf-8')
		print(encoded_parsed_html.body.find('div', attrs={'class':'container'}).text)
		if "analysis" in r.url:
			print("File hash, %s found as malicious!" % hash)
			print(r.url + "\n")
		else:
			print("File hash, %s not found in Virus Total!" % hash)
	except Exception, e:
		print e
		return

