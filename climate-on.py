#!/usr/bin/python
from Crypto.Cipher import Blowfish
import base64
import requests
import urllib

baseURL = 'https://gdcportalgw.its-mo.com/gworchest_0323A/gdc/'

myUsername = 'yourusername'
myPassword = 'yourpassword'

print("Content-Type: text/html")
print("")
print("<HTML>")



def getBasePRM():
    url = baseURL + 'InitialApp.php'
    data = {
	'RegionCode':'NNA',
	'lg':'en-US',
	'initial_app_strings':'geORNtsZe5I4lRGjG9GZiA'
    }
    resp = requests.post(url=url,data=data)
    status = resp.json()['message']
    basePRM = resp.json()['baseprm']
    if  status== 'success':
	return basePRM
    else:
	return -1

def pad_string(str):
    new_str = str
    pad_chars = 8-(len(str) % 8)
    if pad_chars != 0:
	for x in range(pad_chars):
     	    new_str += chr(pad_chars)
    return new_str

def encryptPW( basePRM, PW ):
    plaintext = PW
    crypt_obj = Blowfish.new(basePRM, Blowfish.MODE_ECB)
    ciphertext = crypt_obj.encrypt(pad_string(plaintext))
    return base64.b64encode(ciphertext)

def nissanGetSessionID( userid, encryptedPW ):
    url = baseURL + 'UserLoginRequest.php'
    data = {
	'RegionCode' : 'NNA',
	'lg' : 'en-US',
	'initial_app_strings' : 'geORNtsZe5I4lRGjG9GZiA',
	'UserId' : userid,
        'Password' : encryptedPW
    }
    #PW = urllib.urlencode({'Password' : encryptedPW})
    #url += "?"+PW
    resp = requests.post(url=url,data=data)
    if  resp.json()['status'] == 200 :
        return resp.json()
    else:
	return -1
    
def nissanUpdateStatus():
    url = baseURL + 'BatteryStatusCheckRequest.php'
    data = {
	'RegionCode' : 'NNA',
	'lg' : 'en-US',
        'DCMID' : loginInfo['vehicle']['profile']['dcmId'],
        'VIN' : loginInfo['vehicle']['profile']['vin'],
        'custom_sessionid' : loginInfo['VehicleInfoList']['vehicleInfo'][0]['custom_sessionid']
    }
    resp = requests.post(url=url,data=data)
    if resp.json()['status'] == 200:
        return 1
    else:
        return -1

def nissanACOn():
    url = baseURL + 'ACRemoteRequest.php'
    data = {
	'RegionCode' : 'NNA',
	'lg' : 'en-US',
        'DCMID' : loginInfo['vehicle']['profile']['dcmId'],
        'VIN' : loginInfo['vehicle']['profile']['vin'],
        'custom_sessionid' : loginInfo['VehicleInfoList']['vehicleInfo'][0]['custom_sessionid']
    }
    resp = requests.post(url=url,data=data)
    if resp.json()['status'] == 200:
        return 1
    else:
        return -1
    
PW=encryptPW( getBasePRM(), myPassword )
print "Logging into Nissan server."
loginInfo = nissanGetSessionID( myUsername, PW )
if loginInfo != -1:
  print "Login successful, sending AC On Request"
  if nissanACOn():
    print "AC Request Sent"
  else:
    print "Request failed"
print "</HTML>"
