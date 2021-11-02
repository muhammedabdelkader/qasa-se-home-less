import logging
import secrets
from jinja2 import  Environment,FileSystemLoader
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class util:

    def __init__(self,tokenLength=0):
        # Logging setting up params
        logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s')
        self.logger = logging.getLogger()
        self.level = logging.INFO
        self.logger.setLevel(self.level)
        self.logger.log(self.level, "[!] Starting Utils called")

        # send mail settings
        self.subject = None
        self.sentFrom = 'no-reply@administrator.com'
        self.toAddresses = []
        self.body = None

        # Token Generation
        self.token = None
        self.tokenLength = tokenLength | 64

        # Service Settings
        self.serviceName = None


    def addSender(self,toAddress):
        self.toAddresses.append(toAddress)

    # Allow SCALE
    def setServiceName(self,myserviceName):
        self.serviceName = myserviceName

    def getSenders(self):
        self.toAddresses

    def setSubject(self,mysubject):
        subjectList = {
            "subsctibe":"",
            "unSubsctibe":"",
            "confirmSubscribe":""
        }
        self.subject = mysubject

    def setBody(self, bodyText):
        self.body = bodyText

    def getBody(self):
        return self.body

    def setToken(self):
        self.token = secrets.token_urlsafe(self.tokenLenght)

    def sendHomeList(self,event, context,data,templateName):
        env = Environment(
            loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))
        json_data = data
        template = env.get_template(templateName)
        output = template.render(data=jsonData[0])
        sendMail(output)
        return "Mail sent successfully."

