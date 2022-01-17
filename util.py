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

        # File Storage
        self.lastUpdateTime = "data/lastUpdaTime.json"
        self.clientPreferences = "data/clientPref.json"

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
        return self.loadJsonFiles(self.tokenzStorage)

    def getLastUpdateTime(self,userAccountIdentifier):
        return self.loadLastUpdateTime().get(userAccountIdentifier,"2021-10-05T13:17:06Z")

    def getClientPref(self,userAccountIdentifier):
        return self.loadClientPref().get(userAccountIdentifier,{userAccountIdentifier:{"maxMonthlyCost": 11000, "minRoomCount": 1, "minSquareMeters": 20, "areaIdentifier": ["se/stockholms_kommun", "se/solna_kommun"]}})

    def loadClientPref(self):
        return self.loadJsonFiles(self.clientPreferences)
    def loadLastUpdateTime(self):
        return self.loadJsonFiles(self.lastUpdateTime)

    def loadJsonFiles(self,fileName):
        data = None
        with open(fileName, 'r+') as allData:
            data = json.load(allData)
        return data

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
        '''

        :param userAccountIdentifier:
        :param urToken:
        :return:
        '''
        tokenz = self.loadTokenz()
        if userAccountIdentifier in tokenz and tokenz[userAccountIdentifier]==urToken:
            tokenz.pop(userAccountIdentifier)
            with open(self.tokenzStorage,'w') as myToken:
                json.dump(tokenz,myToken)
        return f"{userAccountIdentifier} removed from our list "


    def writeToken(self,userAccountIdentifier):
        '''

        :param userAccountIdentifier:
        :return:
        '''
        tokenz = self.loadTokenz()
        if not userAccountIdentifier in tokenz:
            self.setToken()
            tokenz[userAccountIdentifier]=self.token
            with open(self.tokenzStorage,'w') as myToken:
                json.dump(tokenz,myToken)

        return tokenz[userAccountIdentifier]

    def setLastUpdatedTime(self,userAccountIdentifier, time):
        return self.writeLastUpdatedTime(userAccountIdentifier=userAccountIdentifier,time=time)

    def writeLastUpdatedTime(self, userAccountIdentifier, time):
        '''

        :param userAccountIdentifier:
        :param time:
        :return:
        '''

        return self.writeDataToJson(loadData=self.loadLastUpdateTime(), userAccountIdentifier=userAccountIdentifier,
                                    setData=time, fileStorage=self.lastUpdateTime)
    def setClientPref(self,userAccountIdentifier,monthlyRent,minRoomCount,minSquareMeters,region):
        '''
        :param userAccountIdentifier:
        :param monthlyRent:
        :param minRoomCount:
        :param minSquareMeters:
        :param region:
        :return:
        '''

        pref={"maxMonthlyCost":monthlyRent,"minRoomCount": minRoomCount,"minSquareMeters": minSquareMeters,"areaIdentifier": region}
        return self.writeClientPref(userAccountIdentifier=userAccountIdentifier,pref=pref)


    def writeClientPref(self, userAccountIdentifier, pref):
        '''

        :param userAccountIdentifier:
        :param pref:
        :return:
        '''
        return self.writeDataToJson(loadData=self.loadClientPref(), userAccountIdentifier=userAccountIdentifier,
                                    setData=pref, fileStorage=self.clientPreferences)

    def writeDataToJson(self,loadData,userAccountIdentifier,setData,fileStorage):
        tokenz = loadData
        tokenz[userAccountIdentifier] = setData
        with open(fileStorage, 'w',encoding="UTF-8") as myToken:
            json.dump(tokenz, myToken)
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

GG = util()
### --  -- ###
GG.setClientPref(userAccountIdentifier="mostafa.elnakeb@gmail.com",monthlyRent=11000,minRoomCount=1,minSquareMeters=20,region=['se/stockholms_kommun', "se/solna_kommun"])
GG.setLastUpdatedTime(time='2021-11-20T08:35:51Z',userAccountIdentifier='mostafa.elnakeb@gmail.com')
### --  -- ###
print("<ClientPref:> ", GG.getClientPref(userAccountIdentifier='mostafa.elnakeb@gmail.com'))
print("<Time:> ", GG.getLastUpdateTime(userAccountIdentifier='mostafa.elnakeb@gmail.com'))
### --  
"""