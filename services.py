import requests 
import json
from datetime import datetime
import logging


"""

"""
class find_home_in_qasa:
    def __init__(self, my_token,local_storage,writeToFile=False):
        self.updateVersionFileName = "lastUpdatedVersionAt.cnf"
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

    def setMessageBody(self,message):
        self.messageBody = message

    def getMessageBody(self):
        return self.messageBody
    """
    {"operationName":"CreateHomeApplication","variables":{"home_id":"323122","counter_offer":18500,"message":"dsds"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {\n  createTenantHomeApplication(\n    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}\n  ) {\n    homeApplication {\n      message\n      endOptimal\n      endUfn\n      id\n      startOptimal\n      status\n      createdAt\n      currency\n      matchInterest\n      origin\n      tenant {\n        uid\n        landlord\n        tenant\n        __typename\n      }\n      home {\n        id\n        __typename\n      }\n      __typename\n    }\n    errors {\n      field\n      codes\n      __typename\n    }\n    __typename\n  }\n}\n"}
    """

    def postMessage(self, home_id, counter_offer):
        """
            @TODO 
            Shall be called out by Link /sendMessageTo = home_id 
            counter_offer is same cost 
            message body is the text we keep it 
        """

        # End Posting if message body is None
        if not self.messageBody:
            return
        query = {"operationName":"CreateHomeApplication","variables":{"home_id":f"{home_id}","counter_offer":counter_offer,"message":f"{self.messageBody}"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {  createTenantHomeApplication(    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}  ) {    homeApplication {      message      endOptimal      endUfn      id      startOptimal      status      createdAt      currency      matchInterest      origin      tenant {        uid        landlord        tenant        __typename      }      home {        id        __typename      }      __typename    }    errors {      field      codes      __typename    }  __typename  }}"}
        response = requests.post(url=self.base_url, headers=self.headers, json=query)
        error = response.json()['data']['createTenantHomeApplication']['error']
        return home_id,error

    def send_email(self,message):
        """
        @TODO 
        Send email with 
            the link to view 
            the  hyperlink to post the person message 
        """
        print("send me message")

    # Copied from : https://dev.to/carola99/send-an-html-email-template-with-python-and-jinja2-1hd0

    def send_mail(self,bodyContent):
        to_email = 'to@gmail.com'
        from_email = 'from@gmail.com'
        subject = 'This is a email from Python with a movies list!'
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = to_email

        message.attach(MIMEText(bodyContent, "html"))
        msgBody = message.as_string()

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'your password')
        server.sendmail(from_email, to_email, msgBody)

        server.quit()

    def writeJsonToFile(self, fileFullPath, jsonData):
            with open(self.prefixFileName + fileFullPath + self.postfixFileName, "w+") as csFile:
                json.dump(jsonData, csFile)
    def queryHomesProtocol(self,region='se/stockholms_län'):
        houses_db = self.findMyHome(region)


    def findMyHome(self,region='se/stockholms_län',limit=25,monthlyRent=10000,minRoomCount=1,minSquareMeters=15,isShared=False,isSenior=False,isStudent=False,type='apartment'):
        keyType = "homeSearch"
        startingOffset = 0
        houses_db = {}
        cnfControl = None
        with open(self.updateVersionFileName,'r') as configControl:
            cnfControl = configControl.read()
        while True:
            #query = {"operationName":"HomeSearchCoordsQuery","variables":{"filterOnArea":False,"platform":"blocket","searchParams":{"homeType":["apartment","loft"],"areaIdentifier":[f"{region}"]}},"query":"query HomeSearchCoordsQuery($platform: PlatformEnum\u0021, $searchParams: HomeSearchParamsInput, $filterOnArea: Boolean) { homeSearchCoords( platform: $platform  searchParams: $searchParams   filterOnArea: $filterOnArea ) {   filterHomesRaw    __typename  }}"}
            query ={
                      "operationName": "HomeSearchQuery",
                      "variables": {
                        "limit": limit,
                        "platform": "blocket",
                        "searchParams": {
                          "homeType": [
                            "apartment",
                            "loft"
                          ],
                          "maxMonthlyCost": monthlyRent,
                          "minRoomCount": minRoomCount,
                          "minSquareMeters": minSquareMeters,
                          "areaIdentifier": [
                            f"{region}"
                          ]
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
            # Next
            startingOffset+=limit
            # Load data
            results = results['nodes']
            self.logger.log(self.level, f"Processing {startingOffset + limit}/{totalCount}")
            for house in results:
                #Dont get records because there is no news
                if house['duration']['updatedAt'] <= cnfControl:
                    startingOffset = totalCount + 1
                    break
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
                      houses_db[house['duration']['updatedAt']][house['id']]["images"].append(f"<img src='{item['url']}'/>")

            # Exit Loop
            if totalCount < startingOffset:
                break
        houses_db = dict(sorted(houses_db.items(),reverse=True))
        with open(self.updateVersionFileName, 'w') as lastUpdate:
            lastUpdate.write(list(houses_db.keys())[0])
        if self.writeToFile:
            self.writeJsonToFile(fileFullPath=keyType,jsonData=houses_db)
        return houses_db

            
             
        
T = find_home_in_qasa("dd",writeToFile=True,local_storage='J.json')
print("dsddsds")
print(T.findMyHome())


