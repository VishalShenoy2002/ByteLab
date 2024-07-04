import smtplib
# import telegram
# from telegram.bot import Bot
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl


MAIL_CONTEXT = ssl.create_default_context()
BOT_TOKEN = "6896748585:AAHZFcsFzHo3SMgUr8vKEh4GmoISDrsq_30"

# class TelegramBot:
    
#     def __init__(self) -> None:
#         self._token = BOT_TOKEN
#         self.bot = Bot(token=self._token)
        
#         self.chat_id = -1002094775831
        
#     def notify(self,message:str):
        
#         self.bot.send_message(self.chat_id,message)
        
#     def notify_with_document(self,document:str,message:str):
#         self.bot.send_document(self.chat_id,document)
#         self.bot.send_message(self.chat_id,message)
        
        
class EmailBot:
    
    def __init__(self) -> None:
        self._email_id = ""
        self._app_password = ""
        
        self.mail_server = smtplib.SMTP_SSL("smtp.gmail.com",port=587,context=MAIL_CONTEXT)
        
    def login(self):
        self.mail_server.login(self._email_id,self._app_password)
        
    def create_mail(self,to:str,subject:str,message:str):
        mail = MIMEMultipart()
        mail["From"] = self._email_id
        mail["To"] = to
        mail["Subject"] = subject
        
        mail.attach(MIMEText(message,"plain"))
        
        return mail
    
    def send_mail(self,to:str,mail:MIMEMultipart):
        self.mail_server.sendmail(self._email_id,to,mail.as_string())
        
    def close(self):
        self.mail_server.close()
        
        
    