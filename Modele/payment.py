import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import codecs

class Payment: #class permetant de chiffrer et dechiffrer des informations bancaires
    def __init__(self, card_number, limit_date, visual_cryptogram, mail_adress): #all in STR
        
        self.card_number = card_number
        self.limit_date = limit_date
        self.visual_cryptogram = visual_cryptogram
        self.mail_adress =  mail_adress

    def encryption_data(self):
        
        KEY = 4
        L = []
        L1 = []
        L2 = []
        
        self.card_number = self.card_number.replace(" ", "")
        for k in self.card_number:
            L.append((int(k) + KEY) %10)
        self.card_number_encrypt = self.card_number
        self.card_number_encrypt = ''.join(str(x) for x in L)
        
        for k in self.visual_cryptogram:
            L1.append((int(k) + KEY) %10)
        self.visual_cryptogram_encrypt = self.visual_cryptogram
        self.visual_cryptogram_encrypt =''.join(str(x) for x in L1)
            
        for k in self.limit_date:
            if k != '/':
                L2.append((int(k) + KEY) %10)
            else:
                L2.append(k)
        self.limit_date_encrypt = ''.join(str(x) for x in L2)
 
    def uncryption_data(self, card_number_encrypt, visual_cryptogram_encrypt, limit_date_encrypt):
        
        KEY = 4
        L = []
        L1 = []
        L2 = []
        
        for k in card_number_encrypt:
            L.append((int(k) - KEY) %10)
        self.card_number = ''.join(str(x) for x in L)
        
        for k in visual_cryptogram_encrypt:
            L1.append((int(k) - KEY) %10)
        self.visual_cryptogram = ''.join(str(x) for x in L1)
        
        for k in limit_date_encrypt:
            if k != '/':
                L2.append((int(k)-KEY) %10)
            else:
                L2.append(k)
        self.limit_date = ''.join(str(x) for x in L2)

    def write_json(self):
        file = open('./Modele/data_payment.json', 'rb+') #on passe en binaire par souci de généralisation des données
        file.seek(0,2) #place le curseur à la position de fin du json
        if file.tell() == 0:
            file.write(b'[')
        else:
            file.seek(-1,2) #place le curseur position 1 avant la fin
            file.write(b',')
            
        x = {
            "card_number" : self.card_number_encrypt, 
            "limit date" : self.limit_date_encrypt, 
            "visual_cryptogram" : self.visual_cryptogram_encrypt, 
            "mail_adress" : self.mail_adress
             }
        
        json.dump(x, codecs.getwriter('utf-8')(file), sort_keys=True, indent=4, ensure_ascii=False)
        file.write(b']')
        file.close()

    def send_mail(self, mail, price, title, concert_date): #envoie un mail pour la confirmation du concert
        
        mail_content = 'Thanks for your reservation of %s\nThe final order of %.2f€ have been successfully performed for the date of %s.\nMail adress saved : %s'%(title, price, concert_date, self.mail_adress)
        #sender_address   = 'concertcommand@laposte.net'
        #sender_address   = 'confirmconcert1@laposte.net'
        sender_address   = SENDER MAIL HERE
        sender_password  = PASSWORD MAIL HERE
        receiver_address = mail

        mail_subject = datetime.now().strftime('Concert confirmed the %d/%m/%Y at %H:%M:%S')
        #MANUAL PARAMETERS OF MAIL
        smtp_host = "smtp.gmail.com"
        smtp_port = 587

        #Setup the MIME

        message = MIMEText(mail_content, 'plain')
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = mail_subject

        #Create SMTP session for sending the mail

        print("> Start sending mail ...")

        session = smtplib.SMTP(smtp_host, smtp_port)
        session.ehlo()
        session.starttls() # Enable security
        session.login(sender_address, sender_password) # Login with mail_id and password
        data = message.as_string()
        session.sendmail(sender_address, receiver_address, data)
        session.close()

        print("> Mail sent !")

