import smtplib
class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", port=465,
        sender="rpgenerator.recovery@gmail.com", password="Capstonerecovery"):

        self.smtp_server = smtp_server
        self.port = port
        self.sender = sender
        self.password = password
        self.server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        self.server.login(self.sender, self.password)
        self.recovery_body = "To: {0}\r\nFrom: " + self.sender +  "\r\nSubject: RPGenerator Account Recovery\r\n\r\nYour recovery code for account {1} is: {2}"

    def send_email(self, recipient, message):
        try:
            self.server.sendmail(self.sender, recipient, message)
            print ('email sent')
            return 0
        except Exception as e:
            print('error sending mail: '+ str(e))
            return -1
  