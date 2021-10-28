import requests 
import json 



"""

"""
class find_home_in_qasa:
    def __init__(self, my_token,local_storage):
        self.storage_file = local_storage
        self.base_url = 'https://api.qasa.se/graphql' 
        self.my_token = my_token
        self.headers = {'Access-Token':my_token,'content-type':'application/json','Referer':'https://bostad.blocket.se','User-Agent':'Mozilla/5.0','Origin':'https://bostad.blocket.se'}
    """
    {"operationName":"CreateHomeApplication","variables":{"home_id":"323122","counter_offer":18500,"message":"dsds"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {\n  createTenantHomeApplication(\n    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}\n  ) {\n    homeApplication {\n      message\n      endOptimal\n      endUfn\n      id\n      startOptimal\n      status\n      createdAt\n      currency\n      matchInterest\n      origin\n      tenant {\n        uid\n        landlord\n        tenant\n        __typename\n      }\n      home {\n        id\n        __typename\n      }\n      __typename\n    }\n    errors {\n      field\n      codes\n      __typename\n    }\n    __typename\n  }\n}\n"}
    """
    def postMessage(self, home_id, counter_offer, message):
        """
            @TODO 
            Shall be called out by Link /sendMessageTo = home_id 
            counter_offer is same cost 
            message body is the text we keep it 
        """
        query = {"operationName":"CreateHomeApplication","variables":{"home_id":f"{home_id}","counter_offer":counter_offer,"message":f"{message}"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {  createTenantHomeApplication(    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}  ) {    homeApplication {      message      endOptimal      endUfn      id      startOptimal      status      createdAt      currency      matchInterest      origin      tenant {        uid        landlord        tenant        __typename      }      home {        id        __typename      }      __typename    }    errors {      field      codes      __typename    }  __typename  }}"}

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
        print(send me message)


    def find_my_home(self,region='se/stockholms_län'):
        query = {"operationName":"HomeSearchCoordsQuery","variables":{"filterOnArea":False,"platform":"blocket","searchParams":{"homeType":["apartment","loft"],"areaIdentifier":[f"{region}"]}},"query":"query HomeSearchCoordsQuery($platform: PlatformEnum\u0021, $searchParams: HomeSearchParamsInput, $filterOnArea: Boolean) { homeSearchCoords( platform: $platform  searchParams: $searchParams   filterOnArea: $filterOnArea ) {   filterHomesRaw    __typename  }}"}
        response = requests.post(url=self.base_url, headers=self.headers, json=query)
        results = (response.json()['data']['homeSearchCoords']['filterHomesRaw'])
        results = json.loads(results)
        houses_db = {}
        with open(self.storage_file, 'r') as local_storage:
            houses_db = json.loads(local_storage.read())
        for house in results:
            if not house['id'] in houses_db:
                houses_db[house['id']]={'house_lat': house['latitude'],'house_lang': house['longitude'] ,'house_rent' : house['cost'] + house['tenant_base_fee'],'house_currency': house['currency'] }

        with open(self.storage_file,'w') as local_storage:
            local_storage.write(json.dumps(houses_db))

            
             
        
T = find_home_in_qasa("dd",local_storage='J.json')
T.find_my_home()


