import requests
from requests.auth  import HTTPBasicAuth

from flask import Flask,json
app = Flask(__name__)


#mpesa details 
consumer_key = 'mR0ImhjJEcC0cVefGItVsZOjVi926cfw'
consumer_secret = 'ZKSVFJqJs3InB03s'

@app.route('/',methods = ['GET'])
def home():
	return 'Hello World'


@app.route('/access_token')
def token():
	mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
	data = (requests.get(mpesa_auth_url,auth = HTTPBasicAuth(consumer_key,consumer_secret))).json()
	return data

# @app.route('/recieve_url',methods = ['GET','POST'])
# def recieve_url(args = None):
# 	# print("*"*80)
# 	# print("receving url")
# 	# print(request.args)
# 	# return jsonify({'status':True})
# 	pass

if __name__ == '__main__':
	app.run(debug = True)
