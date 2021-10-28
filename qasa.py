import requests 
import json 



"""

"""
class find_home_in_qasa:
    def _init_(self, my_token):
        self.base_url = 'https://api.qasa.se/graphql' 
        self.my_token = my_token
        self.headers = {'Access-Token':my_token,'content-type':'application/json','Referer':'https://bostad.blocket.se','User-Agent':'Mozilla/5.0','Origin':'https://bostad.blocket.se'}
    """
    {"operationName":"CreateHomeApplication","variables":{"home_id":"323122","counter_offer":18500,"message":"dsds"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {\n  createTenantHomeApplication(\n    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}\n  ) {\n    homeApplication {\n      message\n      endOptimal\n      endUfn\n      id\n      startOptimal\n      status\n      createdAt\n      currency\n      matchInterest\n      origin\n      tenant {\n        uid\n        landlord\n        tenant\n        __typename\n      }\n      home {\n        id\n        __typename\n      }\n      __typename\n    }\n    errors {\n      field\n      codes\n      __typename\n    }\n    __typename\n  }\n}\n"}
    """
    def postMessage(self, home_id, counter_offer, message):
        query = {"operationName":"CreateHomeApplication","variables":{"home_id":f"{home_id}","counter_offer":counter_offer,"message":f"{message}"},"query":"mutation CreateHomeApplication($home_id: ID!, $counter_offer: Int!, $start_optimal: DateTime, $end_optimal: DateTime, $message: String) {  createTenantHomeApplication(    input: {homeId: $home_id, counterOffer: $counter_offer, startOptimal: $start_optimal, endOptimal: $end_optimal, message: $message}  ) {    homeApplication {      message      endOptimal      endUfn      id      startOptimal      status      createdAt      currency      matchInterest      origin      tenant {        uid        landlord        tenant        __typename      }      home {        id        __typename      }      __typename    }    errors {      field      codes      __typename    }  __typename  }}"}

        response = requests.post(url=self.base_url, headers=self.headers, json=query)
        error = response.json()['data']['createTenantHomeApplication']['error']
        return home_id,error


    def find_my_home(self,region='se/stockholms_län'):
        query = {"operationName":"HomeSearchCoordsQuery","variables":{"filterOnArea":False,"platform":"blocket","searchParams":{"homeType":["apartment","loft"],"areaIdentifier":[f"{region}"]}},"query":"query HomeSearchCoordsQuery($platform: PlatformEnum\u0021, $searchParams: HomeSearchParamsInput, $filterOnArea: Boolean) { homeSearchCoords( platform: $platform  searchParams: $searchParams   filterOnArea: $filterOnArea ) {   filterHomesRaw    __typename  }}"}
        response = requests.post(url=self.base_url, headers=self.headers, json=query)
        results = (response.json()['data']['homeSearchCoords']['filterHomesRaw'])
        results = json.loads(results)

        for house in results:
            for key in house:
                
        break

