import imaplib, email, getpass, re

def process_command(mail):
    #hands off mail object to each function when needed
    user_input = raw_input("PythonEmail> ")
    if user_input == 'one':
        get_one(mail)
    elif user_input == 'quit' or user_input =='q':
        mail.logout()
        raise SystemExit
    elif user_input == 'help' or user_input == 'ls' :
        print "Command list: " + "\n'quit' or 'q' - exits" + "\n'one' - reads first email\nread <num> - read email with id <num>\nunread - view unread emails"
    elif user_input == 'all':
        get_all(mail)
    elif user_input == 'unread':
        unread(mail)
    elif user_input == 'view':
        view_all(mail)
    elif re.match('^read\s[0-9]$',user_input):
        read_id(mail,user_input)
    else:
        print "Command not recognized.\n Type 'help' for list of commands."

def unread(mail):
    typ,unread_ids = mail.search(None,'(UNSEEN)')
    print "You have " + str(len(unread_ids[0].split())) + " unread emails."
    for id in reversed(unread_ids[0].split()):
        typ, data = mail.fetch(id,'(BODY.PEEK[HEADER])') #peek does not mark email as read
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        print "ID: " + str(id) + " -- From: " + email_message['From'] + " " + email_message

def view_all(mail):
    typ, data = mail.search(None, 'ALL')
    for id in reversed(data[0].split()):
        typ, data = mail.fetch(id, '(BODY.PEEK[HEADER])')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        print "ID: " + str(id) + " -- From: " + email_message['From']

def login():    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    email_address = raw_input("Email address: ") # prompt user for email address
    try:
        mail.login(email_address,getpass.getpass()) #prompt for password and then attempt login
    except:
        print "An error has occured during login"
        raise SystemExit

    print "You have logged in as: " + email_address
    print "\nInbox: " + str(mail.select("inbox")[1]).strip("['']") + " messages."
    typ,unread_ids = mail.search(None,'(UNSEEN)')
    print "\nYou have " + str(len(unread_ids[0].split())) + " unread messages"
    return mail

def main():
    mail_obj = login() #login returns mail_obj which is then passed to process loop
    while True:
        process_command(mail_obj)

def read_id(mail,user_input):
    #remove read and whitespace from user_input
    read_id = user_input.strip('read ')
    typ, data = mail.fetch(read_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email)
    print "To: " + email_message['To']
    print "Subject: " + email_message['Subject']
    print "From: " + email_message['From']
    print "Date: " + email_message['Date']
    if email_message.get_content_maintype() == 'multipart':
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                message = part.get_payload(decode=True)
                print "Body: " + message
        
def get_all(mail):
    mail.list()
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')

    for num in data[0].split():
        print "NUM: " + num + "\n"
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        print "To: " + email_message['To']
        print "Subject: " + email_message['Subject']
        print "From: " + email_message['From']        
        if email_message.get_content_maintype() == 'multipart':
            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    message = part.get_payload(decode=True)
                    print "Body: " + message
                    
def get_one(mail):
    mail.list()
    mail.select("inbox")
    result, data = mail.search(None,"ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email)
    print "To: " + email_message['To']
    print "Subject: " + email_message['Subject']
    print "From: " + email_message['From']
    if email_message.get_content_maintype() == 'multipart':
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                message = part.get_payload(decode=True)
                print "Body: " + message

if __name__ == '__main__':
    main()

