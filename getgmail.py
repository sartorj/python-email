import imaplib, email, getpass

def process_command(mail):
    user_input = raw_input("Enter a command: ")
    if user_input == 'one':
        get_one(mail)
    elif user_input == 'quit':
        mail.logout()
        raise SystemExit
    elif user_input == 'help':
        print "\n Command list: " + "\nquit - exits" + "\none - reads first email"
    elif user_input == 'all':
        get_all(mail)
    else:
        print "Command not recognized.\n Type 'help' for list of commands."

def login():    
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    email_address = raw_input("Email address: ") # prompt user for email address
    try:
        mail.login(email_address,getpass.getpass()) #prompt for password and then attempt login
    except:
        print "An error has occured during login"
        raise SystemExit
    print "\nInbox: " + str(mail.select("inbox")[1]).strip("['']") + " messages."
    print str(mail.search(None,'(UNSEEN')) + "unread messages"
    return mail

def main():
    mail_obj = login()
    while True:
        process_command(mail_obj)

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

