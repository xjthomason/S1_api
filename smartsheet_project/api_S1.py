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
	
	1 - Agent Inventory | Smartsheet Update
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
