import requests 
import json
from datetime import datetime
import logging
from util import util
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
"""
Qasa GraphQL class  
"""
class find_home_in_qasa:
    def __init__(self, my_token,local_storage,accountIDentifier,writeToFile=False):
        self.util = util()
        self.accountIDentifier=accountIDentifier
        self.baseDataLocaion = "data/"
        self.updateVersionFileName = f"{self.baseDataLocaion }lastUpdatedVersionAt.cnf"
        # Logging setting up params
        logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s')
        self.logger = logging.getLogger()
        self.level = logging.INFO
        self.logger.setLevel(self.level)
        self.logger.log(self.level, "[!] Searching for a home ... ")

        self.storage_file = local_storage
        self.base_url = 'https://api.qasa.se/graphql' 
        self.my_token = my_token
        self.messageBody = None
        self.headers = {'Access-Token':my_token,'content-type':'application/json','Referer':'https://bostad.blocket.se','User-Agent':'Mozilla/5.0','Origin':'https://bostad.blocket.se'}
        self.prefixFileName = f"{str(datetime.today()).split(' ')[0].replace('-', '')}_{str(datetime.timestamp(datetime.now())).replace('.', '')}_"
        self.postfixFileName = ".json"
        self.writeToFile = writeToFile
        self._myLastUpdateTime = 0

    def setMessageBody(self,message):
        self.messageBody = message
    def getLastUpdatedTime(self):
        tempValue = self._myLastUpdateTime
        self._myLastUpdateTime = 0
        return tempValue

    def getMessageBody(self):
        return self.messageBody
    """
    {"operationName":"CreateHomeApplication","variables":{"home_id":"323122","counter_offer":18500,"message":"dsds"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {\n  createTenantHomeApplication(\n    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}\n  ) {\n    homeApplication {\n      message\n      endOptimal\n      endUfn\n      id\n      startOptimal\n      status\n      createdAt\n      currency\n      matchInterest\n      origin\n      tenant {\n        uid\n        landlord\n        tenant\n        __typename\n      }\n      home {\n        id\n        __typename\n      }\n      __typename\n    }\n    errors {\n      field\n      codes\n      __typename\n    }\n    __typename\n  }\n}\n"}
    """

    def postMessage(self, home_id, counter_offer,accountOpenId=0):
        """
            @TODO 
            Shall be called out by Link /sendMessageTo = home_id 
            counter_offer is same cost 
            message body is the text we keep it 
        """
        if accountOpenId:
            # End Posting if message body is None
            if not self.messageBody:
                return

            self.headers['Access-Token']= accountOpenId
            query = {"operationName":"CreateHomeApplication","variables":{"home_id":f"{home_id}","counter_offer":counter_offer,"message":f"{self.messageBody}"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {  createTenantHomeApplication(    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}  ) {    homeApplication {      message      endOptimal      endUfn      id      startOptimal      status      createdAt      currency      matchInterest      origin      tenant {        uid        landlord        tenant        __typename      }      home {        id        __typename      }      __typename    }    errors {      field      codes      __typename    }  __typename  }}"}
            response = requests.post(url=self.base_url, headers=self.headers, json=query)
            error = response.json()['data']['createTenantHomeApplication']['error']
        else:
            error = f"Check your inbox"
        return home_id,error

    def send_email(self,message):
        """
        @TODO 
        Send email with 
            the link to view 
            the  hyperlink to post the person message 
        """
        print("send me message")

    # Copied from : https://gist.githubusercontent.com/nickoala/569a9d191d088d82a5ef5c03c0690a02/raw/3ab77b718e17ef61cca5f6b1419f8c81c4008e7f/1_sendtext.py

    def sendEmailToday(self,recipients=[],subject='Dry Test',body='Hi!'):
        if len(recipients):
            smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
            smtp_ssl_port = 465
            username = ""
            password = ""
            sender = 'admin@redactive.io'
            targets = recipients
            msg = MIMEMultipart('alternative')
            msgBody= MIMEText(body, 'html')
            msg.attach(msgBody)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(targets)
            server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
            server.login(username, password)
            server.sendmail(sender, targets, msg.as_string())
            server.quit()


    def writeJsonToFile(self, fileFullPath, jsonData):
            with open(self.prefixFileName + fileFullPath + self.postfixFileName, "w+") as csFile:
                json.dump(jsonData, csFile)
    def queryHomesProtocol(self,region='se/stockholms_län'):
        houses_db = self.findMyHome(region)

    def runSearchFor(self,pref={},accountIdentifier={},lastUpdatedTime=0):
        ##TODO : Search Critria for each accountIDentifier
        ##TODO: Data base graphQL
        # Default Search is running, Later run it inside for loop
        allSearchResults = None
        if len(pref) and len(accountIdentifier) and lastUpdatedTime:
            allSearchResults = self.findMyHome(lastTimeUpated=lastUpdatedTime,region=pref.get('areaIdentifier',None),minRoomCount=pref.get('minRoomCount',None),monthlyRent=pref.get('maxMonthlyCost',None),minSquareMeters=pref.get('minSquareMeters',None),isShared=pref.get('shared',False),homeType=pref.get("homeType",["apartment","loft"]))

        else:
          allSearchResults = self.findMyHome()
        #for accountIDentifier in self.util.loadTokenz().keys():
        for post in allSearchResults:
            for item in allSearchResults[post]:
                itemInQ = allSearchResults[post][item]
                #offerThemHyperLink = self.util.submitOfferLinkGeneration(self.accountIDentifier,item,itemInQ['Price'])
                itemInQ['offerThemHyperLink'] = "N/A" #self.util.submitOfferLinkGeneration(self.accountIDentifier,item,itemInQ['Price'])

        return allSearchResults



    def findMyHome(self,region=['se/stockholms_län'], homeType= ["apartment","loft"],limit=100,monthlyRent=12000,minRoomCount=1,minSquareMeters=15,isShared=False,isSenior=False,isStudent=False,type='apartment',lastTimeUpated=0):
        keyType = "homeSearch"
        startingOffset = 0
        houses_db = {}
        cnfControl = None
        runnable = True
        if not lastTimeUpated:
            with open(self.updateVersionFileName,'r') as configControl:
                cnfControl = configControl.read()
        else:
            cnfControl = lastTimeUpated
        while True:
            #query = {"operationName":"HomeSearchCoordsQuery","variables":{"filterOnArea":False,"platform":"blocket","searchParams":{"homeType":["apartment","loft"],"areaIdentifier":[f"{region}"]}},"query":"query HomeSearchCoordsQuery($platform: PlatformEnum\u0021, $searchParams: HomeSearchParamsInput, $filterOnArea: Boolean) { homeSearchCoords( platform: $platform  searchParams: $searchParams   filterOnArea: $filterOnArea ) {   filterHomesRaw    __typename  }}"}
            query ={
                      "operationName": "HomeSearchQuery",
                      "variables": {
                        "limit": limit,
                        "platform": "blocket",
                        "searchParams": {
                          "homeType": homeType,
                          "maxMonthlyCost": monthlyRent,
                          "minRoomCount": minRoomCount,
                          "minSquareMeters": minSquareMeters,
                          "areaIdentifier":  region

                        },
                        "offset": startingOffset,
                        "order": "DESCENDING",
                        "orderBy": "PUBLISHED_AT"
                      },
                      "query": "query HomeSearchQuery($offset: Int, $limit: Int, $platform: PlatformEnum!, $order: HomeSearchOrderEnum, $orderBy: HomeSearchOrderByEnum, $searchParams: HomeSearchParamsInput!) {  homeSearch(    platform: $platform    searchParams: $searchParams    order: $order    orderBy: $orderBy  ) {    filterHomesOffset(offset: $offset, limit: $limit) {      pagesCount      totalCount      hasNextPage      hasPreviousPage      nodes {        id        firsthand        rent        tenantBaseFee        title        landlord {          uid          companyName          premium          professional          profilePicture {            url            __typename          }          proPilot          __typename        }        location {          latitude          longitude          route          locality          sublocality          __typename        }        links {          locale          url          __typename        }        roomCount        seniorHome        shared        squareMeters        studentHome        type        duration {          createdAt          endOptimal          endUfn          id          startAsap          startOptimal          updatedAt          __typename        }        corporateHome        uploads {          id          url          type          title          metadata {            primary            order            __typename          }          __typename        }        numberOfHomes        minRent        maxRent        minRoomCount        maxRoomCount        minSquareMeters        maxSquareMeters        __typename      }      __typename    }    __typename  }}"
                    }
            response = requests.post(url=self.base_url, headers=self.headers, json=query)
            results = (response.json()['data']['homeSearch']['filterHomesOffset'])
            totalCount = results['totalCount']

            # Load data
            results = results['nodes']

            for house in results:
                #Dont get records because there is no news
                if house['duration']['updatedAt'] <= cnfControl:
                    #startingOffset = totalCount + 1
                    continue
                if house['shared'] == isShared and house['studentHome'] == isStudent and house['seniorHome'] == isSenior and type == house['type']:
                    if not house['duration']['updatedAt'] in houses_db:
                        houses_db[house['duration']['updatedAt']] = {}
                    houses_db[house['duration']['updatedAt']][house['id']]={
                        'adLink':f"{house['links'][0]['url']}",
                         'location': f"{house['location']['route']} ,{house['location']['sublocality']} ,{house['location']['locality']}",
                         'updatedAt' : f"{house['duration']['updatedAt']}",
                        "startOptimal" : f"{house['duration']['startOptimal']}",
                        "EndOfContract" : f"{house['duration']['endUfn']}",
                        "endOptimal" : f"{house['duration']['endOptimal']}",
                         "AreaSpaceSquare": f"{house['squareMeters']}",
                        "Price" : f"{(house['tenantBaseFee']+house['rent'])}",
                        "NumberOfRooms":f"{house['roomCount']}",
                        "images":[]
                    }
                    for item in house['uploads']:
                        houses_db[house['duration']['updatedAt']][house['id']]["images"].append(item['url'])

            self.logger.log(self.level, f"Processing {startingOffset}/{totalCount}")
            # Next
            startingOffset += limit
            # Exit Loop
            if startingOffset > totalCount:
                break

        if len(houses_db):
            houses_db = dict(sorted(houses_db.items(),reverse=True))
            if not lastTimeUpated:
                with open(self.updateVersionFileName, 'w') as lastUpdate:
                    lastUpdate.write(list(houses_db.keys())[0])
            else:
                self._myLastUpdateTime = list(houses_db.keys())[0]

            if self.writeToFile:
                self.writeJsonToFile(fileFullPath=f"{self.baseDataLocaion }{keyType}",jsonData=houses_db)
            return houses_db
        return []



