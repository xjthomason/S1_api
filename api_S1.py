#python libraries
import sys, os, time
#local functions
import api_func

def menu():
	
	clear = os.system
	clear('cls')
	#clear('clear')
	
	intro = """
	AVX InfoSec - Sentinel One API Program
	
	Enter one of the following for further options:
	
	1 - Agent Inventory
	2 - Application Inventory
	3 - Threats
	4 - Manual Query
	0 - Exit
	
	"""
	
	print(intro)

def main():
	
	next = True
	
	while next:
		
		menu()
		r = raw_input("Enter: ")
		
		if r == '1':
			try:
				api_func.agents_inventory()
			except Exception, e:
				print e
				next = False
		elif r == '2':
			try:
				api_func.app_inventory()
			except Exception, e:
				print e
				next = False
		elif r == '3':
			try:
				api_func.threats_pull()
			except Exception, e:
				print e
				next = False
		elif r == '4':
			try:
				api_func.manual_query()
			except Exception, e:
				print e
				next = False
		elif r == '0':
			print "Exiting program..."
			time.sleep(1)
			#sys.exit(0)
			break
		else:
			print 'Invalid Entry'
		
		print """
		
		Process Complete!
		
		...Returning to Menu...
		
		"""
		time.sleep(2)
		

main()
#threats_pull()
#agents_inventory()
#app_inventory()
