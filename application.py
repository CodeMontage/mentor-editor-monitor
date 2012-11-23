from flask import Flask, render_template
app = Flask(__name__)

import imaplib
from email.parser import HeaderParser


@app.route("/")
def main():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')#tested with gmail but should work with any IMAP email
	mail.login('some_email@gmail.com', 'password')#set this
	mail.list()
	mail.select("inbox")

	#Grab all the messages and pull header information from them 
	#(Restricted by date just because my inbox has thousands of messages ^_^;;;
	#Otherwise should be mail.uid('search',None,"ALL") )
	result, data = mail.uid('search',"(SINCE 22-Nov-2012)") #search and return unique ids http://tools.ietf.org/html/rfc3501#section-6.4.4
	messages = data[0].split()

	i = 0
	emails = dict()
	for uid in messages:
		result, data = mail.uid('fetch', uid, '(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT TO FROM RECEIVED)])') #Fetch just desired data
		raw_email = data[0][1]

		parser = HeaderParser()
		msg = parser.parsestr(raw_email)

		#Reorganizing the data for the template
		#probably a much better way to do this, interested in knowing it ^_^;;;
		emails[i] = dict()
		emails[i]['From'] = msg['From']
		emails[i]['To'] = msg['To']
		emails[i]['Subject'] = msg['Subject']
		emails[i]['Received'] = msg['Received'] #Returns IP addresses and SMTP id as well.
		i = i+1
	
	return render_template('messages.html', msg=emails)
		
if __name__ == "__main__":
    app.run()