from flask import Flask, request
from loremipsum import generate_paragraph
from services import find_home_in_qasa
from util import util
import re

##TODO: https://flask-sso.readthedocs.io/en/latest/


#  /subscribeMe
# Post email
# send mail to subscribe

# /confirmSubscribingMe
# POST email
# POST token = ()

# /unSubscribeMe
# Link with email and Token

# /IamInterested
# token , home id , counter offer, message template "string"


pathList =['revoke','subscribe','sendMeAds']
app = Flask(__name__)

myutil = util(tokenLength=128,mhostname='10.8.0.2',mport=8080)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Stop Missing Up
## TODO: Add captach
## TODO: Add APP secret key

@app.before_request
def before():
    # Honeybot
    ## TODO: smart text would be a nice trick
    sentences_count, words_count, paragraph = generate_paragraph()
    method = request.method
    path = request.path
    if method == "GET" and path.split("/")[1] in pathList:
        email = path.split("/")[2]
        ## Vanila trap
        if not re.fullmatch(regex,email):
            return paragraph
        pass
    else:
        return paragraph



@app.route('/revoke/<string:email>/<string:token>/', methods=['GET'])
def revokeMyAccess(email,token):
    results = myutil.revokeToken(userAccountIdentifier=email, urToken=token)
    return results

@app.route('/subscribe/<string:email>',methods=['GET'])
def registerInService(email):
    adsLinks = f"/sendMeAds/{email}/{myutil.writeToken(userAccountIdentifier=email)}"

    return "sent you a link"

@app.route('/verifyMe/<string:email>/<string:token>/openId',methods=['GET'])
def verifyMe(email,token,openId):
    myutil.addOpenId(openId=openId,accountIdentifier=email,assumeToken=token)
    return "sent you a link"

@app.route('/sendMeAds/<string:email>/<string:token>',methods=['GET'])
def doSearching(email,token):
    if myutil.verifyToken(accountIdentifier=email,assumeToken=token):
        myQasa = find_home_in_qasa(my_token=token,local_storage=f"{email}.json",accountIDentifier=email)
        myQasa.runSearchFor()
    return "Done"



@app.route('/bid/<string:email>/<string:token>/homeId/offer',methods=['GET'])
def doBid(email,token,homeId,offer):
    if myutil.verifyToken(accountIdentifier=email,assumeToken=token):
        myQasa = find_home_in_qasa(my_token=token,local_storage=f"{email}.json",accountIDentifier=email)

    return f"{str(homeId).encode('UTF-8')} , {str(offer).encode('UTF-8')}"



@app.route('/me/',methods=['GET', 'POST'])
def me():
    return jsonify({'name': 'Jimit',
                    'address': 'India'})


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

if __name__ == '__main__':
    ##TODO: remove HTTP Headers, replace with fake technology to stop scanners
    app.run(host='0.0.0.0', port=8080, use_reloader = True)
