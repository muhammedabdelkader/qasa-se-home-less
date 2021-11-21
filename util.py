import logging
import secrets
from jinja2 import  Environment,FileSystemLoader
import json
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


## Post Message needs email,token, addId, counteroffer
# Condition VerifyToken = True
#

class util:

    def __init__(self,tokenLength=0,mhostname='localhost',mport=8080,mporotocol='http://'):
        self.mhostname = mhostname
        self.mport = mport
        self.mporotocol = mporotocol
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
        self.tokenzStorage = "data/tokenz.csv"
        self.openIdStorage = "data/openId.csv"

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
        self.token = secrets.token_urlsafe(self.tokenLength)

    def getToken(self):
        return self.token

    def loadTokenz(self):
        tokens = None
        with open(self.tokenzStorage, 'r+') as alltokens:
            tokens = json.load(alltokens)
        return tokens

    def loadOpenIds(self):
        tokens = None
        with open(self.openIdStorage,'r+') as alltokens:
            tokens = json.load(alltokens)
        return tokens

    def verifyToken(self,assumeToken,accountIdentifier):
        tokenz = self.loadTokenz()
        if accountIdentifier in tokenz:
            if assumeToken == tokenz[accountIdentifier]:
                return True
        return False

    def addOpenId(self,openId,accountIdentifier,assumeToken):
        if self.verifyToken(assumeToken=assumeToken,accountIdentifier=accountIdentifier):
            openIds = self.loadOpenIds()
            openIds[accountIdentifier] = openId
            with open(self.openIdStorage,'w+') as openIdFile:
                json.dump(openIds,openIdFile)
        return f"{accountIdentifier} can bid now "

    def revokeToken(self,userAccountIdentifier,urToken):
        tokenz = self.loadTokenz()
        if userAccountIdentifier in tokenz and tokenz[userAccountIdentifier]==urToken:
            tokenz.pop(userAccountIdentifier)
            with open(self.tokenzStorage,'w') as myToken:
                json.dump(tokenz,myToken)
        return f"{userAccountIdentifier} removed from our list "


    def writeToken(self,userAccountIdentifier):
        tokenz = self.loadTokenz()
        if not userAccountIdentifier in tokenz:
            self.setToken()
            tokenz[userAccountIdentifier]=self.token
            with open(self.tokenzStorage,'w') as myToken:
                json.dump(tokenz,myToken)

        return tokenz[userAccountIdentifier]


    def submitOfferLinkGeneration(self, accountIdentifier, homeAddId , homeCounterOffer):
        submitToken = (self.openIdStorage()).get(accountIdentifier,0)
        if submitToken:
            submitLink = f"{self.mporotocol}{self.mhostname}:{self.mport}/bid/{accountIdentifier}/{submitToken}/{homeAddId}/{homeCounterOffer}"
            return submitLink
        return -1

    def sendHomeList(self,event, context,data,templateName):
        env = Environment(
            loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))
        json_data = data
        template = env.get_template(templateName)
        output = template.render(data=jsonData[0])
        sendMail(output)
        return "Mail sent successfully."
"""
GG = util()
GG.submitOfferLinkGeneration("G111@gmail.com","1","1000")

"""
