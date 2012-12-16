from src import app
from email.parser import HeaderParser
import imaplib, re, db_interface

def clean_email_data(email_string):
	#What IMAP returns is too variable. Sometimes the email is first and the name second, 
	#sometimes there's no name, sometimes the name is encoded. This isolates data and sorts it ['email', 'name']
	stripped_data = email_string.replace('\'', '').replace('"', '')
	split_email_name = [ i.split(">")[0] for i in stripped_data.split("<") ]
	try:
		if re.match('.*@.*\.[a-z]*', split_email_name[0]) is not None:
			split_email_name.append('No Name') #By appending 'No Name' insuring there's always an index 1
			return split_email_name
		elif re.match('.*@.*\.[a-z]*', split_email_name[1]) is not None:
			return [split_email_name[1], split_email_name[0]]
		else:
			return ['None', 'No Name']
	except:
		return ['None', 'No Name']

def fetch_user_id(raw_email_data):
	clean_email = clean_email_data(raw_email_data)
	return db_interface.user_exist(clean_email)


def get_messages():
	mail = imaplib.IMAP4_SSL(app.config['MAIL_SERVER'])#tested with gmail but should work with any IMAP email
	mail.login(app.config['EMAIL_ADDRESS'], app.config['EMAIL_PASSWORD'])#set this in config.py
	mail.select("inbox")
	
	#Grab all the messages and pull header information from them
	#(Restricted by date just because my inbox has thousands of messages ^_^;;;
	#Otherwise should be mail.uid('search',None,"ALL") )
	result, data = mail.uid('search',"(SINCE 9-Dec-2012)") #search and return unique ids http://tools.ietf.org/html/rfc3501#section-6.4.4
	messages = data[0].split()

		
	emails = []
	for uid in messages:
		result, data = mail.uid('fetch', uid, '(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT TO FROM RECEIVED)])') #Fetch just desired data
		raw_email = data[0][1]
		
		parser = HeaderParser()
		msg = parser.parsestr(raw_email)
			
	#Reorganizing the data for the template
	#probably a much better way to do this, interested in knowing it ^_^;;;
		from_email_id = fetch_user_id(msg['From'])
		to_email_id = fetch_user_id(msg['To'])
		try:
			email = {
				'From': from_email_id[0],
				'To': to_email_id[0],
				'Subject': msg['Subject'],
				'Received': msg['Received'].split(";")[1]#Separate the date from IP address, etc
			}
			if db_interface.check_email_exists(email) is False:
				db_interface.add_email_message(email)
				emails.append(email)
		except:
			break
	return emails
