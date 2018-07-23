import smtplib, datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

date = datetime.date.today()

def send_email(address, file):
	
	gmail_user = 'joshua.thomason@avx.com'
	ASP = open("C:\Users\Josh Thomason\Documents\Work\ASP.txt", 'r')
	#ASP = open("", 'r')
	gmail_password = ASP.read()
	to = address#, 'bill@gmail.com']
	subject = file.replace('.csv','')

	msg = MIMEMultipart()

	msg['FROM'] = gmail_user
	msg['To'] = to
	msg['Subject'] = subject

	body = """
	Hello InfoSec team!

	Please find last week's list of assets with Sentinel One installed attached.

	Let me know if you have any questions or concerns!

	Thanks!

	Joshua Thomason
	Information Security Engineer
	AVX Corporation
	One AVX Blvd.
	Fountain Inn, SC 29644 USA
	TEL: (864) 967-2150 x8109
	joshua.thomason@avx.com"""

	msg.attach(MIMEText(body, 'plain'))

	filename = file
	attachment = open(file, 'rb')

	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename=%s' % filename)

	msg.attach(part)

	#sent_from = gmail_user 

	#message = 'Subject: {}\n\n{}'.format(subject, body)
	#email_text = """\  
	#From: %s  
	#To: %s  
	#Subject: %s

	#%s
	#""" % (sent_from, ", ".join(to), subject, body)

	try:  
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		text = msg.as_string()
		server.sendmail(gmail_user, to, text)
		server.close()

		print 'Email sent!'
	except:  
		print 'Something went wrong...'
		
	return
